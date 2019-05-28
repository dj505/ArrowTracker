import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import json

def replace_diff(diff):
    diff = diff.split('_')
    if diff[0] == 'single':
        diff[0] = 'S'
    elif diff[0] == 'double':
        diff[0] = 'D'
    elif diff[0] == 'half-double':
        diff[0] = 'HD'
    elif diff[0] == 'douper':
        diff[0] = 'DP'
    elif diff[0] == 'sinper':
        diff[0] = 'SP'
    elif diff[0] == 'co-op':
        diff[0] = 'Co-Op'
    elif diff[0] == 'routine':
        diff[0] = 'RT'
    if diff[1].startswith('lv0'):
        diff[1] = diff[1][3:4]
    else:
        diff[1] = diff[1][2:4]
    diff = f"{diff[0]}{diff[1]}"
    return diff

pumpouturl = f"https://pumpout.anyhowstep.com/search/results?display=song"
page = requests.get(pumpouturl)
pumpout = BeautifulSoup(page.text, 'html.parser')
for match in pumpout.find_all('section', class_='main padder'):
    totalsongs = int(match.find('div', class_='text-center').contents[-1].strip().split(' ')[1])
    print(f'Total songs: {totalsongs}')

totalpages = totalsongs // 20
print(f'Total pages: {totalpages}')
pagenum = 1
id = 0
data = {}

while pagenum <= totalpages:
    pumpouturl = f"https://pumpout.anyhowstep.com/search/results?display=song&page={pagenum}"
    page = requests.get(pumpouturl)
    pumpout = BeautifulSoup(page.text, 'html.parser')
    for match in pumpout.find_all('div', class_='list-group-item'):
        song = match.a.div.find('div', class_='media-body').contents[0].strip()
        data[song] = {}
        data[song]['author'] = match.a.div.find('div', class_='media-body').find('span', class_='label bg-primary').text
        data[song]['bpm'] = re.sub(r'\s+', ' ', match.a.div.find('div', class_='hidden-lg').div.span.text.strip())
        data[song]['length'] = match.a.div.find('div', class_='media-body').find('div', class_='hidden-lg').div.find('span', class_='badge bg-inverse').text
        data[song]['genre'] = match.a.div.find('div', class_='media-body').find('div', class_='hidden-lg').div.find('span', class_='badge bg-success').text
        data[song]['id'] = f'{id}'
        thumburl = 'https://pumpout.anyhowstep.com' + match.a.div.find('img', class_='thumb-large')['src']
        urllib.request.urlretrieve(thumburl, f'app/static/songthumbs/{id}.png')
        difflist = []
        for diff in match.a.div.find('div', class_='shift').find_all('img'):
            diff = diff['src'].split('/')[-1].replace('half_double', 'half-double')
            diff = replace_diff(diff)
            difflist.append(diff)
            data[song]['difficulties'] = difflist
        id = id + 1
    print(f'Scraped page {pagenum}')
    pagenum += 1

with open('app/static/gamelists/Pump it Up/complete.json', 'w') as f:
    json.dump(data, f, indent=2)
