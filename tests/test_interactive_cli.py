import os
import csv
import fitz
import pytest
from unittest.mock import patch, MagicMock
from src.interactive_cli import InteractiveCLI


@pytest.fixture
def icli():
    return InteractiveCLI()


@pytest.fixture
def icli_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        writer.writeheader()
        writer.writerow({"name": "张三", "email": "zhangsan@test.com"})
    return str(csv_file)


@pytest.fixture
def icli_text_pdf(tmp_path):
    pdf_path = tmp_path / "template.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Name: {{name}}", fontsize=12)
    page.insert_text((72, 120), "Email: {{email}}", fontsize=12)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


@pytest.fixture
def icli_form_pdf(tmp_path):
    pdf_path = tmp_path / "form.pdf"
    doc = fitz.open()
    page = doc.new_page()
    widget = fitz.Widget()
    widget.field_name = "name"
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.rect = fitz.Rect(100, 60, 300, 80)
    page.add_widget(widget)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


class TestInteractiveCLIInit:

    def test_default_config(self, icli):
        assert icli.config["template_path"] is None
        assert icli.config["data_path"] is None
        assert icli.config["output_dir"] is None
        assert icli.config["mode"] is None
        assert icli.config["naming_pattern"] is None
        assert icli.config["zip_enabled"] is False
        assert icli.config["clean_output"] is False

    def test_history_empty(self, icli):
        assert icli.history == []

    def test_colors_defined(self, icli):
        assert "red" in InteractiveCLI.COLORS
        assert "green" in InteractiveCLI.COLORS
        assert "reset" in InteractiveCLI.COLORS

    def test_max_history(self, icli):
        assert icli.max_history == 50


class TestCleanPathQuotes:

    @pytest.mark.parametrize("input_path,expected", [
        ('"C:\\path\\to\\file"', "C:\\path\\to\\file"),
        ("no quotes", "no quotes"),
        ('"just one side"', "just one side"),
        ('"C:\\path with spaces\\file"', "C:\\path with spaces\\file"),
        ("  path with spaces  ", "path with spaces"),
        ("", ""),
    ])
    def test_clean_quotes(self, icli, input_path, expected):
        assert icli.clean_path_quotes(input_path) == expected

    def test_internal_quotes_preserved(self, icli):
        result = icli.clean_path_quotes('"path\\"internal"')
        assert isinstance(result, str)


class TestValidationMethods:

    def test_validate_file_exists(self, icli, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("x")
        valid, msg = icli.validate_file_exists(str(f))
        assert valid is True
        assert msg == ""

    def test_validate_file_not_exists(self, icli):
        valid, msg = icli.validate_file_exists("nonexistent.txt")
        assert valid is False
        assert "不存在" in msg

    def test_validate_file_empty_path(self, icli):
        valid, msg = icli.validate_file_exists("")
        assert valid is False

    def test_validate_file_is_directory(self, icli, tmp_path):
        valid, msg = icli.validate_file_exists(str(tmp_path))
        assert valid is False
        assert "不是文件" in msg

    def test_validate_pdf_file(self, icli, icli_text_pdf):
        valid, msg = icli.validate_pdf_file(icli_text_pdf)
        assert valid is True

    def test_validate_pdf_non_pdf_extension(self, icli, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("content")
        valid, msg = icli.validate_pdf_file(str(f))
        assert valid is False
        assert "PDF" in msg

    def test_validate_pdf_not_exists(self, icli):
        valid, msg = icli.validate_pdf_file("nonexistent.pdf")
        assert valid is False

    def test_validate_data_file_csv(self, icli, icli_csv):
        valid, msg = icli.validate_data_file(icli_csv)
        assert valid is True

    def test_validate_data_file_unsupported(self, icli, tmp_path):
        f = tmp_path / "data.xyz"
        f.write_text("data")
        valid, msg = icli.validate_data_file(str(f))
        assert valid is False
        assert "不支持" in msg

    def test_validate_data_file_not_exists(self, icli):
        valid, msg = icli.validate_data_file("nonexistent.csv")
        assert valid is False

    def test_validate_directory_exists(self, icli, tmp_path):
        valid, msg = icli.validate_directory_exists(str(tmp_path))
        assert valid is True

    def test_validate_directory_empty(self, icli):
        valid, msg = icli.validate_directory_exists("")
        assert valid is False

    def test_validate_directory_no_parent(self, icli):
        valid, msg = icli.validate_directory_exists("Z:\\totally\\nonexistent\\path")
        assert valid is False


class TestGetInput:

    def test_basic_input(self, icli):
        with patch("builtins.input", return_value="hello"):
            result = icli.get_input("Enter", allow_empty=True)
        assert result == "hello"

    def test_empty_input_with_default(self, icli):
        with patch("builtins.input", return_value=""):
            result = icli.get_input("Enter", default="default_val", allow_empty=True)
        assert result == "default_val"

    def test_empty_input_required(self, icli):
        with patch("builtins.input", side_effect=["", "valid"]):
            result = icli.get_input("Enter", required=True, allow_empty=False)
        assert result == "valid"

    def test_empty_input_not_required(self, icli):
        with patch("builtins.input", return_value=""):
            result = icli.get_input("Enter", required=False, allow_empty=False)
        assert result is None

    def test_path_quotes_cleaned(self, icli):
        with patch("builtins.input", return_value='"C:\\path\\file"'):
            result = icli.get_input("Path", allow_empty=True)
        assert result == "C:\\path\\file"

    def test_history_recorded(self, icli):
        with patch("builtins.input", return_value="test_value"):
            icli.get_input("Prompt", allow_empty=True)
        assert len(icli.history) == 1
        assert icli.history[0]["value"] == "test_value"

    def test_validator_pass(self, icli):
        validator = lambda x: (True, "")
        with patch("builtins.input", return_value="good"):
            result = icli.get_input("Test", validator=validator, allow_empty=True)
        assert result == "good"

    def test_validator_fail_then_retry(self, icli):
        validator = lambda x: (False, "bad input")
        with patch("builtins.input", side_effect=["bad", "n"]):
            result = icli.get_input("Test", validator=validator, allow_empty=True)
        assert result is None


class TestGetChoice:

    def test_valid_choice(self, icli):
        with patch("builtins.input", return_value="1"):
            result = icli.get_choice(["A", "B", "C"])
        assert result == 1

    def test_last_choice(self, icli):
        with patch("builtins.input", return_value="3"):
            result = icli.get_choice(["A", "B", "C"])
        assert result == 3

    def test_invalid_then_valid(self, icli):
        with patch("builtins.input", side_effect=["abc", "0", "2"]):
            result = icli.get_choice(["A", "B", "C"])
        assert result == 2

    def test_empty_then_valid(self, icli):
        with patch("builtins.input", side_effect=["", "1"]):
            result = icli.get_choice(["A", "B"])
        assert result == 1


class TestPrintMethods:

    def test_print_header(self, icli, capsys):
        icli.clear_screen = lambda: None
        icli.print_header()
        captured = capsys.readouterr()
        assert "PDF" in captured.out

    def test_print_section(self, icli, capsys):
        icli.print_section("Test Section")
        captured = capsys.readouterr()
        assert "Test Section" in captured.out

    def test_print_success(self, icli, capsys):
        icli.print_success("Done!")
        captured = capsys.readouterr()
        assert "Done!" in captured.out

    def test_print_error(self, icli, capsys):
        icli.print_error("Failed!")
        captured = capsys.readouterr()
        assert "Failed!" in captured.out

    def test_print_warning(self, icli, capsys):
        icli.print_warning("Careful!")
        captured = capsys.readouterr()
        assert "Careful!" in captured.out

    def test_print_info(self, icli, capsys):
        icli.print_info("Info here")
        captured = capsys.readouterr()
        assert "Info here" in captured.out

    def test_print_menu(self, icli, capsys):
        icli.print_menu(["Option 1", "Option 2"], title="Test Menu")
        captured = capsys.readouterr()
        assert "Test Menu" in captured.out
        assert "Option 1" in captured.out
        assert "Option 2" in captured.out


class TestStepTemplate:

    def test_step_template_success(self, icli, icli_text_pdf):
        with patch("builtins.input", return_value=icli_text_pdf):
            result = icli.step_template()
        assert result is True
        assert icli.config["template_path"] == icli_text_pdf

    def test_step_template_cancel(self, icli):
        with patch("builtins.input", side_effect=["", "n"]):
            with patch.object(icli, "get_input", return_value=None):
                result = icli.step_template()
        assert result is False

    def test_step_template_with_previous_config(self, icli, icli_text_pdf):
        icli.config["template_path"] = icli_text_pdf
        with patch("builtins.input", return_value=icli_text_pdf):
            result = icli.step_template()
        assert result is True


class TestStepData:

    def test_step_data_success(self, icli, icli_csv):
        with patch("builtins.input", return_value=icli_csv):
            result = icli.step_data()
        assert result is True
        assert icli.config["data_path"] == icli_csv

    def test_step_data_cancel(self, icli):
        with patch.object(icli, "get_input", return_value=None):
            result = icli.step_data()
        assert result is False


class TestStepMode:

    def test_step_mode_form(self, icli):
        with patch("builtins.input", return_value="1"):
            result = icli.step_mode()
        assert result is True
        assert icli.config["mode"] == "form"

    def test_step_mode_text(self, icli):
        with patch("builtins.input", return_value="2"):
            result = icli.step_mode()
        assert result is True
        assert icli.config["mode"] == "text"

    def test_step_mode_auto(self, icli):
        with patch("builtins.input", return_value="3"):
            result = icli.step_mode()
        assert result is True
        assert icli.config["mode"] == "auto"


class TestStepNaming:

    def test_step_naming_default(self, icli):
        with patch("builtins.input", return_value=""):
            result = icli.step_naming()
        assert result is True
        assert icli.config["naming_pattern"] == "document_{row}"

    def test_step_naming_custom(self, icli):
        with patch("builtins.input", return_value="{name}_{row}"):
            result = icli.step_naming()
        assert result is True
        assert icli.config["naming_pattern"] == "{name}_{row}"


class TestStepOptions:

    def test_options_zip_yes_clean_no(self, icli):
        with patch("builtins.input", side_effect=["1", "2"]):
            result = icli.step_options()
        assert result is True
        assert icli.config["zip_enabled"] is True
        assert icli.config["clean_output"] is False

    def test_options_zip_no_clean_yes(self, icli):
        with patch("builtins.input", side_effect=["2", "1"]):
            result = icli.step_options()
        assert result is True
        assert icli.config["zip_enabled"] is False
        assert icli.config["clean_output"] is True


class TestStepSummary:

    def test_summary_confirm(self, icli):
        icli.config.update({
            "template_path": "template.pdf",
            "data_path": "data.csv",
            "output_dir": "./output",
            "mode": "form",
            "naming_pattern": "doc_{row}",
            "zip_enabled": True,
            "clean_output": False,
        })
        with patch("builtins.input", return_value="y"):
            result = icli.step_summary()
        assert result is True

    def test_summary_cancel(self, icli):
        icli.config.update({
            "template_path": "template.pdf",
            "data_path": "data.csv",
            "output_dir": "./output",
            "mode": "text",
            "naming_pattern": "doc_{row}",
            "zip_enabled": False,
            "clean_output": False,
        })
        with patch("builtins.input", return_value="n"):
            result = icli.step_summary()
        assert result is False


class TestRun:

    def test_run_interactive_mode(self, icli):
        with patch.object(icli, "run_interactive", return_value=True):
            result = icli.run([])
        assert result == 0

    def test_run_interactive_false(self, icli):
        with patch.object(icli, "run_interactive", return_value=False):
            result = icli.run([])
        assert result == 1

    def test_run_with_args(self, icli, icli_text_pdf, icli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = icli.run(["-t", icli_text_pdf, "-d", icli_csv, "-o", output, "-m", "text"])
        assert result == 0

    def test_run_interactive_flag(self, icli):
        with patch.object(icli, "run_interactive", return_value=True):
            result = icli.run(["--interactive"])
        assert result == 0
