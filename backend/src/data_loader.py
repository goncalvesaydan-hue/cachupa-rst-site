"""Load and parse the content data from content/site.json."""
import json
from pathlib import Path
from typing import Any, Dict


def load_content() -> Dict[str, Any]:
    """
    Load content data from content/site.json.

    Returns:
        Dict containing the raw content data

    Raises:
        FileNotFoundError: If content/site.json doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    root = Path(__file__).resolve().parents[2]  # Go up to project root
    content_path = root / 'content' / 'site.json'

    if not content_path.exists():
        raise FileNotFoundError(f"Content file not found: {content_path}")

    with open(content_path, 'r', encoding='utf-8') as f:
        return json.load(f)