# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time
import os

# Configuration for Flask
app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_model():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # --- SIMULATE GENERATION ---
    time.sleep(3) # Simulate the time it takes for an AI model to run
    
    # 1. Generate a unique, placeholder STL filename based on the current time
    timestamp = int(time.time())
    generated_filename = f"model_{timestamp}.stl" 
    
    # 2. Save a placeholder file in the 'static' folder
    static_dir = os.path.join(app.root_path, 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    placeholder_filepath = os.path.join(static_dir, generated_filename)
    
    # Create an empty file with basic ASCII STL data
    with open(placeholder_filepath, 'w') as f:
        f.write("solid Model\n")
        f.write("facet normal 0 0 1\n")
        f.write("outer loop\n")
        f.write("vertex 0 0 0\n")
        f.write("vertex 10 0 0\n")
        f.write("vertex 0 10 0\n")
        f.write("endloop\n")
        f.write("endfacet\n")
        f.write("endsolid Model")


    # 3. Send back the success response
    return jsonify({
        "status": "success",
        "prompt": prompt,
        "model_filename": generated_filename,
    }), 200

# This is the route that serves the file to the frontend
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
