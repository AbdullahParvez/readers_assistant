import csv
import json

import requests
from bs4 import BeautifulSoup
import subprocess
from kanji.models import Kanji, Radical

def run():


    # kanji = '年'
    # command = 'cd scripts/kanjiVG/; python kvg-lookup.py find-svg '+kanji
    # ret = subprocess.run(command, capture_output=True, shell=True)
    # print(ret.stdout.decode())
    # result = ret.stdout.decode().split('\n')
    # print(result)
    # parts = []
    # for r in result:
    #     # print(r)
    #     part=None
    #     if 'group' in r or '(right)' in r:
    #         if '(left)' in r or '(right)' in r:
    #             # print(r.split('group '))
    #             right = r.split('group ')[-1]
    #             part = right.split(' ')[0]
    #         if '(' not in r:
    #             # print(r.split('group '))
    #             part = r.split('group ')[-1]
    #     if part and part not in parts:
    #         if Kanji.objects.filter(kanji=part).exists() or Radical.objects.filter(radical=part).exists():
    #             parts.append(part)
    # print(parts)

    kanjis = Kanji.objects.all()
    kanji_dic = {}
    for k in kanjis:
        kanji = k.kanji
        # kanji = '験'
        command = 'cd scripts/kanjiVG/; python kvg-lookup.py find-svg '+kanji
        ret = subprocess.run(command, capture_output=True, shell=True)
        result = ret.stdout.decode().split('\n')
        # print(result)
        parts = []
        for r in result:
            # print(r)
            part=None
            if 'group' in r or '(right)' in r:
                if '(left)' in r or '(right)' in r:
                    right = r.split('group ')[-1]
                    part = right.split(' ')[0]
                if '(' not in r:
                    # print(r.split('group '))
                    part = r.split('group ')[-1]
            if part and part not in parts:
                if Kanji.objects.filter(kanji=part).exists() or Radical.objects.filter(radical=part).exists():
                    parts.append(part)
        print(parts)
        kanji_dic[kanji] = parts

    json_object = json.dumps([kanji_dic], indent=4, ensure_ascii=False)
    # # Writing to sample.json
    with open("scripts/kanjivg_kanji_parts.json", "w") as outfile:
        outfile.write(json_object)


    # URL = "http://kanjivg.tagaini.net/viewer.html?kanji=験"
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, "html.parser")
    # # print(soup)
    # results = soup.find(id="group-images")
    # group_image = results.find_all("div", class_="group_image")
    # print(group_image)
    # kanjis = Kanji.objects.all()
    # kanji_dic = {}
    # for k in kanjis:
    #     kanji = k.kanji
    #     URL = "http://kanjivg.tagaini.net/viewer.html?kanji=験"
    #     page = requests.get(URL)
    #     soup = BeautifulSoup(page.content, "html.parser")
    #     # group_image = soup.find_all("div", class_="group_image")
    #     results = soup.find(id="group-image")
    #     print(results)
    #     # URL = "https://jisho.org/search/"+kanji+"%20%23kanji"
        # page = requests.get(URL)

        # soup = BeautifulSoup(page.content, "html.parser")

        # results = soup.find_all("dt", string=lambda text: "parts" in text.lower())
        # kanji_parts = [result.parent for result in results]
        # temp_part = []
        # for kanji_div in kanji_parts:
        #     # print(kanji_div)
        #     # links = kanji_div.getElementsByTagName("dd")
        #     # for l in links:
        #     links = kanji_div.find_all('a')
        #     # print(links)
            
        #     for link in links:
        #         temp_part.append(link.text.strip())
        #         # print(link.text.strip())
        # kanji_dic[k.kanji] = temp_part

        #     print(l.innerText)
    # for result in results:
    #     python_jobs = result.find("dt", string="Parts")
    #     print(python_jobs)
    #     if python_jobs:
    #         links = python_jobs.find('a')
    #         print(links)

    # print(kanji_dic)

    # json_object = json.dumps([kanji_dic], indent=4, ensure_ascii=False)
    

    # # # Writing to sample.json
    # with open("scripts/kanji_parts.json", "w") as outfile:
    #     outfile.write(json_object)
