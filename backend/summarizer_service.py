import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict


try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    word_tokenize('test')
except LookupError:
    nltk.download('punkt')

def extractive_summarize(text: str, num_sentences: int = 5) -> str:
    """
    Extractive Summarization using TF-IDF (Sentence Ranking).
    Selects the most representative existing sentences from the text.
    """
    sentences = sent_tokenize(text)
    
    if len(sentences) <= num_sentences:
        return text # Don't summarize if too short

    # 1. Preprocessing and Vectorization
    # Using TF-IDF to score how important a word is.
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    try:
        tfidf_matrix = vectorizer.fit_transform(sentences)
    except ValueError:
        return "Not enough unique words for extractive summary."

    # 2. Sentence Scoring
    # The score of a sentence is the mean of the TF-IDF scores of its words.
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        # Calculate the average TF-IDF score for the sentence's vector
        sentence_scores[sentence] = tfidf_matrix.getrow(i).mean()

    # 3. Selection
    # Select the top N sentences, maintaining their original order (crucial for readability)
    
    # Sort sentences by score to find the top N
    ranked_sentences = sorted(
        sentence_scores.keys(), 
        key=lambda sent: sentence_scores[sent], 
        reverse=True
    )
    
    # Get the top N highest scoring sentences
    top_n_sentences = ranked_sentences[:num_sentences]
    
    # Re-order the selected sentences based on their appearance in the original text
    final_summary_sentences = [sent for sent in sentences if sent in top_n_sentences]
    
    return ' '.join(final_summary_sentences)

def abstractive_summarize(text: str) -> str:
    """
    Abstractive Summarization (Placeholder).
    This feature requires a large HuggingFace model (e.g., BART/T5) and complex setup.
    """
    # NOTE: Uncomment and implement the following if you install 'transformers' and 'torch'
    from transformers import pipeline
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text[:1024], max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception:
        pass

    # Simple placeholder summary
    first_sentence = sent_tokenize(text)[0] if text else "..."
    return f"[ABSTRACTIVE PLACEHOLDER]: A new summary would typically be generated here, often based on the main idea: '{first_sentence}'."

# Function to calculate text length stats
def get_text_stats(text: str) -> dict:
    return {
        "word_count": len(word_tokenize(text)),
        "sentence_count": len(sent_tokenize(text))
    }