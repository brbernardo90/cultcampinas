import json
from urllib.request import urlopen

from datetime import datetime
import requests
from bs4 import BeautifulSoup, re
from re import compile
from lxml import html
from tqdm import tqdm

def get_desc(html):

    desc = [x for x in html if len(x) > 1][2:]

    return "".join(desc)

def get_date(html):

    regex = compile(r"[0-9][0-9]")
    date = [int(x) for x in regex.findall(str(html))]

    return datetime(2017, date[1], date[0], date[-2], date[-1])

urlApi = 'http://www.cultcampinas.com.br/api/cult'
domain = "http://miscampinas.com.br/"
headers = {'content-type': 'application/json'}
page1 = urlopen(domain + "atv_mes_abril-2017.htm")
bsObj = BeautifulSoup(page1.read())

print("\n")
print(bsObj.h1)
print("\n")

links = bsObj.findAll("a", {"href": re.compile(".*.htm")})
for link in tqdm(links):
    try:
        print(link)

        page2 = urlopen(domain + link["href"])
        page_detail = BeautifulSoup(page2.read())
        print("Titulo: "+ page_detail.h1.text)
        print("Imagem: "+ page_detail.find("img", {"alt" : page_detail.h1.text})["src"])
        desc = get_desc(html.fromstring(str(page_detail)).xpath("//div[@id='conteudo_total']/div[4]/div[2]/div[3]/table/tr/td[2]/text()"))
        date = get_date(html.fromstring(str(page_detail)).xpath("//div[@id='conteudo_total']/div[4]/div[2]/div[2]/text()"))
        # print("Desc: "+ tree)

        print("\n")

        data_json = {
            'title': page_detail.h1.text,
            'date': "[\"" + str(date) + "\"]",
            'desc': desc,
            'img': page_detail.find("img", {"alt": page_detail.h1.text})["src"],
            'link': domain + link["href"],
            'src': 3
        }

        data = json.dumps(data_json)

        requests.post(urlApi, data=data, headers=headers)

    except :
        print("====> ERRO : ")



