"""Helper functions for text normalization, evidence formatting, and score clamping."""
import html
from typing import List, Any


def clamp_score(score: float, min_val: int = 0, max_val: int = 100) -> int:
    """Clamp score between min_val and max_val and return integer."""
    return int(max(min_val, min(max_val, round(score))))


def format_evidence_list(items: List[str], max_items: int = 5, default_empty: str = "None reported") -> str:
    """Format a list of evidence findings into a clean semicolon-separated string."""
    if not items:
        return default_empty
    cleaned = [html.escape(item.strip()) for item in items if item.strip()]
    if not cleaned:
        return default_empty
    return "; ".join(cleaned[:max_items]) + ("." if not cleaned[-1].endswith(".") else "")


def safe_text(val: Any) -> str:
    """Safely escape text for HTML display."""
    return html.escape(str(val)) if val is not None else ""
