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

        // 1. Update status to show generation started
        loadingStatus.textContent = `Generating model for: "${prompt}"... This may take a moment.`;
        viewer.innerHTML = "Initializing 3D generation...";
        
        try {
            // 2. Make the API call to the Flask backend
            const response = await fetch('http://127.0.0.1:5000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();

            if (response.ok) {
                // 3. Successful response from backend
                const modelFileName = data.model_filename || 'generated_model.stl';
                
                loadingStatus.textContent = `✅ Success! Model generation complete. Download of **${modelFileName}** initiated.`;
                viewer.innerHTML = `Model generation complete! Preparing 3D viewer...`;
                
                // 4. Trigger the download of the file
                // We construct the full URL to the static file on the Flask server
                const fileUrl = `http://127.0.0.1:5000/static/${modelFileName}`;
                triggerDownload(fileUrl, modelFileName);
                
            } else {
                // Handle API error messages
                loadingStatus.textContent = `❌ Error: ${data.error || 'Failed to generate model.'}`;
                viewer.innerHTML = `Please check the backend server log for details.`;
            }
        } catch (error) {
            // Handle network connection errors
            loadingStatus.textContent = `❌ Network Error: Could not connect to the backend server (Is http://127.0.0.1:5000 running?).`;
            console.error('Fetch error:', error);
            viewer.innerHTML = `Network error. See console for details.`;
        }
    });
});


/**
 * Function to create a temporary link element and trigger a file download.
 * * @param {string} url The full URL of the file to download (e.g., http://127.0.0.1:5000/static/model.stl).
 * @param {string} filename The suggested name for the downloaded file (e.g., model.stl).
 */
function triggerDownload(url, filename) {
    const link = document.createElement('a');
    
    // Set the file's URL
    link.href = url;
    
    // Set the 'download' attribute to force a download and suggest the filename
    link.download = filename;
    
    // Hide the link element
    link.style.display = 'none';
    
    // Temporarily add the link to the page
    document.body.appendChild(link);
    
    // Simulate a click on the link to start the download
    link.click();
    
    // Clean up by removing the temporary link
    document.body.removeChild(link);
}
