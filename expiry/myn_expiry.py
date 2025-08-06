import requests
import sys
import random
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import sys
import json
import asyncio
import time
from  furl import furl
import requests
import time
from datetime import datetime


def getdata():
    url = "https://roo.bi/api/automation/v11.1/myn_products/"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    # print(result)
    return result

def get_myntra(link: str) -> dict:
    f=furl(link)
    af_android=f.args.get('af_android_url')
    f1 = furl(af_android)
    print(f1)
    link=f1.remove(['utm_source','utm_medium','utm_campaign']).url
    print('link= ',link)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    src = requests.get(link, headers=headers)
    result = src.content
    soup = BeautifulSoup(result, 'html.parser')
    offer_price = None
    scripts = soup.find_all('script')
    
    for script in scripts:
        if "price" in script.text:
            try:
                json1 = json.loads(script.text.replace("\t", "").replace("\n", ""))
                offer_price = (json1["offers"]["price"])     
            except (json.JSONDecodeError, TypeError):
                continue

    return offer_price
    
def update(pid,oprice):
    url = "https://roo.bi/api/automation/v11.1/price_update/"+pid+"/"+str(oprice)+"/+"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    return response['status']

def expiry(pid):
    url = "https://roo.bi/api/automation/v11.1/exp_update/"+pid+"/"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    return response['status']

if __name__ =='__main__':    
    data = getdata()
    count = len(data)
    print('count=', count)
     
    i = 0
    # count=5
    # while i<count:
    #     link = data[i]['product_url']
    #     print(link)
        # if '/buy' in link:
        #     # print('link =', data[i]['product_url'])
        #     new_off_price = get_myntra(data[i]['product_url'])
        #     old_off_price = int(data[i]['product_offer_price'])
        #     print('new_off_price =', new_off_price)
        #     print('old_off_price =', old_off_price)
        #     if(new_off_price is not None):
        #         new_off_price = int(new_off_price)

        #         if(new_off_price>old_off_price):
        #             print('price chnaged')
        #             # update_status = expiry(data[i]['pid'])
        #             # print('update_status =',update_status)
        #         if(new_off_price<old_off_price):
        #             print('price updated')
        #             # change_status = update(data[i]['pid'],new_off_price)
        #             # print('change_status =',change_status)
        # i = i+1