
import argparse
import toml
import os
import uuid
from app.services.voice import VoiceService
from app.services.subtitle import SubtitleService

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio and SRT subtitles from text.")
    parser.add_argument("--text", required=True, help="Path to the input text file.")
    parser.add_argument("--lang", required=True, help="Language and voice to use (e.g., zh-CN).")
    parser.add_argument("--out", help="Output directory for audio and subtitles. Defaults to task/<UUID>.")
    args = parser.parse_args()

    # Load configuration
    if os.path.exists("config.toml"):
        config = toml.load("config.toml")
    else:
        config = toml.load("config.example.toml")

    # Initialize services
    voice_service = VoiceService(config)
    subtitle_service = SubtitleService(config)

    # Read text from file
    with open(args.text, "r") as f:
        text = f.read()

    # Get voice name from config
    voice_name = config["voices"][args.lang]["name"]

    # Determine output directory
    if args.out:
        output_dir = args.out
    else:
        task_id = str(uuid.uuid4())
        output_dir = os.path.join("task", task_id)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate audio and subtitles
    audio_file, word_boundaries = voice_service.synthesize(text, voice_name, 0, 0, 0, output_dir)
    srt_content = subtitle_service.generate_srt(word_boundaries)

    # Save files
    output_audio_path = os.path.join(output_dir, "output.wav")
    output_srt_path = os.path.join(output_dir, "output.srt")

    os.rename(audio_file, output_audio_path)

    with open(output_srt_path, "w") as f:
        f.write(srt_content)

    print(f"Audio saved to {output_audio_path}")
    print(f"SRT saved to {output_srt_path}")

if __name__ == "__main__":
    main()
