import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
url='https://www.amazon.in/s?k=laptops&crid=15QJ5Z8EK4Z67&sprefix=laptops%2Caps%2C268&ref=nb_sb_noss_1'

start_link='https://www.amazon.in'

response = requests.get(url,headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')
NAME=[]
PRICE=[]
RATING=[]
MRP=[]
Links=[]

product=soup.find_all('div',{"class":"s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border"})


#print(product)
for a in product:
    last_link=a.find('a')['href']
    Links.append(start_link+last_link)
    name=a.find('span',{"class":"a-size-medium a-color-base a-text-normal"})
    price=a.find('span',{"class":"a-price-whole"})
    mrp=a.find('span',{"class":"a-price a-text-price"})
    rating= a.find("span", {'class': 'a-icon-alt'})

    NAME.append(name.text)
    PRICE.append(price.text.replace(',', '').strip())
    MRP.append(mrp.text[1:].replace(',','').strip())
    RATING.append(rating.text)



d= ({'NAMES': NAME,'PRICES': PRICE,'Mrp':MRP,'Rating':RATING,'Links':Links})
df=pd.DataFrame.from_dict(d,orient='index')
print(df)
df = df.transpose()

df.to_csv('a.csv', index=False, encoding='utf-8')



