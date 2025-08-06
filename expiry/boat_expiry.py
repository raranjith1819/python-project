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
    url = "https://roo.bi/api/automation/v11.1/boat_products/"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()

    # result_link=result.product_url
    # print(result)
    return result

def get_boat(link:str):
    f=furl(link)
    link=f.remove(['pid','offer_id','sub1','sub2','ref_id']).url
    print('link= ',link)
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(link, headers=headers)
    soup=BeautifulSoup(response.content,'html.parser')
  
    price_span = soup.find('span', class_='price--highlight')
    if price_span:
        try:
            price = price_span.text.strip().replace("Sale price₹",'').replace(',','')
        except:
            price=''
        return int(price)
    
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
    i = 0
    # count=1
    while i<count:
        link = data[i]['product_url']
        if '/collections/' not in link:
            # print('link =', data[i]['product_url'])
            new_off_price = get_boat(data[i]['product_url'])
            old_off_price = int(data[i]['product_offer_price'])
            print('new_off_price =',new_off_price)
            print('old_off_price =',old_off_price)
            if(new_off_price is not None):
                if(new_off_price>old_off_price):
                    print('price chnaged')
                    update_status = expiry(data[i]['pid'])
                    print('update_status =',update_status)
                if(new_off_price<old_off_price):
                    print('price updated')
                    change_status = update(data[i]['pid'],new_off_price)
                    print('change_status =',change_status)
        i = i+1