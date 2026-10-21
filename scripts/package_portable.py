"""Stage examples, source, dependency notices, and a portable ZIP."""
import argparse
import importlib.metadata as metadata
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ("pypdf", "pymupdf", "PySide6-Essentials", "shiboken6", "pandas", "numpy",
           "Jinja2", "MarkupSafe", "chardet", "openpyxl", "xlrd", "python-dateutil", "six", "tzdata", "et_xmlfile",
           "pillow", "psutil", "pyyaml", "packaging")


def source_files():
    roots = [ROOT / name for name in ("src", "tests", "scripts", "assets", "examples", "docs", ".github")]
    for item in ROOT.iterdir():
        if item.is_file() and item.suffix.lower() in (".py", ".txt", ".spec", ".ps1", ".bat", ".md") and item.name != "build_log.txt":
            yield item
    yield ROOT / "LICENSE"
    yield ROOT / ".gitignore"
    for folder in roots:
        for item in folder.rglob("*"):
            if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc":
                yield item


def package(output):
    bundle = ROOT / "dist" / "PDFMailMerge"
    if not (bundle / "PDFMailMerge.exe").is_file():
        raise RuntimeError("Build PDFMailMerge.spec first")
    shutil.copytree(ROOT / "examples", bundle / "examples", dirs_exist_ok=True)
    for name in ("README.md", "LICENSE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(ROOT / name, bundle / name)
    licenses = bundle / "licenses"
    licenses.mkdir(exist_ok=True)
    for package_name in RUNTIME:
        try:
            distribution = metadata.distribution(package_name)
        except metadata.PackageNotFoundError:
            continue  # Optional packages are only shipped when present at build time.
        target = licenses / package_name
        target.mkdir(exist_ok=True)
        (target / "METADATA.txt").write_text(distribution.read_text("METADATA") or "", encoding="utf-8")
        for item in distribution.files or []:
            if any("license" in part.lower() or "copying" in part.lower() for part in item.parts):
                source = Path(distribution.locate_file(item))
                if source.is_file():
                    relative = Path(*item.parts[1:])
                    destination = target / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
    shutil.copytree(ROOT / "licenses", licenses / "upstream", dirs_exist_ok=True)
    python_license = Path(sys.base_prefix) / "LICENSE.txt"
    if python_license.exists():
        shutil.copy2(python_license, licenses / "Python-LICENSE.txt")
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    source_archive = output / "PDFMailMerge-2.0.0-source.zip"
    with zipfile.ZipFile(source_archive, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in source_files():
            archive.write(item, str(Path("PDFMailMerge-source") / item.relative_to(ROOT)))
        for item in (ROOT / "licenses").rglob("*"):
            if item.is_file():
                archive.write(item, str(Path("PDFMailMerge-source") / item.relative_to(ROOT)))
    shutil.copy2(source_archive, bundle / "PDFMailMerge-source.zip")
    portable = output / "PDFMailMerge-2.0.0-windows-x64-portable.zip"
    with zipfile.ZipFile(portable, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in bundle.rglob("*"):
            if item.is_file():
                archive.write(item, str(Path("PDFMailMerge") / item.relative_to(bundle)))
    print(portable)
    print(source_archive)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=ROOT / "dist")
    package(parser.parse_args().output)
