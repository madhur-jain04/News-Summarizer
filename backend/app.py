from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer_service import extractive_summarize, abstractive_summarize, get_text_stats
from scraper_service import get_article_text_from_url

# Initialize Flask App start
app = Flask(__name__)
# Enable CORS for the frontend to communicate with the backend
CORS(app) 

@app.route('/summarize', methods=['POST'])
def summarize_endpoint():
    data = request.get_json()
    input_text = data.get('text', '').strip()
    input_url = data.get('url', '').strip()
    
    article_text = ""
    
    # 1. Get the raw text either from the URL or direct input
    if input_url:
        print(f"Processing URL: {input_url}")
        article_text = get_article_text_from_url(input_url)
    elif input_text:
        print("Processing Text Input")
        article_text = input_text
    
    if not article_text or article_text.startswith("ERROR"):
        error_message = article_text if article_text.startswith("ERROR") else "No valid text or URL content could be retrieved."
        return jsonify({"error": error_message}), 400
    
    # Check if the article is too short to be summarized meaningfully
    if len(article_text.split()) < 50:
         return jsonify({"error": "The input text is too short (less than 50 words) to generate a meaningful summary. Please provide a longer article."}), 400

    try:
        # 2. Run both summarization techniques
        extractive_summary = extractive_summarize(article_text)
        abstractive_summary = abstractive_summarize(article_text)
        
        original_stats = get_text_stats(article_text)
        extractive_stats = get_text_stats(extractive_summary)

        # 3. Return the results
        return jsonify({
            "status": "success",
            "original_text": article_text,
            "extractive_summary": extractive_summary,
            "abstractive_summary": abstractive_summary,
            "original_stats": original_stats,
            "extractive_stats": extractive_stats
        })

    except Exception as e:
        print(f"Summarization error: {e}")
        return jsonify({"error": f"An internal summarization error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Flask API on http://127.0.0.1:5000")

    app.run(debug=True, port=5000)
