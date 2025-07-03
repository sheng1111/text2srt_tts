import re

MAX_TEXT_LENGTH = 5000


def sanitize_text(text: str) -> str:
    """Remove non-printable characters from the input text."""
    return re.sub(r"[^\x20-\x7E\n\r\t]", "", text)


def validate_text(text: str, max_length: int = MAX_TEXT_LENGTH):
    """Sanitize text and check length.

    Returns the sanitized text. Raises ValueError if length exceeds limit.
    """
    sanitized = sanitize_text(text)
    if len(sanitized) > max_length:
        raise ValueError(f"Text too long (max {max_length} characters)")
    return sanitized
