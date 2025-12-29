import requests
from bs4 import BeautifulSoup as bs
import random as rand
from ddgs import DDGS

ddgs = DDGS()

        
filepath = input("Enter the file path: ")


with open (filepath, 'r') as file:
    lines = [line.strip() for line in file if line.strip()]

samples = rand.sample(lines,len(lines)//5)

clean_samples = []
for sample in samples:
    cleaned = sample.strip()
    clean_samples.append(cleaned)
print(clean_samples)



def check_sample(sample):
    query = sample
    urls = []
    results = ddgs.text(query,max_results=5)
    
    for result in results:
        urls.append(result["href"])
    
    for url in urls:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url,headers=headers,timeout=20).text
        doc = bs(response,"html")
        
    
    



        