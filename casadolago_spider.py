import json
import os
from time import sleep
from urllib.request import urlopen
from selenium import webdriver
from datetime import datetime
import requests
from bs4 import BeautifulSoup, re
from parse import parse
from re import compile
# from lxml import html
from selenium.webdriver import DesiredCapabilities
import pdb

def return_json(title, dayMonth, hourMinute, desc, img, domain, pageUrl):
    data_json = {
        'title': title,
        'date': "[\"" + str(datetime(2016, int(dayMonth[1]), int(dayMonth[0]), int(hourMinute[0]))) + "\",\"" + str(
            datetime(datetime.now().year, int(dayMonth[1]), int(dayMonth[0]), int(hourMinute[2]))) + "\"]",
        'desc': desc,
        'img': img,
        'link': domain + pageUrl,
        'src': 4,
        'location': "-22.8123378,-47.0709872",
        'place': "Casa do Lago"
    }

    return json.dumps(data_json)

urlApi = 'http://www.cultcampinas.com.br/api/cult'
domain = "http://www.casadolago.preac.unicamp.br"
pageUrl = "/?p=9763"
headers = {'content-type': 'application/json'}

# try:

page1 = urlopen(domain + pageUrl)
bsPage1 = BeautifulSoup(page1.read())

print("\n")
print(bsPage1.h1)
print("\n")

html = bsPage1.findAll("article", {"class": "post"})[0]
htmlText = html.text.replace("\n","")


regexDesc = compile(r'(<b>|<strong>)(Sinopse):(</b>|</strong>)(.+)')
arrayDesc = regexDesc.findall(str(bsPage1))

regexTitle = compile(r'(<strong>Título: </strong>|<strong>Título</strong>:)(.+)(<br/>)')
arrayTitle = regexTitle.findall(str(bsPage1))

regexHour = compile(r'(<strong>Horário das sessões</strong>:)(.+)(<br/>)')
arrayHour = regexHour.findall(str(bsPage1))

regexDate = compile(r'<strong>(SEGUNDA-FEIRA|TERÇA-FEIRA|QUARTA-FEIRA|QUINTA-FEIRA|SEXTA-FEIRA)(.+)</strong>')
arrayDate = regexDate.findall(str(bsPage1))

arrayImg = re.findall("src=\"(.*?.jpg)\"", str(html))
arrayImg = arrayImg[1:]

size = len(arrayTitle)

for x in range(len(arrayTitle)):

    try:

        title = arrayTitle[x][1].strip()

        desc = arrayDesc[x][-1].strip()

        img = arrayImg[x]

        dayMonth = re.findall("[0-9]{2}", arrayDate[x][1])

        hourMinute = re.findall("[0-9]{2}", arrayHour[x][1])

        data = return_json(title, dayMonth, hourMinute, desc, img, domain, pageUrl)

        print(data + "\n\n")

        requests.post(urlApi, data=data, headers=headers)


    except Exception:
        pdb.post_mortem()
        print("ERROR\n")

