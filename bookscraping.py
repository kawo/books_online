import requests

book_url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

# checking if url is alive
r = requests.get(book_url)

if r.status_code == 200:
    print(r.text)
else:
    print("Nooooo!")
