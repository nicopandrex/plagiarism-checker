import requests
from bs4 import BeautifulSoup as bs
from ddgs import DDGS
import time
import similarity as sim
import re

ddgs = DDGS()

BAD_PATTERNS = [
    "access denied",
    "enable javascript",
    "cookies to continue",
    "too many requests",
    "rate-limited",
    "captcha",
    "cloudflare",
    "forbidden",
    "not authorized",
    "request blocked",
    "unusual traffic",
    "service unavailable",
    "temporarily unavailable",
    "your browser is outdated",
    "check supported browsers",
    
    
]

BOILER_PLATE = [
    "accept cookies", 
    "reject cookies", 
    "login",
    "register", 
    "skip to main content", 
    "powered by",
    "all activity",
    "enable cookies",
    "cookie settings",
    "we use cookies"
]

def is_error_page(text):
    t = text.lower()
    return any(p in t for p in BAD_PATTERNS)

def boiler_plate_markers(text):
    t = text.lower()
    bad = 0
    for item in BOILER_PLATE:
        if item in t:
            bad+=1
    return bad > 2
        
def get_body(url):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    response = requests.get(url,headers=headers,timeout=20).text
    doc = bs(response,"html.parser")
    
    for item in doc(["script", "style", "nav", "footer", "header"]):
        item.decompose()
    
    main_area = doc.find('article') or doc.find('div', {'id': 'main-content'}) or doc.find('div',{'class': 'article-body'}) or doc.find('body')
    
    if main_area:
        body_text = main_area.get_text(separator=' ', strip=True)
        return body_text



def get_articles(sample):
    query = sample
    urls = []
    bodys = []
    body_scores = []
    good_bodys = []
    results = ddgs.text(query,max_results=4)
    
    for result in results:
        urls.append(result["href"])
    
    for url in urls:
        try:
            body = get_body(url)
            if not body:
                continue
            if not is_error_page(body) and body and body.strip() :
                if len(body) >= 150 and not boiler_plate_markers(body):
                    bodys.append(body)
        except requests.exceptions.ConnectionError:
            continue
        time.sleep(2)
    for body in bodys:
        score =  sim.cheap_relevance(sample,body)
        body_scores.append((score,body))
        
        
    body_scores.sort()
    if len(bodys) > 1:
        good_bodys.append(body_scores[-1][1])
        good_bodys.append(body_scores[-2][1])
    else:
        good_bodys = bodys
        
        
    return good_bodys
        
        

def flatten_articles(articles_2d):
    flat = []
    for sub in articles_2d:
        if not sub:
            continue
        for body in sub:
            if body and body.strip():
                flat.append(body)
    return flat        
        
        
def split_article_into_chunks(body):
    # First try paragraph breaks
    chunks = [p.strip() for p in body.split("\n\n") if p.strip()]

    # If the page text is one giant blob, fallback:
    if len(chunks) <= 1:
        # Split into sentence-ish pieces, then bundle into ~3-5 sentences per chunk
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]
        if not sents:
            return []
        bundle_size = 4
        chunks = [" ".join(sents[i:i+bundle_size]) for i in range(0, len(sents), bundle_size)]

    return chunks        
    
   



        