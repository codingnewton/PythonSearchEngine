# Indexer Database Schema

This document describes the design of the SQLite3 database schema for the indexer. It includes all supporting databases required for forward and inverted indexes, as well as mapping tables for URL <=> page ID and word <=> word ID conversion.

## Database Tables

1. **pages**: This table stores the crawled pages' information, including the page's content.
   - page_id (INTEGER PRIMARY KEY)
   - url (TEXT)
   - content (TEXT)

2. **forward_index**: This table is used for forward indexing and stores the word frequencies for each page.
   - page_id (INTEGER)
   - word_freq (TEXT)

3. **inverted_index**: This table is used for inverted indexing and stores the page frequencies for each word.
   - word_id (INTEGER)
   - page_freq (TEXT)

4. **urls**: This table maps the URLs to page_id for easy access.
   - url (TEXT PRIMARY KEY)
   - page_id (INTEGER)

5. **words**: This table maps the words to word_id for easy access.
   - word (TEXT PRIMARY KEY)
   - word_id (INTEGER)

## Database Operations

1. **dbforward**: Inserts crawled data into the database for forward indexing.
2. **dbinverted**: Calculates the inverted index and puts it into the database.
3. **dbtest**: Retrieves the contents of the db file to display the data stored in the inverted_index table.

## Spider and Test Program

1. **Crawler**: `A.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)`

   This function starts the crawling process at the given URL with a specified maximum number of pages to crawl.

2. **Database Creation**: `A.createdb()`

   This function initializes the database schema by creating all required tables.

3. **Database Operations**: `A.dbforward()`, `A.dbinverted()`, `A.dbtest()`

   These functions handle the insertion and retrieval of data from the database.

4. **Export Results**: `A.export('return')`

   This function exports the crawl results to a text file.

## Execution

To execute the spider and test the program, follow the steps below:

1. Run the crawler with a specified URL and the maximum number of pages to crawl.
2. Initialize the database schema by calling the `createdb()` function.
3. Insert crawled data into the database for forward indexing by calling the `dbforward()` function.
4. Calculate the inverted index and put it into the database by calling the `dbinverted()` function.
5. (Optional) Retrieve the contents of the db file to display the data stored in the inverted_index table by calling the `dbtest()` function.
6. Export the crawl results to a text file by calling the `export('return')` function.

**Note**: The `dbforward()`, `dbinverted()`, and `dbtest()` functions must be executed in the provided order for proper data manipulation.