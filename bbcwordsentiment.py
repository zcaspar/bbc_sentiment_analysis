
# coding: utf-8

# In[429]:


from bs4 import BeautifulSoup
import requests
import re


# In[430]:


a = 'https://www.bbc.co.uk/'


# In[ ]:


def get_page(page_address):
    page = requests.get(a)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


# In[432]:


soup = get_page(a)


# In[640]:


print(soup.h3.find('span',class_='top-story__title').text) #Prints the first top story


# In[691]:


def get_headlines(soup):
    all_headlines = (soup.find_all('h3'))
    return all_headlines


# In[692]:


all_headlines = get_headlines(soup)


# In[642]:


word_list = []
for i in all_headlines:
    word_list.append(i.text)


# In[643]:


indiv_word_lists = []
for i in word_list:
    indiv_word_lists.append(i.split())


# In[694]:


individual_words = []
for i in indiv_word_lists:
    for word in i:
        individual_words.append(word)


# In[646]:


unique_words = set(individual_words)


# In[701]:


dict_file = 'senticnet.xml'


# In[702]:


import xml.etree.ElementTree as ET
import pprint


# In[703]:


tree = ET.parse(dict_file)


# In[704]:


root = tree.getroot()


# In[705]:


i = 0
data=[] # Data holds a tuple of the word and then its score
while i < len(root):
    data.append((root[i][1].text,root[i][2].text))
    i+=1


# In[706]:


data_list = list(data)
# data_list contains ('word,'0.1') this is the one with the score
# unique_words ('word','word') this is taken from the bbc


# In[596]:


#for i in data_list:
    #print('December' in i)


# In[690]:


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
print(sum(total_value_dict)/len(total_value_dict)*10000000)

