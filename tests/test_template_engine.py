import os
import pytest
from jinja2 import Template
from src.template_engine import (
    parse_template,
    render_template,
    render_template_string,
    detect_template_fields,
    extract_template_fields,
    validate_template_fields,
    create_field_mapping,
    format_template_value,
    batch_render,
    StringLoader,
    TemplateEngineError,
)


class TestParseTemplate:

    def test_valid_template(self):
        tpl = parse_template("Hello {{name}}")
        assert isinstance(tpl, Template)

    def test_complex_template(self):
        tpl = parse_template("{{a}} and {{b}} and {{c}}")
        result = render_template(tpl, {"a": "1", "b": "2", "c": "3"})
        assert "1" in result and "2" in result and "3" in result

    def test_invalid_syntax(self):
        with pytest.raises(TemplateEngineError, match="Invalid template syntax"):
            parse_template("{{unclosed")

    def test_empty_template(self):
        tpl = parse_template("")
        result = render_template(tpl, {})
        assert result == ""

    def test_template_without_placeholders(self):
        tpl = parse_template("Just plain text")
        result = render_template(tpl, {})
        assert result == "Just plain text"


class TestRenderTemplate:

    def test_basic_render(self):
        tpl = parse_template("Hello {{name}}!")
        result = render_template(tpl, {"name": "张三"})
        assert result == "Hello 张三!"

    def test_missing_variable(self):
        tpl = parse_template("Hello {{name}}!")
        result = render_template(tpl, {})
        assert result == "Hello !"

    def test_extra_data_ignored(self):
        tpl = parse_template("Hello {{name}}!")
        result = render_template(tpl, {"name": "test", "extra": "ignored"})
        assert result == "Hello test!"

    def test_numeric_value(self):
        tpl = parse_template("Count: {{count}}")
        result = render_template(tpl, {"count": 42})
        assert result == "Count: 42"

    def test_none_value(self):
        tpl = parse_template("Value: {{val}}")
        result = render_template(tpl, {"val": None})
        assert result == "Value: None"


class TestRenderTemplateString:

    def test_basic_render(self):
        result = render_template_string("Hello {{name}}", {"name": "world"})
        assert result == "Hello world"

    def test_multiple_vars(self):
        result = render_template_string(
            "{{a}}-{{b}}-{{c}}", {"a": "1", "b": "2", "c": "3"}
        )
        assert result == "1-2-3"

    def test_no_vars(self):
        result = render_template_string("plain text", {})
        assert result == "plain text"

    def test_invalid_template(self):
        with pytest.raises(TemplateEngineError):
            render_template_string("{{unclosed", {})

    def test_chinese_characters(self):
        result = render_template_string("你好 {{name}}！", {"name": "世界"})
        assert result == "你好 世界！"


class TestDetectTemplateFields:

    def test_basic_detection(self):
        fields = detect_template_fields("Hello {{name}} and {{email}}")
        assert sorted(fields) == ["email", "name"]

    def test_no_fields(self):
        fields = detect_template_fields("No placeholders here")
        assert fields == []

    def test_duplicates_removed(self):
        fields = detect_template_fields("{{x}} and {{x}} and {{x}}")
        assert fields == ["x"]

    def test_sorted_output(self):
        fields = detect_template_fields("{{z}} {{a}} {{m}}")
        assert fields == ["a", "m", "z"]

    def test_underscore_in_name(self):
        fields = detect_template_fields("{{first_name}} {{last_name}}")
        assert sorted(fields) == ["first_name", "last_name"]

    def test_mixed_content(self):
        fields = detect_template_fields("Order #{{order_id}} for {{customer_name}}")
        assert sorted(fields) == ["customer_name", "order_id"]

    def test_empty_string(self):
        fields = detect_template_fields("")
        assert fields == []

    def test_adjacent_placeholders(self):
        fields = detect_template_fields("{{a}}{{b}}")
        assert sorted(fields) == ["a", "b"]


class TestExtractTemplateFields:

    def test_from_file(self, tmp_path):
        f = tmp_path / "tpl.txt"
        f.write_text("Hello {{name}}, welcome to {{company}}!")
        fields = extract_template_fields(str(f))
        assert sorted(fields) == ["company", "name"]

    def test_nonexistent_file(self):
        fields = extract_template_fields("nonexistent.txt")
        assert fields == []

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        fields = extract_template_fields(str(f))
        assert fields == []


class TestValidateTemplateFields:

    def test_all_matched(self):
        result = validate_template_fields(["a", "b"], ["a", "b"])
        assert result["valid"] is True
        assert sorted(result["matched"]) == ["a", "b"]
        assert result["unmatched_template"] == []
        assert result["unmatched_data"] == []

    def test_unmatched_template_fields(self):
        result = validate_template_fields(["a", "b", "c"], ["a", "b"])
        assert result["valid"] is False
        assert result["unmatched_template"] == ["c"]

    def test_unmatched_data_fields(self):
        result = validate_template_fields(["a"], ["a", "x", "y"])
        assert result["valid"] is True
        assert sorted(result["unmatched_data"]) == ["x", "y"]
        assert len(result["warnings"]) == 1

    def test_no_fields(self):
        result = validate_template_fields([], [])
        assert result["valid"] is True
        assert result["matched"] == []

    def test_no_template_fields(self):
        result = validate_template_fields([], ["a", "b"])
        assert result["valid"] is True
        assert result["unmatched_data"] == ["a", "b"]

    def test_no_data_fields(self):
        result = validate_template_fields(["a", "b"], [])
        assert result["valid"] is False
        assert result["unmatched_template"] == ["a", "b"]


class TestCreateFieldMapping:

    def test_exact_match(self):
        mapping = create_field_mapping(["a", "b"], ["a", "b"])
        assert mapping == {"a": "a", "b": "b"}

    def test_partial_match(self):
        mapping = create_field_mapping(["a", "b", "c"], ["a", "c"])
        assert mapping == {"a": "a", "c": "c"}
        assert "b" not in mapping

    def test_no_match(self):
        mapping = create_field_mapping(["x", "y"], ["a", "b"])
        assert mapping == {}

    def test_auto_map_false(self):
        mapping = create_field_mapping(["a", "b"], ["a", "b"], auto_map=False)
        assert mapping == {}

    def test_empty_lists(self):
        mapping = create_field_mapping([], [])
        assert mapping == {}


class TestFormatTemplateValue:

    def test_text_value(self):
        assert format_template_value("hello", "text") == "hello"

    def test_number_value(self):
        assert format_template_value(1234.567, "number") == "1,234.57"

    def test_number_integer(self):
        assert format_template_value(1000, "number") == "1,000.00"

    def test_number_invalid(self):
        result = format_template_value("not_a_number", "number")
        assert result == "not_a_number"

    def test_date_value(self):
        result = format_template_value("2024-03-01", "date")
        assert result == "2024-03-01"

    def test_date_with_slash(self):
        result = format_template_value("2024/03/01", "date")
        assert result == "2024-03-01"

    def test_date_invalid(self):
        result = format_template_value("not-a-date", "date")
        assert result == "not-a-date"

    def test_none_value(self):
        assert format_template_value(None, "text") == ""
        assert format_template_value(None, "number") == ""
        assert format_template_value(None, "date") == ""

    def test_integer_as_text(self):
        assert format_template_value(42, "text") == "42"

    def test_unknown_format(self):
        assert format_template_value("test", "unknown") == "test"


class TestBatchRender:

    def test_basic_batch(self):
        results = batch_render(
            "Hello {{name}}",
            [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        )
        assert results == ["Hello A", "Hello B", "Hello C"]

    def test_empty_list(self):
        results = batch_render("Hello {{name}}", [])
        assert results == []

    def test_partial_error(self):
        results = batch_render(
            "Hello {{name}}",
            [{"name": "ok"}, {"bad": "missing_name"}, {"name": "fine"}],
        )
        assert results[0] == "Hello ok"
        assert results[1] == "Hello "
        assert results[2] == "Hello fine"

    def test_all_errors(self):
        results = batch_render("{{x}}", [{}, {}])
        assert len(results) == 2
        assert results[0] == ""
        assert results[1] == ""

    def test_chinese_data(self):
        results = batch_render(
            "员工: {{name}}", [{"name": "张三"}, {"name": "李四"}]
        )
        assert results == ["员工: 张三", "员工: 李四"]


class TestStringLoader:

    def test_loader_returns_source(self):
        loader = StringLoader("test content")
        source, filename, uptodate = loader.get_source(None, "template")
        assert source == "test content"
        assert filename is None
        assert uptodate() is True
