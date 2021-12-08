#!/usr/bin/python
import sys
import time
import requests
import threadpool
import urllib3
import json
import os

from mylog import *
import myflag
import myfile
import mynet


session = requests.session()
url_token = 'https://api.amadeus.com/v1/security/oauth2/token'
url_flightOffersSearch = 'https://api.amadeus.com/v2/shopping/flight-offers'
url_flightOffersPrice = 'https://api.amadeus.com/v2/shopping/flight-offers/pricing'
url_flightOffersBook = 'https://api.amadeus.com/v1/security/oauth2/token'


ret, base_config = myfile.read_json('config.base.json')
if ret == False:
    exit(0)

ret, book_config_list = myfile.read_json('config.book.json')
if ret == False:
    exit(0)

def limit():
    # 2021-11-20 00:00 我是
    # pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-12-30 00:00', '%Y-%m-%d %H:%M'):
        logger.warning('试用期限已到...')
        return True
    return False



def get_access_token() :

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    payload = "grant_type=client_credentials&client_id=te8ZC3BmobVE8DYpJck8s1Isvx73FZ7m&client_secret=SkdB6l1jU1UK7j0Z"

    ret, response = mynet.post(session=session, url=url_token, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    try:
        access_token = json.loads(response.text)['access_token']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('access_token = ' + access_token)

    return True, access_token



def flight_offers_search(access_token, book_comp, book_flight, book_date, book_from, book_to) :

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
    }

    payload = {
        "currencyCode": "USD",
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": book_from,
                "destinationLocationCode": book_to,
                "departureDateTimeRange": {
                    "date": book_date
                }
            }
        ],
        "travelers": [
            {
                "id": "1",
                "travelerType": "ADULT"
            }
        ],
        "sources": [
            "GDS"
        ],
        "searchCriteria": {
            "maxFlightOffers": 3,
            "flightFilters": {
                "carrierRestrictions": {
                    "includedCarrierCodes": [book_comp]
                }
            }
        }
    }


    ret, response = mynet.post(session=session, url=url_flightOffersSearch, headers=headers, payload=json.dumps(payload))
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, {}

    try:
        json_reponse = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, {}


    if "data" not in json_reponse :
        logger.warning(sys._getframe().f_code.co_name + ' 返回信息有误 .')
        return False, {}

    try :
        data = json_reponse['data']

        for elem in data :
            data_from = elem['itineraries'][0]['segments'][0]['departure']['iataCode']
            data_to = elem['itineraries'][0]['segments'][0]['arrival']['iataCode']
            data_comp = elem['itineraries'][0]['segments'][0]['carrierCode']
            data_flight = elem['itineraries'][0]['segments'][0]['number']

            if data_comp != book_comp \
                or data_flight != book_flight \
                or data_from != book_from \
                or data_to != book_to :
                continue

            return True, elem

    except :
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, 0


    return False, 0



def flight_offers_price(access_token, elem) :


    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
    }

    payload = json.dumps(elem)

    ret, response = mynet.post(session=session, url=url_flightOffersPrice, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False
    #
    # try:
    #     access_token = json.loads(response.text)['access_token']
    # except json.decoder.JSONDecodeError as e:
    #     logger.warning('解析json失败 : ' + str(e))
    #     logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
    #     return False, ''
    #
    # logger.warning('access_token = ' + access_token)

    return True













def quick_prebook(book_comp, book_flight, book_space, book_date, book_from, book_to):
    logger.warning('航班 [' + book_comp + book_flight + '] 执行快速预订')

    quick_booking_cmd = 'SS ' + book_comp + book_flight + ' ' + book_space + ' ' + book_date + ' ' + book_from + book_to + ' NN1'

    return True



def auto_book(sessionid):

    name = book_config['user'].strip('N.').replace('/', '')
    id = msg['text'].split('\n')[0].split('/')[0]
    logger.warning('存档 : ' + name + '-' + id)
    myfile.save(name + '-' + id, msg['text'])
    logger.warning('订票存档成功 !!!')
    os.system(r'start /b BookInfo.exe')

    return True



def main():
    pass


if __name__ == '__main__':

    branch_size = base_config['branch_size']

    for book_config in book_config_list:

        logger.warning('')
        logger.warning('')
        logger.warning('开始订票 = ' + json.dumps(book_config))

        book_date = book_config["date"]
        book_from = book_config["from"]
        book_to = book_config["to"]
        book_comp = book_config["comp"]
        book_flight = book_config["flight"]
        book_space = book_config["space"][0]
        book_user = book_config["user"]
        book_contact = book_config["contact"]
        book_email = book_config["email"]

        while True:
            if limit() == True:
                exit(0)

            myflag.set_flag_relogin(False)

            ret, access_token = get_access_token()
            if ret == False :
                continue

            ret, elem = flight_offers_search(access_token, book_comp, book_flight, book_date, book_from, book_to)
            if ret == False:
                continue

            ret = flight_offers_price(access_token, elem)
            if ret == False:
                continue

            break


        ret = quick_prebook(book_comp, book_flight, book_space, book_date, book_from, book_to)
        if ret == False :
            continue

        if myflag.get_flag_relogin() == True:
            continue

        break

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
