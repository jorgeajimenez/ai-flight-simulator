import base64
from google.cloud import texttospeech
from config import logger


class AudioSynthesisService:
    """
    Immersive Audio Engine powered by Google Cloud Text-to-Speech.
    Converts AI-generated flight advisories into lifelike studio-quality voice.
    """

    @staticmethod
    def synthesize_advisory(text: str, voice_type: str = "pilot") -> str:
        """
        Synthesizes the given text into an MP3 file using the 'en-US-Studio-O' voice.
        Returns a base64 encoded MP3 string for the frontend player.
        """
        try:
            logger.info("Audio: Synthesizing advisory...")
            client = texttospeech.TextToSpeechClient()

            # 1. Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # 2. Build the voice request: Use a different voice for ATC vs Pilot
            voice_name = "en-US-Journey-D" if voice_type == "atc" else "en-US-Studio-O"

            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", name=voice_name
            )

            # 3. Select the audio file type
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # 4. Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # 5. Return base64 encoded audio
            return base64.b64encode(response.audio_content).decode("utf-8")

        except Exception as e:
            logger.error(f"Audio Error: Failed to synthesize speech: {e}")
            # AI_WIRING_POINT: Handle TTS failures (e.g., return silent audio or error)
            return ""
