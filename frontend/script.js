// script.js
document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generate-button');
    const promptInput = document.getElementById('prompt-input');
    const loadingStatus = document.getElementById('loading-status');
    const viewer = document.getElementById('3d-viewer');

    generateButton.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();

        if (prompt === "") {
            loadingStatus.textContent = "Please enter a description for your 3D model.";
            return;
        }

        loadingStatus.textContent = `Generating model for: "${prompt}"... This may take a moment.`;
        viewer.innerHTML = "Initializing 3D generation...";
        
        // **IMPORTANT:** This is where the real API call to the backend will go.
        try {
            const response = await fetch('http://127.0.0.1:5000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();

            if (response.ok) {
                // In a real application, 'data.model_url' would point to the generated 3D file
                loadingStatus.textContent = `✅ Success! Model generation complete.`;
                viewer.innerHTML = `Model data received! File: ${data.model_filename}`;
                // Future step: Load the 3D model into the viewer (e.g., using Three.js)
            } else {
                loadingStatus.textContent = `❌ Error: ${data.error || 'Failed to generate model.'}`;
                viewer.innerHTML = `Please check the backend server.`;
            }
        } catch (error) {
            loadingStatus.textContent = `❌ Network Error: Could not connect to the backend server (Is http://127.0.0.1:5000 running?).`;
            console.error('Fetch error:', error);
            viewer.innerHTML = `Network error. See console for details.`;
        }
    });
});
