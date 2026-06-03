"""Utility functions for the RAG chatbot backend."""

import re
from typing import List, Tuple


def extract_video_references(text: str) -> List[str]:
    """Extract video references (A or B) from text."""
    pattern = r'\bVideo\s+([AB])\b'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return list(set(matches))


def extract_timestamps(text: str) -> List[Tuple[int, int]]:
    """Extract timestamp references from text (e.g., '00:15' or '5s')."""
    # Look for MM:SS or Xs patterns
    patterns = [
        r'(?:(\d{1,2}):(\d{2}))',  # MM:SS
        r'(\d+)s(?!mall)',  # Xs (seconds)
    ]

    timestamps = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            if len(match.groups()) == 2 and match.group(1):
                minutes, seconds = int(match.group(1)), int(match.group(2))
                total_seconds = minutes * 60 + seconds
                timestamps.append((total_seconds, total_seconds))
            elif len(match.groups()) == 1 and match.group(1):
                seconds = int(match.group(1))
                timestamps.append((seconds, seconds))

    return timestamps


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage."""
    return f"{value:.{decimals}f}%"


def format_number(value: int) -> str:
    """Format number with thousand separators."""
    return f"{value:,}"


def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    # Remove leading/trailing whitespace
    text = text.strip()
    # Limit length
    if len(text) > 5000:
        text = text[:5000]
    return text
