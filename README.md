# PythonSearchEngine
Python Base Search Engine


To install necessary library, pip version 24.0 is required. 


### Database Schema:
1. pages(page_id, url, content)
2. forward_index(page_id, word_freq)
3. inverted_index(word_id, page_freq)
4. urls(url, page_id)           # Mapping Table
5. words(word_id, word)         # Mapping Table

### Design:
"pages" stores crawled pages content mapped to internal IDs
"forward_index" rows are page-word relationships
"inverted_index" rows are word-page relationships
"urls" maps URL strings to page IDs
"words" maps tokenized words to IDs
