import copy
import csv
import requests
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# set number of laptops on one page
PAGE_SIZE = 20
# set max page or parse all pages with float('inf')
MAX_PAGE = 1

cookies = {
    'MVID_CITY_ID': 'CityCZ_975',
    'MVID_REGION_ID': '1',
    'MVID_REGION_SHOP': 'S002',
    'MVID_TIMEZONE_OFFSET': '3',
}

GET_VIDEOCARD_IDS_URL = (
    'https://www.mvideo.ru/bff/products/listing'
    '?categoryId=5429'
    '&offset={}'
    '&limit={}'
    '&filterParams=WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ%3D%3D'
    '&doTranslit=true'
)
GET_VIDEOCARDS_DETAILS_URL = 'https://www.mvideo.ru/bff/product-details/list'
GET_VIDEOCARD_DETAILS_JSON_BODY = {
    "productIds": [],
    "mediaTypes": ["images"],
    "category": True,
    "status": True,
    "brand": True,
    "propertyTypes": ["KEY"],
    "propertiesConfig": {"propertiesPortionSize": 5},
    "multioffer": False
}
GET_VIDEOCARDS_PRICES_URL = (
    'https://www.mvideo.ru/bff/products/prices'
    '?productIds={}'
    '&addBonusRubles=true'
    '&isPromoApplied=true'
)

def parse_videocards(url):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    parsed_info = {}
    PAGE_COUNTER = 0

    while PAGE_COUNTER < MAX_PAGE:
        logger.info(f'started parsing laptops page №{PAGE_COUNTER}')

        # get page <PAGE_COUNTER> laptop ids
        videocard_ids = requests.get(
            GET_VIDEOCARD_IDS_URL.format(PAGE_COUNTER * PAGE_SIZE, PAGE_SIZE),
            headers={'User-Agent': 'Mozilla/5.0 (U; Linux x86_64) Gecko/20100101 Firefox/69.6'},
            cookies=cookies,
        ).json()['body']['products']
        logger.info('laptops ids parsed')

        # get all laptop details
        json_body = copy.deepcopy(GET_VIDEOCARD_DETAILS_JSON_BODY)
        json_body['productIds'] = videocard_ids
        videocards_details = requests.post(
            GET_VIDEOCARDS_DETAILS_URL,
            json=json_body,
            headers={
                'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118?from=under_search',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            },
            cookies=cookies,
        ).json()
        logger.info('laptops details parsed')

        # parse collected laptops details
        for videocard in videocards_details['body']['products']:
            parsed_info[videocard['productId']] = {
                'id': videocard['productId'],
                'name': videocard['name'],
                'rating': videocard['rating']['star'],
                'review_count': videocard['rating']['count']
            }

        # Get all laptop prices
        videocards_prices = requests.get(
            GET_VIDEOCARDS_PRICES_URL.format(','.join(videocard_ids)),
            headers={
                'referer': 'https://www.mvideo.ru/komputernye-komplektuushhie-5427/videokarty-5429',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            },
            cookies=cookies,
        ).json()
        logger.info('laptops prices parsed')

        #parse collected laptops prices
        for videocard in videocards_prices['body']['materialPrices']:
            parsed_info[videocard['productId']]['base_price'] = videocard['price']['basePrice']
            parsed_info[videocard['productId']]['sale_price'] = videocard['price']['salePrice']

        PAGE_COUNTER += 1

    return parsed_info
@app.route('/parse', methods=['GET'])
def parse():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL is not provided'}), 400

    parsed_info = parse_videocards(url)
    return jsonify(parsed_info)

if __name__ == '__main__':
    app.run(debug=True)