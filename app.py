from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_mashable():
    url = 'https://mashable.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    # Mashable uses h2 tags with class 'article-title' (this can change — always inspect)
    for item in soup.find_all('a', class_='sc-1out364-0 hMndXN'):
        title = item.get_text(strip=True)
        link = item['href']
        if not link.startswith('http'):
            link = 'https://mashable.com' + link
        articles.append({'title': title, 'link': link})

    articles.reverse()  
    return articles

@app.route('/')
def index():
    articles = scrape_mashable()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
