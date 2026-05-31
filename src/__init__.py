"""
PDF Mail Merge Tool
A powerful tool for batch generating personalized PDFs from templates and data sources.
"""

__version__ = "1.0.0"
__author__ = "PDF Mail Merge Team"

from .data_loader import load_csv, load_excel, load_json, detect_encoding
from .pdf_processor import fill_form_pdf, replace_text, read_form_fields
from .template_engine import parse_template, render_template

__all__ = [
    "load_csv",
    "load_excel",
    "load_json",
    "detect_encoding",
    "fill_form_pdf",
    "replace_text",
    "read_form_fields",
    "parse_template",
    "render_template",
]
