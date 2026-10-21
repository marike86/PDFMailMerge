"""Regressions for data loss, invalid success reports and Unicode rendering."""
import zipfile
from pathlib import Path
from threading import Event

import pandas as pd
import pymupdf as fitz
import pytest
from pypdf import PdfReader
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject

from src.cli import MailMergeCLI
from src.data_loader import load_csv, data_to_dict_list
from src.merge_service import inspect_inputs, run_merge, MergeError
from src.pdf_processor import fill_form_pdf, replace_text, detect_text_placeholders, PDFProcessError
from src.utils import parse_naming_pattern, create_zip_archive, extract_zip_archive, validate_path


def test_csv_preserves_ids_blanks_and_na(tmp_path):
    source = tmp_path / "ids.csv"
    source.write_text("id,name,region\n000123,,NA\n", encoding="utf-8-sig")
    row = data_to_dict_list(load_csv(source))[0]
    assert row == {"id": "000123", "name": "", "region": "NA"}


def test_missing_json_cells_are_empty():
    assert data_to_dict_list(pd.DataFrame([{"a": 1}, {"b": None}]))[1] == {"a": "", "b": ""}


def test_unicode_form_value_and_widget_appearance(form_template_pdf, tmp_path):
    output = tmp_path / "unicode.pdf"
    fill_form_pdf(form_template_pdf, {"name": "张三", "email": "a@example.com"}, output)
    reader = PdfReader(output)
    assert reader.get_fields()["name"]["/V"] == "张三"
    widget = reader.pages[0]["/Annots"][0].get_object()
    assert widget["/V"] == "张三"
    assert widget["/AP"]["/N"].get_data()
    with fitz.open(output) as doc:
        assert "张三" in doc[0].get_text()
        assert doc[0].get_pixmap().width > 0


def test_orphan_widgets_are_reattached(form_template_pdf, tmp_path):
    broken = tmp_path / "orphan.pdf"
    writer = PdfWriter(clone_from=form_template_pdf)
    writer.root_object["/AcroForm"][NameObject("/Fields")] = ArrayObject()
    writer.write(broken)
    output = tmp_path / "repaired.pdf"
    fill_form_pdf(broken, {"name": "张三", "email": "a@example.com"}, output)
    assert PdfReader(output).get_fields()["name"]["/V"] == "张三"


def test_ambiguous_form_tree_is_rejected(form_template_pdf, tmp_path):
    broken = tmp_path / "ambiguous.pdf"
    writer = PdfWriter(clone_from=form_template_pdf)
    widget = writer.pages[0]["/Annots"][0].get_object()
    duplicate = DictionaryObject(widget)
    writer.root_object["/AcroForm"]["/Fields"][0] = writer._add_object(duplicate)
    writer.write(broken)
    output = tmp_path / "output.pdf"
    with pytest.raises(PDFProcessError, match="Ambiguous"):
        fill_form_pdf(broken, {"name": "张三"}, output)
    assert not output.exists()


def test_checkbox_fields_are_detected_and_filled(tmp_path):
    from src.pdf_processor import get_form_field_names
    source, output = tmp_path / "checkbox.pdf", tmp_path / "checked.pdf"
    with fitz.open() as doc:
        page = doc.new_page()
        widget = fitz.Widget()
        widget.field_name = "approved"
        widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
        widget.rect = fitz.Rect(50, 50, 70, 70)
        page.add_widget(widget)
        doc.save(source)
    assert get_form_field_names(source) == ["approved"]
    fill_form_pdf(source, {"approved": True}, output)
    reader = PdfReader(output)
    value = reader.get_fields()["approved"]["/V"]
    assert value != "/Off"
    assert reader.pages[0]["/Annots"][0].get_object()["/AS"] == value


def test_all_form_pages_are_filled(tmp_path):
    source, output = tmp_path / "two-pages.pdf", tmp_path / "filled-pages.pdf"
    with fitz.open() as doc:
        for name in ("first", "second"):
            page = doc.new_page()
            widget = fitz.Widget()
            widget.field_name = name
            widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            widget.rect = fitz.Rect(50, 50, 250, 80)
            page.add_widget(widget)
        doc.save(source)
    fill_form_pdf(source, {"first": "第一页", "second": "第二页"}, output)
    reader = PdfReader(output)
    for index, name in enumerate(("first", "second")):
        assert reader.pages[index]["/Annots"][0].get_object()["/V"] == reader.get_fields()[name]["/V"]
    with fitz.open(output) as doc:
        assert "第一页" in doc[0].get_text()
        assert "第二页" in doc[1].get_text()


def test_rotated_placeholder_returns_explicit_error(tmp_path):
    source = tmp_path / "rotated.pdf"
    with fitz.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 200), "{{name}}", rotate=90)
        doc.save(source)
    with pytest.raises(PDFProcessError, match="Rotated"):
        replace_text(source, {"name": "Alice"}, tmp_path / "out.pdf")


def test_text_preserves_neighbour_and_background(tmp_path):
    source, output = tmp_path / "template.pdf", tmp_path / "filled.pdf"
    with fitz.open() as doc:
        page = doc.new_page()
        page.draw_rect(fitz.Rect(40, 35, 500, 100), color=(0, 0, 1), fill=(0.9, 0.95, 1))
        page.insert_text((60, 65), "Name: {{ name }} / Keep this", fontsize=14, color=(0, 0, 1))
        doc.save(source)
    assert detect_text_placeholders(source) == ["name"]
    replace_text(source, {"name": "张三"}, output)
    with fitz.open(output) as doc:
        text = doc[0].get_text()
        assert "张三" in text and "Keep this" in text and "{{" not in text
        assert len(doc[0].get_drawings()) >= 1
        assert doc[0].get_pixmap().pixel(50, 40) == (229, 242, 255)


def test_overflow_is_an_error_and_leaves_no_output(text_template_pdf, tmp_path):
    output = tmp_path / "failed.pdf"
    with pytest.raises(PDFProcessError, match="too long"):
        replace_text(text_template_pdf, {"name": "Long value " * 300}, output)
    assert not output.exists()


def test_template_cannot_be_overwritten(text_template_pdf):
    before = Path(text_template_pdf).read_bytes()
    with pytest.raises(PDFProcessError, match="overwrite"):
        replace_text(text_template_pdf, {}, text_template_pdf)
    assert Path(text_template_pdf).read_bytes() == before


@pytest.mark.parametrize("pattern", ["../../{name}", "C:\\outside\\{name}", "CON", "nul.pdf", "...", "hello?*"])
def test_names_are_portable_basenames(pattern):
    name = parse_naming_pattern(pattern, {"name": "x/y"})
    assert name and all(char not in name for char in '/\\:<>"|?*')
    assert name.upper().split(".")[0] not in ("CON", "NUL")
    assert not name.endswith((".", " "))


def test_mapping_duplicates_existing_files_and_zip(text_template_pdf, tmp_path):
    data = tmp_path / "source.csv"
    data.write_text("姓名,email,company\n张三,a@example.com,示例\n张三,b@example.com,示例\n", encoding="utf-8")
    plan = inspect_inputs(text_template_pdf, data, mapping={"name": "姓名"})
    output = tmp_path / "output"
    output.mkdir()
    old = output / "张三.pdf"
    old.write_bytes(b"keep existing")
    result = run_merge(plan, output, "{姓名}.pdf", zip_enabled=True)
    assert not result.errors
    assert len(result.files) == 2
    assert len(set(result.files)) == 2
    assert old.read_bytes() == b"keep existing"
    with zipfile.ZipFile(result.archive) as bundle:
        assert set(bundle.namelist()) == {Path(p).name for p in result.files}
        assert old.name not in bundle.namelist()


def test_failures_reported_and_failed_files_removed(text_template_pdf, tmp_path):
    data = tmp_path / "data.json"
    import json
    data.write_text(json.dumps([{"name": "x" * 10000, "email": "a", "company": "b"}]), encoding="utf-8")
    result = run_merge(inspect_inputs(text_template_pdf, data), tmp_path / "out")
    assert not result.files and len(result.errors) == 1
    assert list((tmp_path / "out").iterdir()) == []


def test_cancel_between_records(text_template_pdf, sample_csv, tmp_path):
    cancel = Event()
    result = run_merge(inspect_inputs(text_template_pdf, sample_csv), tmp_path / "out",
                       cancel=cancel, progress=lambda *_: cancel.set())
    assert result.cancelled and len(result.files) == 1


def test_validate_only_and_invalid_input_never_clean(text_template_pdf, sample_csv, tmp_path):
    output = tmp_path / "results"
    output.mkdir()
    keep = output / "keep.txt"
    keep.write_text("keep")
    args = ["-t", text_template_pdf, "-d", sample_csv, "-o", str(output), "--clean", "--validate-only"]
    assert MailMergeCLI().run(args) == 0
    assert keep.exists()
    args[1] = "missing.pdf"
    args.remove("--validate-only")
    assert MailMergeCLI().run(args) == 1
    assert keep.exists()


def test_clean_refuses_input_directory(text_template_pdf, sample_csv, tmp_path):
    plan = inspect_inputs(text_template_pdf, sample_csv)
    with pytest.raises(MergeError, match="Inputs are inside"):
        run_merge(plan, Path(text_template_pdf).parent, clean=True, data_path=sample_csv)
    assert Path(text_template_pdf).exists()


def test_empty_data_and_missing_mapping_fail_before_output(text_template_pdf, tmp_path):
    data = tmp_path / "empty.csv"
    data.write_text("name,email\n")
    with pytest.raises(MergeError, match="empty"):
        inspect_inputs(text_template_pdf, data)
    data.write_text("name\nAlice\n")
    with pytest.raises(MergeError, match="Missing data"):
        run_merge(inspect_inputs(text_template_pdf, data), tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_zip_does_not_include_itself_and_rejects_traversal(tmp_path):
    (tmp_path / "hello.txt").write_text("hello")
    archive = tmp_path / "archive.zip"
    assert create_zip_archive(tmp_path, archive)
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.namelist() == ["hello.txt"]
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr("../escape.txt", "bad")
    assert not extract_zip_archive(archive, tmp_path / "unzip")
    assert not (tmp_path / "escape.txt").exists()


def test_validation_does_not_destroy_existing_probe_file(tmp_path):
    probe = tmp_path / ".write_test"
    probe.write_text("keep me")
    assert validate_path(str(tmp_path))[0]
    assert probe.read_text() == "keep me"
