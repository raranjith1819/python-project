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
    url = "https://roo.bi/api/automation/v11.1/ajio_products/"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    # print(result)
    return result

def get_ajio(link:str):
    f=furl(link)
    af_android=f.args.get('redirect')
    f1 = furl(af_android)
    print(f1)
    res=requests.get(link)
    soup=BeautifulSoup(res.content,'html.parser')
    s=soup.find_all('script')
    for script in s:
        try:
            if "price" in script.text:
                json1 = json.loads(script.text.replace("\t", "").replace("\n", ""))
                return int(json1["hasVariant"][0]["offers"]["lowPrice"])
        except Exception as e:
            print(e)
            pass
    
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
    # count = len(data)
    i = 0
    count=10
    while i<count:
        link = data[i]['product_url']
        if '/c/' not in str(link) or '/s/' not in str(link):
            # print('link =', data[i]['product_url'])
            new_off_price = get_ajio(data[i]['product_url'])
            old_off_price = int(data[i]['product_offer_price'])
            print('new_off_price =',new_off_price)
            print('old_off_price =',old_off_price)
            if(new_off_price is not None):
                new_off_price = int(new_off_price)

                if(new_off_price>old_off_price):
                    print('price chnaged')
                    # update_status = expiry(data[i]['pid'])
                    # print('update_status =',update_status)
                if(new_off_price<old_off_price):
                    print('price updated')
                    # change_status = update(data[i]['pid'],new_off_price)
                    # print('change_status =',change_status)

        i = i+1
        