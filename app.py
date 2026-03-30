from flask import Flask, render_template, request, jsonify, send_from_directory
from config import logger # AI_WIRING_POINT: Config & Logging
from services.vault import VaultService
from services.geospatial import EarthEngineClient
from services.ai_vision import AIVisionService
from services.audio_engine import AudioSynthesisService
from services.state_sync import GlobalMultiverseClient
from services.control_tower import ControlTowerAgent

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
    # AI_WIRING_POINT: Service 5 (Vault)
    return render_template('index.html', google_maps_api_key=VaultService.get_maps_api_key())

@app.route('/slides')
def slides():
    return render_template('slides.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


@app.route('/locate', methods=['POST'])
def locate():
    try:
        data = request.json
        lat, lon = data.get('lat'), data.get('lon')
        
        # 1. Ask the Agentic Control Tower (ADK Pattern)
        atc_response = ControlTowerAgent.contact_tower(lat, lon)
        
        # 2. Synthesize the audio (Using a distinct ATC voice)
        audio_b64 = AudioSynthesisService.synthesize_advisory(atc_response, voice_type="atc")
        
        return jsonify({"audio": audio_b64, "text": atc_response})
    except Exception as e:
        logger.error(f"ATC Agent Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/terraform', methods=['POST'])
def terraform():
    try:
        data = request.json
        lat, lon, prompt = data.get('lat'), data.get('lon'), data.get('prompt', 'Cyberpunk City')
        
        # AI_WIRING_POINT: Service 2 (Geospatial)
        image_content, bounds = EarthEngineClient.fetch_satellite_tile(lat, lon)

        # AI_WIRING_POINT: Service 1 (Vision)
        ai_result = AIVisionService.analyze_and_terraform(image_content, prompt)

        # AI_WIRING_POINT: Service 3 (Audio)
        audio_b64 = AudioSynthesisService.synthesize_advisory(ai_result['advisory'])

        # AI_WIRING_POINT: Service 4 (Persistence & CDN)
        texture_url = GlobalMultiverseClient.log_terraform_event(lat, lon, prompt, ai_result['image_b64'])

        return jsonify({
            "image": ai_result['image_b64'], "audio": audio_b64,
            "narrative": ai_result['advisory'], "bounds": bounds,
            "texture_url": texture_url
        })
    except Exception as e:
        logger.error(f"Terraforming Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
