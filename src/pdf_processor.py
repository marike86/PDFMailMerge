"""
PDF Processor Module
Handles PDF form filling and text replacement operations.
"""

import os
import re
import fitz
from typing import Dict, List
from pypdf import PdfReader, PdfWriter


class PDFProcessError(Exception):
    """Custom exception for PDF processing errors"""

    pass


def read_form_fields(pdf_path: str) -> Dict[str, str]:
    """
    Read all form fields from a PDF.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Dictionary mapping field names to field types

    Raises:
        PDFProcessError: If PDF cannot be read or has no form
    """
    if not os.path.exists(pdf_path):
        raise PDFProcessError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)

        if not reader.get_form_text_fields():
            return {}

        fields = reader.get_form_text_fields()
        return fields

    except Exception as e:
        raise PDFProcessError(f"Error reading PDF form fields: {str(e)}")


def get_form_field_names(pdf_path: str) -> List[str]:
    """
    Get list of form field names from PDF.

    Args:
        pdf_path: Path to PDF file

    Returns:
        List of field names
    """
    fields = read_form_fields(pdf_path)
    return list(fields.keys())


def fill_form_pdf(pdf_path: str, data: Dict[str, str], output_path: str) -> bool:
    """
    Fill PDF form with provided data.

    Args:
        pdf_path: Path to source PDF template
        data: Dictionary mapping field names to values
        output_path: Path for output PDF file

    Returns:
        True if successful

    Raises:
        PDFProcessError: If PDF cannot be filled
    """
    if not os.path.exists(pdf_path):
        raise PDFProcessError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        writer.clone_document_from_reader(reader)

        if reader.get_form_text_fields():
            for page in writer.pages:
                writer.update_page_form_field_values(page, data)
        else:
            raise PDFProcessError("PDF has no form fields to fill")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        return True

    except PDFProcessError:
        raise
    except Exception as e:
        raise PDFProcessError(f"Error filling PDF form: {str(e)}")


def detect_text_placeholders(pdf_path: str) -> List[str]:
    """
    Detect {{placeholder}} patterns in PDF text.

    Args:
        pdf_path: Path to PDF file

    Returns:
        List of detected placeholder names

    Raises:
        PDFProcessError: If PDF cannot be read
    """
    if not os.path.exists(pdf_path):
        raise PDFProcessError(f"PDF file not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        placeholders = set()

        for page in doc:
            text = page.get_text()
            matches = re.findall(r"\{\{(\w+)\}\}", text)
            placeholders.update(matches)

        doc.close()
        return sorted(list(placeholders))

    except Exception as e:
        raise PDFProcessError(f"Error detecting text placeholders: {str(e)}")


def replace_text(pdf_path: str, replacements: Dict[str, str], output_path: str) -> bool:
    """
    Replace {{placeholder}} text in PDF with provided values.
    Uses PyMuPDF for text replacement operations.

    Args:
        pdf_path: Path to source PDF template
        replacements: Dictionary mapping placeholders to values
        output_path: Path for output PDF file

    Returns:
        True if successful

    Raises:
        PDFProcessError: If PDF cannot be processed
    """
    if not os.path.exists(pdf_path):
        raise PDFProcessError(f"PDF file not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc):
            page_text = page.get_text()

            for placeholder, value in replacements.items():
                pattern = "{{" + placeholder + "}}"

                if pattern in page_text:
                    text_instances = page.search_for(pattern)

                    for inst in text_instances:
                        try:
                            page.add_redact_annot(inst, fill=(1, 1, 1))
                            page.apply_redactions()

                            font_size = 12
                            try:
                                blocks = page.get_text("dict", flags=11)["blocks"]
                                for block in blocks:
                                    for line in block.get("lines", []):
                                        for span in line.get("spans", []):
                                            if pattern in span.get("text", ""):
                                                font_size = span.get("size", 12)
                                                break
                            except Exception:
                                pass

                            page.insert_text(
                                (inst.x0, inst.y0 + font_size * 0.85),
                                value,
                                fontsize=font_size,
                                fontname="china-ss",
                                color=(0, 0, 0),
                            )
                        except Exception as e:
                            print(
                                f"Warning: Could not replace {pattern} on page {page_num + 1}: {e}"
                            )
                            continue

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        doc.save(output_path)
        doc.close()

        return True

    except Exception as e:
        raise PDFProcessError(f"Error replacing text in PDF: {str(e)}")


def get_pdf_info(pdf_path: str) -> Dict[str, any]:
    """
    Get PDF metadata and information.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Dictionary with PDF information

    Raises:
        PDFProcessError: If PDF cannot be read
    """
    if not os.path.exists(pdf_path):
        raise PDFProcessError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)
        doc = fitz.open(pdf_path)

        form_text_fields = reader.get_form_text_fields()
        info = {
            "num_pages": len(reader.pages),
            "metadata": reader.metadata,
            "form_fields": list(form_text_fields.keys()) if form_text_fields else [],
            "file_size": os.path.getsize(pdf_path),
            "is_encrypted": reader.is_encrypted,
        }

        doc.close()
        return info

    except Exception as e:
        raise PDFProcessError(f"Error reading PDF info: {str(e)}")


def validate_template(
    pdf_path: str, required_fields: List[str], mode: str = "form"
) -> Dict[str, any]:
    """
    Validate PDF template has required fields.

    Args:
        pdf_path: Path to PDF template
        required_fields: List of field names that must exist
        mode: 'form' or 'text' processing mode

    Returns:
        Dictionary with validation results
    """
    result = {"valid": True, "missing_fields": [], "found_fields": [], "warnings": []}

    if mode == "form":
        found_fields = get_form_field_names(pdf_path)
    else:
        found_fields = detect_text_placeholders(pdf_path)

    result["found_fields"] = found_fields

    for field in required_fields:
        if field not in found_fields:
            result["valid"] = False
            result["missing_fields"].append(field)

    if not found_fields:
        result["warnings"].append(f"No fields found in PDF template (mode: {mode})")

    return result
