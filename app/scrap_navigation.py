# coding: utf-8

import requests
from bs4 import BeautifulSoup
from requests.exceptions import (
    ConnectTimeout,
    HTTPError,
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    ProxyError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
    URLRequired,
)

books_url = []
recursion_pointer = False
base_url = ""


class ScrapCategory:
    def scrapCategoryList():
        try:
            r = requests.get("http://books.toscrape.com/index.html")
            if r.ok:
                # instancing BS4 object with url
                # using content instead of text to grab the header with the body
                # using lxml parser instead of default html.parser because it's faster
                soup = BeautifulSoup(r.content, "lxml")

                # building dict for categories
                # key -> name, value -> url
                category_list = {}
                for data in soup.find_all("div", class_="side_categories"):
                    for link in data.find_all("a"):
                        category_url = "http://books.toscrape.com/" + link.get(
                            "href"
                        ).replace("index.html", "")
                        category_name = link.text.replace("\n", "").strip()
                        category_list[category_name] = category_url
                return category_list
        except (
            HTTPError,
            ConnectionError,
            ProxyError,
            SSLError,
            TimeoutError,
            ConnectTimeout,
            ReadTimeout,
            URLRequired,
            TooManyRedirects,
            MissingSchema,
            InvalidSchema,
            InvalidURL,
        ) as err:
            print(f"Error: {err}")

    def scrapCategoryPage(self, category_url):

        # ugly way to check if the domain IS books.toscrape.com
        # will use regex if time
        url_domain = "http://books.toscrape.com"
        if category_url.startswith(url_domain):
            try:
                # scraping url with requests
                r = requests.get(category_url)

                # checking if url is alive
                # r.ok check if HTTP request return 200
                if r.ok:
                    # instancing BS4 object with url
                    # using content instead of text to grab the header with the body
                    # using lxml parser instead of default html.parser because it's faster
                    soup = BeautifulSoup(r.content, "lxml")

                    # building array from article section
                    # with url to books
                    for article in soup.find_all("article", class_="product_pod"):
                        for img in article.find_all("div", class_="image_container"):
                            for link in img.find_all("a"):
                                book_url = link.get("href").replace(
                                    "../../../", url_domain + "/catalogue/"
                                )
                                books_url.append(book_url)

                    # looking for pagination
                    if soup.find_all("ul", class_="pager"):
                        for data in soup.find_all("ul", class_="pager"):
                            for nav in data.find_all("li", class_="next"):
                                for link in nav.find_all("a"):
                                    # uuugly way to manage the url changing with recursion
                                    global recursion_pointer, base_url
                                    if recursion_pointer is False:
                                        base_url = category_url
                                        next_page = category_url + link.get("href")
                                        recursion_pointer = True
                                    else:
                                        next_page = base_url + link.get("href")
                                    return self.scrapCategoryPage(next_page)
                    return books_url

            # generic except according https://docs.python-requests.org/en/latest/_modules/requests/exceptions/
            except (
                HTTPError,
                ConnectionError,
                ProxyError,
                SSLError,
                TimeoutError,
                ConnectTimeout,
                ReadTimeout,
                URLRequired,
                TooManyRedirects,
                MissingSchema,
                InvalidSchema,
                InvalidURL,
            ) as err:
                print(f"Error: {err}")
        else:
            print(
                f"Sorry, this scrapper only works for {url_domain} domain! URL you provided: {category_url} :("
            )
