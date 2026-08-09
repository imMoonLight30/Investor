#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_python() -> str:
    candidates = (sys.executable, "python3.13", "python3.12", "python3.11")
    for candidate in candidates:
        executable = shutil.which(candidate)
        if executable is None:
            continue
        version = subprocess.run(
            [executable, "-c", "import sys; print(sys.version_info >= (3, 11))"],
            check=True,
            capture_output=True,
            text=True,
        )
        if version.stdout.strip() == "True":
            return executable
    raise RuntimeError("Python 3.11 or newer is required but was not found.")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    virtual_environment = root / ".venv"
    if not virtual_environment.exists():
        subprocess.run([find_python(), "-m", "venv", str(virtual_environment)], check=True)

    python = virtual_environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(
        [str(python), "-m", "pip", "install", "--upgrade", "pip"],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [str(python), "-m", "pip", "install", "-e", ".[dev]"],
        cwd=root,
        check=True,
    )
    print(f"Environment ready. Python: {python}")


if __name__ == "__main__":
    main()
