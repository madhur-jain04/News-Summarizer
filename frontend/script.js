document.addEventListener('DOMContentLoaded', () => {
    const summarizeBtn = document.getElementById('summarize-btn');
    const urlInput = document.getElementById('url-input');
    const textInput = document.getElementById('text-input');
    const resultsDiv = document.getElementById('results');
    const errorMessage = document.getElementById('error-message');
    const loadingSpinner = document.getElementById('loading-spinner');

    const BACKEND_URL = 'http://127.0.0.1:5000/summarize';

    summarizeBtn.addEventListener('click', async () => {
        // Reset state
        resultsDiv.classList.add('results-hidden');
        errorMessage.classList.add('error-hidden');
        errorMessage.textContent = '';
        
        let inputText = textInput.value.trim();
        let inputUrl = urlInput.value.trim();
        let payload = {};

        if (inputUrl && inputText) {
            // Priority given to URL if both are provided
            displayError("Please provide EITHER a URL OR text, not both.");
            return;
        } else if (inputUrl) {
            payload = { url: inputUrl };
        } else if (inputText) {
            payload = { text: inputText };
        } else {
            displayError("Please enter a news article URL or paste the text.");
            return;
        }

        // Show loading spinner and disable button
        loadingSpinner.classList.remove('spinner-hidden');
        summarizeBtn.disabled = true;

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                // Handle API error response
                displayError(data.error || "An unknown API error occurred.");
                return;
            }

            // Success: Display results
            displayResults(data);

        } catch (error) {
            console.error('Fetch Error:', error);
            displayError("Could not connect to the Flask server. Make sure the backend is running at " + BACKEND_URL);
        } finally {
            // Hide loading spinner and re-enable button
            loadingSpinner.classList.add('spinner-hidden');
            summarizeBtn.disabled = false;
        }
    });
    
    // Helper function to show errors
    function displayError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('error-hidden');
        resultsDiv.classList.add('results-hidden');
    }

    // Helper function to display successful results
    function displayResults(data) {
        const originalWords = data.original_stats.word_count;
        const extractiveWords = data.extractive_stats.word_count;
        const reduction = ((originalWords - extractiveWords) / originalWords) * 100;
        
        // Update stats
        document.getElementById('original-word-count').textContent = originalWords.toLocaleString();
        document.getElementById('extractive-word-count').textContent = extractiveWords.toLocaleString();
        document.getElementById('reduction-percentage').textContent = `${reduction.toFixed(1)}%`;

        // Update summaries
        document.getElementById('extractive-output').textContent = data.extractive_summary;
        document.getElementById('abstractive-output').textContent = data.abstractive_summary;
        document.getElementById('original-output').textContent = data.original_text;

        // Show the results section
        resultsDiv.classList.remove('results-hidden');
    }
});