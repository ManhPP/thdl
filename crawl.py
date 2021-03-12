import requests
from bs4 import BeautifulSoup
import re
import json
import config


def crawl_hhm():
    url = config.link["hhm"]
    pages = config.page["hhm"]
    data = {}

    for page in pages:
        response = requests.get(url + str(page))
        soup = BeautifulSoup(response.content, "html.parser")

        product_item_list = soup.find_all("div", class_="col-content lts-product")
        for product_item in product_item_list:
            products = product_item.find_all("div", class_="item")

            for item in products:
                info = item.find("div", class_="info")

                try:
                    title = info.find("a", class_="title").text
                    price = int(re.sub('[^0-9]', '', info.find("span", class_="price").find("strong").text))
                except:
                    continue

                try:
                    listed_price = int(re.sub('[^0-9]', '', info.find("strike").text))
                    key = info.find("a", class_="title").attrs["title"]
                except:
                    listed_price = 0
                    key = title
                if key in data.keys():
                    print("da ton tai: ", key)
                data[key] = {"title": title, "price": price, "listed_price": listed_price}
    with open('hhm.json', 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    return 0


def crawl_cps():
    url = config.link["cps"]
    pages = config.page["cps"]
    data = {}

    for page in pages:
        response = requests.get(url + str(page), headers=config.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        product_list = soup.find_all("li", class_="cate-pro-short")
        for product in product_list:
            try:
                special_price = re.sub('[^0-9]', '',
                                       product.find("p", class_="special-price").find("span", class_="price").text)
                id = product.attrs["data-id"]
                product_name = product.find("h3").text.strip().replace("\t", "")
            except Exception as e:
                print(e)
                continue

            try:
                old_price = re.sub('[^0-9]', '',
                                   product.find("p", class_="old-price").find("span", class_="price").text)

            except:
                old_price = 0

            data[id] = {"product_name": product_name, "special_price": special_price, "old_price": old_price}
    with open('cps.json', 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    return 0


def crawl_nk():
    url = config.link["nk"]
    pages = config.page["nk"]
    data = {}

    for page in pages:
        response = requests.get(url + str(page), headers=config.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        product_list = soup.find("div", id="pagination_contents").find_all("div",
                                                                           class_="item nk-fgp-items nk-new-layout-product-grid")
        for product in product_list:

            try:
                id = product.attrs["id"]
                main_item = product.find("div", class_="nk-product-desc")
                label = main_item.find("p", class_="label").find("span").text
                price_item = main_item.find("div", class_="price-details")
                now_price = re.sub('[^0-9]', '', price_item.find("div", class_="price-now").find("span").text)
            except Exception as e:
                continue

            try:
                input = product.find("input")
                brand = input.attrs["data-brand"]
                currency = input.attrs["data-currency"]
                description = input.attrs["data-description"]
                old_price = re.sub('[^0-9]', '', price_item.find("p", class_="price-old").find("span").text)

            except:
                brand = ""
                currency = ""
                description = ""
                old_price = 0

            data[id] = {"label": label, "now_price": now_price, "old_price": old_price,
                        "brand": brand, "currency": currency, "description": description}
    with open('nk.json', 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    # crawl_hhm()
    crawl_cps()
    # crawl_nk()
    # link = "https://cellphones.com.vn/mobile.html?p=1"

    # response = requests.get(link)
    # soup = BeautifulSoup(response.content, "html.parser")
    # len(soup.find_all("ul", class_ ="homeproduct item2020 ")[0].find_all("li", class_= "item"))
