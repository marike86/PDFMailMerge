"""Chinese Fluent desktop shell. PDF work runs serially off the UI thread."""
import sys
import os
import tempfile
from pathlib import Path
from threading import Event

from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QFontDatabase, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QScrollArea, QSpinBox, QSplitter, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)
from .merge_service import inspect_inputs, run_merge, render_record, validate_mapping
from .pdf_processor import _open

STYLE = """
QWidget { font-family: 'Segoe UI', 'Microsoft YaHei UI'; font-size: 13px; color: #202b3c; }
QMainWindow, QWidget#root { background: #f3f5f8; }
QFrame#sidebar { background: #edf1f7; border-right: 1px solid #e0e5ed; }
QLabel#brand { color: #0f6cbd; font-size: 19px; font-weight: 700; }
QLabel#muted { color: #64748b; }
QLabel#title { font-size: 28px; font-weight: 700; color: #17243b; }
QLabel#section { font-size: 16px; font-weight: 600; }
QLabel#number { font-size: 25px; font-weight: 600; color: #0f6cbd; }
QLabel#badge { background: #e4f0fc; color: #0f6cbd; padding: 5px 10px; border-radius: 12px; font-size: 11px; }
QFrame#card { background: white; border: 1px solid #e1e6ee; border-radius: 9px; }
QPushButton { background: white; border: 1px solid #d3dbe6; border-radius: 5px; padding: 8px 14px; }
QPushButton:hover { background: #f0f6fc; border-color: #9cbfdf; }
QPushButton:pressed { background: #deebf8; }
QPushButton:disabled { color: #9ca8b8; background: #f5f6f8; border-color: #e4e8ee; }
QPushButton#primary { background: #0f6cbd; color: white; border: 1px solid #0f6cbd; font-weight: 600; }
QPushButton#primary:hover { background: #115ea3; }
QPushButton#primary:disabled { background: #b5cde1; border-color: #b5cde1; color: #f7fafc; }
QPushButton#nav { text-align: left; background: transparent; border: 0; padding: 12px 14px; }
QPushButton#nav:checked { background: #dceafa; color: #0f6cbd; font-weight: 600; border-left: 3px solid #0f6cbd; }
QLineEdit, QComboBox, QSpinBox { background: #fafbfd; border: 1px solid #d9e0e9; border-bottom: 1px solid #aebaca; border-radius: 5px; padding: 7px; min-height: 20px; selection-background-color: #0f6cbd; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border-bottom: 2px solid #0f6cbd; }
QSpinBox QLineEdit { padding: 0; border: 0; background: transparent; min-height: 0; }
QComboBox QAbstractItemView { background: white; selection-background-color: #e4f0fc; selection-color: #0f6cbd; }
QTableWidget { background: white; border: 1px solid #e1e6ee; border-radius: 5px; gridline-color: #edf0f4; selection-background-color: #e4f0fc; selection-color: #17243b; }
QHeaderView::section { background: #f6f8fb; border: 0; border-bottom: 1px solid #e1e6ee; padding: 10px; text-align: left; font-weight: 600; }
QPlainTextEdit { background: #fafbfd; border: 1px solid #e1e6ee; border-radius: 5px; padding: 8px; }
QScrollArea { background: transparent; border: 0; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 2px; }
QScrollBar::handle:vertical { background: #c3cddb; min-height: 28px; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QProgressBar { background: #e5ebf2; border: 0; border-radius: 3px; min-height: 6px; max-height: 6px; }
QProgressBar::chunk { background: #0f6cbd; border-radius: 3px; }
QCheckBox { spacing: 8px; }
QCheckBox::indicator { width: 17px; height: 17px; border: 1px solid #a8b6c7; border-radius: 4px; background: white; }
QCheckBox::indicator:checked { background: #0f6cbd; border: 4px solid #0f6cbd; image: url(); }
QSplitter::handle { background: transparent; width: 16px; }
"""


def label(text, name="", wrap=False):
    item = QLabel(text)
    if name:
        item.setObjectName(name)
    item.setWordWrap(wrap)
    return item


def button(text, callback, name=""):
    item = QPushButton(text)
    item.setCursor(Qt.CursorShape.PointingHandCursor)
    if name:
        item.setObjectName(name)
    item.clicked.connect(callback)
    return item


def card(title, subtitle=""):
    frame = QFrame()
    frame.setObjectName("card")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(20, 18, 20, 18)
    layout.setSpacing(12)
    if title:
        layout.addWidget(label(title, "section"))
    if subtitle:
        layout.addWidget(label(subtitle, "muted", True))
    return frame, layout


def pdf_image(path, page_number=0):
    with _open(path) as doc:
        page_number = min(page_number, len(doc) - 1)
        page = doc[page_number]
        scale = min(1.5, 1000 / page.rect.width)
        import pymupdf as fitz
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        return pix.tobytes("png"), len(doc)


class Worker(QThread):
    succeeded = Signal(object)
    failed = Signal(str)
    progress = Signal(int, int, str)

    def __init__(self, operation, parent):
        super().__init__(parent)
        self.operation = operation

    def run(self):
        try:
            self.succeeded.emit(self.operation(self.progress.emit))
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Mail Merge")
        self.resize(1280, 870)
        self.setMinimumSize(1080, 760)
        self.plan = None
        self.worker = None
        self.cancel = Event()
        self.page_count = 1
        self.preview_generated = False
        self.result_output = ""
        self._build()
        self._update_actions()

    def _build(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(190)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(16, 28, 16, 22)
        side.setSpacing(9)
        side.addWidget(label("PDF / MERGE", "brand"))
        side.addWidget(label("批量文档工作台", "muted"))
        side.addSpacing(30)
        self.nav = []
        for index, text in enumerate(("01   导入与设置", "02   字段映射", "03   生成结果")):
            item = button(text, lambda checked=False, i=index: self.go(i), "nav")
            item.setCheckable(True)
            side.addWidget(item)
            self.nav.append(item)
        side.addStretch()
        side.addWidget(label("PORTABLE EDITION", "badge"))
        side.addWidget(label("本地处理 · 无需联网\n版本 2.0", "muted"))
        outer.addWidget(sidebar)
        content = QWidget()
        main = QVBoxLayout(content)
        main.setContentsMargins(28, 26, 28, 22)
        main.setSpacing(18)
        heading = QHBoxLayout()
        titles = QVBoxLayout()
        titles.addWidget(label("让每份文档，都恰好属于一个人。", "title"))
        titles.addWidget(label("选择 PDF 模板与数据，批量生成个性化文档。", "muted"))
        heading.addLayout(titles)
        heading.addStretch()
        heading.addWidget(label("PDF MAIL MERGE", "badge"))
        main.addLayout(heading)
        stats = QHBoxLayout()
        self.stats = []
        for name, value in (("数据记录", "—"), ("模板字段", "—"), ("已生成", "0")):
            frame, layout = card("")
            layout.setContentsMargins(18, 12, 18, 12)
            number = label(value, "number")
            layout.addWidget(number)
            layout.addWidget(label(name, "muted"))
            stats.addWidget(frame)
            self.stats.append(number)
        main.addLayout(stats)
        split = QSplitter(Qt.Orientation.Horizontal)
        split.setHandleWidth(16)
        self.pages = QStackedWidget()
        self._input_page()
        self._mapping_page()
        self._result_page()
        split.addWidget(self.pages)
        preview, preview_layout = card("文档预览", "先检查模板，再预览一条数据的实际效果。")
        preview.setMinimumWidth(320)
        preview_controls = QHBoxLayout()
        preview_controls.addWidget(label("记录", "muted"))
        self.record = QSpinBox()
        self.record.setRange(1, 1)
        self.record.valueChanged.connect(self.record_changed)
        self.record.setFixedWidth(75)
        preview_controls.addWidget(self.record)
        preview_controls.addStretch()
        self.preview_button = button("预览效果", self.preview, "primary")
        preview_controls.addWidget(self.preview_button)
        preview_layout.addLayout(preview_controls)
        self.preview_area = QScrollArea()
        self.preview_area.setWidgetResizable(True)
        self.preview_label = label("PDF\n\n导入模板后，预览将显示在这里。", "muted", True)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(260, 280)
        self.preview_label.setStyleSheet("background: #e9eef5; border-radius: 6px; padding: 12px;")
        self.preview_area.setWidget(self.preview_label)
        preview_layout.addWidget(self.preview_area, 1)
        footer = QHBoxLayout()
        self.preview_caption = label("尚未导入模板", "muted")
        footer.addWidget(self.preview_caption, 1)
        self.page = QSpinBox()
        self.page.setPrefix("页 ")
        self.page.setFixedWidth(85)
        self.page.setRange(1, 1)
        self.page.valueChanged.connect(self.change_page)
        footer.addWidget(self.page)
        footer.addWidget(button("‹", lambda: self.page.setValue(self.page.value() - 1)))
        footer.addWidget(button("›", lambda: self.page.setValue(self.page.value() + 1)))
        preview_layout.addLayout(footer)
        split.addWidget(preview)
        split.setSizes([570, 400])
        split.setStretchFactor(0, 3)
        split.setStretchFactor(1, 2)
        main.addWidget(split, 1)
        self.status = label("准备就绪 · 从选择模板开始", "muted", True)
        main.addWidget(self.status)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        main.addWidget(self.progress)
        bottom = QHBoxLayout()
        bottom.addWidget(label("PDF、CSV、Excel 和 JSON · 所有文件在本机处理", "muted"), 1)
        self.cancel_button = button("取消任务", self.stop)
        bottom.addWidget(self.cancel_button)
        self.start_button = button("开始批量生成  →", self.generate, "primary")
        self.start_button.setMinimumWidth(160)
        bottom.addWidget(self.start_button)
        main.addLayout(bottom)
        outer.addWidget(content, 1)
        self.go(0)

    def _path_row(self, layout, title, placeholder, kind):
        layout.addWidget(label(title))
        row = QHBoxLayout()
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setMinimumWidth(100)
        edit.setAccessibleName(title)
        row.addWidget(edit, 1)
        row.addWidget(button("浏览…", lambda: self.browse(edit, kind)))
        layout.addLayout(row)
        if kind != "output":
            edit.textChanged.connect(self.invalidate)
        return edit

    def _input_page(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        files, fields = card("01  导入文件", "支持 PDF 表单，或包含 {{字段名}} 的文字模板。")
        self.template_path = self._path_row(fields, "PDF 模板", "选择 .pdf 文件", "template")
        self.data_path = self._path_row(fields, "数据文件", "选择 .csv / .xlsx / .xls / .json", "data")
        row = QHBoxLayout()
        self.mode = QComboBox()
        for name, value in (("自动识别模板", "auto"), ("PDF 表单", "form"), ("文本占位符", "text")):
            self.mode.addItem(name, value)
        self.mode.currentIndexChanged.connect(self.invalidate)
        row.addWidget(self.mode, 1)
        self.inspect_button = button("加载并检查", self.inspect, "primary")
        row.addWidget(self.inspect_button)
        fields.addLayout(row)
        layout.addWidget(files)
        settings, options = card("02  输出设置")
        self.output_path = self._path_row(options, "保存位置", "选择生成文件的文件夹", "output")
        options.addWidget(label("文件命名规则"))
        self.pattern = QLineEdit("document_{row}")
        self.pattern.setAccessibleName("文件命名规则")
        options.addWidget(self.pattern)
        options.addWidget(label("使用 {row}、{timestamp} 或 {数据列名}。重名时自动编号。", "muted", True))
        self.zip_enabled = QCheckBox("同时将本次生成的 PDF 打包为 ZIP")
        options.addWidget(self.zip_enabled)
        layout.addWidget(settings)
        layout.addStretch()
        scroll.setWidget(inner)
        self.pages.addWidget(scroll)

    def _mapping_page(self):
        frame, layout = card("字段映射", "将每个模板字段关联到一个数据列。同名字段会自动匹配。")
        self.mapping_table = QTableWidget(0, 3)
        self.mapping_table.setHorizontalHeaderLabels(["模板字段", "数据列", "首条数据"])
        self.mapping_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mapping_table.verticalHeader().hide()
        layout.addWidget(self.mapping_table, 1)
        layout.addWidget(label("数据预览 · 前 100 条", "section"))
        self.data_table = QTableWidget()
        self.data_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.data_table.setMaximumHeight(200)
        layout.addWidget(self.data_table)
        self.pages.addWidget(frame)

    def _result_page(self):
        frame, layout = card("生成结果", "任务进度、生成文件和错误原因会显示在这里。")
        self.result_summary = label("还没有生成任务。", "section", True)
        layout.addWidget(self.result_summary)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumBlockCount(3000)
        layout.addWidget(self.log, 1)
        self.open_button = button("打开结果文件夹", self.open_output)
        self.open_button.setEnabled(False)
        layout.addWidget(self.open_button)
        self.pages.addWidget(frame)

    def go(self, index):
        self.pages.setCurrentIndex(index)
        for i, nav in enumerate(self.nav):
            nav.setChecked(i == index)

    def browse(self, edit, kind):
        if kind == "output":
            path = QFileDialog.getExistingDirectory(self, "选择输出文件夹", edit.text())
        else:
            filters = "PDF 模板 (*.pdf)" if kind == "template" else "数据文件 (*.csv *.xlsx *.xls *.json)"
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", edit.text(), filters)
        if path:
            edit.setText(path)
            if kind == "data" and not self.output_path.text():
                self.output_path.setText(str(Path(path).parent / "PDFMailMerge_Output"))
            if kind != "output" and self.template_path.text() and self.data_path.text():
                self.inspect()

    def invalidate(self, *_):
        self.plan = None
        self.preview_generated = False
        if hasattr(self, "stats"):
            self.stats[0].setText("—")
            self.stats[1].setText("—")
        if hasattr(self, "preview_label"):
            self.preview_label.clear()
            self.preview_label.setText("输入已更新\n\n点击「加载并检查」以刷新预览。")
            self.preview_caption.setText("等待检查")
            self.mapping_table.setRowCount(0)
            self.data_table.setRowCount(0)
        self._update_actions()

    def _update_actions(self):
        if not hasattr(self, "start_button"):
            return
        busy = self.worker is not None
        ready = self.plan is not None
        if ready:
            try:
                validate_mapping(self.plan)
            except ValueError:
                ready = False
        self.start_button.setEnabled(ready and not busy)
        self.preview_button.setEnabled(ready and not busy)
        self.inspect_button.setEnabled(not busy)
        self.record.setEnabled(not busy and ready)
        self.page.setEnabled(not busy and self.plan is not None)
        self.pages.setEnabled(not busy)
        self.cancel_button.setEnabled(busy and self.job_kind == "batch")

    def _run(self, kind, operation, callback):
        if self.worker is not None:
            return
        self.job_kind = kind
        self.cancel.clear()
        self.worker = Worker(operation, self)
        self.worker.succeeded.connect(callback)
        self.worker.failed.connect(self.error)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self._idle)
        self.progress.setRange(0, 0)
        self._update_actions()
        self.worker.start()

    def _idle(self):
        old_worker = self.worker
        self.worker = None
        old_worker.deleteLater()
        if self.progress.maximum() == 0:
            self.progress.setRange(0, 100)
            self.progress.setValue(0)
        self._update_actions()

    def error(self, message):
        self.status.setText("操作未完成：" + message)
        self.log.appendPlainText("错误：" + message)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

    def inspect(self):
        template = self.template_path.text().strip().strip('"')
        data = self.data_path.text().strip().strip('"')
        mode = self.mode.currentData()
        self.plan = None
        self.status.setText("正在读取模板和数据…")

        def operation(progress):
            plan = inspect_inputs(template, data, mode)
            return plan, pdf_image(plan.template)

        self._run("inspect", operation, self.inspected)

    def inspected(self, result):
        self.plan, image = result
        self.stats[0].setText(str(len(self.plan.records)))
        self.stats[1].setText(str(len(self.plan.fields)))
        self.record.setRange(1, len(self.plan.records))
        self.record.setValue(1)
        self.preview_generated = False
        self.set_image(image, "原始模板")
        self.populate_mapping()
        missing = [f for f in self.plan.fields if self.plan.mapping[f] not in self.plan.columns]
        if missing:
            self.status.setText("文件已加载 · 请先为所有模板字段选择数据列。")
            self.go(1)
        else:
            self.status.setText(f"检查通过 · {len(self.plan.records)} 条记录，{len(self.plan.fields)} 个字段，可预览或生成。")

    def populate_mapping(self):
        self.mapping_table.setRowCount(len(self.plan.fields))
        for row, name in enumerate(self.plan.fields):
            item = QTableWidgetItem(name)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.mapping_table.setItem(row, 0, item)
            combo = QComboBox()
            combo.addItem("请选择数据列", "")
            for column in self.plan.columns:
                combo.addItem(column, column)
            index = combo.findData(self.plan.mapping[name])
            combo.setCurrentIndex(max(0, index))
            combo.currentIndexChanged.connect(lambda _, n=name, c=combo, r=row: self.mapping_changed(n, c.currentData(), r))
            self.mapping_table.setCellWidget(row, 1, combo)
            self._mapping_value(row, self.plan.mapping[name])
            self.mapping_table.setRowHeight(row, 48)
        records = self.plan.records[:100]
        self.data_table.setColumnCount(len(self.plan.columns))
        self.data_table.setRowCount(len(records))
        self.data_table.setHorizontalHeaderLabels(self.plan.columns)
        for row, record in enumerate(records):
            for col, name in enumerate(self.plan.columns):
                self.data_table.setItem(row, col, QTableWidgetItem(str(record.get(name, ""))))
        self.data_table.resizeColumnsToContents()

    def _mapping_value(self, row, column):
        item = QTableWidgetItem(str(self.plan.records[0].get(column, "")))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.mapping_table.setItem(row, 2, item)

    def mapping_changed(self, name, column, row):
        self.plan.mapping[name] = column
        self._mapping_value(row, column)
        self.preview_generated = False
        self.preview_label.clear()
        self.preview_label.setText("映射已更新\n\n点击「预览效果」查看最新结果。")
        self.preview_caption.setText("等待刷新")
        self.status.setText("字段映射已更新 · 可预览或生成。")
        self._update_actions()

    def record_changed(self):
        if self.preview_generated and not self.worker:
            self.preview_label.clear()
            self.preview_label.setText("记录已更改\n\n点击「预览效果」查看所选记录。")
            self.preview_caption.setText("等待刷新")
            self.preview_generated = False

    def set_image(self, result, caption):
        png, self.page_count = result
        pixmap = QPixmap()
        pixmap.loadFromData(png)
        width = max(240, self.preview_area.viewport().width() - 30)
        self.preview_label.setPixmap(pixmap.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation))
        self.preview_label.setMinimumHeight(0)
        self.preview_caption.setText(caption)
        self.page.blockSignals(True)
        self.page.setRange(1, self.page_count)
        self.page.blockSignals(False)

    def preview(self):
        if not self.plan:
            return
        plan, index, page = self.plan, self.record.value() - 1, self.page.value() - 1
        self.status.setText("正在生成预览…")

        def operation(progress):
            with tempfile.TemporaryDirectory(prefix="PDFMailMerge_") as temporary:
                output = Path(temporary) / "preview.pdf"
                render_record(plan, index, output)
                return pdf_image(output, page)

        def done(result):
            self.preview_generated = True
            self.set_image(result, f"生成效果 · 记录 {index + 1}")
            self.status.setText("预览已更新 · 确认效果后即可批量生成。")

        self._run("preview", operation, done)

    def change_page(self):
        if not self.plan or self.worker:
            return
        if self.preview_generated:
            self.preview()
        else:
            path, page = self.plan.template, self.page.value() - 1
            self._run("page", lambda progress: pdf_image(path, page), lambda image: self.set_image(image, "原始模板"))

    def generate(self):
        if not self.plan:
            return
        template, data = self.template_path.text().strip().strip('"'), self.data_path.text().strip().strip('"')
        mode, mapping = self.mode.currentData(), dict(self.plan.mapping)
        output, pattern = self.output_path.text().strip(), self.pattern.text()
        zip_enabled = self.zip_enabled.isChecked()
        self.go(2)
        self.log.clear()
        self.result_summary.setText("正在生成文档…")
        self.open_button.setEnabled(False)
        self.status.setText("正在检查输入文件并开始生成…")

        def operation(progress):
            plan = inspect_inputs(template, data, mode, mapping)
            return run_merge(plan, output, pattern, zip_enabled, self.cancel, progress)

        def done(result):
            self.stats[2].setText(str(len(result.files)))
            state = "已取消" if result.cancelled else ("部分失败" if result.errors else "生成完成")
            summary = f"{state} · 成功 {len(result.files)} / {result.total}，错误 {len(result.errors)}"
            self.result_summary.setText(summary)
            self.status.setText(summary)
            if result.errors:
                self.log.appendPlainText("\n失败详情\n" + "\n".join(result.errors))
            if result.archive:
                self.log.appendPlainText("\nZIP: " + result.archive)
            self.result_output = str(Path(output).resolve())
            self.open_button.setEnabled(bool(result.files))
            self.progress.setRange(0, result.total)
            self.progress.setValue(len(result.files) + min(result.total - len(result.files), len(result.errors)))

        self._run("batch", operation, done)

    def on_progress(self, current, total, message):
        self.progress.setRange(0, total)
        self.progress.setValue(current)
        self.status.setText(f"正在处理 {current} / {total}")
        self.log.appendPlainText(f"{current:04d}  {message}")

    def stop(self):
        self.cancel.set()
        self.cancel_button.setEnabled(False)
        self.status.setText("正在取消 · 当前文档完成后停止。")

    def open_output(self):
        if self.result_output:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.result_output))

    def closeEvent(self, event):
        if self.worker:
            self.stop()
            self.status.setText("任务停止后可关闭窗口。")
            event.ignore()
        else:
            event.accept()


def configure_app(app):
    # The headless Qt platform does not enumerate Windows system fonts.
    if not QFontDatabase.families() and sys.platform == "win32":
        fonts = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
        for filename in ("segoeui.ttf", "msyh.ttc"):
            QFontDatabase.addApplicationFont(str(fonts / filename))
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    app.setApplicationName("PDFMailMerge")
    app.setOrganizationName("PDFMailMerge")
    app.setFont(QFont("Segoe UI", 10))
    assets = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)) / "assets"
    icon = QIcon(str(assets / "app.ico"))
    app.setWindowIcon(icon)


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    configure_app(app)
    window = MainWindow()
    window.show()
    return app.exec()
