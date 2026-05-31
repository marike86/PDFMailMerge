import os
import csv
import fitz
import pytest
from unittest.mock import patch, MagicMock
from src.cli import MailMergeCLI


@pytest.fixture
def cli():
    return MailMergeCLI()


@pytest.fixture
def cli_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        writer.writeheader()
        writer.writerow({"name": "张三", "email": "zhangsan@test.com"})
        writer.writerow({"name": "李四", "email": "lisi@test.com"})
    return str(csv_file)


@pytest.fixture
def cli_text_pdf(tmp_path):
    pdf_path = tmp_path / "template.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Name: {{name}}", fontsize=12)
    page.insert_text((72, 120), "Email: {{email}}", fontsize=12)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


@pytest.fixture
def cli_form_pdf(tmp_path):
    pdf_path = tmp_path / "form_template.pdf"
    doc = fitz.open()
    page = doc.new_page()
    widget = fitz.Widget()
    widget.field_name = "name"
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.rect = fitz.Rect(100, 60, 300, 80)
    page.add_widget(widget)
    widget2 = fitz.Widget()
    widget2.field_name = "email"
    widget2.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget2.rect = fitz.Rect(100, 100, 300, 120)
    page.add_widget(widget2)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


class TestMailMergeCLIParser:

    def test_parser_creation(self, cli):
        assert cli.parser is not None

    def test_required_args(self, cli):
        with pytest.raises(SystemExit):
            cli.parser.parse_args([])

    def test_template_arg(self, cli):
        args = cli.parser.parse_args(["-t", "template.pdf", "-d", "data.csv"])
        assert args.template == "template.pdf"

    def test_data_arg(self, cli):
        args = cli.parser.parse_args(["-t", "template.pdf", "-d", "data.csv"])
        assert args.data == "data.csv"

    def test_output_default(self, cli):
        args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv"])
        assert args.output == "./output"

    def test_mode_choices(self, cli):
        for mode in ["form", "text", "auto"]:
            args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv", "-m", mode])
            assert args.mode == mode

    def test_zip_flag(self, cli):
        args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv", "--zip"])
        assert args.zip is True

    def test_clean_flag(self, cli):
        args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv", "--clean"])
        assert args.clean is True

    def test_verbose_flag(self, cli):
        args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv", "-v"])
        assert args.verbose is True

    def test_validate_only_flag(self, cli):
        args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv", "--validate-only"])
        assert args.validate_only is True

    def test_name_pattern(self, cli):
        args = cli.parser.parse_args(["-t", "t.pdf", "-d", "d.csv", "-n", "{name}_{row}"])
        assert args.name == "{name}_{row}"


class TestMailMergeCLIRun:

    def test_run_text_mode(self, cli, cli_text_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", cli_text_pdf, "-d", cli_csv, "-o", output, "-m", "text"])
        assert result == 0
        files = [f for f in os.listdir(output) if f.endswith(".pdf")]
        assert len(files) == 2

    def test_run_auto_mode_text(self, cli, cli_text_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", cli_text_pdf, "-d", cli_csv, "-o", output, "-m", "auto"])
        assert result == 0

    def test_run_auto_mode_form(self, cli, cli_form_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", cli_form_pdf, "-d", cli_csv, "-o", output, "-m", "auto"])
        assert result == 0

    def test_run_form_mode(self, cli, cli_form_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", cli_form_pdf, "-d", cli_csv, "-o", output, "-m", "form"])
        assert result == 0

    def test_validate_only(self, cli, cli_text_pdf, cli_csv, capsys):
        result = cli.run(["-t", cli_text_pdf, "-d", cli_csv, "--validate-only"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Validation passed" in captured.out

    def test_verbose_output(self, cli, cli_text_pdf, cli_csv, tmp_path, capsys):
        output = str(tmp_path / "output")
        result = cli.run(["-t", cli_text_pdf, "-d", cli_csv, "-o", output, "-m", "text", "-v"])
        assert result == 0
        captured = capsys.readouterr()
        assert "PDF Mail Merge Tool" in captured.out

    def test_clean_output(self, cli, cli_text_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        os.makedirs(output, exist_ok=True)
        old_file = os.path.join(output, "old_file.txt")
        with open(old_file, "w") as f:
            f.write("old")
        result = cli.run(["-t", cli_text_pdf, "-d", cli_csv, "-o", output, "-m", "text", "--clean"])
        assert result == 0
        assert not os.path.exists(old_file)

    def test_custom_naming(self, cli, cli_text_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run([
            "-t", cli_text_pdf, "-d", cli_csv, "-o", output,
            "-m", "text", "-n", "{name}_doc"
        ])
        assert result == 0
        files = os.listdir(output)
        assert any("张三" in f for f in files)

    def test_nonexistent_template(self, cli, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", "nonexistent.pdf", "-d", cli_csv, "-o", output])
        assert result == 1

    def test_nonexistent_data(self, cli, cli_text_pdf, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", cli_text_pdf, "-d", "nonexistent.csv", "-o", output])
        assert result == 1

    def test_zip_creation(self, cli, cli_text_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        parent = str(tmp_path)
        result = cli.run([
            "-t", cli_text_pdf, "-d", cli_csv, "-o", output,
            "-m", "text", "--zip"
        ])
        assert result == 0
        zip_files = [f for f in os.listdir(parent) if f.endswith(".zip")]
        assert len(zip_files) > 0

    def test_keyboard_interrupt(self, cli):
        with patch("argparse.ArgumentParser.parse_args", side_effect=KeyboardInterrupt):
            result = cli.run([])
        assert result == 130

    def test_auto_mode_no_fields(self, cli, simple_pdf, cli_csv, tmp_path):
        output = str(tmp_path / "output")
        result = cli.run(["-t", simple_pdf, "-d", cli_csv, "-o", output, "-m", "auto"])
        assert result == 1
