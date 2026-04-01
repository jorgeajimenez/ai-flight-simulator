import base64
from google.cloud import texttospeech

class AudioSynthesisService:

    @staticmethod
    def synthesize_advisory(text: str, voice_type: str = "pilot") -> str:
        # Instantiate the Google Cloud Text-to-Speech client
        client = texttospeech.TextToSpeechClient()
        
        # Configure the voice based on the requested persona
        voice_name = "en-US-Journey-D" if voice_type == "atc" else "en-US-Studio-O"
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", 
            name=voice_name
        )
        
        # Request MP3 format. A speaking_rate of 1.05 provides a professional cadence.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.05
        )
        
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=text), 
            voice=voice, 
            audio_config=audio_config
        )
        
        # Return base64 encoded bytes
        return base64.b64encode(response.audio_content).decode('utf-8')
