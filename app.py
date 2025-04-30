from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_the_verge():
    url = 'https://www.theverge.com'
    response = requests.get(url)

    # Check the status of the request
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Debugging: Print the first 500 characters of the HTML to inspect the structure
    print("Response Content Preview:", response.content[:500])

    articles = []

    # Debugging: Try finding all <a> tags and print them to check the structure
    for item in soup.find_all('a'):
        print(item)  # Print each <a> tag found in the HTML

    # Update this to match the correct class
    for item in soup.find_all('a', class_='c-entry-box--compact__title'):
        title = item.get_text(strip=True)
        link = item['href']
        if not link.startswith('http'):
            link = 'https://www.theverge.com' + link  # Ensure the link is complete
        articles.append({'title': title, 'link': link})

    print(f"Articles found: {len(articles)}")  # Debugging: Check how many articles were found
    return articles

@app.route('/')
def index():
    articles = scrape_the_verge()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
