#working without selenium
import requests
from bs4 import BeautifulSoup
path_template = 'http://addgene.org/search/catalog/plasmids/?page_number={}&page_size={}&q={}'
total_page = 1
page_size = 10
plasmid = "pqm"
path = path_template.format(total_page, page_size,plasmid)
page = requests.get(path)
parser = BeautifulSoup(page.text, 'html.parser')
text = str(parser)
print(path_template.format(i, page_size,plasmid))
for line in text.split('\n'):
  if '<div class="col-xs-10">#' in line:
            line = line.strip()
            ## example: <div class ="col-xs-10" >  # 107251</div>
            id = line.split('#')[1].split('</div>')[0]
            a_id.append(id)
print(a_id[0])

path_template = 'http://www.addgene.org/{}/sequences/'

path = path_template.format(a_id[0])
print(path)
driver.get(path)
#page = driver.page_source
#parser = BeautifulSoup(page, "lxml")

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
    print(dna.upper())
