param([string]$OutputDirectory = "$PSScriptRoot\dist")
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    python scripts/create_examples.py
    if ($LASTEXITCODE -ne 0) { throw 'Example generation failed' }
    python -m PyInstaller --noconfirm PDFMailMerge.spec
    if ($LASTEXITCODE -ne 0) { throw 'Portable build failed' }
    python scripts/package_portable.py --output $OutputDirectory
    if ($LASTEXITCODE -ne 0) { throw 'Portable packaging failed' }
} finally {
    Pop-Location
}
