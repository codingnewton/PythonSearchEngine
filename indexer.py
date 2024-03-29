!python /content/files/Porter.py #use for google colab?
# Import necessary libraries
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from Porter import Porter  # Assuming Porter.py is a custom class for stemming
nltk.download('punkt')  # Download required NLTK resources
nltk.download('stopwords')

# Create an instance of the Porter class for stemming
stemmer = PorterStemmer()

# Open and read the file
file = open('file.txt', encoding='utf8')
read = file.read()
file.seek(0)

# Obtain the number of lines in the file
line = 1
for word in read:
    if word == '\n':
        line += 1
print("Number of lines in the file is: ", line)

# Create a list to store each line in the file as an element of the list
array = []
for i in range(line):
    array.append(file.readline())  

# Tokenization function
def tokenize_words(file_contents):
    result = []  # Result array to store stemmed tokens

    for i in range(len(file_contents)):
        tokenized = file_contents[i].split()  # Tokenize each line
        stemmed_tokens = [stemmer.stem(token) for token in tokenized]  # Apply stemming to each token
        result.append(stemmed_tokens)

    return result

# Create a list to store each line as an element of the list
tokenized_contents = []
for i in range(line):
    check = array[i].lower()
    tokenized_line = tokenize_words([check])[0]
    stemmed_tokens = [stemmer.stem(token) for token in tokenized_line]
    tokenized_contents.append(stemmed_tokens)

punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
for ele in read:
    if ele in punc:
        read = read.replace(ele, " ")

# Convert the text to lowercase for uniformity
read = read.lower()

# Tokenize the text and remove stopwords
text_tokens = word_tokenize(read)
tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
print(tokens_without_sw)

# Define the dictionary to store inverted items
dict = {}

# Iterate over each line and check for the presence of tokens
for i in range(line):
    check = array[i].lower()
    for item in tokens_without_sw:
        if item in check:
            if item not in dict:
                dict[item] = []
            if item in dict:
                dict[item].append(i + 1)

print(dict)

# Open the output file in write mode
with open("output.txt", "w") as file:
    # Iterate over each item in the dictionary
    for item in dict:
        # Write the dictionary key to the file
        file.write(item + "\n")
        # Iterate over each element in the dictionary's key value
        for j in dict[item]:
            file.write(str(j) + "\n")