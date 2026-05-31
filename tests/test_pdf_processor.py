import os
import fitz
import pytest
from src.pdf_processor import (
    read_form_fields,
    get_form_field_names,
    fill_form_pdf,
    detect_text_placeholders,
    replace_text,
    get_pdf_info,
    validate_template,
    PDFProcessError,
)


class TestReadFormFields:

    def test_pdf_with_form_fields(self, form_template_pdf):
        fields = read_form_fields(form_template_pdf)
        assert isinstance(fields, dict)
        assert len(fields) == 2

    def test_pdf_without_form_fields(self, simple_pdf):
        fields = read_form_fields(simple_pdf)
        assert isinstance(fields, dict)
        assert len(fields) == 0

    def test_nonexistent_file(self):
        with pytest.raises(PDFProcessError, match="not found"):
            read_form_fields("nonexistent.pdf")

    def test_non_pdf_file(self, tmp_path):
        txt = tmp_path / "not.pdf"
        txt.write_text("not a pdf")
        with pytest.raises(PDFProcessError):
            read_form_fields(str(txt))


class TestGetFormFieldNames:

    def test_pdf_with_fields(self, form_template_pdf):
        names = get_form_field_names(form_template_pdf)
        assert isinstance(names, list)
        assert "name" in names
        assert "email" in names

    def test_pdf_without_fields(self, simple_pdf):
        names = get_form_field_names(simple_pdf)
        assert names == []

    def test_nonexistent_file(self):
        with pytest.raises(PDFProcessError):
            get_form_field_names("nonexistent.pdf")


class TestFillFormPdf:

    def test_fill_form(self, form_template_pdf, tmp_path):
        output = str(tmp_path / "filled.pdf")
        data = {"name": "张三", "email": "zhangsan@test.com"}
        result = fill_form_pdf(form_template_pdf, data, output)
        assert result is True
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0

    def test_output_creates_directory(self, form_template_pdf, tmp_path):
        output = str(tmp_path / "subdir" / "nested" / "filled.pdf")
        data = {"name": "test", "email": "test@test.com"}
        result = fill_form_pdf(form_template_pdf, data, output)
        assert result is True
        assert os.path.exists(output)

    def test_nonexistent_template(self, tmp_path):
        output = str(tmp_path / "out.pdf")
        with pytest.raises(PDFProcessError, match="not found"):
            fill_form_pdf("nonexistent.pdf", {"a": "b"}, output)

    def test_pdf_no_form_fields(self, simple_pdf, tmp_path):
        output = str(tmp_path / "out.pdf")
        with pytest.raises(PDFProcessError, match="no form fields"):
            fill_form_pdf(simple_pdf, {"a": "b"}, output)


class TestDetectTextPlaceholders:

    def test_detect_placeholders(self, text_template_pdf):
        placeholders = detect_text_placeholders(text_template_pdf)
        assert isinstance(placeholders, list)
        assert sorted(placeholders) == ["company", "email", "name"]

    def test_no_placeholders(self, simple_pdf):
        placeholders = detect_text_placeholders(simple_pdf)
        assert placeholders == []

    def test_nonexistent_file(self):
        with pytest.raises(PDFProcessError, match="not found"):
            detect_text_placeholders("nonexistent.pdf")

    def test_sorted_output(self, text_template_pdf):
        placeholders = detect_text_placeholders(text_template_pdf)
        assert placeholders == sorted(placeholders)


class TestReplaceText:

    def test_basic_replacement(self, text_template_pdf, tmp_path):
        output = str(tmp_path / "replaced.pdf")
        replacements = {"name": "张三", "email": "zhangsan@test.com", "company": "百度"}
        result = replace_text(text_template_pdf, replacements, output)
        assert result is True
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0

    def test_partial_replacement(self, text_template_pdf, tmp_path):
        output = str(tmp_path / "partial.pdf")
        replacements = {"name": "only_name"}
        result = replace_text(text_template_pdf, replacements, output)
        assert result is True

    def test_empty_replacements(self, text_template_pdf, tmp_path):
        output = str(tmp_path / "empty.pdf")
        result = replace_text(text_template_pdf, {}, output)
        assert result is True
        assert os.path.exists(output)

    def test_nonexistent_template(self, tmp_path):
        with pytest.raises(PDFProcessError, match="not found"):
            replace_text("nonexistent.pdf", {"a": "b"}, str(tmp_path / "out.pdf"))

    def test_output_creates_dir(self, text_template_pdf, tmp_path):
        output = str(tmp_path / "deep" / "nested" / "out.pdf")
        result = replace_text(text_template_pdf, {"name": "test"}, output)
        assert result is True


class TestGetPdfInfo:

    def test_basic_info(self, simple_pdf):
        info = get_pdf_info(simple_pdf)
        assert isinstance(info, dict)
        assert info["num_pages"] == 1
        assert info["file_size"] > 0
        assert "metadata" in info
        assert "form_fields" in info
        assert "is_encrypted" in info

    def test_pdf_with_form_fields(self, form_template_pdf):
        info = get_pdf_info(form_template_pdf)
        assert len(info["form_fields"]) == 2
        assert "name" in info["form_fields"]

    def test_multi_page_pdf(self, tmp_path):
        pdf = tmp_path / "multi.pdf"
        doc = fitz.open()
        doc.new_page()
        doc.new_page()
        doc.new_page()
        doc.save(str(pdf))
        doc.close()
        info = get_pdf_info(str(pdf))
        assert info["num_pages"] == 3

    def test_nonexistent_file(self):
        with pytest.raises(PDFProcessError, match="not found"):
            get_pdf_info("nonexistent.pdf")


class TestValidateTemplate:

    def test_valid_form_template(self, form_template_pdf):
        result = validate_template(form_template_pdf, ["name", "email"], mode="form")
        assert result["valid"] is True
        assert result["missing_fields"] == []
        assert "name" in result["found_fields"]
        assert "email" in result["found_fields"]

    def test_missing_fields_form(self, form_template_pdf):
        result = validate_template(
            form_template_pdf, ["name", "email", "phone"], mode="form"
        )
        assert result["valid"] is False
        assert "phone" in result["missing_fields"]

    def test_valid_text_template(self, text_template_pdf):
        result = validate_template(
            text_template_pdf, ["name", "email", "company"], mode="text"
        )
        assert result["valid"] is True

    def test_missing_fields_text(self, text_template_pdf):
        result = validate_template(
            text_template_pdf, ["name", "missing_field"], mode="text"
        )
        assert result["valid"] is False
        assert "missing_field" in result["missing_fields"]

    def test_no_fields_warning(self, simple_pdf):
        result = validate_template(simple_pdf, [], mode="text")
        assert len(result["warnings"]) > 0

    def test_empty_required_fields(self, form_template_pdf):
        result = validate_template(form_template_pdf, [], mode="form")
        assert result["valid"] is True
