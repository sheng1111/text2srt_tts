import os
import asyncio
import edge_tts
import azure.cognitiveservices.speech as speechsdk
import re


class VoiceService:
    """
    Voice synthesis service supporting both Azure Cognitive Services and Edge TTS.
    Provides text-to-speech synthesis with word boundary extraction for subtitle timing.
    """

    def __init__(self, config):
        """
        Initialize the voice service with configuration.

        Args:
            config: Configuration dictionary containing service settings
        """
        self.config = config

    def synthesize(self, text, voice_name, rate, pitch, volume, output_dir):
        """
        Synthesize speech from text using the available TTS service.

        Args:
            text: Input text to synthesize
            voice_name: Name of the voice to use
            rate: Speech rate adjustment (-50 to +50)
            pitch: Pitch adjustment (-50 to +50)
            volume: Volume adjustment (-50 to +50)
            output_dir: Directory to save the output audio file

        Returns:
            tuple: (audio_file_path, word_boundaries)
        """
        use_azure = self.config.get(
            "AZURE_KEY") and self.config.get("AZURE_REGION")
        if use_azure:
            try:
                return self._synthesize_with_azure(text, voice_name, rate, pitch, volume, output_dir)
            except Exception as e:
                print(f"Azure TTS failed: {e}. Falling back to Edge TTS.")
                return self._synthesize_with_edge(text, voice_name, rate, pitch, volume, output_dir)
        else:
            return self._synthesize_with_edge(text, voice_name, rate, pitch, volume, output_dir)

    def _synthesize_with_azure(self, text, voice_name, rate, pitch, volume, output_dir):
        """
        Synthesize speech using Azure Cognitive Services Speech SDK.

        Args:
            text: Input text to synthesize
            voice_name: Azure voice name
            rate: Speech rate adjustment percentage
            pitch: Pitch adjustment percentage
            volume: Volume adjustment percentage
            output_dir: Output directory for audio file

        Returns:
            tuple: (audio_file_path, word_boundaries)
        """
        speech_config = speechsdk.SpeechConfig(
            subscription=self.config["AZURE_KEY"],
            region=self.config["AZURE_REGION"]
        )
        speech_config.speech_synthesis_voice_name = voice_name
        audio_file = os.path.join(output_dir, "output.wav")

        # Create SSML with voice parameters
        ssml_string = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
            <voice name='{voice_name}'>
                <mstts:express-as style='general'>
                    <prosody rate='{rate}%' pitch='{pitch}%' volume='{volume}%'>
                        {text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None
        )
        word_boundaries = []

        def word_boundary_cb(evt):
            """Callback function to capture word boundary events."""
            word_boundaries.append({
                "text": evt.text,
                "offset": evt.audio_offset / 10000,  # Convert to milliseconds
                "duration": evt.audio_duration / 10000
            })

        # Connect word boundary callback
        speech_synthesizer.synthesis_word_boundary.connect(word_boundary_cb)
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with open(audio_file, "wb") as f:
                f.write(result.audio_data)
            return audio_file, word_boundaries
        else:
            raise Exception(f"Azure TTS synthesis failed: {result.reason}")

    def _synthesize_with_edge(self, text, voice_name, rate, pitch, volume, output_dir):
        """
        Synthesize speech using Edge TTS (wrapper for async function).

        Args:
            text: Input text to synthesize
            voice_name: Edge TTS voice name
            rate: Speech rate adjustment percentage
            pitch: Pitch adjustment percentage
            volume: Volume adjustment percentage
            output_dir: Output directory for audio file

        Returns:
            tuple: (audio_file_path, word_boundaries)
        """
        return asyncio.run(self._edge_tts_async(text, voice_name, rate, pitch, volume, output_dir))

    async def _edge_tts_async(self, text, voice_name, rate, pitch, volume, output_dir):
        """
        Asynchronously synthesize speech using Edge TTS.

        Args:
            text: Input text to synthesize
            voice_name: Edge TTS voice name
            rate: Speech rate adjustment percentage
            pitch: Pitch adjustment percentage
            volume: Volume adjustment percentage
            output_dir: Output directory for audio file

        Returns:
            tuple: (audio_file_path, word_boundaries)
        """
        audio_file = os.path.join(output_dir, "output.mp3")

        # Format parameters for Edge TTS
        rate_str = f'+{rate}%' if rate >= 0 else f'{rate}%'
        pitch_str = f'+{pitch}Hz' if pitch >= 0 else f'{pitch}Hz'
        volume_str = f'+{volume}%' if volume >= 0 else f'{volume}%'

        # Create Edge TTS communicate instance
        communicate = edge_tts.Communicate(
            text,
            voice_name,
            rate=rate_str,
            pitch=pitch_str,
            volume=volume_str
        )
        word_boundaries = []

        # Stream synthesis and collect word boundaries
        with open(audio_file, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    word_boundaries.append({
                        "text": chunk["text"],
                        "offset": chunk["offset"],
                        "duration": chunk["duration"]
                    })

        return audio_file, word_boundaries
