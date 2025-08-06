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
    url = "https://roo.bi/api/automation/v11.1/fkt_products/"
    payload={}
    headers = {
    'Token': '2304d5f65a9273202dce611154ba0c93'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    return result

def hit_url(link):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    date_time = dt_string
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    payload={}
    headers = {'User-Agent':'PostmanRuntime/7.28.4','Accept':'*/*','Host':'www.flipkart.com','Postman-Token':'af7ecd7f-076c-414f-bf84-c781716cf81d','Accept-Encoding':'gzip, deflate, br','Connection':'Keep-Alive','Cookie': 'K-ACTION=null; SN=VIF84FC67A70384F66B7FBD02EC63BC0ED.TOK79EEBA1CFA654FD181C90D02114F9CA1.'+str(epoch)+'.LO; T=TI169852077651600117861865684816050298814055202201422554557908897094; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFkOTYzYzUwLTM0YjctNDA1OC1iMTNmLWY2NDhiODFjYTBkYSJ9.eyJleHAiOjE3MDAyNDg3NzgsImlhdCI6MTY5ODUyMDc3OCwiaXNzIjoia2V2bGFyIiwianRpIjoiODFiMTE4YzAtNjFmYy00MDIzLTgzOGYtOTBhMWI3YjE3YzE4IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNjk4NTIwNzc2NTE2MDAxMTc4NjE4NjU2ODQ4MTYwNTAyOTg4MTQwNTUyMDIyMDE0MjI1NTQ1NTc5MDg4OTcwOTQiLCJrZXZJZCI6IlZJRjg0RkM2N0E3MDM4NEY2NkI3RkJEMDJFQzYzQkMwRUQiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.mAoMSllxANU5WmJvX7mYhH5_k_jh-ypHaS0Cmccir3c'
    }
    # print(headers)
    response = requests.request("GET", link, headers=headers)
    # print(response.text)
    return response

def get_price(link:str)->tuple:
    retry=True
    if 1: 
        f=furl(link)
        link=f.remove(['affid','affExtParam1','affExtParam2','pwsvid']).url
        print('link= ',link)
        res=hit_url(link)
        soup=BeautifulSoup(res.content,'html.parser')
        dom = etree.HTML(str(soup))
        store=re.search(r'https?://www\.(.+?)\.(?:com|in)', res.url).group(1)
        if(store.lower()=="flipkart"):
            try:
               for a in soup.find_all('div',{'class':'DOjaWF YJG4Cf'}):
                    available=(dom.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[3]/div[2]/text()'))
                    if 'This item is currently out of stock' in available:
                        # tru_val='This item is currently out of stock'
                        return 'not avilable'
                    else:        
                        # offer_val=a.contents[0].text.replace('₹','')
                        # offer_val=int(offer_val.replace(',',''))
                        offer_val= int(soup.find_all('div',{'class':'Nx9bqj CxhGGd'})[0].text.replace('₹','').replace(',',''))
                    retry=False
                    return offer_val
                    
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
    count = len(data)
    i = 0
    # count=1
    while i<count:
        link = data[i]['product_url']
        print(link)
        if '?sid=' not in link:
            # print('link =', data[i]['product_url'])
            new_off_price = get_price(data[i]['product_url'])
            old_off_price = int(data[i]['product_offer_price'])
            print('new_off_price =',new_off_price)
            print('old_off_price =',old_off_price)
            if(new_off_price is not None):
                if(new_off_price!= 'not avilable'):
                    if(new_off_price>old_off_price):
                        print('price changed')
                        # print(data[i]['pid'])
                        # update_status = expiry(data[i]['pid'])
                        # print('update_status =',update_status)
                    if(new_off_price<old_off_price):
                        print('price updated')
                        # change_status = update(data[i]['pid'],new_off_price)
                        # print('change_status =',change_status)
        i = i+1