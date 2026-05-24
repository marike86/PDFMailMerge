# Test Data Loader Module

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import load_csv, load_excel, load_json, detect_encoding, validate_data, data_to_dict_list
import pandas as pd


def test_load_csv():
    """Test CSV loading functionality"""
    print("\n=== Testing CSV Loader ===")
    
    try:
        data = load_csv('examples/sample_data.csv')
        print(f"✓ Loaded {len(data)} rows")
        print(f"✓ Columns: {', '.join(data.columns)}")
        print(f"✓ First row: {data.iloc[0].to_dict()}")
        
        validation = validate_data(data, required_fields=['name', 'email'])
        print(f"✓ Validation: {'Passed' if validation['valid'] else 'Failed'}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_detect_encoding():
    """Test encoding detection"""
    print("\n=== Testing Encoding Detection ===")
    
    try:
        encodings = []
        
        csv_files = [
            'examples/sample_data.csv',
        ]
        
        for file in csv_files:
            if os.path.exists(file):
                enc = detect_encoding(file)
                encodings.append(f"{file}: {enc}")
                print(f"✓ {file} -> {enc}")
        
        return len(encodings) > 0
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_data_conversion():
    """Test data conversion functions"""
    print("\n=== Testing Data Conversion ===")
    
    try:
        df = load_csv('examples/sample_data.csv')
        records = data_to_dict_list(df)
        
        print(f"✓ Converted {len(records)} records to dict list")
        print(f"✓ Sample record: {records[0]}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == '__main__':
    print("Running Data Loader Tests")
    print("=" * 50)
    
    results = []
    results.append(("CSV Loading", test_load_csv()))
    results.append(("Encoding Detection", test_detect_encoding()))
    results.append(("Data Conversion", test_data_conversion()))
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
    
    sys.exit(0 if all_passed else 1)