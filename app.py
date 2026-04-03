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

# TODO: Paste the /locate route here (See Module 2)

# TODO: Paste the /terraform route here (See Module 2)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
