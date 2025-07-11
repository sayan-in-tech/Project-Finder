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

nlp = spacy.blank("en")  # Lightweight, just for sentence splitting
nlp.add_pipe('sentencizer')

def normalize_url(url):
    url = urldefrag(url)[0]
    parsed = urlparse(url)
    return parsed._replace(fragment='').geturl()

def crawl_and_summarize_website(start_url, max_depth=1, max_chars=10000, summary_sentences=10):
    """
    Crawl the website starting from start_url, extract text, and return a summary using NLP.
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
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            texts = list(soup.stripped_strings)
            page_text = '\n'.join(texts)
            all_text.append(page_text)
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

    full_text = '\n'.join(all_text)
    if not full_text.strip():
        return None
    # Use spaCy to split into sentences (fallback if sumy fails)
    try:
        parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, summary_sentences)
        summary_text = '\n'.join(str(sentence) for sentence in summary)
        if summary_text.strip():
            return summary_text
    except Exception:
        pass
    # Fallback: return first N sentences
    doc = nlp(full_text)
    sentences = list(doc.sents)
    return '\n'.join(str(s) for s in sentences[:summary_sentences]) 