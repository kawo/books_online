# coding: utf-8

import requests
from bs4 import BeautifulSoup

book_url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

# requesting url
r = requests.get(book_url)
# fix bad guess of encoding resulting in bad £ symbol showing
r.encoding = "UTF-8"

# checking if url is alive
# r.ok check if HTTP request return 200
if r.ok:
    # instancing BS4 object with url
    # using lxml parser instead of default html.parser because it's faster
    soup = BeautifulSoup(r.text, "lxml")

    title = soup.find("li", class_="active")

    # one solution was to take the description in header,
    # other is to look for the only "p" tag without class..
    description = soup.find_all("p", class_="")

    # building dictionarie from book's information table
    product_infos = {}
    table = soup.find("table", class_="table table-striped")
    for row in table.find_all("tr"):
        row_title = row.find("th")
        row_value = row.find("td")
        product_infos[row_title.text] = row_value.text

    # only one list with "breadcrumb" class for category
    # effective category is always in pos 2 within array
    product_category = []
    list = soup.find("ul", class_="breadcrumb")
    for item in list.find_all("li"):
        product_category.append(item.text)

    # parsing all class name with "star-rating"
    # only the first occurence is about the active book
    # so we gather the second item in the array
    rating = []
    for element in soup.find_all(class_="star-rating"):
        for value in element["class"]:
            rating.append(value)

    book_img = soup.find("img", alt=title.text)
    book_img_url = book_img.get("src").replace("../..", "http://books.toscrape.com")

    # printing all data collected for debugging purpose
    # before writing CSV
    print("product_page_url: " + book_url)
    print("upc: " + product_infos["UPC"])
    print("title: " + title.text)
    print(
        "price_including_tax: " + product_infos["Price (incl. tax)"]
    )  # TO-DO: extract only the value
    print("price_excluding_tax: " + product_infos["Price (excl. tax)"])  # TO-DO: same
    print("number_available: " + product_infos["Availability"])
    print("product_description: " + description[0].text)
    print("category: " + product_category[2])
    print("rating: " + rating[1])
    print("image_url: " + book_img_url)
else:
    print("Nooooo!")
