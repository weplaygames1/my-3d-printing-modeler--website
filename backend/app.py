# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS # We need to install Flask-CORS for cross-origin requests

app = Flask(__name__)
CORS(app) # Enables CORS for all routes

@app.route('/generate', methods=['POST'])
def generate_model():
    # 1. Get the prompt from the user
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

print(f"Received prompt: '{prompt}'")
    
    # --- 2. THE AI MAGIC HAPPENS HERE ---
    # In the future, this is where you would call your actual text-to-3D model.
    # For now, we simulate the processing time and result.
    
    # Simulate a time-consuming AI process (e.g., 5 seconds)
    import time
    time.sleep(5)
    
    # 3. Send back a placeholder result
    
    # The 'filename' is a placeholder for the path to the generated 3D file (e.g., 'model.glb')
    return jsonify({
        "status": "success",
        "prompt": prompt,
        "model_filename": "generated_model_123.glb",
        "model_url": f"/static/models/generated_model_123.glb"
    }), 200

if __name__ == '__main__':
    # Running on port 5000 is standard for Flask development
    app.run(debug=True, port=5000)
