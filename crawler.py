import requests
from bs4 import BeautifulSoup
import numpy as np
from kss import split_sentences
import pandas as pd
from konlpy.tag import Okt

def get_nate_links(page_num = 5):
    links = []

    #page number
    for i in range(1, page_num+1):
        res = requests.get("https://pann.nate.com/talk/c20001?page=" + str(i))
        if res.status_code != 200:
            continue
        res.encoding = None
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        link_list = soup.find('div',{'class':'posting_wrap'}).findAll('td', {'class':'subject'})

        for ll in link_list:
            link = ll.find('a')
            links.append('https://pann.nate.com' + link.get('href'))


    return links

def get_nate_content(links):
    contents = []
    okt = Okt()
    for link in links:
        res = requests.get(link)
        if res.status_code != 200:
            continue
        res.encoding = None
        html = res.text
        soup = BeautifulSoup(html,'html.parser')

        content_html = soup.find('div', {'id':'contentArea'})
        if content_html == None:
            continue
        content_string = split_sentences(content_html.text.strip())

        for str in content_string:
            string = str[:]
            string = string.split('\n')
            for s in string:
                s= okt.normalize(s)
                contents.append(s)


    return contents


def get_ruliweb_links(page_num = 5):
    links = []

    #page number
    for i in range(1, page_num+1):
        res = requests.get("https://bbs.ruliweb.com/community/board/300143?cate=519&page=" + str(i))
        if res.status_code != 200:
            continue
        res.encoding = None
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        link_list = soup.find('table', {'class':'board_list_table'}).findAll(lambda tag : tag.name == 'tr' and
                                                                              tag.get('class')==['table_body'])

        for ll in link_list:
            link = ll.find('a', {'class':'deco'})
            links.append(link.get('href'))


    return links

def get_ruliweb_content(links):
    contents = []
    okt = Okt()
    for link in links:
        res = requests.get(link)
        if res.status_code != 200:
            continue
        res.encoding = None
        html = res.content.decode('utf-8','replace')
        soup = BeautifulSoup(html,'html.parser')

        content_html = soup.find('div', {'class':'view_content'})
        if content_html == None:
            continue
        content_string = split_sentences(content_html.text.strip())
        for str in content_string:
            string = str[:]
            string = string.split('\n')
            for s in string:
                s = okt.normalize(s)
                contents.append(s)

    return contents

def create_csv(drop_len = 2,path='data.csv', page_num = 3):
    ruliweb_links = get_ruliweb_links(page_num)
    ruliweb_contents = get_ruliweb_content(ruliweb_links)

    nate_links = get_nate_links(page_num)
    nate_contents = get_nate_content(nate_links)

    contents_list = []
    contents_list.extend(ruliweb_contents)
    contents_list.extend(nate_contents)

    contents={'content': contents_list}

    data =pd.DataFrame(contents)
    data = data.drop(data[data.content.str.len() <drop_len].index)
    data = data.reset_index(drop=True)
    data["label"] = np.nan

    data.to_csv(path, index=False,encoding="utf-8-sig")
    total_data = data.shape[0]

    return total_data
