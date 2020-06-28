import json
from bs4 import BeautifulSoup
import requests
import re
import xml.etree.ElementTree as ET
import pprint
import boto3
import datetime



def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def get_page(page_address):
    page = requests.get(page_address)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_headlines(soup):
    all_headlines = (soup.find_all('h3'))
    return all_headlines

def main(event, context):
    a = 'https://www.bbc.co.uk/'
    soup = get_page(a)
    main_headline = soup.h3.find('span',class_='top-story__title').text # Creates the first top story
    all_headlines = get_headlines(soup)
    word_list = []
    for i in all_headlines:
        word_list.append(i.text)
    indiv_word_lists = []
    for i in word_list:
        indiv_word_lists.append(i.split())
    individual_words = []
    for i in indiv_word_lists:
        for word in i:
            individual_words.append(word)
    unique_words = set(individual_words)
    dict_file = 'senticnet.xml'
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
    score_dict = [] # Has all the bbc words and scores in it, eventually including the zero words
    zero_words = []
    for i in data_list: # i is the word in the score dictionary
        for ii in unique_words:
            bbc_word = ii
            if bbc_word in i:
                score_dict.append((bbc_word,float(i[1])))
            else:
                zero_words.append(bbc_word)
    total_value_dict = []
    for i in zero_words:
        score_dict.append((i,0))
    for i in score_dict:
        total_value_dict.append(i[1])
    end_score = int(sum(total_value_dict)/len(total_value_dict)*10000000)

    # Put end_score into DynamoDB

    client = boto3.resource('dynamodb')

    # Get the current date and time
    date_now = str(datetime.datetime.now())

    # this will search for dynamoDB table 
    table = client.Table("WordSentiment")

    table.put_item(Item= {'Score': end_score,'Headline':main_headline, 'DateTime': date_now})

    print(end_score)
    #print(ddb_data = json.loads(json.dumps(end_score), parse_float=Decimal))
    return end_score, sum(total_value_dict)/len(total_value_dict)*10000000

if __name__ == "__main__":
    main('', '')
