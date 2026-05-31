import os
import sys
import csv
import json
import fitz
import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "test_data.csv"
    rows = [
        {"name": "张三", "email": "zhangsan@test.com", "company": "百度", "salary": "25000"},
        {"name": "李四", "email": "lisi@test.com", "company": "阿里", "salary": "30000"},
        {"name": "王五", "email": "wangwu@test.com", "company": "腾讯", "salary": "22000"},
    ]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email", "company", "salary"])
        writer.writeheader()
        writer.writerows(rows)
    return str(csv_file)


@pytest.fixture
def sample_csv_gbk(tmp_path):
    csv_file = tmp_path / "test_gbk.csv"
    rows = [
        {"name": "张三", "email": "zhangsan@test.com"},
        {"name": "李四", "email": "lisi@test.com"},
    ]
    with open(csv_file, "w", newline="", encoding="gbk") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        writer.writeheader()
        writer.writerows(rows)
    return str(csv_file)


@pytest.fixture
def sample_json(tmp_path):
    json_file = tmp_path / "test_data.json"
    data = [
        {"name": "张三", "email": "zhangsan@test.com", "company": "百度"},
        {"name": "李四", "email": "lisi@test.com", "company": "阿里"},
    ]
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return str(json_file)


@pytest.fixture
def sample_json_dict(tmp_path):
    json_file = tmp_path / "test_data_dict.json"
    data = {"data": [{"name": "张三", "email": "zhangsan@test.com"}]}
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return str(json_file)


@pytest.fixture
def sample_excel(tmp_path):
    xlsx_file = tmp_path / "test_data.xlsx"
    df = pd.DataFrame({
        "name": ["张三", "李四"],
        "email": ["zhangsan@test.com", "lisi@test.com"],
        "company": ["百度", "阿里"],
    })
    df.to_excel(str(xlsx_file), index=False, engine="openpyxl")
    return str(xlsx_file)


@pytest.fixture
def simple_pdf(tmp_path):
    pdf_path = tmp_path / "simple.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello World", fontsize=12)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


@pytest.fixture
def text_template_pdf(tmp_path):
    pdf_path = tmp_path / "template_text.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Name: {{name}}", fontsize=12)
    page.insert_text((72, 120), "Email: {{email}}", fontsize=12)
    page.insert_text((72, 168), "Company: {{company}}", fontsize=12)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


@pytest.fixture
def form_template_pdf(tmp_path):
    pdf_path = tmp_path / "template_form.pdf"
    doc = fitz.open()
    page = doc.new_page()
    widget = fitz.Widget()
    widget.field_name = "name"
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.rect = fitz.Rect(100, 60, 300, 80)
    page.add_widget(widget)
    widget2 = fitz.Widget()
    widget2.field_name = "email"
    widget2.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget2.rect = fitz.Rect(100, 100, 300, 120)
    page.add_widget(widget2)
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)


@pytest.fixture
def output_dir(tmp_path):
    out = tmp_path / "output"
    out.mkdir()
    return str(out)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name": ["张三", "李四", "王五"],
        "email": ["zhangsan@test.com", "lisi@test.com", "wangwu@test.com"],
        "company": ["百度", "阿里", "腾讯"],
    })
