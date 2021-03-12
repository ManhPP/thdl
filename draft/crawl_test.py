import requests
from bs4 import BeautifulSoup

def crawNewsData(baseUrl, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    titles = soup.findAll('h3', class_='title-news')
    links = [link.find('a').attrs["href"] for link in titles]
    data = []
    for link in links:
        news = requests.get(baseUrl + link)
        soup = BeautifulSoup(news.content, "html.parser")
        title = soup.find("h1", class_="article-title").text
        abstract = soup.find("h2", class_="sapo").text
        body = soup.find("div", id="main-detail-body")
        content = ""
        try:
            content = body.findChildren("p", recursive=False)[0].text + body.findChildren("p", recursive=False)[1].text
        except:
            content = ""
        image = body.find("img").attrs["src"]
        data.append({
            "title": title,
            "abstract": abstract,
            "content": content,
            "image": image,
        })
    return data


if __name__ == "__main__":
    pass