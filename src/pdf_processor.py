"""PDF operations with atomic writes and explicit replacement errors."""
import os
import re
import tempfile
from contextlib import contextmanager
from pathlib import Path
from io import BytesIO

import pymupdf as fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, TextStringObject

PLACEHOLDER = re.compile(r"\{\{\s*(\w+)\s*\}\}")


class PDFProcessError(Exception):
    """A PDF could not be inspected or generated."""


@contextmanager
def atomic_output(source, output):
    destination = Path(output).resolve()
    if Path(source).resolve() == destination:
        raise PDFProcessError("Output must not overwrite the PDF template")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(suffix=".pdf", dir=destination.parent)
    os.close(fd)
    try:
        yield temporary
        os.replace(temporary, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)


def _reader(path):
    if not Path(path).is_file():
        raise PDFProcessError(f"PDF file not found: {path}")
    reader = PdfReader(path)
    if reader.is_encrypted and not reader.decrypt(""):
        raise PDFProcessError("Password-protected PDFs are not supported")
    return reader


def _widgets(document):
    for page in document.pages:
        for ref in page.get("/Annots", []):
            widget = ref.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            ancestors = [widget]
            while "/Parent" in ancestors[-1]:
                parent = ancestors[-1]["/Parent"]
                if any(parent is item for item in ancestors) or len(ancestors) > 100:
                    raise PDFProcessError("Cyclic form field tree")
                ancestors.append(parent)
            name = ".".join(str(item["/T"]) for item in reversed(ancestors) if "/T" in item)
            yield name, widget, ancestors


def _form_structure(document):
    canonical = document.get_fields() or {}
    fields = {name: item for name, item in canonical.items()
              if item.get("/FT") in ("/Tx", "/Ch", "/Btn")
              and not (item.get("/FT") == "/Btn" and int(item.get("/Ff", 0)) & 65536)}
    orphans = {}
    known_refs = {name: getattr(item, "indirect_reference", None) for name, item in canonical.items()}
    for name, widget, ancestors in _widgets(document):
        if not name:
            continue
        kind = next((item["/FT"] for item in ancestors if "/FT" in item), None)
        if kind not in ("/Tx", "/Ch", "/Btn"):
            continue
        refs = [getattr(item, "indirect_reference", None) for item in ancestors]
        if name in known_refs and known_refs[name] not in refs:
            raise PDFProcessError(f"Ambiguous form field and widget: {name}")
        if name not in canonical:
            node = next(item for item in ancestors if "/T" in item)
            fields[name] = DictionaryObject(node)
            fields[name][NameObject("/FT")] = kind
            if kind == "/Btn":
                states = widget.get("/AP", {}).get("/N", {})
                fields[name][NameObject("/_States_")] = ArrayObject(NameObject(k) for k in states)
            known_refs[name] = getattr(node, "indirect_reference", None)
            root = ancestors[-1]
            reference = getattr(root, "indirect_reference", None)
            if reference is None:
                raise PDFProcessError(f"Malformed orphan form field: {name}")
            orphans[(reference.idnum, reference.generation)] = root
    return fields, list(orphans.values())


def read_form_fields(pdf_path):
    """Return fillable text, checkbox and choice fields, excluding signatures."""
    try:
        fields, _ = _form_structure(_reader(pdf_path))
        return {name: field.get("/V", "") for name, field in fields.items()}
    except PDFProcessError:
        raise
    except Exception as exc:
        raise PDFProcessError(f"Error reading PDF form fields: {exc}") from exc


def get_form_field_names(pdf_path):
    return list(read_form_fields(pdf_path))


def _unicode_form_font(writer, values):
    """Embed MuPDF's redistributable CJK font for Unicode appearances and editing."""
    unicode_fields = {name for name, value in values.items() if any(ord(c) > 255 for c in value)}
    if not unicode_fields:
        return
    font = fitz.Font("china-ss")
    for name in unicode_fields:
        if any(not font.has_glyph(ord(c)) for c in values[name] if not c.isspace()):
            raise PDFProcessError(f"Unsupported character in form field: {name}")
    with fitz.open() as font_doc:
        page = font_doc.new_page()
        page.insert_font(fontname="PMMCJK", fontbuffer=font.buffer)
        font_reader = PdfReader(BytesIO(font_doc.tobytes()))
        resource = font_reader.pages[0]["/Resources"]["/Font"]["/PMMCJK"]
        acroform = writer.root_object["/AcroForm"]
        resources = acroform.setdefault(NameObject("/DR"), DictionaryObject())
        fonts = resources.setdefault(NameObject("/Font"), DictionaryObject())
        font_name = "/PMMCJK"
        while font_name in fonts:
            font_name += "X"
        fonts[NameObject(font_name)] = resource.clone(writer)
        for target_page in writer.pages:
            for ref in target_page.get("/Annots", []):
                widget = ref.get_object()
                ancestors = [widget]
                while "/Parent" in ancestors[-1]:
                    parent = ancestors[-1]["/Parent"]
                    if any(parent is item for item in ancestors):
                        raise PDFProcessError("Cyclic form field tree")
                    ancestors.append(parent)
                name = ".".join(str(item["/T"]) for item in reversed(ancestors) if "/T" in item)
                if name not in unicode_fields:
                    continue
                appearance = str(widget.get("/DA", acroform.get("/DA", "/Helvetica 0 Tf 0 g")))
                appearance = re.sub(r"/[^\s/]+\s+[\d.]+\s+Tf", f"{font_name} 0 Tf", appearance)
                widget[NameObject("/DA")] = TextStringObject(appearance)


def fill_form_pdf(pdf_path, data, output_path):
    try:
        reader = _reader(pdf_path)
        fields, orphans = _form_structure(reader)
        if not fields:
            raise PDFProcessError("PDF has no form fields to fill")
        unknown = set(data) - set(fields)
        if unknown:
            raise PDFProcessError(f"Unknown form fields: {', '.join(sorted(unknown))}")
        values = {}
        for key, value in data.items():
            field = fields[key]
            if field.get("/FT") == "/Sig":
                raise PDFProcessError("Signature fields cannot be filled as text")
            text = "" if value is None else str(value)
            if field.get("/FT") == "/Btn":
                states = [str(v) for v in field.get("/_States_", [])]
                if text.lower() in ("true", "1", "yes", "是"):
                    text = next((v for v in states if v != "/Off"), "/Yes")
                elif text.lower() in ("false", "0", "no", "否", ""):
                    text = "/Off"
                elif not text.startswith("/"):
                    text = "/" + text
                if states and text not in states:
                    raise PDFProcessError(f"Invalid checkbox/radio value for {key}: {text}")
            values[key] = text
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        if orphans:
            # Attach only verified orphan roots. Blind reattachment can create
            # a second canonical field with the same name as a page widget.
            _, writer_orphans = _form_structure(writer)
            acroform = writer.root_object.setdefault(NameObject("/AcroForm"), DictionaryObject())
            tree = acroform.setdefault(NameObject("/Fields"), ArrayObject())
            for root in writer_orphans:
                if root.indirect_reference not in tree:
                    tree.append(root.indirect_reference)
        _unicode_form_font(writer, values)
        writer.update_page_form_field_values(None, values, auto_regenerate=False)
        with atomic_output(pdf_path, output_path) as temporary:
            writer.write(temporary)
            reopened = PdfReader(temporary)
            written = reopened.get_fields() or {}
            for key, value in values.items():
                if key not in written or str(written[key].get("/V", "")) != value:
                    raise PDFProcessError(f"Form field was not saved correctly: {key}")
            for name, widget, ancestors in _widgets(reopened):
                if name not in values:
                    continue
                effective = next((item["/V"] for item in ancestors if "/V" in item), "")
                if str(effective) != values[name] or not widget.get("/AP", {}).get("/N"):
                    raise PDFProcessError(f"Form widget was not saved correctly: {name}")
        return True
    except PDFProcessError:
        raise
    except Exception as exc:
        raise PDFProcessError(f"Error filling PDF form: {exc}") from exc


def _open(path):
    if not Path(path).is_file():
        raise PDFProcessError(f"PDF file not found: {path}")
    doc = fitz.open(path)
    if doc.needs_pass and not doc.authenticate(""):
        doc.close()
        raise PDFProcessError("Password-protected PDFs are not supported")
    return doc


def detect_text_placeholders(pdf_path):
    try:
        with _open(pdf_path) as doc:
            return sorted({match.group(1) for page in doc
                           for match in PLACEHOLDER.finditer(page.get_text())})
    except PDFProcessError:
        raise
    except Exception as exc:
        raise PDFProcessError(f"Error detecting text placeholders: {exc}") from exc


def replace_text(pdf_path, replacements, output_path):
    """Fit single-line values inside tokens; reject unreadable overflow.

    Collect original spans before redacting. Keep pictures, line art, text color
    and baseline. A failed replacement never produces a successful output.
    """
    try:
        with _open(pdf_path) as doc:
            for page in doc:
                original = page.get_text("dict")
                chars = [char for block in page.get_text("rawdict")["blocks"]
                         for line in block.get("lines", [])
                         for span in line.get("spans", []) for char in span.get("chars", [])]
                jobs = []
                for match in PLACEHOLDER.finditer(page.get_text()):
                    key = match.group(1)
                    if key not in replacements:
                        continue
                    if "\n" in match.group(0) or "\r" in match.group(0):
                        raise PDFProcessError(f"Multiline placeholder is not supported: {key}")
                    for rect in page.search_for(match.group(0)):
                        if any(rect == job[0] for job in jobs):
                            continue
                        spans = [span for block in original["blocks"]
                                 for line in block.get("lines", [])
                                 for span in line.get("spans", [])
                                 if fitz.Rect(span["bbox"]).intersects(rect)]
                        span = spans[0] if spans else {}
                        lines = [line for block in original["blocks"] for line in block.get("lines", [])
                                 if any(fitz.Rect(item["bbox"]).intersects(rect) for item in line.get("spans", []))]
                        if any(tuple(line.get("dir", (1, 0))) != (1, 0) for line in lines):
                            raise PDFProcessError(f"Rotated placeholder is not supported: {key}")
                        value = "" if replacements[key] is None else str(replacements[key])
                        if "\n" in value or "\r" in value:
                            raise PDFProcessError(f"Multiline value requires a form field: {key}")
                        fontname = "china-ss" if any(ord(c) > 255 for c in value) else "helv"
                        font = fitz.Font(fontname)
                        if any(not font.has_glyph(ord(c)) for c in value if not c.isspace()):
                            raise PDFProcessError(f"Unsupported character in placeholder: {key}")
                        size = float(span.get("size", 12))
                        length = font.text_length(value, fontsize=size)
                        following = [char["bbox"][0] for char in chars
                                     if char["bbox"][0] >= rect.x1 - 0.2
                                     and abs(char["origin"][1] - span.get("origin", (0, rect.y1))[1]) < 2]
                        right = min(following) - 1 if following else page.rect.width - 24
                        available = max(rect.width, right - rect.x0)
                        if length > available:
                            size *= available / length
                        if value and size < 6:
                            raise PDFProcessError(f"Value too long for placeholder '{key}'; enlarge the template field")
                        baseline = span.get("origin", (rect.x0, rect.y1 - 2))[1]
                        color = fitz.sRGB_to_pdf(span.get("color", 0))
                        jobs.append((rect, value, fontname, size, baseline, color))
                for rect, *_ in jobs:
                    page.add_redact_annot(rect, fill=False, cross_out=False)
                if jobs:
                    page.apply_redactions(images=0, graphics=0)
                for rect, value, fontname, size, baseline, color in jobs:
                    if value:
                        page.insert_text((rect.x0, baseline), value, fontsize=size,
                                         fontname=fontname, color=color)
            with atomic_output(pdf_path, output_path) as temporary:
                doc.save(temporary, garbage=4, deflate=True)
        return True
    except PDFProcessError:
        raise
    except Exception as exc:
        raise PDFProcessError(f"Error replacing text in PDF: {exc}") from exc


def get_pdf_info(pdf_path):
    try:
        reader = _reader(pdf_path)
        return {"num_pages": len(reader.pages), "metadata": reader.metadata,
                "form_fields": get_form_field_names(pdf_path),
                "file_size": os.path.getsize(pdf_path), "is_encrypted": reader.is_encrypted}
    except PDFProcessError:
        raise
    except Exception as exc:
        raise PDFProcessError(f"Error reading PDF info: {exc}") from exc


def validate_template(pdf_path, required_fields, mode="form"):
    if mode not in ("form", "text"):
        raise PDFProcessError(f"Unsupported mode: {mode}")
    found = get_form_field_names(pdf_path) if mode == "form" else detect_text_placeholders(pdf_path)
    missing = [field for field in required_fields if field not in found]
    return {"valid": not missing, "missing_fields": missing, "found_fields": found,
            "warnings": [] if found else [f"No fields found in PDF template (mode: {mode})"]}
