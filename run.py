#!/usr/bin/env python
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venve"
if os.name == "nt":
    VENV_PY = VENV_DIR / "Scripts" / "python.exe"
else:
    VENV_PY = VENV_DIR / "bin" / "python"

REQUIREMENTS = ROOT / "requirements.txt"


def run(cmd, **kwargs):
    print(f"[run.py] Running: {' '.join(map(str, cmd))}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        sys.exit(result.returncode)


def ensure_venv():
    if VENV_DIR.is_dir() and VENV_PY.is_file():
        print(f"[run.py] Using existing virtual environment at {VENV_DIR}")
        return False  # not newly created

    print(f"[run.py] Creating virtual environment at {VENV_DIR}")
    # Use the interpreter running this script to build the venv
    run([sys.executable, "-m", "venv", str(VENV_DIR)])
    if not VENV_PY.is_file():
        print("[run.py] Error: virtual environment python not found after creation.")
        sys.exit(1)
    return True  # newly created


def install_requirements():
    if not REQUIREMENTS.is_file():
        print(f"[run.py] No requirements.txt found at {REQUIREMENTS}, skipping install.")
        return
    print(f"[run.py] Installing dependencies from {REQUIREMENTS}")
    run([str(VENV_PY), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(VENV_PY), "-m", "pip", "install", "-r", str(REQUIREMENTS)])


def run_main():
    print("[run.py] Starting application with python Core/Main.py")
    run([str(VENV_PY), "Core/Main.py"])


def main():
    newly_created = ensure_venv()
    if newly_created:
        install_requirements()
    try:
        run_main()
    except:
        install_requirements()

if __name__ == "__main__":
    main()