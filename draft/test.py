import requests
from bs4 import BeautifulSoup

response = requests.get("https://tiki.vn/dien-thoai-smartphone/c1795?page=2")
soup = BeautifulSoup(response.content, "html.parser")
print(soup)
# titles = soup.findAll('h3', class_='title-news')
# print(titles)

# links = [link.find('a').attrs["href"] for link in titles]
# print(links)

# for link in links:
#     news = requests.get("https://tuoitre.vn" + link)
#     soup = BeautifulSoup(news.content, "html.parser")
#     title = soup.find("h1", class_="article-title").text
#     abstract = soup.find("h2", class_="sapo").text
#     body = soup.find("div", id="main-detail-body")
#     content = body.findChildren("p", recursive=False)[0].text +      body.findChildren("p", recursive=False)[1].text
#     image = body.find("img").attrs["src"]
#     print("Tiêu đề: " + title)
#     print("Mô tả: " + abstract)
#     print("Nội dung: " + content)
#     print("Ảnh minh họa: " + image)
#     print("_________________________________________________________________________")


# from PIL import Image, ImageDraw, ImageFont

# img = Image.new('RGB', (650, 625), color="white")
# font = ImageFont.load_default()

# d = ImageDraw.Draw(img)
# d.text((10, 10), "Hello World", font=font, fill="black")

# img.show()

# img = Image.new('RGB', (650, 625), color="white")
# font = ImageFont.load_default()

# d = ImageDraw.Draw(img)

# addImg = Image.open("anh.jpg")

# img.paste(addImg, (10, 10))

# d.text((300, 10), "Cái text nè ahihi", font=font, fill="black")

# img.show()