import requests
from bs4 import BeautifulSoup as bs
from ddgs import DDGS
import time

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
    results = ddgs.text(query,max_results=1)
    
    for result in results:
        urls.append(result["href"])
    
    for url in urls:
        body = get_body(url)
        if not body:
            continue
        if not is_error_page(body) and body and body.strip() :
            if len(body) >= 150 and not boiler_plate_markers(body):
                bodys.append(body)
        time.sleep(2)
    return bodys
        
        

        
        
        
        
    
   



        