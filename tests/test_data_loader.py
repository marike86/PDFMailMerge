import os
import json
import pytest
import pandas as pd
from src.data_loader import (
    detect_encoding,
    load_csv,
    load_excel,
    load_json,
    load_data,
    validate_data,
    data_to_dict_list,
    get_field_names,
    DataLoadError,
)


class TestDetectEncoding:

    def test_utf8_file(self, sample_csv):
        enc = detect_encoding(sample_csv)
        assert enc in ("utf-8", "ascii")

    def test_gbk_file(self, sample_csv_gbk):
        enc = detect_encoding(sample_csv_gbk)
        assert isinstance(enc, str)
        assert len(enc) > 0

    def test_nonexistent_file(self):
        with pytest.raises(DataLoadError, match="File not found"):
            detect_encoding("nonexistent.txt")

    def test_returns_string(self, sample_csv):
        enc = detect_encoding(sample_csv)
        assert isinstance(enc, str)


class TestLoadCsv:

    def test_basic_load(self, sample_csv):
        df = load_csv(sample_csv)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == ["name", "email", "company", "salary"]

    def test_load_with_encoding(self, sample_csv):
        df = load_csv(sample_csv, encoding="utf-8")
        assert len(df) == 3

    def test_load_gbk(self, sample_csv_gbk):
        df = load_csv(sample_csv_gbk)
        assert len(df) == 2
        assert "张三" in df["name"].values

    def test_file_not_found(self):
        with pytest.raises(DataLoadError, match="not found"):
            load_csv("nonexistent.csv")

    def test_invalid_csv_format(self, tmp_path):
        bad = tmp_path / "bad.csv"
        bad.write_text("a;b\n1;2\n3", encoding="utf-8")
        df = load_csv(str(bad), sep=",")
        assert len(df.columns) == 1

    def test_column_names(self, sample_csv):
        df = load_csv(sample_csv)
        assert "name" in df.columns
        assert "email" in df.columns


class TestLoadExcel:

    def test_basic_load(self, sample_excel):
        df = load_excel(sample_excel)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "name" in df.columns

    def test_file_not_found(self):
        with pytest.raises(DataLoadError, match="not found"):
            load_excel("nonexistent.xlsx")

    def test_invalid_file(self, tmp_path):
        bad = tmp_path / "bad.xlsx"
        bad.write_text("not excel")
        with pytest.raises(DataLoadError):
            load_excel(str(bad))


class TestLoadJson:

    def test_list_json(self, sample_json):
        df = load_json(sample_json)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "name" in df.columns

    def test_dict_with_data_key(self, sample_json_dict):
        df = load_json(sample_json_dict)
        assert len(df) == 1

    def test_dict_without_data_key(self, tmp_path):
        f = tmp_path / "single.json"
        with open(f, "w", encoding="utf-8") as fh:
            json.dump({"name": "test", "value": 42}, fh)
        df = load_json(str(f))
        assert len(df) == 1
        assert df["name"].iloc[0] == "test"

    def test_file_not_found(self):
        with pytest.raises(DataLoadError, match="not found"):
            load_json("nonexistent.json")

    def test_invalid_json(self, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("{invalid json content")
        with pytest.raises(DataLoadError, match="Invalid JSON"):
            load_json(str(f))

    def test_unsupported_structure(self, tmp_path):
        f = tmp_path / "string.json"
        f.write_text('"just a string"')
        with pytest.raises(DataLoadError, match="Unsupported JSON structure"):
            load_json(str(f))


class TestLoadData:

    def test_auto_detect_csv(self, sample_csv):
        df = load_data(sample_csv)
        assert len(df) == 3

    def test_auto_detect_excel(self, sample_excel):
        df = load_data(sample_excel)
        assert len(df) == 2

    def test_auto_detect_json(self, sample_json):
        df = load_data(sample_json)
        assert len(df) == 2

    def test_unsupported_extension(self, tmp_path):
        f = tmp_path / "data.xyz"
        f.write_text("content")
        with pytest.raises(DataLoadError, match="Unsupported file type"):
            load_data(str(f))

    def test_uppercase_extension(self, tmp_path):
        f = tmp_path / "data.CSV"
        with open(f, "w", newline="", encoding="utf-8") as fh:
            writer = __import__("csv").DictWriter(fh, fieldnames=["a"])
            writer.writeheader()
            writer.writerow({"a": "1"})
        df = load_data(str(f))
        assert len(df) == 1


class TestValidateData:

    def test_valid_data(self, sample_df):
        result = validate_data(sample_df)
        assert result["valid"] is True
        assert result["statistics"]["total_rows"] == 3
        assert result["statistics"]["total_columns"] == 3

    def test_missing_required_fields(self, sample_df):
        result = validate_data(sample_df, required_fields=["name", "nonexistent"])
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "nonexistent" in result["errors"][0]

    def test_all_fields_present(self, sample_df):
        result = validate_data(sample_df, required_fields=["name", "email"])
        assert result["valid"] is True
        assert result["errors"] == []

    def test_empty_rows_warning(self):
        df = pd.DataFrame({"a": [1, None], "b": [2, None]})
        result = validate_data(df)
        assert len(result["warnings"]) == 1
        assert "empty rows" in result["warnings"][0]

    def test_statistics_content(self, sample_df):
        result = validate_data(sample_df)
        stats = result["statistics"]
        assert "total_rows" in stats
        assert "total_columns" in stats
        assert "columns" in stats
        assert "missing_values" in stats
        assert "data_types" in stats


class TestDataToDictList:

    def test_conversion(self, sample_df):
        records = data_to_dict_list(sample_df)
        assert isinstance(records, list)
        assert len(records) == 3
        assert isinstance(records[0], dict)
        assert "name" in records[0]

    def test_first_record_values(self, sample_df):
        records = data_to_dict_list(sample_df)
        assert records[0]["name"] == "张三"
        assert records[0]["email"] == "zhangsan@test.com"

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["a", "b"])
        records = data_to_dict_list(df)
        assert records == []


class TestGetFieldNames:

    def test_field_names(self, sample_df):
        fields = get_field_names(sample_df)
        assert fields == ["name", "email", "company"]

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        fields = get_field_names(df)
        assert fields == []
