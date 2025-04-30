from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_the_verge():
    url = 'https://www.theverge.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    # Update the class name if necessary, ensure the correct class for article titles
    for item in soup.find_all('h2', class_='c-entry-box--compact__title'):
        link_tag = item.find('a')
        if link_tag:
            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            # Ensure relative links are properly formatted
            if link.startswith('/'):
                link = 'https://www.theverge.com' + link
            articles.append({'title': title, 'link': link})

    # Reverse the articles if you want the most recent first
    articles.reverse() 
    return articles

@app.route('/')
def index():
    articles = scrape_the_verge()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)

