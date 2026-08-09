$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $RepoRoot ".venv"

if (-not (Test-Path $Venv)) {
    $PythonCommand = Get-Command python3.12, python3.11, python -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if (-not $PythonCommand) {
        throw "Python 3.11 or newer is required but was not found."
    }
    & $PythonCommand.Source -c "import sys; raise SystemExit(sys.version_info < (3, 11))"
    & $PythonCommand.Source -m venv $Venv
}

$Python = Join-Path $Venv "Scripts/python.exe"
& $Python -m pip install --upgrade pip
& $Python -m pip install -e "$RepoRoot[dev]"

Write-Host "Environment ready. Activate with: .\.venv\Scripts\Activate.ps1"
