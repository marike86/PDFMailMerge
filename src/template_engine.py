"""
Template Engine Module
Handles Jinja2 template parsing and rendering for PDF text replacement.
"""

import re
from typing import Dict, List
from jinja2 import Template, TemplateError, Environment, BaseLoader


class TemplateEngineError(Exception):
    """Custom exception for template engine errors"""

    pass


class StringLoader(BaseLoader):
    """Custom Jinja2 loader for string templates"""

    def __init__(self, template_string: str):
        self.template_string = template_string

    def get_source(self, environment, template):
        return self.template_string, None, lambda: True


def parse_template(template_content: str) -> Template:
    """
    Parse a Jinja2 template string.

    Args:
        template_content: Template string with Jinja2 syntax

    Returns:
        Compiled Jinja2 Template object

    Raises:
        TemplateEngineError: If template syntax is invalid
    """
    try:
        env = Environment(loader=StringLoader(template_content))
        template = env.get_template("template")
        return template
    except TemplateError as e:
        raise TemplateEngineError(f"Invalid template syntax: {str(e)}")


def render_template(template: Template, data: Dict[str, any]) -> str:
    """
    Render a Jinja2 template with provided data.

    Args:
        template: Compiled Jinja2 Template object
        data: Dictionary of variables to render

    Returns:
        Rendered string

    Raises:
        TemplateEngineError: If rendering fails
    """
    try:
        return template.render(**data)
    except Exception as e:
        raise TemplateEngineError(f"Error rendering template: {str(e)}")


def render_template_string(template_str: str, data: Dict[str, any]) -> str:
    """
    Render a template string directly with data.

    Args:
        template_str: Template string with {{field}} syntax
        data: Dictionary of variables to render

    Returns:
        Rendered string
    """
    try:
        template = Template(template_str)
        return template.render(**data)
    except Exception as e:
        raise TemplateEngineError(f"Error rendering template string: {str(e)}")


def detect_template_fields(text: str) -> List[str]:
    """
    Detect all {{field_name}} patterns in text.

    Args:
        text: Input text to scan

    Returns:
        List of unique field names found
    """
    pattern = r"\{\{(\w+)\}\}"
    matches = re.findall(pattern, text)
    return sorted(list(set(matches)))


def extract_template_fields(template_path: str) -> List[str]:
    """
    Extract field names from a template file.

    Args:
        template_path: Path to template file

    Returns:
        List of detected field names
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        return detect_template_fields(content)
    except Exception:
        return []


def validate_template_fields(
    fields: List[str], data_fields: List[str]
) -> Dict[str, any]:
    """
    Validate that template fields match data source fields.

    Args:
        fields: List of template field names
        data_fields: List of data source field names

    Returns:
        Dictionary with validation results
    """
    result = {
        "valid": True,
        "matched": [],
        "unmatched_template": [],
        "unmatched_data": [],
        "warnings": [],
    }

    for field in fields:
        if field in data_fields:
            result["matched"].append(field)
        else:
            result["valid"] = False
            result["unmatched_template"].append(field)

    for data_field in data_fields:
        if data_field not in fields:
            result["unmatched_data"].append(data_field)

    if result["unmatched_data"]:
        result["warnings"].append(
            f"Data fields not used in template: {', '.join(result['unmatched_data'])}"
        )

    return result


def create_field_mapping(
    template_fields: List[str], data_fields: List[str], auto_map: bool = True
) -> Dict[str, str]:
    """
    Create mapping between template fields and data fields.

    Args:
        template_fields: List of template field names
        data_fields: List of data source field names
        auto_map: Automatically map matching field names

    Returns:
        Dictionary mapping template fields to data fields
    """
    mapping = {}

    if auto_map:
        for template_field in template_fields:
            if template_field in data_fields:
                mapping[template_field] = template_field

    return mapping


def format_template_value(value: any, format_type: str = "text") -> str:
    """
    Format a value for template rendering.

    Args:
        value: Value to format
        format_type: Type of formatting ('text', 'number', 'date')

    Returns:
        Formatted string value
    """
    if value is None:
        return ""

    if format_type == "number":
        try:
            return f"{float(value):,.2f}"
        except Exception:
            return str(value)

    elif format_type == "date":
        try:
            from datetime import datetime

            if isinstance(value, str):
                dt = datetime.fromisoformat(value.replace("/", "-"))
                return dt.strftime("%Y-%m-%d")
            return str(value)
        except Exception:
            return str(value)

    else:
        return str(value)


def batch_render(template_str: str, data_list: List[Dict[str, any]]) -> List[str]:
    """
    Render template multiple times with different data.

    Args:
        template_str: Template string
        data_list: List of data dictionaries

    Returns:
        List of rendered strings
    """
    results = []

    for data in data_list:
        try:
            rendered = render_template_string(template_str, data)
            results.append(rendered)
        except Exception as e:
            results.append(f"Error: {str(e)}")

    return results
