# Examples Directory

This directory contains example files for testing the PDF Mail Merge Tool.

## Files

- `sample_data.csv` - Sample data source with employee information
- `template_form.pdf` - PDF form template with fillable fields (create your own)
- `template_text.pdf` - Text-based template with `{{field}}` placeholders

## Creating PDF Templates

### Form PDF Template

1. Create a PDF with form fields using tools like Adobe Acrobat
2. Name the form fields to match your data columns (e.g., "name", "email")
3. Save as template_form.pdf

Example form field names:
- name
- email
- company
- position
- salary
- start_date

### Text-Based PDF Template

1. Create a PDF document with text placeholders
2. Use `{{field_name}}` syntax for replaceable fields

Example content:
```
姓名: {{name}}
邮箱: {{email}}
公司: {{company}}
职位: {{position}}
薪资: {{salary}}
入职日期: {{start_date}}
```

## Testing

Run the tool with sample data:

```bash
# Test with form mode
python -m src.cli --template examples/template_form.pdf --data examples/sample_data.csv --output ./test_output --mode form

# Test with text mode
python -m src.cli --template examples/template_text.pdf --data examples/sample_data.csv --output ./test_output --mode text

# Validate only (no PDF generation)
python -m src.cli --template examples/template_form.pdf --data examples/sample_data.csv --validate-only
```