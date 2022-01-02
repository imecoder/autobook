#!/usr/bin/python
import requests
import json
import os

from mylog import *
import myflag
import myfile
import mynet
import mypayload

session = requests.session()
url_token = 'https://test.api.amadeus.com/v1/security/oauth2/token'
url_flightOffersSearch = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
url_flightOffersSeatMap = 'https://test.api.amadeus.com/v1/shopping/seatmaps'
url_flightOffersPrice = 'https://test.api.amadeus.com/v2/shopping/flight-offers/pricing'
url_flightOffersBook = 'https://test.api.amadeus.com/v1/booking/flight-orders'


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

    payload = mypayload.for_access_token()

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

    payload = mypayload.for_flight_offers_search(book_comp, book_date, book_from, book_to)


    ret, response = mynet.post(session=session, url=url_flightOffersSearch, headers=headers, payload=json.dumps(payload))
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, {}

    try:
        elem = json.loads(response.text)['data'][0]
        data_from = elem['itineraries'][0]['segments'][0]['departure']['iataCode']
        data_to = elem['itineraries'][0]['segments'][0]['arrival']['iataCode']
        data_comp = elem['itineraries'][0]['segments'][0]['carrierCode']
        data_flight = elem['itineraries'][0]['segments'][0]['number']

        if data_comp != book_comp \
            or data_flight != book_flight \
            or data_from != book_from \
            or data_to != book_to :
            logger.warning('未找到航班 [' + book_comp + book_flight + ']')
            return False, {}

    except :
        logger.warning('解析json失败 : ')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, 0

    logger.warning('找到航班 [' + book_comp + book_flight + ']')
    return True, elem


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


def flight_offers_seatmap(access_token, elem) :


    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
    }

    payload = json.dumps(mypayload.for_flight_offers_seatmap(elem))

    ret, response = mynet.post(session=session, url=url_flightOffersSeatMap, headers=headers, payload=payload)
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




def flight_offers_booking(access_token, elem, book_travelers) :


    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
    }

    payload = json.dumps(mypayload.for_flight_offers_booking(elem, book_travelers))



    ret, response = mynet.post(session=session, url=url_flightOffersBook, headers=headers, payload=payload)
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
        book_travelers = book_config["travelers"]

        while True:
            if limit() == True:
                exit(0)

            myflag.set_flag_relogin(False)

            logger.warning("111111111111111111111111111111111111111111")
            ret, access_token = get_access_token()
            if ret == False :
                continue
            logger.warning("2222222222222222222222")

            ret, elem = flight_offers_search(access_token, book_comp, book_flight, book_date, book_from, book_to)
            if ret == False:
                continue
            logger.warning("33333333333333333333")

            ret = flight_offers_seatmap(access_token, elem)
            if ret == False:
                continue
            logger.warning("444444444444444444")

            ret = flight_offers_price(access_token, elem)
            if ret == False:
                continue
            logger.warning("5555555555555555555555")

            ret = flight_offers_booking(access_token, elem, book_travelers)
            if ret == False:
                continue
            logger.warning("666666666666666666666")

            break


        if myflag.get_flag_relogin() == True:
            continue

        break

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
