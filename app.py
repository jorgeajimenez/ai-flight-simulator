from flask import Flask, render_template, request, jsonify, send_from_directory
from config import logger 
from services.vault import VaultService
from services.geospatial import ReverseGeocode
from services.ai_vision import AIVisionService
from services.audio_engine import AudioSynthesisService
from services.state_sync import PersistentWorldClient
from services.control_tower import CopilotAgent

app = Flask(__name__, static_folder=".", template_folder=".")

@app.route("/")
def index():
    return render_template(
        "index.html", google_maps_api_key=VaultService.get_maps_api_key()
    )

@app.route("/slides")
def slides():
    return render_template("slides.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(".", filename)

@app.route("/locate", methods=["POST"])
def locate():
    """
    Reverse geocodes coordinates and hails the Copilot to contact the Control Tower.
    """
    try:
        data = request.json
        lat, lon = data.get("lat"), data.get("lon")

        # 1. Ground the AI: Convert coordinates into a real city name
        city_name = ReverseGeocode.get_location_name(lat, lon)

        # 2. Hailing the Copilot: Triggers the direct ADK Agent-to-Agent call
        atc_response = CopilotAgent.request_airspace_update(city_name)

        # 3. Text-to-Speech: Synthesize the transmission
        audio_b64 = AudioSynthesisService.synthesize_advisory(
            atc_response, voice_type="atc"
        )

        return jsonify({"audio": audio_b64, "text": atc_response, "city": city_name})
    except Exception as e:
        logger.error(f"Locate Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/terraform", methods=["POST"])
def terraform():
    """
    Uses the Procedural Biome Engine to generate a new world texture for the current city.
    """
    try:
        data = request.json
        lat, lon, prompt = (
            data.get("lat"),
            data.get("lon"),
            data.get("prompt", "Cyberpunk City"),
        )

        # 1. Reverse Geocode to identify the city biome
        city_name = ReverseGeocode.get_location_name(lat, lon)

        # 2. Procedural Biome Generation: Gemini designs it, Imagen paints it
        ai_result = AIVisionService.generate_biome_texture(city_name, prompt)

        # 3. Voice Briefing
        audio_b64 = AudioSynthesisService.synthesize_advisory(ai_result["advisory"])

        # 4. Persistence: Upload texture to CDN and log to standard event log
        texture_url = PersistentWorldClient.log_terraform_event(
            lat, lon, prompt, ai_result["image_b64"]
        )

        # 5. Calculate bounds for the frontend Cesium renderer
        offset = 0.0025
        bounds = [lat - offset, lon - offset, lat + offset, lon + offset]

        return jsonify(
            {
                "image": ai_result["image_b64"],
                "audio": audio_b64,
                "narrative": ai_result["advisory"],
                "texture_url": texture_url,
                "city": city_name,
                "bounds": bounds
            }
        )
    except Exception as e:
        logger.error(f"Terraforming Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
