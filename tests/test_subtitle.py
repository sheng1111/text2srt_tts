import pytest
from app.services.subtitle import SubtitleService
import toml

@pytest.fixture
def config():
    return toml.load("config.example.toml")

def test_generate_srt(config):
    service = SubtitleService(config)
    word_boundaries = [
        {'text': 'Hello,', 'offset': 2250000, 'duration': 3300000},
        {'text': 'world.', 'offset': 5650000, 'duration': 4400000}
    ]
    max_line_length = 10

    srt_content = service.generate_srt(word_boundaries, max_line_length)

    expected_srt1 = """1
00:00:00,225 --> 00:00:00,555
Hello,"""
    expected_srt2 = """2
00:00:00,565 --> 00:00:01,005
world."""
    assert expected_srt1 in srt_content
    assert expected_srt2 in srt_content