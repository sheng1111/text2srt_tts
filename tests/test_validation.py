import pytest
from app.utils.validation import sanitize_text, validate_text, MAX_TEXT_LENGTH


def test_sanitize_text_removes_invalid_chars():
    dirty = 'hello\x00world\x1f!'
    assert sanitize_text(dirty) == 'helloworld!'


def test_validate_text_length_limit():
    text = 'a' * (MAX_TEXT_LENGTH + 1)
    with pytest.raises(ValueError):
        validate_text(text)
