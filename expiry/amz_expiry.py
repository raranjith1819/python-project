import requests
import sys
import random
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import json
import asyncio
import time
from  furl import furl
import requests
import time
from datetime import datetime

def getdata():
    url = "https://roo.bi/api/automation/v11.1/amz_products/"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    return result

def get_amazon(link: str):
    f = furl(link)
    link = f.remove(['tag', 'linkCode', 'th', 'psc']).url
    print('link =', link)
    return link

def get_pid(url):
    if 'amazon.in' in url:
        pid = re.search(r'/(?:dp|product)/(\w+)', url).group(1)
        pos = '63'
        store = 'amazon'
    result = {'pid': pid, 'pos': pos, 'store': store}
    return result

def get_interpid(pos, pid):
    url = f"https://buyhatke.com/api/productData?pos={pos}&pid={pid}"
    response = requests.get(url)
    final = response.json()
    internalPid = final['data']['internalPid']
    title = re.sub(r'(-)\1+', r'\1', re.sub(r'[^a-z0-9\-]', '-', final['data']['name'].lower()))
    result = {'internalPid': internalPid, 'title': title}
    return result

def final_data(store, title, pos, internalPid):
    url = f"https://buyhatke.com/{store}-{title}-price-in-india-{pos}-{internalPid}/__data.json?x-sveltekit-invalidated=001"
    response = requests.get(url)
    final = response.json()
    # print(url)

    for item in final['nodes'][2]['data']:
        if isinstance(item, str) and '2024' in item:
            line = item
            last_star_index = line.rfind('*')
            date_price_str_modified = line[:last_star_index]
            date_price_list = date_price_str_modified.split("~")
            prices = date_price_list[1::3]
            if prices:
                last_value = prices[-1]
                return last_value

def update(pid, oprice):
    url = "https://roo.bi/api/automation/v11.1/price_update/"+pid+"/"+str(oprice)+"/+"

    headers = {
        'Token': ''
    }
    response = requests.get(url, headers=headers)
    response = response.json()
    return response['status']

def expiry(pid):
    url = "https://roo.bi/api/automation/v11.1/exp_update/"+pid+"/"
    headers = {
        'Token': ''
    }
    response = requests.get(url, headers=headers)
    response = response.json()
    return response['status']

if __name__ == '__main__':
    data = getdata()
    data_length = len(data)
    # print(data_length)
    i = 0
    count=3
    while i < data_length:
        link = data[i]['product_url']
        # print(link)
        if 'dp/' in link:
            old_off_price = int(data[i]['product_offer_price'])
            proUrl = get_amazon(data[i]['product_url'])
            data_pid = get_pid(proUrl)
            data1 = get_interpid(data_pid['pos'], data_pid['pid'])
            new_off_price = final_data(data_pid['store'], data1['title'], data_pid['pos'], data1['internalPid'])           
            new_off_price = int(new_off_price)          
            print('new_off_price =', new_off_price)
            print('old_off_price =', old_off_price)
            if new_off_price is not None:
                if new_off_price > old_off_price:
                    print('price changed')
                    update_status = expiry(data[i]['pid'])
                    print('update_status =', update_status)
                if new_off_price < old_off_price:
                    print('price updated')
                    change_status = update(data[i]['pid'], new_off_price)
                    print('change_status =', change_status)
        i =i+ 1