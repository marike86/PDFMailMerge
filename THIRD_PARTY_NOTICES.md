# Third-party notices

The application source retains its original MIT license. Bundled libraries are not relicensed under MIT. License texts and package metadata are included in the portable archive under `licenses/`. Shared Qt DLLs are distributed separately in `_internal` and may be replaced with compatible builds. Application source, tests, build scripts, and dependency versions are included in `PDFMailMerge-source.zip`.

| Component | Version tested | License / upstream source |
| --- | --- | --- |
| Python | 3.14 | PSF; https://www.python.org/downloads/source/ |
| PySide6 Essentials / shiboken6 | 6.12.0 | LGPL-3.0 / GPL alternatives or commercial; https://code.qt.io/cgit/pyside/pyside-setup.git/tree/?h=v6.12.0 |
| Qt libraries | 6.12.0 | LGPL-3.0 / GPL alternatives or commercial; https://code.qt.io/cgit/qt/qtbase.git/tree/?h=v6.12.0 |
| PyMuPDF / MuPDF | 1.28.2 | AGPL-3.0 or Artifex commercial; https://github.com/pymupdf/PyMuPDF/tree/1.28.2 and https://github.com/ArtifexSoftware/mupdf/tree/1.28.2 |
| pypdf | 6.21.1 | BSD-3-Clause; https://github.com/py-pdf/pypdf |
| pandas | 3.0.6 | BSD-3-Clause; https://github.com/pandas-dev/pandas |
| NumPy | 2.5.4 | BSD-3-Clause and bundled component notices; https://github.com/numpy/numpy |
| Jinja2 / MarkupSafe | 3.1.6 / 3.0.4 | BSD-3-Clause; https://github.com/pallets/jinja and https://github.com/pallets/markupsafe |
| chardet | 7.7.0 | See bundled package metadata and license; https://github.com/chardet/chardet |
| openpyxl | 3.1.5 | MIT; https://foss.heptapod.net/openpyxl/openpyxl |
| xlrd | 2.0.2 | BSD; https://github.com/python-excel/xlrd |
| python-dateutil | 2.9.0.post0 | Apache-2.0 / BSD-3-Clause; https://github.com/dateutil/dateutil |
| six | 1.17.0 | MIT; https://github.com/benjaminp/six |
| tzdata | 2026.5 | Apache-2.0 and public domain IANA data; https://github.com/python/tzdata |
| et_xmlfile | 2.0.0 | MIT; https://foss.heptapod.net/openpyxl/et_xmlfile |

MuPDF's built-in Droid Sans Fallback is used for Chinese text and form appearances. Its font data is carried by the MuPDF distribution; upstream third-party notices apply. Existing template fonts remain subject to their original licenses.

Optional modules detected in the build environment (Pillow, psutil, PyYAML and packaging) may be carried by dependency hooks. Their license texts and metadata are included when installed. Their upstream sources are https://github.com/python-pillow/Pillow, https://github.com/giampaolo/psutil, https://github.com/yaml/pyyaml and https://github.com/pypa/packaging.

Build tooling: PyInstaller uses GPL-2.0-or-later with its bootloader exception. Build tooling and test dependencies are not required on the end user's machine.
