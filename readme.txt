PythonSearchEngine -  Basic Python Search Engine
This program is developed by Group 15 of COMP4321 for completing the project.

To install necessary library, pip version 24.0 is required. 

For starters, please open the module.py file and download all the necessary libraries described in the file.
Alternatively, open your IDE, copy the commands from module.py and press Enter.

The test program is already built-in. So, please open scraper.py with your IDE and run the python file.
The test results should be available at spider-result.txt.



Database Schema:
1. forward_index(page_id, word_freq)        # word_freq is a dictionary stored in a TEXT format
2. inverted_index(word_id, page_freq)       # page_freq is a dictionary stored in a TEXT format
3. content(page_id, url, pagetitle, last_mod_date, file_size, child_link, parent_link)      # Store all the necessary content
4. urls(url, page_id)           # Mapping Table
5. words(word, word_id)         # Mapping Table

Design:
"forward_index" rows are page-word relationships
"inverted_index" rows are word-page relationships
"content" rows are content of each respective page
"urls" maps URL strings to page IDs
"words" maps tokenized words to IDs

