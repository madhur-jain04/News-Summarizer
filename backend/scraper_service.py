import requests
from bs4 import BeautifulSoup
import re

def get_article_text_from_url(url: str) -> str:
    """
    Fetches the content of a URL and attempts to extract the main article text.
    Uses common patterns for news articles.
    """
    try:
        # Use a common user agent to prevent blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'lxml')
        
        # 1. Try to find common article tags
        # News sites often use semantic tags like <article> or specific classes
        article_tag = soup.find('article')
        
        if article_tag:
            # If <article> tag is found, extract all text from within it
            text = article_tag.get_text()
        else:
            # Fallback: Find all paragraphs and join them.
            paragraphs = soup.find_all('p')
            text = '\n'.join([p.get_text() for p in paragraphs])

        # 2. Cleanup: Remove extra whitespace, tabs, and newlines
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        
        # Basic check to ensure text is long enough to be an article
        if len(cleaned_text.split()) < 100:
             # If cleanup was too aggressive or page was not an article, use a broader selection
             return soup.body.get_text('\n', strip=True) 

        return cleaned_text

    except requests.exceptions.RequestException as e:
        return f"ERROR: Failed to fetch URL or connect to the internet. ({e})"
    except Exception as e:
        return f"ERROR: An unknown error occurred during scraping. ({e})"