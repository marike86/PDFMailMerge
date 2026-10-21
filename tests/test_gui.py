"""Exercise the actual desktop workflow and worker completion."""
import os
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication
from src.gui import MainWindow, configure_app


def wait(app, window):
    deadline = time.monotonic() + 30
    while window.worker and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    assert window.worker is None, "Desktop worker did not finish"


def test_desktop_import_map_preview_generate(text_template_pdf, sample_csv, tmp_path):
    app = QApplication.instance() or QApplication([])
    configure_app(app)
    window = MainWindow()
    assert not window.start_button.isEnabled()
    window.template_path.setText(text_template_pdf)
    window.data_path.setText(sample_csv)
    window.output_path.setText(str(tmp_path / "output"))
    window.inspect()
    wait(app, window)
    assert window.plan is not None, window.status.text()
    assert window.start_button.isEnabled()
    assert window.mapping_table.rowCount() == 3
    window.preview()
    wait(app, window)
    assert window.preview_generated, window.status.text()
    assert not window.preview_label.pixmap().isNull()
    window.zip_enabled.setChecked(True)
    window.generate()
    wait(app, window)
    assert window.stats[2].text() == "3", window.log.toPlainText()
    assert len(list((tmp_path / "output").glob("*.pdf"))) == 3
    assert len(list((tmp_path / "output").glob("*.zip"))) == 1
    assert "生成完成" in window.result_summary.text()
    window.data_path.setText("missing.csv")
    assert window.plan is None and not window.start_button.isEnabled()
    window.close()


def test_desktop_failed_import_and_unmapped_fields(text_template_pdf, tmp_path):
    app = QApplication.instance() or QApplication([])
    configure_app(app)
    window = MainWindow()
    window.template_path.setText(text_template_pdf)
    window.data_path.setText("missing.csv")
    window.inspect()
    wait(app, window)
    assert window.plan is None and not window.start_button.isEnabled()
    source = tmp_path / "other.csv"
    source.write_text("姓名,邮箱,公司\n张三,a@example.com,示例\n", encoding="utf-8")
    window.data_path.setText(str(source))
    window.inspect()
    wait(app, window)
    assert window.pages.currentIndex() == 1
    assert not window.start_button.isEnabled()
    for row, name in enumerate(window.plan.fields):
        mapped = {"name": "姓名", "email": "邮箱", "company": "公司"}[name]
        combo = window.mapping_table.cellWidget(row, 1)
        combo.setCurrentIndex(combo.findData(mapped))
    assert window.start_button.isEnabled()
    window.close()
