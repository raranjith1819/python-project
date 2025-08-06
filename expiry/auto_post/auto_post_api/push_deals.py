import json
import requests
# from functions import *

        

def send_deals_to_api(result):
    """Send the deals data to the API."""
    url = "https://roo.bi/roobai/api/admin/PutData"
    headers = {'Content-Type': 'application/json'}
    
    result1 = json.loads((result))
    buy_price = 0
    sprice = 0
    offerprice =0
    print(result1)

    # print('*********** Unique List Count : ',len(result1),' ************')
    print(f"*********** Unique List Count : {len(result1)} ************", flush=True)
    
  
    if len(result1) > 0:
        for data in result1:
            print(f"*********** {data['buy_title']} ************", flush=True)
            print("================data==============")
            print(data)
            print("================data==============")
            
            # Check if 'buy_price' and 'offerprice' are not None and convert safely
            if data['buy_price'] is not None:
                # 
                try:
                    buy_price = int(data['buy_price'])
                except ValueError:
                    print("Error: 'buy_price' is not a valid integer.")
                    continue  # Skip this iteration if 'buy_price' is invalid
                
                try:
                    offerprice = int(data['offerprice'])
                except ValueError:
                    print("Error: 'offerprice' is not a valid integer.")
                    continue  # Skip this iteration if 'offerprice' is invalid
            else:
                data['buy_price'] = '0'
            
            if data['buy_mrp'] is not None:
                try:
                    if buy_price == int(data['buy_price']):
                        sprice = int(data['mrp']) 
                    else:
                        sprice = int(data['buy_mrp']) 
                except ValueError:
                    sprice=0
                    print("Error: 'buy_mrp' or 'mrp' is not a valid integer.")
                    continue  # Skip this iteration if 'buy_mrp' or 'mrp' is invalid
        
            if sprice != 0:
                percentage = (sprice - (offerprice / sprice)) * 100
            else:
                percentage = 0
                
            # if percentage < 30:
            #     break
            print(f"***********  Percentage : {percentage} ************", flush=True)
            payload = json.dumps({
                    "product_name": data['buy_title'],
                    "product_url": data['convert_url'],
                    "product_description": data['description'],
                    "product_image": data['buy_img'],
                    "product_sale_price": sprice,
                    "product_offer_price": offerprice,
                    "deal_type": "1",
                    "admin_name": data['source'],
                    "date_time": "2",
                    "product_store": data['store_sid'],
                    "device_type": "web",
                    "product_coupon": data['coupon'],
                    "catagory": data['category'],
                    "subcatagory": data['subcategory'],
                    "device_ip": "10.200.00.0",
                    "product_variation_url": "",
                    "product_variation_url1": "",
                    "product_variation_url2": ""
            })
            # print("================payload==============")
            
            # print(payload)
            # print("================payload==============")
            
            
            try:
                response = requests.post(url, headers=headers, data=payload)
                response.raise_for_status()
                value = response.text.encode().decode('utf-8-sig')
                json_object = json.loads(value)
                print(json_object)
                print(json_object['message'])
            except Exception as e:
                print(f"Failed to send deal to API: {str(e)}")

