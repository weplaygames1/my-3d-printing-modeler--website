# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time
import os

# Configuration for Flask
# We specify the static_folder to be 'static' inside the backend directory
app = Flask(__name__, static_folder='static')
CORS(app) # Enables CORS for all routes

@app.route('/generate', methods=['POST'])
def generate_model():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Line 17 (The one we had trouble with) is now guaranteed clean:
    print(f"Received prompt: '{prompt}'")
    
    # --- SIMULATE GENERATION ---
    time.sleep(3) # Simulate the time it takes for an AI model to run
    
    # 1. Generate a unique, placeholder STL filename based on the current time
    timestamp = int(time.time())
    generated_filename = f"model_{timestamp}.stl" 
    
    # 2. Save a placeholder file in the 'static' folder for the test to succeed
    
    # Path to the static folder (create if it doesn't exist)
    static_dir = os.path.join(app.root_path, 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    # Create an empty file with basic STL data (a single triangle)
    placeholder_filepath = os.path.join(static_dir, generated_filename)
    
    # Note: We are writing ASCII STL data here for simplicity. 
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


    # 3. Send back the success response with the generated filename
    return jsonify({
        "status": "success",
        "prompt": prompt,
        "model_filename": generated_filename,
    }), 200

# This is the route that allows the frontend to request the generated file for download
@app.route('/static/<path:filename>')
def static_files(filename):
    # This securely serves the file from the 'static' folder
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
