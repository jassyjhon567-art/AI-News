import requests
from bs4 import BeautifulSoup
import json

def get_news():
    # একটি উদাহরণ সোর্স (TechCrunch)
    url = "https://techcrunch.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_list = []
    for item in soup.select('h2')[:5]: # ৫টি নিউজ নেবে
        news_list.append({"title": item.text.strip(), "link": url})
    
    with open('news.json', 'w') as f:
        json.dump(news_list, f)

get_news()
