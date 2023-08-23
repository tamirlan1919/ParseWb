import pandas as pd
import requests
import json
import urllib.parse

def get_category(url,text_to_encode):

 

    urll = text_to_encode

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.by',
        'Referer': f'{url}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }
    # Check if the response contains JSON data
    response = requests.get(url=urll, headers=headers)
    if 'application/json' in response.headers.get('content-type', '').lower():
        # The response contains JSON data, you can access it using response.json()
        json_data = response.json()
        print(json_data)
    else:
        print('No JSON data found in the response.')

    return response.json()

def prepare_items(response):
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'sale': product.get('sale', None),
                'priceU': float(product.get('priceU', None)) / 100 if product.get('priceU', None) != None else None,
                'salePriceU': float(product.get('salePriceU', None)) / 100 if product.get('salePriceU',
                                                                                          None) != None else None,
            })

    return products

def yes(url,text):
        # Check if the request was successful (status code 200)
    response = get_category(url=url,text_to_encode=text)
    products = prepare_items(response)

    pd.DataFrame(products).to_csv('products.csv', index=False)