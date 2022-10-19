#https://github.com/wolfgangB33r/ai-text-model-studio/blob/main/src/app.py
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import os
import pickle
import base64
#text libraries
import re
from time import time  # To time our operations

from gensim.models import Word2Vec

# used for text scraping
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

def inject(tag):
    with open(os.path.dirname(st.__file__) + "/static/index.html", 'r') as file:
        str = file.read()
        if str.find(tag) == -1:
            idx = str.index('<head>')
            new_str = str[:idx] + tag + str[idx:]
            with open(os.path.dirname(st.__file__) + "/static/index.html", 'w') as file:
                file.write(new_str)

st.session_state['stopwords'] = {'also', 'often', 'may', 'use', 'within', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'} 
st.session_state['ignore_stop_words'] = True

def text_to_words(raw_text, remove_stopwords=True):
    # 1. Remove non-letters, but including numbers
    letters_only = re.sub("[^0-9a-zA-Z]", " ", raw_text)
    # 2. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    if remove_stopwords:
        stops = st.session_state['stopwords'] # In Python, searching a set is much faster than searching
        meaningful_words = [w for w in words if not w in stops] # Remove stop words
        words = meaningful_words
    return words 

def extract_visible_text(soup):
    result = []
    visible_text = soup.getText()
    sentences = visible_text.splitlines()
    for sentence in sentences:
        words = text_to_words(sentence, remove_stopwords=st.session_state['ignore_stop_words'])
        if len(words) > 5:
            result.append(words)
    return result

def fill_scrape_stats(url, result):
    word_count = 0
    char_count = 0
    for s in result:
        word_count = word_count + len(s)
        for w in s:
            char_count = char_count + len(w)
    if 'url_scrape_stats' in st.session_state:
        print({'Url' : url, 'Characters' : char_count, 'Words' : word_count, 'Sentences' : len(result)})
        st.session_state['url_scrape_stats'].append({'Url' : url, 'Characters' : char_count, 'Words' : word_count, 'Sentences' : len(result)})
        
a_id = []
page = requests.get("http://addgene.org/search/catalog/plasmids/?page_number=1&page_size=10&q=pqm")
parser = BeautifulSoup(page.text, 'html.parser')
text = str(parser)
#st.success(text)
for line in text.split('\n'):
    if '<div class="col-xs-10">#' in line:
       line = line.strip()
       ## example: <div class ="col-xs-10" >  # 107251</div>
       id = line.split('#')[1].split('</div>')[0]
       a_id.append(id)
st.success(a_id[0])
path_template = 'http://www.addgene.org/{}/sequences/'
path = path_template.format(a_id[0])
page = requests.get(path)
parser = BeautifulSoup(page.text, 'html.parser')
list_of_attributes = {"class": "copy-from form-control"}
tags = parser.findAll('textarea', attrs=list_of_attributes)
for tag in tags:
    tag = tag.text
    lines = tag.split('\n')
    ref = lines[0].strip()
    lines = lines[1:]
    dna = ('').join(lines).strip()
    st.success(dna.upper())
