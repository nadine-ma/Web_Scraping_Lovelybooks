import math
import requests
import time
import warnings
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from book import Book


def get_books(genre: str, batch_size: int, page: int):
    """
    Function, to query genre book collections on lovelybooks.de website

    :param genre: str, which book genre collection to query
    :param batch_size: int, which batch size to use when querying the website
    :param page: int, which page to query
    :return: list[Book], list containing Book objects
    """
    url_books = f"https://www.lovelybooks.de/mapi/books/recommendations?tag={genre}&size={batch_size}&page={page}"
    max_retries = 3
    retry_counter = 0
    retry_time = 2
    json_string = ""
    books = []
    # retry management
    while json_string == "" and retry_counter < max_retries:
        try:
            json_string = requests.get(url_books).json()
            is_empty = json_string["empty"]
            if not is_empty:
                for el in json_string['content']:
                    book_instance = get_book_data(el)
                    books.append(book_instance)

        except Exception as e:
            # print(f"{url_books} Retry No. {retry_counter} --> \t {e}")
            time.sleep(retry_time)
            retry_time *= 2
    return books


def get_book_data(json_book: dict):
    """
    Extracts book information from the provided json content

    :param json_book: dict
    :return: Book, an instance of the Book class
    """
    try:
        book = json_book['book']
        identifier = book['id']
        isbn = book['isbn']
        title = book['title']

        # Apply markup cleanup on selected textual attribute values using BeautifulSoup
        if title is not None:
            title = BeautifulSoup(title, "html.parser").text
        subtitle = book['subtitle']
        if subtitle is not None:
            subtitle = BeautifulSoup(subtitle, "html.parser").text
        summary = book['summary']
        if summary is not None:
            summary = BeautifulSoup(summary, "html.parser").text

        book_type = book['bookTypeDescription']
        pages = book['numberOfPages']
        author_name = book['author']['name']
        author_id = book['author']['id']
        genre = book['genre']
        language = book["language"]
        publisher = book['publisher']
        first_publishing_date = book["firstEditionPublicationDate"]
        ratings = book['ratingDistribution']
        average_rating = book['averageRating']
        number_of_ratings = book['numberOfRatings']
        number_of_reviews = book['numberOfReviews']
        cover_url = book['cover']['url']

        # Instantiate Book object with extracted data
        book_instance = Book(identifier=identifier, title=title, subtitle=subtitle, author=author_name,
                             author_id=author_id,
                             summary=summary, isbn=isbn, average_rating=average_rating, rating_distribution=ratings,
                             number_of_ratings=number_of_ratings, number_of_reviews=number_of_reviews,
                             publisher=publisher,
                             first_publishing_date=first_publishing_date, book_type=book_type, pages=pages,
                             genre=genre, language=language, cover_url=cover_url
                             )
    except Exception as e:
        print(f"Could not extract book information from json dict")
    return book_instance


def add_tags_to_book(book: Book):
    """
    Adds tag information to Book objects by querying the associated api link

    :param book: Book
    :return: Book, returns the updated Book object
    """
    max_retries = 3
    retry_counter = 0
    retry_time = 2
    json_string = ""
    identifier = book.identifier
    url_tags = f"https://www.lovelybooks.de/mapi/targeting/data?page=BOOK&identifier={identifier}"
    # retry management
    while json_string == "" and retry_counter < max_retries:
        try:
            json_string = requests.get(url_tags).json()
            tags = json_string["tags"]
            book.set_tags(tags)
        except Exception as e:
            # print(f"{url_tags} Retry No. {retry_counter} --> \t {e}")
            time.sleep(retry_time)
            retry_time *= 2
    return book


def add_community_statistics_to_book(book: Book):
    """
    Adds community statistics to Book objects by querying the associated api link

    :param book: Book
    :return: Book, returns the updated Book object
    """
    max_retries = 3
    retry_counter = 0
    retry_time = 2
    json_string = ""
    identifier = book.identifier
    url_community_statistics = f"https://www.lovelybooks.de/mapi/books/{identifier}/communityInfo"
    # retry management
    while json_string == "" and retry_counter < max_retries:
        try:
            json_string = requests.get(url_community_statistics).json()
            number_of_readers = json_string["numberOfReaders"]
            number_of_owners = json_string["numberOfOwners"]
            number_of_wishlist = json_string["numberOfWishlist"]
            book.set_number_of_readers(number_of_readers)
            book.set_number_of_owners(number_of_owners)
            book.set_number_of_wishlist(number_of_wishlist)
        except Exception as e:
            # print(f"{url_community_statistics} Retry No. {retry_counter} --> \t {e}")
            time.sleep(retry_time)
            retry_time *= 2
    return book


def remove_stopwords(text: str):
    """
    Remove german stopwords from input text using nltk

    :param text: str, input text to remove stopwords from
    :return: str, input text without stopwords
    """
    stop_words = set(stopwords.words('german'))
    text_tokens = word_tokenize(text)
    filtered_text = [w for w in text_tokens if not w.lower() in stop_words and len(w) > 1]
    filtered_text = " ".join(filtered_text)
    return filtered_text


def get_approx_max_pages(genre: str, batch_size: int):
    """
    This function gets an approximated value of the number of pages for books listed in the specified genre using the specified batch size

    :param genre: str
    :param batch_size: int, specifies how many books are listed per page
    :return: int, an approximated value of the number of pages
    """
    url_books = f"https://www.lovelybooks.de/mapi/books/recommendations?tag={genre}&size={batch_size}&page=1"
    json_string = requests.get(url_books).json()
    total_elements = json_string["totalElements"]
    approx_last_page = math.ceil(total_elements / batch_size)
    return approx_last_page
