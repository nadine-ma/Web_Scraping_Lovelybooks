import json
import os

from tqdm import tqdm

import variables
from book import Book


def load_books(filepath):
    """
    Load all books

    :param filepath: str, filepath to json file containing book data
    :return: list[Book], list containing Book objects
    """
    books = []
    with open(filepath, encoding='utf-8') as f:
        json_string = json.load(f)
        for book in json_string["books"]:
            books.append(Book(**book))
    print(f"finished loading {len(books)} books")
    return books


def write_data_to_file(books: list[Book]):
    """
    Write all book data to json file

    :param books: list[Book]
    """
    for j, book in tqdm(enumerate(books), total=len(books), desc=f"Writing book information to json"):
        is_first = False
        is_last = False
        if j == 0:
            is_first = True
        if j == len(books) - 1:
            is_last = True
        write_book_infos_to_json(book, is_first, is_last)
    print(f"No. of books: {len(books)}")


def write_book_infos_to_json(book: Book, is_first: bool = False, is_last: bool = False):
    """
    Write data from one book to json

    :param book: Book, book object that will be appended to json file containing all books' data
    :param is_first: bool, whether the Book object is the first to be written to file
    :param is_last: bool, whether the Book object is the last to be written to file
    """
    with open(os.path.join("output", variables.FILENAME_JSON + '_' + variables.TIMESTAMP + '.json'), 'a',
              encoding='utf-8') as jsonfile:
        if is_first:
            jsonfile.write('{"books": [')
        jsonfile.write(book.to_json())
        if not is_last:
            jsonfile.write(',')
        if is_last:
            jsonfile.write(']}')
