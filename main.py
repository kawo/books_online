from app.scrap_book import ScrapBook
from app.scrap_navigation import ScrapCategory


def main():

    # grabing dict of categories
    cat_list = ScrapCategory.scrapCategoryList()
    cat_url = cat_list["Mystery"]

    # grabing list of books from one category
    book_list = ScrapCategory()
    book_list = book_list.scrapCategoryPage(cat_url)

    # scraping all books from cat!
    scrap = ScrapBook()
    for book in book_list:
        scrap.scrapBookPage(book)


if __name__ == "__main__":
    main()
