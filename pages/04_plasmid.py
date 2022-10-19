#https://github.com/wolfgangB33r/ai-text-model-studio/blob/main/src/app.py
import streamlit as st
from bs4 import BeautifulSoup
import requests

a_id = []
plasmid = "pqm"
path_template = "http://addgene.org/search/catalog/plasmids/?page_number=1&page_size=10&q={}"
path = path_template.format(plasmid)
page = requests.get(path)
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
