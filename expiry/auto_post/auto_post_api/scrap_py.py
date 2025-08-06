from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from scrap_py import *
import regex as re
import json
from functions import *
from findsimilarity import *
import time
from push_deals import *
import datetime
import pytz

# from earnpe import *

app = FastAPI()
class post_item(BaseModel):
    link : str
    auth: str

class post_url(BaseModel):
    link : str
    subid: str
class url_link(BaseModel):
    url : str
    subid: Optional[str]
class admit_web(BaseModel):
    offset : str
#start of Decorato

#start of Decorators
#When you hit the address http://127.0.0.1:8000/ This will return {"Hello": "World"}  as dict 
@app.get("/")
def carrotgreetings():
    return "Hello! Thangal roobai ku varugai thanthamaiku nandri"

@app.get("/auto_post/")
def get_url():

    urls = [
        'https://www.dealsmagnet.com/new',
        'https://www.desidime.com/new',
        'https://indiadesire.com/lootdeals'
    ]

    i = 0

    while True:
        start_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        
        # print('========== ',(i+1),' Job Run Started| ',start_time,' ==========')
        print(f"========== {(i+1)} Job Run Started| {start_time} ==========", flush=True)
        all_data = []
    
        dealsmagnet_arr = dealsmagnet_fetch_deals(urls[0])
        
        desidime_arr = desidime_fetch_deals(urls[1])
            
        indiadesire_arr = indiadesire_fetch_deals(urls[2])
        
        # Combine all website datas
        all_data.extend(dealsmagnet_arr)
        all_data.extend(desidime_arr)
        all_data.extend(indiadesire_arr)   


        result = json.dumps(all_data, indent=4)

        #similarity
        unique_list = process_deals(all_data)
        
        send_deals_to_api(unique_list)
        end_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        elapsed_time = (end_time - start_time)  # this is a timedelta object
        elapsed_seconds = elapsed_time.total_seconds() # convert timedelta to seconds
        print('========== ',(i+1),' Job Run Completed| ',start_time,' ==========')
        i += 1
        # print('elapsed_time= ',elapsed_time)

        if elapsed_seconds < 60:
            wait_time = 60 - elapsed_seconds
            print(f'========== Wait Time {wait_time:.2f} seconds ==========')
            time.sleep(wait_time)