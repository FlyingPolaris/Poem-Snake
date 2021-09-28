# -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import requests

poem_links = []
for page_num in range(1, 5):
    url = 'https://www.shicimingju.com/chaxun/zuozhe/91_{}.html'.format(
        page_num)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36'}
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.text, "lxml")
    contents = soup.find_all('div', class_="shici_list_main")

    for content in contents:
        links = content.find_all('a')
        for link in links:
            poem_links.append('https://www.shicimingju.com/'+link['href'])

poem_list = []


def get_poem(url):
    # url = 'https://www.shicimingju.com/chaxun/list/48905.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    poem = soup.find_all('div', class_='item_content')[0].text.strip()
    # print(poem)
    poem = poem.encode('ISO-8859-1').decode('utf-8')
    # print(poem)

    poem = poem.replace(' ', '')
    poem = re.sub(re.compile(r"\([\s\S]*?\)"), '', poem)
    poem = re.sub(re.compile(r"（[\s\S]*?）"), '', poem)
    poem = re.sub(re.compile(r"。\([\s\S]*?）"), '', poem)
    poem = poem.replace('!', '！').replace('?', '？').replace(',','，')
    poem_list.append(poem)




executor = ThreadPoolExecutor(max_workers=10)
future_tasks = [executor.submit(get_poem, url) for url in poem_links]
wait(future_tasks, return_when=ALL_COMPLETED)

open('./poem.txt', 'w')
poems = list(set(poem_list))
poems = sorted(poems, key=lambda x: len(x))
for poem in poems:
    poem = poem.replace('《', '').replace('》', '') \
               .replace('：', '').replace('“', '')
    poem = "".join(poem.split())
    # print(poem)
    with open('./poem.txt', 'a', encoding='utf-8') as f:
        f.write(poem)
        f.write('\n')
