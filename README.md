## Web Scraping lovelybooks.de

The code provided in this repository provides the functionality to scrape genre-based book lists from the book-rating website lovelybooks.de.


##### Run the code using the standard settings (scrape all books listed in the genres "fantasy" and "romantasy"):
`python run_scraping.py`

##### Specify which genres to scrape:
`python run_scraping.py --genres "fantasy,crime,romantasy,scifi"`

##### Specify how many pages of book lists to scrape(one page typically contains information for 60 books). The page value will be applied to each genre:
`python run_scraping.py --max_pages 2`


