# Market Analysis for Books Online

Books Online is a virtual company for my first course project @OpenClassrooms.
I'm in charge of developing a python script to grab books from [http://books.toscrape.com/](http://books.toscrape.com/) and write them in csv files.

Environment:

- vscode
- wsl2

Libs used:

- python.requests
- python.os
- python.logging
- python.csv
- BeautifulSoup4

Profiler:

- cProfile
- snakeviz

## Installation

1. Download or clone the repository
2. Create a virtualenv with Python **3.9.x**
3. Install required packages:
    > pip install -r requirements.txt
4. run the script:
    > python main.py

## Features

- Looks for all categories then looping inside to scrap all books
- One CSV file per category in Books folder
- Covers of books are in books/covers/category folder (for easier read)
- Encoding compliant with Excel (and all sheets)

## Optimizations

Here are some optimizations I found with profiling. Thoses optimizations are not part of previous beta (showing my way of working).

### requests.session

Using session() instead of direct get() to keep connection alive and not creating a new one for each call (BIG time reduction in execution).

### cchardet

cchardet is a lib for guessing encoding MUCH faster than python's vanilla or Dammit from BS4. Found it in [BS4 docs](https://beautiful-soup-4.readthedocs.io/en/latest/#improving-performance).

## Previous versions

The previous versions were steps from the course. Please switch to the approriate tag for instructions.

### beta 1

Export one book page to a CSV file.

**Status: released.**

## beta 2

Automate the process for all books from one category.

**Status: released.**

## beta 3

Scrap the whole site.

**Status: released.**
