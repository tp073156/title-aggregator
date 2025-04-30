import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def scrape_mashable():
    url = 'https://sea.mashable.com/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    
    for article in soup.find_all('li', class_='blogroll ARTICLE'):
        link_element = article.find('a', href=True)
        if link_element:
            title = link_element.find('div', class_='caption').get_text(strip=True)
            link = link_element['href']
            
            date_element = article.find('time', class_='datepublished')
            if date_element:
                date_str = date_element.get_text(strip=True)

                date = datetime.strptime(date_str, '%B %d, %Y').replace(tzinfo=timezone.utc)
            else:
                print(f"No date element found for article: {title}")
                continue

            articles.append((date, title, link))
            print(f"Article found: {title} - {link} - {date}")

    articles.sort(reverse=True, key=lambda x: x[0])

    return articles

def display_articles(articles):
    with open("articles.html", "w") as file:
        file.write("<html><head><title>Title Aggregator</title>")
        file.write("<link rel='stylesheet' type='text/css' href='style.css'>")
        file.write("</head><body>")
        file.write("<h1>Mashable Article 2022 Upwards</h1>")
        for date, title, link in articles:
            file.write(f"<p><a href='{link}'>{title}</a> - {date.strftime('%B %d, %Y')}</p>")
        file.write("</body></html>")

if __name__ == "__main__":
    articles = scrape_mashable()
    display_articles(articles)