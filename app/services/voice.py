
import os
import asyncio
import edge_tts
import azure.cognitiveservices.speech as speechsdk
import re

class VoiceService:
    def __init__(self, config):
        self.config = config

    def synthesize(self, text, voice_name, rate, pitch, volume, output_dir):
        use_azure = self.config.get("AZURE_KEY") and self.config.get("AZURE_REGION")
        if use_azure:
            try:
                return self._synthesize_with_azure(text, voice_name, rate, pitch, volume, output_dir)
            except Exception as e:
                print(f"Azure TTS failed: {e}. Falling back to Edge TTS.")
                return self._synthesize_with_edge(text, voice_name, rate, pitch, volume, output_dir)
        else:
            return self._synthesize_with_edge(text, voice_name, rate, pitch, volume, output_dir)

    def _synthesize_with_azure(self, text, voice_name, rate, pitch, volume, output_dir):
        speech_config = speechsdk.SpeechConfig(subscription=self.config["AZURE_KEY"], region=self.config["AZURE_REGION"])
        speech_config.speech_synthesis_voice_name = voice_name
        audio_file = os.path.join(output_dir, "output.wav")

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

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        word_boundaries = []

        def word_boundary_cb(evt):
            word_boundaries.append({
                "text": evt.text,
                "offset": evt.audio_offset / 10000,
                "duration": evt.audio_duration / 10000
            })

        speech_synthesizer.synthesis_word_boundary.connect(word_boundary_cb)
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with open(audio_file, "wb") as f:
                f.write(result.audio_data)
            return audio_file, word_boundaries
        else:
            raise Exception(f"Azure TTS synthesis failed: {result.reason}")

    def _synthesize_with_edge(self, text, voice_name, rate, pitch, volume, output_dir):
        return asyncio.run(self._edge_tts_async(text, voice_name, rate, pitch, volume, output_dir))

    async def _edge_tts_async(self, text, voice_name, rate, pitch, volume, output_dir):
        audio_file = os.path.join(output_dir, "output.mp3")
        
        rate_str = f'+{rate}%' if rate >= 0 else f'{rate}%'
        pitch_str = f'+{pitch}Hz' if pitch >= 0 else f'{pitch}Hz'
        volume_str = f'+{volume}%' if volume >= 0 else f'{volume}%'

        communicate = edge_tts.Communicate(text, voice_name, rate=rate_str, pitch=pitch_str, volume=volume_str)
        word_boundaries = []

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
