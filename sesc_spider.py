import json
from time import sleep
from urllib.request import urlopen
from selenium import webdriver
from datetime import datetime
import requests
from bs4 import BeautifulSoup, re
from re import compile
from lxml import html
import ssl
import pdb
from tqdm import tqdm


urlApi = 'http://www.cultcampinas.com.br/api/cult'
domain = "https://www.sescsp.org.br"
headers = {'content-type': 'application/json'}

# driver = webdriver.PhantomJS("/Users/brayan/Documents/cultcampinascrawler/cultcampinasCrawler/phantomjs")
# fp = webdriver.FirefoxProfile()
# driver = webdriver.Firefox(firefox_profile=fp)
driver = webdriver.Chrome()
driver.get(domain + "/unidades/16_CAMPINAS#/uaba=programacao")
sleep(5)
hasButton = True

while(hasButton):

    el = driver.find_element_by_class_name("carregar-mais")

    if el.is_displayed():
        el.click()
    else:
        hasButton = False
        # driver.quit()

    sleep(3)



html = driver.page_source
driver.quit()
# page1 = urlopen()
bsObj = BeautifulSoup(html)

print("\n")
print(bsObj.h1)
print("\n")


# links = bsObj.findAll("a", {"href": re.compile("http://www.institutocpfl.org.br/cultura/evento/.*")})
blocks = bsObj.findAll("div", {"class": "block_agenda-container"})

for block in tqdm(blocks):
    try:

        temp = block.findAll("div", {"class": "colocaHover"})
        link = domain + temp[0].a["href"]
        print(link)

        title = temp[0].a.text.replace("\t","").replace("\n", "").lstrip()

        day = re.sub(r'\s', '', temp[1].findAll("span")[0].text)

        date = ""
        if "a" in day:
            date = "INVALID"
            print(day)
            raise ValueError('DIAS INVÁLIDOS')
        else:
            date = "VALID"


        hour = re.sub(r'\s', '', temp[1].findAll("span")[1].text)


        if "Diversos" in hour:
            dateH = "INVALID"
            print(hour)
            raise ValueError('DIAS INVÁLIDOS')
        else:
            dateH = "VALID"

        tempDate = hour.split("às")
        tempDate = tempDate[0].split("h")
        tempDay = tempDate[0]
        tempMinute = "00"
        if len(tempDate) == 2:
            tempMinute = tempDate[1]
            if len(tempMinute) == 0:
                tempMinute = 0

        dayX = day.split("/")
        final_date = datetime(2017, int(dayX[1]), int(dayX[0]), int(tempDay), int(tempMinute))

        context = ssl._create_unverified_context()
        print(link)
        for w in range(5):
            try:
                page2 = urlopen(link, context=context)
            except:
                continue

        page_detail2 = BeautifulSoup(page2.read())
        sleep(1)

        desc = page_detail2.findAll("div", {"class" : "rich_content" })[0].text.replace("\n","").lstrip()
        img = page_detail2.findAll("article", {"class" : "half_content" })[0].img["src"]

        print(title)
        print(day)
        print(hour)
        print(final_date)
        print(desc)
        print(domain + img)
        print("\n")

        data_json = {
            'title': title,
            'date': "[\"" + str(final_date) + "\"]",
            'desc': desc,
            'img': domain + img,
            'link': link,
            'src': 2
        }

        data = json.dumps(data_json)

        # print(data['date'])

        resp = requests.post(urlApi, data=data, headers=headers)
        print(resp)
        print("\n\n")
    except ValueError:
        print("############## ERROR ################## " + str(ValueError))
        print("\n\n")

#
#
#
# for x in range(len(blocks)):
#
#     pageNumber = x + 1
#     page2 = urlopen(domain + "cultura/programacao/page/" + str(pageNumber))
#     page_detail = BeautifulSoup(page2.read())
#
#     links = page_detail.findAll("li", {"class": "event-item"})
#
#     print("page number " + str(pageNumber))
#     for link in links:
#
#         try:
#             print(link.a["href"])
#
#             array = link.a["title"].split("|")
#             dates = re.findall("[0-9][0-9]", array[0])
#             day = dates[0]
#             month = dates[1]
#             hour = re.findall("[0-9][0-9]", array[2])
#             title = array[3]
#             date = datetime(2016, int(month), int(day), int(hour[0]))
#
#             page3 = urlopen(link.a["href"])
#             page_detail3 = BeautifulSoup(page3.read())
#             content = page_detail3.find("section", {"class": "entry"})
#             biggest_p = ""
#             for p in content.findAll("p"):
#                 if len(str(p)) > len(biggest_p) and p.strong == None:
#                     biggest_p = str(p)
#
#             desc = str(re.sub('<[^<]+?>', '', biggest_p))
#             print(date)
#             print(title)
#
#             print(desc)
#
#             print("\n")
#
#             data_json = {
#                 'title': title,
#                 # 'date': "[\"" + str(date) + "\"]",
#                 'date': str(date),
#                 'desc': desc,
#                 'img': page_detail.find("a", {"href" : link.a["href"]}).img["src"],
#                 'link': link.a["href"],
#                 'src': 1
#             }
#
#             data = json.dumps(data_json)
#
#             resp = requests.post(urlApi, data=data, headers=headers)
#
#             print(resp)
#
#             print("\n")
#
#         except:
#             print(" ####### ERROR ##########################")
#             print("\n")
#
