import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

import chromedriver_binary
from selenium.webdriver.chrome import webdriver

link = 'https://www.myntra.com/myntra-fashion-store?p='



from selenium import webdriver

browser = webdriver.Chrome()
browser.get(link)


def save_checkpoint(data, file_name):
    df = pd.DataFrame(data, columns=['product_name', 'brand_name', 'rating', 'rating_count', 'marked_price',
                                     'discounted_price', 'sizes', 'product_link', 'img_link'])
    df.to_csv("checkpoints/" + file_name, index=False)

    print(file_name + " saved")


data = []

link = 'https://www.myntra.com/myntra-fashion-store?p='

for page in tqdm(range(1, 31)):

    if (page % 100 == 0):
        file_name = str(page) + '.csv'
        save_checkpoint(data, file_name)

        data = []

    try:

        page_link = link + str(page)

        browser.get(page_link)

        browser.execute_script("window.scrollTo(0,1500)")
        time.sleep(.5)

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        for prod in soup.find('ul', class_='results-base').find_all('li', class_='product-base'):

            # Rating Count
            try:
                rating_count = prod.find('div', class_='product-ratingsContainer').find('div',
                                                                                        class_='product-ratingsCount').text[
                               1:].strip()
            except:
                rating_count = 0
            # Rating
            try:
                rating = prod.find('div', class_='product-ratingsContainer').find('span').text.strip()
            except:
                rating = 0
            # Product Link
            try:
                product_link = prod.find('a', target='_blank').get('href').strip()
            except:
                product_link = np.nan
            # Product Size
            try:
                size = []
                for _ in prod.find('div', class_='product-sizeButtonsContaier').find_all('button',
                                                                                         class_='product-sizeButton'):
                    size.append(_.text)
                sizes = ",".join(size)
            except:
                sizes = np.nan
            # Product Image Link
            try:
                img_link = prod.find('img').get('src').strip()
            except:
                img_link = np.nan
                # Brand of the Product
            try:
                brand_name = prod.find('h3').text.strip()
            except:
                brand_name = np.nan
                # Product Name
            try:
                product_name = prod.find('h4').text.strip()
            except:
                product_name = np.nan
                # Product Price
            try:
                if (len(prod.find('div', class_='product-price').find_all('span')) == 1):
                    discounted_price = int(prod.find('div', class_='product-price').find('span').text.strip()[4:])
                    marked_price = int(prod.find('div', class_='product-price').find('span').text.strip()[4:])

                else:
                    discounted_price = int(prod.find('div', class_='product-price').find('span',
                                                                                         class_='product-discountedPrice').text.strip()[
                                           4:])
                    marked_price = int(
                        prod.find('div', class_='product-price').find('span', class_='product-strike').text.strip()[4:])
            except:
                discounted_price = np.nan
                marked_price = np.nan

            data.append([product_name, brand_name, rating, rating_count, marked_price,
                         discounted_price, sizes, product_link, img_link])
    except:
        pass