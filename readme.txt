PythonSearchEngine -  Basic Python Search Engine
This program is developed by Group 15 of COMP4321 for completing the project.
This readme serves as a introduction of setup and run our spider program.
===============================================================================
Dependencies:

We have the following libraries installed:
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    import io
    import sqlite3
    import json
    import datetime
    import dateutil.parser
    import copy

So, to ensure proper execution, we recommend installing the following package by running the following code:

pip install nltk
pip install sqlite3
pip install urllib
pip install bs4

Copy the code above and run it on local IDE should resolve the issue

OR go to modules.py and run the code listed there
======================================================================================
Running the program

1. Going to main.py and run Python main.py on your IDE terminal to execute the spider program.
2. Then check the "search" result on spider-result.txt
======================================================================================
That's it, we hope you have a pleasant experience using our program :)
And please give us a better rating
