import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import time
from tempfile import NamedTemporaryFile
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
import re
from google import genai

nlp = spacy.blank("en")  # Lightweight, just for sentence splitting
nlp.add_pipe('sentencizer')

def normalize_url(url):
    url = urldefrag(url)[0]
    parsed = urlparse(url)
    return parsed._replace(fragment='').geturl()

def clean_and_truncate_text(text, max_chars=2000):
    """
    Clean and truncate text to reduce token usage.
    """
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove common web artifacts
    text = re.sub(r'cookie|privacy|terms|contact|login|signup', '', text, flags=re.IGNORECASE)
    # Truncate to max_chars, preferably at sentence boundary
    if len(text) > max_chars:
        sentences = text.split('.')
        truncated = ''
        for sentence in sentences:
            if len(truncated + sentence + '.') <= max_chars:
                truncated += sentence + '.'
            else:
                break
        return truncated.strip()
    return text

def crawl_and_summarize_website(start_url, max_depth=1, max_chars=5000, summary_sentences=5):
    """
    Crawl the website starting from start_url, extract text, and return a concise summary.
    Optimized for token efficiency.
    """
    visited = set()
    domain = urlparse(start_url).netloc
    all_text = []

    # --- Setup Headless Chrome ---
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    def extract_text(url, depth=0):
        if depth > max_depth or len(' '.join(all_text)) > max_chars:
            return
        try:
            driver.get(url)
            time.sleep(1)  # Reduced wait time
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            # Extract only main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|body'))
            if main_content:
                texts = list(main_content.stripped_strings)
            else:
                texts = list(soup.stripped_strings)
            page_text = ' '.join(texts)
            if page_text:
                all_text.append(page_text)
            # Limit crawling to avoid excessive content
            if len(all_text) >= 3:  # Only crawl first 3 pages
                return
            for link in soup.find_all('a', href=True):
                abs_url = normalize_url(urljoin(url, link['href']))
                if abs_url not in visited and domain in abs_url:
                    visited.add(abs_url)
                    extract_text(abs_url, depth + 1)
        except Exception:
            pass

    normalized_start = normalize_url(start_url)
    visited.add(normalized_start)
    extract_text(normalized_start)
    driver.quit()

    full_text = ' '.join(all_text)
    if not full_text.strip():
        return None

    # Clean and truncate the text
    cleaned_text = clean_and_truncate_text(full_text, max_chars=2000)

    # Use spaCy for efficient summarization
    try:
        doc = nlp(cleaned_text)
        sentences = list(doc.sents)
        # Take only first few sentences for efficiency
        summary_sentences = min(summary_sentences, len(sentences))
        return ' '.join(str(s) for s in sentences[:summary_sentences])
    except Exception:
        # Fallback: return first 2000 characters
        return cleaned_text[:2000]

def preview_gemini_token_count(prompt, api_key=None, model="gemini-2.5-flash-lite-preview-06-17"):
    """
    Returns the number of tokens that would be sent to Gemini for a given prompt.
    """
    if api_key:
        genai.configure(api_key=api_key)
    client = genai.Client()
    total_tokens = client.models.count_tokens(
        model=model, contents=prompt
    )
    return total_tokens

def crawl_summarize_and_preview_tokens(start_url, api_key=None, max_depth=1, max_chars=5000, summary_sentences=5, model="gemini-2.5-flash-lite-preview-06-17"):
    """
    Crawl and summarize the website, and return both the summary and the Gemini token count preview.
    """
    summary = crawl_and_summarize_website(start_url, max_depth=max_depth, max_chars=max_chars, summary_sentences=summary_sentences)
    if not summary:
        return {"summary": None, "token_count": 0}
    token_count = preview_gemini_token_count(summary, api_key=api_key, model=model)
    return {"summary": summary, "token_count": token_count} 