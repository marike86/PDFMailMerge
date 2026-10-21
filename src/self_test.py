"""Offline smoke test for source and frozen desktop builds."""
import json
import os
import sys
import time
from pathlib import Path


def main(args):
    if len(args) != 1:
        raise SystemExit("Usage: PDFMailMerge-CLI.exe --self-test OUTPUT_DIRECTORY")
    os.environ.setdefault("QT_QPA_PLATFORM", "windows" if sys.platform == "win32" else "offscreen")
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication
    from .gui import MainWindow, configure_app
    output = Path(args[0]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[1]
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    configure_app(app)
    window = MainWindow()
    window.show()
    window.template_path.setText(str(root / "examples" / "invitation_template.pdf"))
    window.data_path.setText(str(root / "examples" / "demo_data.csv"))
    window.output_path.setText(str(output / "pdfs"))
    window.pattern.setText("{id}_{name}")
    window.zip_enabled.setChecked(True)
    state = {"stage": "inspect", "passed": False}
    started = time.monotonic()

    def finish(code, error=""):
        state["error"] = error
        state["elapsed_seconds"] = round(time.monotonic() - started, 2)
        (output / "self-test.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        window.close()
        app.exit(code)

    def tick():
        try:
            if time.monotonic() - started > 90:
                raise RuntimeError("Desktop self-test timed out")
            if window.worker:
                QTimer.singleShot(30, tick)
                return
            if state["stage"] == "inspect":
                assert window.plan, window.status.text()
                state["records"] = len(window.plan.records)
                state["stage"] = "preview"
                window.preview()
            elif state["stage"] == "preview":
                assert window.preview_generated, window.status.text()
                window.grab().save(str(output / "desktop-preview.png"))
                window.go(1)
                app.processEvents()
                window.grab().save(str(output / "desktop-mapping.png"))
                state["stage"] = "generate"
                window.generate()
            else:
                assert window.stats[2].text() == "3", window.log.toPlainText()
                assert "生成完成" in window.result_summary.text(), window.status.text()
                window.grab().save(str(output / "desktop-results.png"))
                state["passed"] = True
                state["generated"] = 3
                finish(0)
                return
            QTimer.singleShot(30, tick)
        except Exception as exc:
            if window.worker:
                window.cancel.set()
                window.worker.wait(10000)
            finish(1, str(exc))

    window.inspect()
    QTimer.singleShot(30, tick)
    exit_code = app.exec()
    if not state["passed"]:
        # A successful process exit alone is not evidence of a completed test.
        window.cancel.set()
        if window.worker:
            window.worker.wait(10000)
        state["error"] = state.get("error") or "Application exited before the self-test completed"
        (output / "self-test.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return exit_code or 1
    return exit_code
