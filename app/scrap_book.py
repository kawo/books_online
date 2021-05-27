# coding: utf-8

import requests
from bs4 import BeautifulSoup
import csv
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


class ScrapBook:
    def scrapBookPage(self, book_url):

        # ugly way to check if the domain IS books.toscrape.com
        # will use regex if time
        url_domain = "http://books.toscrape.com"
        if book_url.startswith(url_domain):
            try:
                # scraping url with requests
                r = requests.get(book_url)

                # checking if url is alive
                # r.ok check if HTTP request return 200
                if r.ok:
                    # instancing BS4 object with url
                    # using content instead of text to grab the header with the body
                    # using lxml parser instead of default html.parser because it's faster
                    soup = BeautifulSoup(r.content, "lxml")

                    # grabing the title
                    title = soup.find("li", class_="active")

                    # one solution was to take the description in header,
                    # other is to look for the only "p" tag without class..
                    description = soup.find_all("p", class_="")

                    # building dictionary from book's information table
                    product_infos = {}
                    table = soup.find("table", class_="table table-striped")
                    for row in table.find_all("tr"):
                        row_title = row.find("th")
                        row_value = row.find("td")
                        product_infos[row_title.text] = row_value.text
                    # grab only the number for availability
                    availability = int(
                        "".join(i for i in product_infos["Availability"] if i.isdigit())
                    )

                    # only one list with "breadcrumb" class for category
                    # effective category is always in pos 2 within array
                    product_category = []
                    list = soup.find("ul", class_="breadcrumb")
                    for item in list.find_all("li"):
                        product_category.append(item.text)
                    # cleaning unnecessary new lines
                    category = product_category[2].replace("\n", "")

                    # parsing all class name with "star-rating"
                    # only the first occurence is about the active book
                    # so we gather the second item in the array (the class rating)
                    rating = []
                    for element in soup.find_all(class_="star-rating"):
                        for value in element["class"]:
                            rating.append(value)

                    # grabing book cover
                    # trunkating url to get the absolute one
                    book_img = soup.find("img", alt=title.text)
                    book_img_url = book_img.get("src").replace(
                        "../..", "http://books.toscrape.com"
                    )

                    # building dictionary for easy csv creation
                    book = {}
                    book["product_page_url"] = book_url
                    book["universal_product_code"] = product_infos["UPC"]
                    book["title"] = title.text
                    book["price_including_tax"] = product_infos["Price (incl. tax)"]
                    book["price_excluding_tax"] = product_infos["Price (excl. tax)"]
                    book["number_available"] = availability
                    book["product_description"] = description[0].text.replace("\n", "")
                    book["category"] = category
                    book["review_rating"] = rating[1]
                    book["image_url"] = book_img_url

                    # csv creation
                    # using "utf-8-sig" for excel compatibility
                    try:
                        with open(
                            "books/book.csv", "w", encoding="utf-8-sig", newline=""
                        ) as csvfile:
                            fieldnames = [
                                "product_page_url",
                                "universal_product_code",
                                "title",
                                "price_including_tax",
                                "price_excluding_tax",
                                "number_available",
                                "product_description",
                                "category",
                                "review_rating",
                                "image_url",
                            ]
                            writer = csv.DictWriter(
                                csvfile, fieldnames=fieldnames, dialect=csv.excel
                            )
                            writer.writeheader()
                            writer.writerow(book)
                        print(f"CSV generated with {csvfile.encoding} encoding!")
                    except IOError as err:
                        print(f"IOError {err}!")
                        raise SystemExit
                else:
                    # basic error handling
                    # will tweak it if there is time
                    print(f"The requested url ({book_url}) is not valid!")
                    raise SystemExit
                return print(
                    f"Book \"{book['title']}\" from \"{category}\" category added to CSV!"
                )
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
                f"Sorry, this scrapper only works for {url_domain} domain! URL you provided: {book_url} :("
            )
