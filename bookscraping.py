import requests
from bs4 import BeautifulSoup

book_url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

# checking if url is alive
r = requests.get(book_url)

if r.status_code == 200:
    with open("temp/temp.html", "wb") as f:
        f.write(r.content)
else:
    print("Nooooo!")

with open("temp/temp.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

print(soup.prettify())
