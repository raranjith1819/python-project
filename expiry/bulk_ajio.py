import requests
from bs4 import BeautifulSoup
import json
from  furl import furl
from  urllib import parse

def add_affli_ajio(urls:str,param1:str,param2:str):
    # url_re_dict={}
    # f=furl(urls)
    # con_url=f.remove(['pid','offer_id','ref_id','sub1','utm_source','utm_medium','utm_campaign','gclid','pwsvid']).add(args={'utm_source':'earnpe','utm_medium':'affiliate','utm_campaign':param2})
    # return con_url


    f=furl(urls)
    con_url=f.remove(['utm_source','utm_medium','utm_campaign','gclid','pwsvid'])
    con_url  = parse.quote(str(con_url),safe='')
    con_url_final=f'https://tracking.ajio.business/click?pid=20&offer_id=2&sub1={param2}&sub2={param2}&redirect={con_url}'
    return con_url_final
    

    

def get_price_ajio_bulk(link:str):
    link_conv = add_affli_ajio(link,'TLBR1','website')
    # return {'title':'', 'offer_price':'', 'mrp':'', 'url':str(link_conv), 'image':''}
    res=requests.get(link)
    soup=BeautifulSoup(res.content,'html.parser')
    s=soup.find_all('script',type="application/ld+json")[-1]
    json_content = s.string
    data = json.loads(json_content)
    url = data['itemListElement'][0]['url']
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    s=soup.find_all('script')
    for script in s:
        try:
            if "price" in script.text:
                json1 = json.loads(script.text.replace("\t", "").replace("\n", ""))
                link_conv = add_affli_ajio(link,'TLBR1','website')
                return {'title':json1["name"], 'offer_price':str(json1["hasVariant"][0]["offers"]["lowPrice"]), 'mrp':str(json1["hasVariant"][0]["offers"]["highPrice"]), 'url':str(link_conv), 'image':json1["image"]}
        except Exception as e:
            print(e)
            pass

def get_price_ajio(link:str):
    res=requests.get(link)
    soup=BeautifulSoup(res.content,'html.parser')
    s=soup.find_all('script')
    for script in s:
        try:
            if "price" in script.text:
                json1 = json.loads(script.text.replace("\t", "").replace("\n", ""))
                link_conv = add_affli_ajio(link,'TLBR1','website')
                return {'title':json1["name"], 'offer_price':str(json1["hasVariant"][0]["offers"]["lowPrice"]), 'mrp':str(json1["hasVariant"][0]["offers"]["highPrice"]), 'url':str(link_conv), 'image':json1["image"]}
        except Exception as e:
            print(e)
            pass

if __name__ =='__main__':
    link='https://www.ajio.com/men-jackets-coats/c/830216010'
    if '/c/' in link or '/s/' in link:
        d=get_price_ajio_bulk(link)
    else:
        d=get_price_ajio(link) 
    print(d)