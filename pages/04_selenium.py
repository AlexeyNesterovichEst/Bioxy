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
