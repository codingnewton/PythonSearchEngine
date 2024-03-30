# PythonSearchEngine
Python Base Search Engine


To install necessary library, pip version 24.0 is required. 


### Database Schema:
1. pages(page_id, url, childlink, parentlink, last....)   # to be created
2. forward_index(page_id, word_freq)   # word_freq is a dictionary stored in a TEXT format
3. inverted_index(word_id, page_freq)   # page_freq is a dictionary stored in a TEXT format
4. urls(url, page_id)           # Mapping Table
5. words(word, word_id)         # Mapping Table

### Design:
"pages" stores crawled pages content mapped to internal IDs
"forward_index" rows are page-word relationships
"inverted_index" rows are word-page relationships
"urls" maps URL strings to page IDs
"words" maps tokenized words to IDs
