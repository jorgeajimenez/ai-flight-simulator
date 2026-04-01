# Module 5: Immersive Audio (Text-to-Speech)

A flight simulator is not complete without an immersive audio experience. In this module, we will implement **Service 4: The Immersive Audio Engine** to turn Gemini's text advisories into a high-quality human voice.

## Multi-Voice Immersion
We are using **Cloud Text-to-Speech** to bring our AI entities to life. To differentiate between the Pilot and the Control Tower (ATC), our service accepts a `voice_type` parameter to select distinct voice models:

*   **The Pilot (`voice_type="pilot"`):** Uses `en-US-Studio-O` for natural briefings.
*   **The ATC (`voice_type="atc"`):** Uses `en-US-Journey-D` for an authoritative tone.

![Architecture: Audio Engine](./assets/05_immersive_audio.png)

*This diagram highlights the routing of AI-generated text to the Cloud TTS Engine, which then returns base64-encoded audio directly to the browser.*

---

## Implementation: `AudioSynthesisService`

**Action Marker 5.1:** Terminate the Flask server (CTRL+C). Open `services/audio_engine.py`, locate the `[CODELAB STEP 4]` marker, and paste the following neural TTS synthesis code.

```python
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
```

**Action Marker 5.2:** Restart the Flask server (`uv run app.py`).
