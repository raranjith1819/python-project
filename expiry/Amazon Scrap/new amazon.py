import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

URL = "https://www.amazon.in/s?i=electronics&bbn=5605728031&rh=n%3A5605728031%2Cp_6%3AA14CZOWI0VEHLG%2Cp_36%3A98000-%2Cp_89%3AAmazfit%7CApple%7CFire-Boltt%7CGIONEE%7CGionee%7CNoise%7COnePlus%7CPTron%7CSamsung%7CTAGG%7CXiaomi%7CZEBRONICS%7CboAt%2Cp_n_pct-off-with-tax%3A2665401031&s=price-asc-rank"
res = requests.get(URL,headers=HEADERS)

soup = BeautifulSoup(res.content, "html.parser")
# print(soup)
all_products=soup.find_all('div',{'class':'s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t1 puis-include-content-margin puis puis-v3gpyfwsnoypgd232yfieockiop s-latency-cf-section s-card-border'})
# print(all_products)
start_link="https://www.amazon.in"
list=[]
links=[]

# Vertical Page

for a in all_products:
    try:
        last_link = a.find('a', {'class': "a-link-normal s-no-outline"}).get('href')
    except:
        last_link = ''

    try:
        name = a.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}).text
    except:
        name = ''
    try:
        price = a.find('span', {'class': "a-price-whole"}).text.replace(',', '').strip()
    except:
        price = ''

    try:
        mrp = a.find('span', {'class': 'a-price a-text-price'}).text.replace(',', '').strip()
    except:
        mrp = ''

    links = start_link + last_link
    list.append({"name": name, "price": price, "mrp": mrp, "link": links})

# Horizontal page

if(len(list) == 0):
    res = requests.get(URL, headers=HEADERS)
    # print(res)
    soup = BeautifulSoup(res.content, "html.parser")
    all_products =soup.find_all('div', {'class': 's-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t1 puis-expand-height puis-include-content-margin puis puis-v3gpyfwsnoypgd232yfieockiop s-latency-cf-section s-card-border'})
    start_link = "https://www.amazon.in"
    for a in all_products:
        try:
            last_link = a.find('a', {'class': "a-link-normal s-no-outline"}).get('href')
        except:
            last_link = ''

        try:
            name = a.find('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'}).text
        except:
            name = ''
        # print(name)
        try:
            price = a.find('span', {'class': "a-price-whole"}).text.replace(',', '').strip()
        except:
            price = ''

        try:
            mrp = a.find('span', {'class': 'a-price a-text-price'}).text[1:].replace(',', '').strip()
        except:
            mrp = ''
        links = start_link + last_link
        list.append({"name": name, "price": price, "mrp": mrp, "link": links})
print(json.dumps(list))
