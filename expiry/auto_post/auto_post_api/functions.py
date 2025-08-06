from itertools import count
from bs4 import BeautifulSoup
import requests
from unshortenit import UnshortenIt
from urllib.parse import urlparse, parse_qs
import re
import json
import requests
from requests.exceptions import HTTPError
# from push_deals import *

def unshorturl(url):
    """Unshorten a URL using the UnshortenIt library."""
    unshortener = UnshortenIt()
    return unshortener.unshorten(url)

def process_deal(title, price, mrp, store, link1, image, coupon, source, deals):
    """Process the deal by sending it to the API and appending the enriched data to the deals list."""

    # print('LInk===>  ',link1)

    url = "https://roo.bi/roobai/api/admin/adminurl"
    payload = json.dumps({
        "adminname": "bot",
        "url": link1
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        value = response.text.encode().decode('utf-8-sig')
        json_object = json.loads(value)

        # Extract data from the JSON response
        new_title = json_object['result']['product_name']
        new_offprice = json_object['result']['bhknow']
        new_mrp = json_object['result']['bhkmax']
        new_avg = json_object['result']['bhkavg']
        img = json_object['result']['product_image']
        p_url=json_object['result']['product_url']
        category=json_object['result']['catagory']
        subcategory=json_object['result']['subcatagory']
        description=json_object['result']['product_description']
        store_sid=json_object['result']['product_store']

        if new_offprice is not None:
            new_offprice = float(new_offprice)
        # print('type= ',type(new_offprice))

        if store.lower() in ['amazon', 'flipkart', 'myntra', 'ajio', 'boat']: 
            deal = {
                "title": title,
                "offerprice": price,
                "mrp": mrp,
                "store": store,
                "url": link1,
                "image": image,
                "coupon": coupon,
                "source": source,
                "buy_title": new_title,
                "buy_price": new_offprice,
                "buy_mrp": new_mrp,
                "buy_avg": new_avg,
                "buy_img": img,
                "convert_url": p_url,
                "category": category,
                "subcategory": subcategory,
                "description": description,
                "store_sid": store_sid
            }

            # Append the deal to the deals list
            # print(deal)
            # print("===================== Deals ===================")
            # print(deal)
            # print("===================== Deals ===================")
            deals.append(deal)

        else:
            return('Invalid Store')

    except HTTPError as e:
        # print(payload)
        print(f"HTTPError occurred: {e.response.status_code} - {e.response.text}")
        return(f"HTTPError occurred: {e.response.status_code}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return deals

def dealsmagnet_fetch_deals(url):
    
    with open('titles.json', 'r') as file: 
        data = json.load(file)

    last_product = data['dealsmagnet']
    print("""Scrape Deals From Dealsmagnet Started""")
    print("Last Product Name: ",last_product)
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    products = soup.find_all('div', {'class': 'col-lg-3 col-md-4 col-sm-6 col-6 pl-1 pr-1 pb-2'})
    deals = []
    i=1
    count=0
    for product in products:
                
        if i>5:
            break
        
        try:
            title = product.find('p', {'class': 'card-text mb-1 font-weight-bold'}).text.strip()
        except AttributeError:
            title = ''
        if (title == last_product):
            break     
            
        if count==0:
            data['dealsmagnet'] = title
            with open('titles.json', 'w') as file: 
                json.dump(data, file) 
                count+=1
                
        # print(i,'. ',title)
      
        print(f"========== {i} . {title} ==========", flush=True)

        try:
            price = product.find('div', {'class': 'col-12 p-0 card-DealPrice'}).text.replace('₹', '').strip()
        except AttributeError:
            price = '0'
            
        try:
            mrp = product.find('div', {'class': 'col-12 card-OriginalPrice p-0 d-inline m-0'}).text.replace('₹', '').strip()
        except AttributeError:
            mrp = '0'
            
        try:
            image = product.find('img', {'class': 'lazy card-img-top'}).get('data-src')
        except AttributeError:
            image = ''   
             
        try:
            div_element = product.find('div', {'class': 'col-5 p-0 pt-1 bg-white rounded text-center mt-1'})
            if div_element:
                img_tag = div_element.find('img')
                if img_tag and 'alt' in img_tag.attrs:
                    store = img_tag['alt']
        except AttributeError:
            store = ''
            
        try:
            code = product.find('button', {'class': 'btn buy-button btn-primary btn-sm'}).get('data-code')
        except AttributeError:
            code = ''
            
        if not code:
            try:
                scrap_url = product.find('p', attrs={'class':'card-text mb-1 font-weight-bold'}).a['href']
            except:
                scrap_url = ''    

            res = requests.get(scrap_url)
            soup1 = BeautifulSoup(res.content, "html.parser")

            try:
                code = soup1.find('button', {'class': 'btn buy-button col-12 btn-md btn-primary BuyNowButton d-block m-0 rounded pl-4 pr-4'}).get('data-code')
            except AttributeError:
                code = ''
            
        con_url = "https://www.dealsmagnet.com/buy?"
        link = unshorturl(con_url + code).replace('/dealsmagnet.com/', '/') 

        if 'ww44.affinit' in link:
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            link = query_params.get('d', [None])[0]
        
        if 'linkredirect' in link:
            captured_value = urlparse(link)
            dict_result = parse_qs(captured_value.query)
            link1 = unshorturl(dict_result['dl'][0])
        else:
            link1 = link

        if '/s?' in link1:
            # print(link1)

            break


        try:
            coupon = product.find('div', {'class': 'Ribbon'}).text.strip()
        except AttributeError:
            coupon = ''

        result = process_deal(title, price, mrp, store, link1, image, coupon, "bot_dm", deals)
        if 'HTTPError occurred' not in result:
            if 'Invalid Store' not in result:
            # print("====================== ",i,' ================')
            # print(result)
                i+= 1

    print("""Scrape Deals From Dealsmagnet Ended""")
    return deals

def desidime_fetch_deals(url):
    
    with open('titles.json', 'r') as file: 
        data = json.load(file)

    last_product = data['desidime']
        
    print("""Scrape Deals From Desidime Started""")
    print("Last Product Name: ",last_product)
    
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    products = soup.find_all('div', {'class': 'grid-80 tablet-grid-75 pad-left20'})
    deals = []
    i=1
    count=0
    for a in products:
        
        if i>5:
            break
        
        try:
            title = a.find('div', attrs={'class': 'l-deal-dsp bold'}).text.replace('\n', '').strip()
        except AttributeError:
            title = ''

        if (title == last_product):
            break     
            
        if count==0:
            data['desidime'] = title
            with open('titles.json', 'w') as file: 
                json.dump(data, file) 
                count+=1
                
        print(i,'. ',title)
        
        try:
            link = a.find('a', attrs={'class': 'continuelink'}).get('href')
        except AttributeError:
            link = ''

        try:
            store = a.find('div', attrs={'class': 'plr10'}).text.replace('\n', '').strip()
        except AttributeError:
            store = '' 

        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")

        try:
            image = soup1.find('a', attrs={'class':"dealpromoimage p15 tc"}).img['data-src']
        except AttributeError:
            image = ''  

        try:
            link1 = unshorturl(soup1.find('a', attrs={'class': 'buy_now_tag btn-buynow gtm-buynow-tag-top'}).get('href'))
        except AttributeError:
            link1 = ''

        if '/s?' in link1:
            # print(link1)

            break
    
        try:
            price = soup1.find('div', attrs={'class': 'dealprice'}).find('span').text
        except AttributeError:
            price = ''

        try:
            mrp = soup1.find('span', attrs={'class': 'line-through'}).text.replace('.0', '').strip()
        except AttributeError:
            mrp = ''

        result = process_deal(title, price, mrp, store, link1, image, "", "bot_dd", deals)
        
        if 'HTTPError occurred' not in result:
            if 'Invalid Store' not in result:
            # print("====================== ",i,' ================')
            # print(result)
                i+= 1
        
    print("""Scrape Deals From Desidime Ended""")
    return deals


def indiadesire_fetch_deals(url):
    
    with open('titles.json', 'r') as file: 
        data = json.load(file)

    last_product = data['indiadesire']
    
    print("""Scrape Deals From IndiaDesire Started""")
    print("Last Product Name: ",last_product)
    
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    products = soup.find_all('div', {'class': 'boxcard boxcard-root boxcard-rounded innerpadding'})

    flag = 1
    deals = []
    count = 0

    for a in products:
        if flag > 5:
            break

        try:
            title1 = a.find('a', attrs={'class': 'anchor'}).text.replace('\n', '')
            title = re.sub(r'\[.*?Coupon\]:|\[Use Code - .*?\]', '', title1).strip()
        except AttributeError:
            title = ''
            
        if count==0:
            data['indiadesire'] = title
            with open('titles.json', 'w') as file: 
                json.dump(data, file) 
                count+=1
            

        if last_product in title:
            break
        
        print(flag,'. ',title)
        
        try:
            store = a.find('img', attrs={'class': 'imgleft'}).get('title', '')
        except AttributeError:
            store = ''

        # Initialize link1 before conditional logic
        link1 = ''
        try:
            link2 = a.find('a', attrs={'class': 'myButton'}).get('href', '')
            # print('link2===>  ',link2)
            captured_value = parse_qs(urlparse(link2).query)
            # print('captured_value===>  ',captured_value)
            # print('redirect=>',captured_value['redirect'])
            final_url = captured_value.get('redirect', [''])[0].replace("https://indiadesire.com/Redirect?redirect", "")
          
            if "pid1=" in final_url and "flipkart" in store:
                link1 = ("https://www.flipkart.com/flipkart/p/item?" + final_url).replace("pid1", "pid").replace("&indiadesire=","&=")

            elif "sid" in final_url:
                link1 = link2.replace("https://indiadesire.com/Redirect?redirect=", "").replace("&indiadesire=","&=")

            elif "pid1=" in final_url and "amazon" in store:
                link1 = ("https://www.amazon.in/dp/" + final_url).replace("pid1=", "")
            elif "myntra" in store:
                # link1 = ("https://www.myntra.com/a/b/c/" + final_url + "/buy?").replace("pid1=", "")
                link1 = link2.replace("https://indiadesire.com/Redirect?redirect=", "")
            elif "ajio" in store:
                # link1 = ("https://www.ajio.com/p/" + final_url).replace("pid1=", "")
                link1 = link2.replace("https://indiadesire.com/Redirect?redirect=", "")
        except AttributeError:
            link1 = ''

            # print('link1=====>  ',link1)
            
        if '/s?' in link1:
            # print(link1)

            break
        
        try:
            coupons = re.search(r'\[([^]]+)\]', title)
            coupon = coupons.group(1).replace("\u20b9","").replace('Use Code - ','')
        except AttributeError:
            coupon = ''

        try:
            price = a.find('div', attrs={'class': 'cprice'}).text.replace('₹', '').strip()
        except AttributeError:
            price = ''

        try:
            mrp = a.find('div', attrs={'class': 'oprice'}).text.replace('₹', '').strip()
        except AttributeError:
            mrp = ''
        
        try:
            image = a.find('img', attrs={'class': 'lazyload'}).get('data-src')
        except:    
            image = ''
        result = process_deal(title, price, mrp, store, link1, image, coupon, "bot_id", deals)
        
        if 'HTTPError occurred' not in result:
            # print(result)
            if 'Invalid Store' not in result:
                flag += 1
        
    print("""Scrape Deals From IndiaDesire Ended""")
    return deals

