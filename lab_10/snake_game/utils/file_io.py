# utils/file_io.py
# Simple JSON file utilities

import json
from pathlib import Path


def save_json(data: dict, path: Path):
    """Save a dict to a JSON file."""
    with path.open('w') as f:
        json.dump(data, f, indent=2)


def load_json(path: Path) -> dict:
    """Load a dict from a JSON file."""
    with path.open() as f:
        return json.load(f)