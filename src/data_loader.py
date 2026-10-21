"""
Data Loader Module
Handles loading data from CSV, Excel, and JSON files with automatic encoding detection.
"""

import os
import json
import chardet
import pandas as pd
from typing import Union, Dict, List, Optional


class DataLoadError(Exception):
    """Custom exception for data loading errors"""

    pass


def detect_encoding(file_path: str) -> str:
    """
    Detect file encoding automatically.

    Args:
        file_path: Path to the file

    Returns:
        Detected encoding string (e.g., 'utf-8', 'gbk')

    Raises:
        DataLoadError: If file cannot be read
    """
    if not os.path.exists(file_path):
        raise DataLoadError(f"File not found: {file_path}")

    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
            confidence = result["confidence"]

            if confidence < 0.7:
                return "utf-8"

            if encoding:
                encoding = encoding.lower()
                if "gb18030" in encoding:
                    return "gb18030"
                elif "gb" in encoding or "gbk" in encoding:
                    return "gbk"
                elif "utf-8" in encoding or "utf8" in encoding:
                    return "utf-8"
                elif encoding in ("utf-16", "utf-32", "ascii"):
                    return encoding

            return "utf-8"

    except Exception as e:
        raise DataLoadError(f"Error detecting encoding: {str(e)}")


def load_csv(file_path: str, encoding: Optional[str] = None, **kwargs) -> pd.DataFrame:
    """
    Load CSV file with automatic encoding detection.

    Args:
        file_path: Path to CSV file
        encoding: Force specific encoding (optional)
        **kwargs: Additional arguments for pandas.read_csv

    Returns:
        pandas DataFrame with loaded data

    Raises:
        DataLoadError: If CSV cannot be loaded
    """
    if not os.path.exists(file_path):
        raise DataLoadError(f"CSV file not found: {file_path}")

    if encoding is None:
        encoding = detect_encoding(file_path)

    kwargs.setdefault("dtype", str)
    kwargs.setdefault("keep_default_na", False)
    try:
        df = pd.read_csv(file_path, encoding=encoding, **kwargs)
        return df
    except UnicodeDecodeError:
        encodings = ["utf-8-sig", "gb18030", "utf-16"]
        for enc in encodings:
            try:
                df = pd.read_csv(file_path, encoding=enc, **kwargs)
                return df
            except (UnicodeError, pd.errors.ParserError):
                continue
        raise DataLoadError("Failed to load CSV with supported encodings")
    except Exception as e:
        raise DataLoadError(f"Error loading CSV: {str(e)}")


def load_excel(
    file_path: str, sheet_name: Union[str, int] = 0, **kwargs
) -> pd.DataFrame:
    """
    Load Excel file (.xlsx, .xls).

    Args:
        file_path: Path to Excel file
        sheet_name: Sheet name or index (default: 0)
        **kwargs: Additional arguments for pandas.read_excel

    Returns:
        pandas DataFrame with loaded data

    Raises:
        DataLoadError: If Excel cannot be loaded
    """
    if not os.path.exists(file_path):
        raise DataLoadError(f"Excel file not found: {file_path}")

    try:
        kwargs.setdefault("dtype", str)
        kwargs.setdefault("keep_default_na", False)
        engine = kwargs.pop("engine", "xlrd" if str(file_path).lower().endswith(".xls") else "openpyxl")
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine=engine, **kwargs)
        return df
    except Exception as e:
        raise DataLoadError(f"Error loading Excel: {str(e)}")


def load_json(file_path: str, encoding: Optional[str] = None, **kwargs) -> pd.DataFrame:
    """
    Load JSON file and convert to DataFrame.

    Args:
        file_path: Path to JSON file
        encoding: File encoding (default: auto-detect)
        **kwargs: Additional arguments for json.load

    Returns:
        pandas DataFrame with loaded data

    Raises:
        DataLoadError: If JSON cannot be loaded
    """
    if not os.path.exists(file_path):
        raise DataLoadError(f"JSON file not found: {file_path}")

    if encoding is None:
        encoding = detect_encoding(file_path)

    try:
        with open(file_path, "r", encoding=encoding) as f:
            data = json.load(f, **kwargs)

        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            if "data" in data:
                df = pd.DataFrame(data["data"])
            else:
                df = pd.DataFrame([data])
        else:
            raise DataLoadError(f"Unsupported JSON structure: {type(data)}")

        return df

    except json.JSONDecodeError as e:
        raise DataLoadError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise DataLoadError(f"Error loading JSON: {str(e)}")


def load_data(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Auto-detect file type and load data.

    Args:
        file_path: Path to data file
        **kwargs: Additional arguments for loading

    Returns:
        pandas DataFrame with loaded data

    Raises:
        DataLoadError: If file type not supported or loading fails
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        return load_csv(file_path, **kwargs)
    elif ext in [".xlsx", ".xls"]:
        return load_excel(file_path, **kwargs)
    elif ext == ".json":
        return load_json(file_path, **kwargs)
    else:
        raise DataLoadError(f"Unsupported file type: {ext}")


def validate_data(
    df: pd.DataFrame, required_fields: Optional[List[str]] = None
) -> Dict[str, any]:
    """
    Validate data and return statistics.

    Args:
        df: DataFrame to validate
        required_fields: List of required field names

    Returns:
        Dictionary with validation results and statistics
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "statistics": {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
        },
    }

    if required_fields:
        missing = [field for field in required_fields if field not in df.columns]
        if missing:
            result["valid"] = False
            result["errors"].append(f"Missing required fields: {', '.join(missing)}")

    empty_rows = df.isnull().all(axis=1).sum()
    if empty_rows > 0:
        result["warnings"].append(f"Found {empty_rows} empty rows")

    return result


def data_to_dict_list(df: pd.DataFrame) -> List[Dict]:
    """
    Convert DataFrame to list of dictionaries.

    Args:
        df: Input DataFrame

    Returns:
        List of dictionaries, one per row
    """
    return df.astype(object).where(pd.notna(df), "").to_dict(orient="records")


def get_field_names(df: pd.DataFrame) -> List[str]:
    """
    Get all field names from DataFrame.

    Args:
        df: Input DataFrame

    Returns:
        List of column names
    """
    return list(df.columns)
