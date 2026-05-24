# PDF Mail Merge Tool

A powerful and easy-to-use PDF mail merge tool that allows you to batch generate personalized PDFs from templates and data sources.

## Features

- **Multiple Data Source Support**: CSV, Excel, JSON formats
- **Dual Mode Processing**:
  - Form PDF mode: Fill PDF form fields
  - Text replacement mode: Replace `{{field_name}}` placeholders
- **Batch Processing**: Generate hundreds of PDFs efficiently
- **Cross-Platform**: Works on Windows, macOS, Linux
- **MIT Licensed**: Open source and free to use

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### CLI Usage

```bash
# Form PDF mode
python src/cli.py --template template.pdf --data data.csv --output ./output --mode form

# Text replacement mode
python src/cli.py --template template.pdf --data data.csv --output ./output --mode text

# Specify field mapping
python src/cli.py --template template.pdf --data data.csv --output ./output --mapping name=姓名,age=年龄
```

### Python API

```python
from src.pdf_processor import fill_form_pdf, replace_text
from src.data_loader import load_csv

# Load data
data = load_csv("data.csv")

# Fill form PDF
for row in data:
    fill_form_pdf("template.pdf", row, f"output_{row['id']}.pdf")

# Replace text in non-form PDF
replace_text("template.pdf", {"name": "张三", "age": "25"}, "output.pdf")
```

## Project Structure

```
pdf-mail-merge/
├── src/                    # Source code
│   ├── pdf_processor.py    # PDF processing core
│   ├── data_loader.py      # Data loading module
│   ├── template_engine.py  # Template engine
│   ├── cli.py              # Command-line interface
│   └── utils.py            # Utility functions
├── tests/                  # Test cases
├── examples/               # Example files
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
└── README.md
```

## Requirements

- Python 3.8+
- pypdf >= 3.0.0
- pandas >= 1.5.0
- Jinja2 >= 3.0.0

## License

MIT License - See [LICENSE](docs/LICENSE) for details.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## Support

If you encounter any issues, please open an issue on GitHub.