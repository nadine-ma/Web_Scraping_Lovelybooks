import progressbar
from tqdm import tqdm
import datetime
import gc
import time
from multiprocessing.pool import Pool
from typing import Optional

import variables
from data_operations import add_tags_to_book, add_community_statistics_to_book, get_books, get_approx_max_pages
from file_operations import write_data_to_file


def run_scraping(genres: list[str], batch_size: Optional[int] = 60, max_pages: Optional[int] = None):
    """

    :param genres:
    :param batch_size:
    :param max_pages:
    """
    books = {}
    start = datetime.datetime.now()
    variables.TIMESTAMP = start.strftime("%Y-%m-%d_%H-%M-%S")

    # Instantiate multiprocessing pool
    pool = Pool()
    try:
        # iterate over all genres for which to scrape book list from the website
        for genre_i, genre in enumerate(genres):
            print(f"\nScraping Genre {genre_i + 1} of {len(genres)}")
            max_pages_total = get_approx_max_pages(genre, batch_size)
            if max_pages is not None:
                max_pages_to_use = max_pages
                if max_pages > max_pages_total:
                    max_pages_to_use = max_pages_total
            else:
                max_pages_to_use = max_pages_total

            bar = progressbar.ProgressBar(start=0)

            bar.max_value = max_pages_to_use
            pages = [*range(1, max_pages_to_use + 1, 1)]

            j = 0
            starmap_args = [(genre, batch_size, page) for page in pages]
            bar.start()
            for books_list in pool.starmap(get_books, starmap_args):
                if books_list:
                    for book_instance in books_list:
                        if book_instance.identifier not in books:
                            books[book_instance.identifier] = book_instance
                j += 1
                bar.update(j, force=True)
                time.sleep(0.02)
            bar.finish()

        time.sleep(1)
        books = list(books.values())
        print(f"\nFinished getting basic book data for {len(books)} books")

        books = list(tqdm(pool.imap(add_tags_to_book, books), total=len(books),
                          desc="Getting book tags"))
        time.sleep(1)
        books = list(tqdm(pool.imap(add_community_statistics_to_book, books), total=len(books),
                          desc="Getting book community statistics"))

    except Exception as e:
        print(f"{e}")
    finally:
        gc.collect()
        pool.close()
        pool.join()
        end_multiprocessing = datetime.datetime.now()
        print(f"\nCleaned up. Running took {end_multiprocessing - start}")
    return books


if __name__ == "__main__":
    import nltk
    import argparse

    nltk.download('punkt_tab')
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_pages", default=None, type=int)
    parser.add_argument("--genres", default="romantasy,fantasy", help='delimited list input', type=str)
    args = parser.parse_args()

    genres_list = [item.strip() for item in args.genres.split(',')]
    print(f"scraping genres: {genres_list}")

    books = run_scraping(genres=genres_list, max_pages=args.max_pages)
    write_data_to_file(books)
