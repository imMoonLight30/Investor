import sys
from pathlib import Path

# Ensure the src layout package is importable without installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
