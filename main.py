from app.scrap_book import ScrapBook
from app.scrap_navigation import ScrapCategory
import logging

# TODO: optimization with cProfile

logging.basicConfig(filename="logs/scap.log", encoding="utf-8", level=logging.DEBUG)


def bookScraping(book_list):
    scrap_book = ScrapBook()

    for book in book_list:
        scrap_book.scrapBookPage(book)


def main():

    # grabing all categories in dict
    # then looping to scrap all products
    book_list = ScrapCategory()
    cat_list = ScrapCategory.scrapCategoryList()
    for name, url in cat_list.items():
        print(f"Scraping all books from {name} category...")
        logging.info(f"Scraping all books from {name} category with {url} url")
        books = book_list.scrapCategoryPage(url)
        bookScraping(books)


if __name__ == "__main__":
    main()
