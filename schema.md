# Indexer Database Schema

This document describes the design of the SQLite3 database schema for the indexer. It includes all supporting databases required for forward and inverted indexes, a table for pages content, as well as mapping tables for URL <=> page ID and word <=> word ID conversion. All the database operations were defined within the `HTML_list` class in the python file of `scraper.py`.

## Prerequisites

- Make sure you have Python 3 installed on your system.
- Install the required libraries by running the command mentioned in readme at python terminal.

## Database Tables

1. **forward_index**: This table is used for forward indexing and stores the word frequencies for each page.
   - page_id (INTEGER)
   - word_freq (TEXT)

2. **inverted_index**: This table is used for inverted indexing and stores the page frequencies for each word.
   - word_id (INTEGER)
   - page_freq (TEXT)

3. **forward_title_index**: This table is used for forward indexing of *page title* and stores the word frequencies for each *page title*.
   - page_id (INTEGER)
   - word_freq (TEXT)

4. **inverted_title_index**: This table is used for inverted indexing of *page title* and stores the page frequencies for each word.
   - word_id (INTEGER)
   - page_freq (TEXT)

5. **content**: This table is for storing content of pages.
   - page_id (INTEGER)
   - url (TEXT)
   - pagetitle (TEXT)
   - last_mod_date (DATETIME)
   - file_size (INTEGER)
   - child_link (TEXT)
   - parent_link (TEXT)

6. **urls**: This table maps the URLs to page_id for easy access.
   - url (TEXT PRIMARY KEY)
   - page_id (INTEGER)

7. **words**: This table maps the words to word_id for easy access.
   - word (TEXT PRIMARY KEY)
   - word_id (INTEGER)

## Database Operations

1. **createdb**: Create the .db file for storing pages newly fetched pages OR Clean an existing .db file to store newly fetched pages.
2. **dbforward**: Inserts crawled data into the database for forward indexing.
3. **dbinverted**: Calculates the inverted index and puts it into the database.

## Spider and Test Program

1. **Crawler**: `spider.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)`

   This function starts the crawling process at the given URL with a specified maximum number of pages to crawl.

2. **Database Creation**: `spider.createdb()`

   This function initializes the database schema by creating all required tables.

3. **Database Operations**: `spider.dbforward()`, `spider.dbinverted()`, `spider.dbtest()`

   These functions handle the insertion and retrieval of data from the database.

4. **Export Results**: `spider.export('return')`

   This function exports the crawl results to a text file.

## The Test Program

1. You may paste the following code to an empty python file within this program to test the database:

  ```python
  from scraper import HTML_list
  
  def main():
      # Initialize the HTML_list object
      spider = HTML_list()
  
      # Start the web crawling process
      spider.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)
  
      filename = "indexertest.db"
  
      # Create the SQLite database
      spider.createdb(filename)
  
      # Perform forward indexing
      spider.dbforward(filename)
  
      # Perform inverted indexing
      spider.dbinverted(filename)

      # Retrieve content of the database table
      spider.dbtest(filename, tablename)
  
      # Export the search results to a text file
      spider.export('return')
  
  if __name__ == "__main__":
      main()
  ```

## Execution

The spider (test program) was executed according to the following steps.

1. Run the crawler with a specified URL and the maximum number of pages to crawl.
2. Initialize the database schema by calling the `createdb()` function.
3. Insert crawled data into the database for forward indexing by calling the `dbforward()` function.
4. Calculate the inverted index and put it into the database by calling the `dbinverted()` function.
5. (Optional) Retrieve the contents of the db file to display the data stored in the inverted_index table by calling the `dbtest()` function.
6. Export the crawl results to a text file by calling the `export('return')` function.

**Note**: The `dbforward()`, `dbinverted()`, and `dbtest()` functions must be executed in the provided order for proper data manipulation.

---

## Indexing

As the database structure and the functions were not defined with a class of itself, which enables us to embed more functionality within the class type we defined when handling database data. That includes calculation cosine similarity and extracting relevant pages based on users' queries input in the search engine.
The functions are as follow:

- `HTML_list.queryretrieve()` - Retrieve the inverted index of query terms from database file and output a 2D array ready for cosine similarity processing
- `HTML_list.vector_space()` - Generate Vector Space for both pages' bodies and titles
- `HTML_list.cossim()` - Calculating the cosine similarity between each page and the query
- **`HTML_list.retrieve()`** - Calculating the similarity score of related pages and query based on cosine similarity and tf/idf. This is a function enclosing all the three functions mentioned above

The function `HTML_list.retrieve()` will be utilized in the main.py for search engine.