# Test Template Engine Module

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from template_engine import (
    parse_template,
    render_template,
    render_template_string,
    detect_template_fields,
    validate_template_fields,
    create_field_mapping,
    format_template_value
)


def test_detect_fields():
    """Test placeholder detection"""
    print("\n=== Testing Field Detection ===")
    
    test_cases = [
        "Hello, {{name}}! Your email is {{email}}.",
        "Order #{{order_id}} for {{customer}}",
        "No placeholders here",
        "{{field1}} and {{field2}} and {{field3}}"
    ]
    
    for text in test_cases:
        fields = detect_template_fields(text)
        print(f"✓ Text: {text[:50]}...")
        print(f"  Fields: {fields}")


def test_render_template():
    """Test template rendering"""
    print("\n=== Testing Template Rendering ===")
    
    template_str = "Hello, {{name}}! Welcome to {{company}}."
    data = {
        'name': '张三',
        'company': '百度'
    }
    
    try:
        result = render_template_string(template_str, data)
        print(f"✓ Template: {template_str}")
        print(f"✓ Data: {data}")
        print(f"✓ Result: {result}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_complex_template():
    """Test complex template with filters"""
    print("\n=== Testing Complex Template ===")
    
    template_str = """
    员工信息卡
    姓名: {{name}}
    职位: {{position}}
    薪资: {{salary}}
    入职日期: {{start_date}}
    """
    
    data = {
        'name': '李四',
        'position': '产品经理',
        'salary': 30000,
        'start_date': '2024-01-15'
    }
    
    try:
        result = render_template_string(template_str, data)
        print(f"✓ Rendered successfully")
        print(f"  Preview: {result[:100]}...")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_field_validation():
    """Test field validation"""
    print("\n=== Testing Field Validation ===")
    
    template_fields = ['name', 'email', 'company']
    data_fields = ['name', 'email', 'company', 'extra_field']
    
    result = validate_template_fields(template_fields, data_fields)
    
    print(f"✓ Template fields: {template_fields}")
    print(f"✓ Data fields: {data_fields}")
    print(f"  Valid: {result['valid']}")
    print(f"  Matched: {result['matched']}")
    print(f"  Unmatched template: {result['unmatched_template']}")
    print(f"  Unmatched data: {result['unmatched_data']}")
    print(f"  Warnings: {result['warnings']}")


def test_field_mapping():
    """Test field mapping creation"""
    print("\n=== Testing Field Mapping ===")
    
    template_fields = ['name', 'email', 'address']
    data_fields = ['full_name', 'email', 'home_address']
    
    mapping = create_field_mapping(template_fields, data_fields, auto_map=True)
    
    print(f"✓ Template fields: {template_fields}")
    print(f"✓ Data fields: {data_fields}")
    print(f"✓ Auto-mapped: {mapping}")


def test_value_formatting():
    """Test value formatting"""
    print("\n=== Testing Value Formatting ===")
    
    test_values = [
        (1000, 'number'),
        (1234.567, 'number'),
        ('2024-03-01', 'date'),
        ('Hello World', 'text'),
        (None, 'text')
    ]
    
    for value, format_type in test_values:
        formatted = format_template_value(value, format_type)
        print(f"✓ {value} ({format_type}) -> {formatted}")


if __name__ == '__main__':
    print("Running Template Engine Tests")
    print("=" * 50)
    
    test_detect_fields()
    test_render_template()
    test_complex_template()
    test_field_validation()
    test_field_mapping()
    test_value_formatting()
    
    print("\n" + "=" * 50)
    print("All template engine tests completed!")