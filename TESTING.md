# Verification

Validated on Windows x64 with Python 3.14, using the versions in `requirements-lock.txt`.

- `python -m pytest -q`: **297 passed**.
- `python -m ruff check src main.py scripts tests/test_gui.py tests/test_regressions.py --select F`: passed.
- Source desktop offline self-test: imports the bundled template and CSV, previews record 1, generates 3 PDFs and ZIP, writes screenshots and JSON.
- Form verification checks canonical `/AcroForm/Fields` values, page widget values, appearance streams and rendered/extracted Chinese text, including multiple pages and checkboxes.
- PDF appearance was visually inspected using Poppler-rendered PNGs and the application's preview.
- The portable smoke test clears Python paths and uses only the Windows system PATH. Build dependency discovery also excludes unrelated application PATH entries, preventing ICU DLL conflicts from other installed tools.

## Run tests

```powershell
python -m pip install -r requirements-lock.txt
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Desktop tests use Qt's offscreen platform and perform the real import, mapping, preview and batch workflows. They do not send email, require network access, or use personal data. Sample email addresses use `example.com`.

## Test a portable build

```powershell
./build.ps1
./dist/PDFMailMerge/PDFMailMerge-CLI.exe --self-test ./dist/smoke-test
```

The self-test exits with 0 on success, writes `self-test.json`, three desktop screenshots, generated PDFs and a ZIP. The GitHub workflow runs this check against the frozen executable after building.

## Limits of this verification

The desktop was rendered and exercised automatically in the available Windows environment. A separate clean Windows VM, every possible PDF producer, complex-script typography, rotated text replacement, OCR and digital-signature workflows have not been certified. The UI uses Qt with Fluent styling. It is not a native WinUI 3 implementation.
