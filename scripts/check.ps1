$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $RepoRoot ".venv/Scripts/python.exe"

if (-not (Test-Path $Python)) {
    throw "Run scripts/bootstrap.ps1 before checks."
}

Push-Location $RepoRoot
try {
    & $Python -m ruff check .
    & $Python -m mypy
    & $Python -m pytest
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        Push-Location "apps/web"
        try {
            npm install
            npm run build
        } finally {
            Pop-Location
        }
    }
} finally {
    Pop-Location
}
