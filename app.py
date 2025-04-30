from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_the_verge():
    url = 'https://www.theverge.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    # Check if the page is retrieved correctly
    if response.status_code != 200:
        print("Failed to retrieve the page. Status code:", response.status_code)
        return articles
    
    # Try using a more general selector, or inspect the correct one
    for item in soup.find_all('h2'):
        link_tag = item.find('a')
        if link_tag:
            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            # Ensure relative links are properly formatted
            if link.startswith('/'):
                link = 'https://www.theverge.com' + link
            articles.append({'title': title, 'link': link})

    # If no articles are found, print a message
    if not articles:
        print("No articles found with the current scraping logic.")
    
    articles.reverse()  # Optionally reverse the order
    return articles

@app.route('/')
def index():
    articles = scrape_the_verge()
    # Print articles to check if any were scraped
    print(articles)
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
