from app.scrap_book import ScrapBook


def main():
    book_url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

    scrap = ScrapBook()
    scrap.scrapBookPage(book_url)


if __name__ == "__main__":
    main()
