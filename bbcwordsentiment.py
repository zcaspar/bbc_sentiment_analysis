import spacy #Load the language
# Install bs4: sudo apt-get install python3-bs4
nlp = spacy.load('en_core_web_lg') # Use the following to install from command line: python3 -m spacy download en_core_web_lg
# Change the below to the location of the dictionary file
dict_file = '/home/caspar/Documents/Data Science/bbc_sentiment_analysis/senticnet.xml'

from bs4 import BeautifulSoup
import requests
import json

# Use this to compare how long code takes

def time_execution(code):
    start = time.clock()
    code_part = eval('code')
    stop = time.clock()
    run_time = stop - start
    return run_time

# A container for Spacy to analyse sentiment
sentiment_words = []

# Word identified that I don't want to be included
stop_words = []

a = 'https://www.bbc.co.uk/news'

def get_page(page_address):
    page = requests.get(a)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_headlines(soup):
    all_headlines = soup.find_all(['h1','h2','h3','h4','h5'])
    return all_headlines


# Get full page html

soup = get_page(a)

# Get the headlines including html tags

all_headlines = get_headlines(soup)

# Get just a list of headline strings

headline_list = []
for i in all_headlines:
    if i.text not in headline_list and (i.text != ''):
        headline_list.append(i.text)
        
# Remove BBC links
headline_list = headline_list[5:]


# Remove stop words and punctuation and put remaining words in sentiment_words

# Create a list of individual words in headline and put into this:
individualized_headline_words = []

for headline in headline_list:
    doc = nlp(headline)
    individualized_headline_words.append(headline.split())
    sentiment_words.append([token.lemma_ for token in doc if not token.is_stop if not token.lemma_ in stop_words if token.is_punct == False])

# Create a large list for all words in all headlines
all_words = [] # e.f. ['virus', 'update', 'UK', 'world', 'live']

# Now populate this list
for headline in sentiment_words:
    for word in headline:
        all_words.append(word)

# Define a dictionary file with word sentiments
import xml.etree.ElementTree as ET
import pprint

tree = ET.parse(dict_file)
root = tree.getroot()

i = 0
data=[] # Data holds a tuple of the word and then its score
while i < len(root):
    data.append((root[i][1].text,root[i][2].text))
    i+=1

data_list = list(data)
# data_list contains ('word,'0.1') this is the one with the score
# unique_words ('word','word') this is taken from the bbc

### Convert data_list to a dictionary

polarity_dictionary = {}

for i in data_list:
    key_word = i[0]
    polarity_value = i[1]
    polarity_dictionary[key_word] = float(polarity_value)

score_dict = [] # Has all the bbc words and scores in the format [('Saturday', 0.935),('abuse', -0.684)]
zero_words = [] # Has all the words without a polarity rating as a list of strings ['virus','update','UK']

for bbc_word in all_words:
    if bbc_word in polarity_dictionary:
        score_dict.append(polarity_dictionary[bbc_word])
    else:
        zero_words.append(bbc_word)

    # Takes a python dictionary and turns it into a json file

def dict_to_json(dict,file_name):
    # dict should be a python dictionary and file_name in the format "my_file.json",
    # which will be created when function is run.
    a_file = open(file_name, "w")
    json.dump(dict, a_file, sort_keys=True, indent=4, separators=(',', ': '))
    a_file.close()

# Takes a json file and turns it into a pythong dictionary

def json_to_dic(file_name):
    with open('try_it.json', 'r') as f:
        this_dict = json.load(f)
    return this_dict
   
result = round((sum(score_dict)/len(score_dict)),2)

# Get polarity score for individual headline

#NEW
# Add headline score to a list
# last_serial contains the last serial no. in the dictionary
# Opening JSON file


with open('/home/caspar/Documents/Data Science/bbc_sentiment_analysis/headline_scores.json') as json_file: 
    data = json.load(json_file) 

counter = 0
for i in reversed(data):
    while counter < 1:
        last_serial = int(i)
        counter += 1


headline_score = 0
#serial_no = 0
new_headline_list = []
headline_dict = {} #json_to_dic('/home/caspar/Documents/Data Science/bbc_sentiment_analysis/headline_scores.json')


#start the count at the end of the last dictionary
headline_counter = int(last_serial)
# Get the current date and time

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

for headline in headline_list:
    # Check if headline is already in the headline_list
    if headline not in new_headline_list:
        # Add headline score to a list
        single_word_sentiment = []
        for bbc_word in headline.split():
            if bbc_word in polarity_dictionary:
                single_word_sentiment.append(polarity_dictionary[bbc_word])
        if len(single_word_sentiment) > 0:
            headline_score = round(sum(single_word_sentiment)/len(single_word_sentiment),2)
        else:
            headline_score = 0
        new_headline_list.append((headline_list[headline_counter-int(last_serial)],headline_score))
        headline_dict[headline_counter+1] = (new_headline_list[headline_counter-int(last_serial)],dt_string,headline_score,0)
        headline_counter += 1
        last_serial += 1
'''
OLD
# Add headline score to a list
headline_score = 0
new_headline_list = []
headline_dict = {}
headline_counter = 0
for headline in individualized_headline_words:
    # Add headline to a list

    # Add headline score to a list
    single_word_sentiment = []
    for bbc_word in headline:
        if bbc_word in polarity_dictionary:
            single_word_sentiment.append(polarity_dictionary[bbc_word])
    if len(single_word_sentiment) > 0:
        headline_score = round(sum(single_word_sentiment)/len(single_word_sentiment),2)
    else:
        headline_score = 0
    new_headline_list.append((headline,headline_score))
    headline_dict[headline_counter] = (headline,headline_score)
    headline_counter += 1
'''
dict_to_json(headline_dict,'/home/caspar/Documents/Data Science/bbc_sentiment_analysis/headline_scores.json')

print(result)