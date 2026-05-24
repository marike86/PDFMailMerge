# Test PDF Processor Module

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_processor import (
    read_form_fields,
    get_form_field_names,
    detect_text_placeholders,
    get_pdf_info,
    validate_template
)


def test_pdf_info():
    """Test PDF information reading"""
    print("\n=== Testing PDF Info ===")
    
    pdf_files = [
        'examples/template_form.pdf',
        'examples/template_text.pdf'
    ]
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            try:
                info = get_pdf_info(pdf_file)
                print(f"✓ {pdf_file}:")
                print(f"  Pages: {info['num_pages']}")
                print(f"  Size: {info['file_size']} bytes")
                print(f"  Form fields: {info['form_fields']}")
            except Exception as e:
                print(f"✗ {pdf_file}: {e}")
        else:
            print(f"⚠ {pdf_file}: File not found (create template to test)")


def test_form_fields():
    """Test form field detection"""
    print("\n=== Testing Form Field Detection ===")
    
    pdf_file = 'examples/template_form.pdf'
    
    if os.path.exists(pdf_file):
        try:
            fields = get_form_field_names(pdf_file)
            print(f"✓ Form fields found: {', '.join(fields) if fields else 'None'}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print(f"⚠ File not found: {pdf_file}")
        print("  Create a PDF form template to test form field functionality")


def test_text_placeholders():
    """Test text placeholder detection"""
    print("\n=== Testing Text Placeholder Detection ===")
    
    pdf_file = 'examples/template_text.pdf'
    
    if os.path.exists(pdf_file):
        try:
            placeholders = detect_text_placeholders(pdf_file)
            print(f"✓ Placeholders found: {', '.join(placeholders) if placeholders else 'None'}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print(f"⚠ File not found: {pdf_file}")
        print("  Create a PDF with {{placeholder}} text to test text replacement")


def test_validation():
    """Test template validation"""
    print("\n=== Testing Template Validation ===")
    
    required_fields = ['name', 'email', 'company']
    
    for pdf_file in ['examples/template_form.pdf', 'examples/template_text.pdf']:
        if os.path.exists(pdf_file):
            try:
                result = validate_template(pdf_file, required_fields, mode='form')
                print(f"✓ {pdf_file}:")
                print(f"  Valid: {result['valid']}")
                print(f"  Found fields: {result['found_fields']}")
                print(f"  Missing fields: {result['missing_fields']}")
            except Exception as e:
                print(f"✗ {pdf_file}: {e}")


if __name__ == '__main__':
    print("Running PDF Processor Tests")
    print("=" * 50)
    
    test_pdf_info()
    test_form_fields()
    test_text_placeholders()
    test_validation()
    
    print("\n" + "=" * 50)
    print("Note: Some tests may show 'File not found' if template PDFs")
    print("are not yet created. Create template PDFs in the examples/")
    print("directory to complete testing.")