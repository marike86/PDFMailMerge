# -*- mode: python ; coding: utf-8 -*-
# Unpack-and-run distribution: shared Qt DLLs remain replaceable.
a = Analysis(
    ['main.py'],
    pathex=[SPECPATH],
    binaries=[],
    datas=[('assets/app.ico', 'assets')],
    hiddenimports=['xlrd', 'openpyxl'],
    hookspath=[], hooksconfig={}, runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'IPython', 'notebook', 'pytest',
              'ruff', 'onnxruntime', 'networkx', 'pymupdf4llm', 'pymupdf_layout'],
    noarchive=False, optimize=0,
)
pyz = PYZ(a.pure)
common = dict(exclude_binaries=True, debug=False, strip=False, upx=False,
              icon='assets/app.ico', version='assets/version.txt')
gui = EXE(pyz, a.scripts, [], name='PDFMailMerge', console=False, **common)
cli = EXE(pyz, a.scripts, [], name='PDFMailMerge-CLI', console=True, **common)
coll = COLLECT(gui, cli, a.binaries, a.datas, strip=False, upx=False, name='PDFMailMerge')
