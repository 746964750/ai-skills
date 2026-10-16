"""Entropy entry point; never deletes or rewrites code."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
from check import main
if __name__ == "__main__":
    sys.exit(main(["entropy", *sys.argv[1:]]))
