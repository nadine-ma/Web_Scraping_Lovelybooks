from typing import Optional
import json
from datetime import datetime


class Book:
    """
    A class representing a book object
    """

    def __init__(self, identifier: str, url: Optional[str] = None, title: Optional[str] = None,
                 subtitle: Optional[str] = None, author: Optional[str] = None, author_id: Optional[str] = None,
                 summary: Optional[str] = None, tags: Optional[list] = None,
                 isbn: Optional[str] = None, average_rating: Optional[float] = None,
                 rating_distribution: Optional[list] = None, number_of_ratings: Optional[int] = None,
                 number_of_reviews: Optional[int] = None,
                 publisher: Optional[str] = None, first_publishing_date: Optional[datetime] = None,
                 book_type: Optional[str] = None, pages: Optional[int] = None,
                 genre: Optional[str] = None, language: Optional[str] = None,
                 number_of_readers: Optional[int] = None, number_of_owners: Optional[int] = None,
                 number_of_wishlist: Optional[int] = None,
                 series_identifier: Optional[str] = None,
                 cover_url: Optional[str] = None):
        self.url = url
        self.identifier = identifier
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.author_id = author_id
        self.summary = summary
        self.tags = tags
        self.isbn = isbn
        self.average_rating = average_rating
        self.rating_distribution = rating_distribution
        self.number_of_ratings = number_of_ratings
        self.number_of_readers = number_of_readers
        self.number_of_owners = number_of_owners
        self.number_of_wishlist = number_of_wishlist
        self.number_of_reviews = number_of_reviews
        self.publisher = publisher
        self.first_publishing_date = first_publishing_date
        self.book_type = book_type
        self.pages = pages
        self.genre = genre
        self.language = language
        self.series_identifier = series_identifier
        self.cover_url = cover_url

    def set_tags(self, tags: list):
        self.tags = tags

    def set_number_of_readers(self, number_of_readers: int):
        self.number_of_readers = number_of_readers

    def set_number_of_owners(self, number_of_owners: int):
        self.number_of_owners = number_of_owners

    def set_number_of_wishlist(self, number_of_wishlist: int):
        self.number_of_wishlist = number_of_wishlist

    def to_json(self):
        """
        Transform book object to json format
        """
        return json.dumps(self.__dict__, ensure_ascii=False)
