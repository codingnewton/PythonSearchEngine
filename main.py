import scraper as sp

spider = sp.HTML_list()
spider.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)      # recursively crawl the pages

db_filename = 'indexer.db'          # Specify the name of the db file you have/ you will create
spider.createdb(db_filename)        # Create the .db file for storing pages newly fetched pages OR Clean an existing .db file to store newly fetched pages.
spider.dbforward(db_filename)       # Inserting data into table {urls, forward_index, content}
spider.dbinverted(db_filename)      # Calculate inverted index and insert data into table {words, inverted_index}

# spider.dbtest(db_filename, tablename = 'words')   # Retrieve and print contents of table "words" from db file

spider.export(mode = 'return')             # Create spider-result.txt by mode = 'return' (mode='print' will print the results instead)
