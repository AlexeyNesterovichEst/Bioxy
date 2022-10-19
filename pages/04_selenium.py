from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-extensions')
options.add_argument('start-maximized')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

total_page = 1
page_size = 10

a_id = []

driver = webdriver.Chrome('chromedriver',options=options)

plasmid = "pqm" #@param {type:"string"}

path_template = 'http://addgene.org/search/catalog/plasmids/?page_number={}&page_size={}&q={}'

for i in range(1,(total_page+1)):
    driver.get(path_template.format(i, page_size,plasmid))
    page = driver.page_source
    for line in page.split('\n'):
        if '<div class="col-xs-10">#' in line:
            line = line.strip()
            ## example: <div class ="col-xs-10" >  # 107251</div>
            id = line.split('#')[1].split('</div>')[0]
            a_id.append(id)
print(a_id[0])
from selenium import webdriver
from bs4 import BeautifulSoup

path_template = 'http://www.addgene.org/{}/sequences/'

path = path_template.format(a_id[0])
driver.get(path)
page = driver.page_source
parser = BeautifulSoup(page, "lxml")
list_of_attributes = {"class": "copy-from form-control"}
tags = parser.findAll('textarea', attrs=list_of_attributes)
for tag in tags:
    tag = tag.text
    lines = tag.split('\n')
    ref = lines[0].strip()
    lines = lines[1:]
    dna = ('').join(lines).strip()
    st.success(dna.upper())
