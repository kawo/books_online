from app.scrap_book import ScrapBook
from app.scrap_navigation import ScrapCategory

# BUG: out of range with Default cat


def main():

    # grabing dict of categories
    cat_list = ScrapCategory.scrapCategoryList()
    for name, url in cat_list.items():
        print(f"{name}")
    cat_name = input(f"Type a category from the list above: ")
    cat_url = cat_list[cat_name]

    # grabing list of books from one category
    book_list = ScrapCategory()
    book_list = book_list.scrapCategoryPage(cat_url)

    # scraping all books from cat!
    scrap = ScrapBook()
    for book in book_list:
        scrap.scrapBookPage(book)


if __name__ == "__main__":
    main()
