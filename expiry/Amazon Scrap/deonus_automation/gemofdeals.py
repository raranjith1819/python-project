from bs4 import BeautifulSoup
import requests
import json
import re
from unshortenit import UnshortenIt

def unshorturl(url):
    unshortener = UnshortenIt()
    uri = unshortener.unshorten(url)
    return uri

url ='https://www.gemofdeals.com/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)

products = soup.find_all('div',{'class':'comp-kxp1flyr1 YzqVVZ wixui-repeater__item'})
list=[]
flag=1
for a in products:
    try:
        title=a.find('a',attrs={'target':'_blank'}).text
    except:
        title=''
    try:
        mrp = a.find("del").text.replace('$', '').strip()
    except:
        mrp=''
    try:
        price = a.find("b").text.replace('$', '').strip()
    except:
        price=''
    try:
        link=a.find('a',attrs={'class':'StylableButton2545352419__root style-lhr8vxgq__root wixui-button StylableButton2545352419__link'}).get('href')
    except:
        link=''
    res1 = requests.get(link)
    soup1 = BeautifulSoup(res1.content, 'html.parser')

    try:
        coupons=soup1.find('p',attrs={'style':'color:black; font-size:15px;'})
        coupons1 = re.findall(r"<b>[A-Z0-9]+</b>", str(coupons))
        coupons2 = str(coupons1).replace("'<b>", "")
        coupon = str(coupons2)[1:-1].replace("</b>'", "")
    except:
        coupon=''
    # print(coupon)

    try:
        link1=unshorturl(soup1.find('a',attrs={'class':'StylableButton2545352419__root style-ky8cdwff1__root wixui-button StylableButton2545352419__link'}).get('href'))
    except:
        link1=''
    # print(link1)

    try:
        store=a.find('span',attrs={'class':'color_18 wixui-rich-text__text'}).text
    except:
        store=''
    # print(store)
    if (store =='Amazon'):
        list.append({"title":title,"offerprice": price, "mrp": mrp, "url": store, "url ": link1,"Coupons":coupon,"source":"gemofdeals"})

    flag = flag + 1
    if (flag > 5):
        break





