## Web Scraping lovelybooks.de

The code in this repository provides the functionality to scrape genre-based book lists from the book-rating website [lovelybooks.de.](https://www.lovelybooks.de/)

<b>Disclaimer</b>: This project is a 'just for fun' project to try out web scraping

Currently the code extracts the following book information for books listed in genre-specific book lists:
- `title`: Book title
- `subtitle`: Book subtitle
- `author`: Name of the main author
- `summary`: Textual description of the book's content
- `tags`: Collection of tags associated with the book's content
- `isbn`: Unique book identifier
- `user rating distribution`: On a rating scale from 1-5 stars, how many users have given the book each star rating
- `average user rating`: Average of all user ratings for the book
- `rating count`: how many users have rated the book on the website
- `reader count`: How many users have currently marked the book in their library as 'currently reading'
- `owner count`: How many users have specified that they own the book
- `wishlist count`: How many users have this book on their wishlist
- `review count`: How many users have left a review (text-based not simply rating-based)
- `publisher`
- `first publishing date`
- `book type`
- `page count`
- `genre`
- `language`
- `cover url`



### How to run it

##### Run the code using the standard settings (scrape all books listed in the genres "fantasy" and "romantasy"):
`python src/run_scraping.py`

##### Specify which genres to scrape:
`python src/run_scraping.py --genres "fantasy,crime,romantasy,scifi"`

##### Specify how many pages of book lists to scrape(one page typically contains information for 60 books). The page value will be applied to each genre:
`python src/run_scraping.py --max_pages 2`


