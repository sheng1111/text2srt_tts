import pytest
from app.services.voice import VoiceService
import toml
import os

@pytest.fixture
def config():
    # Create a dummy config that forces Edge TTS usage
    # by ensuring Azure keys are not present.
    config = toml.load("config.example.toml")
    config["AZURE_KEY"] = ""
    config["AZURE_REGION"] = ""
    return config

def test_synthesize_with_edge_tts(config, tmp_path):
    """Tests if the service correctly uses Edge TTS when Azure keys are missing."""
    service = VoiceService(config)
    text = "Hello, world."
    voice_name = "en-US-JennyNeural"
    rate = 0
    pitch = 0
    volume = 0
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()

    audio_file, word_boundaries = service.synthesize(text, voice_name, rate, pitch, volume, str(output_dir))

    assert audio_file is not None
    assert os.path.exists(audio_file)
    assert audio_file.endswith(".mp3") # Edge TTS produces mp3
    assert word_boundaries is not None
    assert len(word_boundaries) > 0
    os.remove(audio_file)