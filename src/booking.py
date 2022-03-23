#!/usr/bin/python
import sys

import requests
import json
import os

import threadpool

from mylog import *
import myflag
import myfile
import mynet
import mypayload
import mylimit

session = requests.session()

ret, base_config = myfile.read_json('config.base.json')
if ret == False:
    exit(0)

ret, book_config_list = myfile.read_json('config.book.json')
if ret == False:
    exit(0)

def get_access_token() :
    url_token = 'https://test.api.amadeus.com/v1/security/oauth2/token'

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


def Airline_Code_Lookup(access_token) :

    url_Airline_Code_Lookup = 'https://test.api.amadeus.com/v1/reference-data/airlines'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
    }

    payload = mypayload.for_Airline_Code_Lookup()


    ret, response = mynet.post(session=session, url=url_Airline_Code_Lookup, headers=headers, payload=json.dumps(payload))
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



def flight_offers_search(access_token, book_comp, book_flight, book_date, book_from, book_to) :

    url_flightOffersSearch = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

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

    url_flightOffersPrice = 'https://test.api.amadeus.com/v1/shopping/flight-offers/pricing'

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

    url_flightOffersSeatMap = 'https://test.api.amadeus.com/v1/shopping/seatmaps'

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

    url_flightOffersBook = 'https://test.api.amadeus.com/v1/booking/flight-orders'

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


def booking(blist):
    print("-----------------")
    # print(blist["access_token"])
    # print(blist["flight_offers"])
    # print(blist["book_travelers"])
    # return
    # start = time.time()
    while True:
        ret = flight_offers_booking(blist["access_token"], blist["flight_offers"], blist["book_travelers"])
        if ret == False:
            break
        #
        # end = time.time()
        # if end - start > 5 :
        #     break


def main():
    pass


if __name__ == '__main__':

    branch_size = base_config['branch_size']
    print(branch_size)

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
            if mylimit.limit() == True:
                exit(0)

            myflag.set_flag_relogin(False)

            ret, access_token = get_access_token()
            if ret == False :
                continue

            # ret, _ = Airline_Code_Lookup(access_token)
            # if ret == False:
            #     continue
            #
            # exit(0)

            # import time
            #
            # start = time.time()
            #
            ret, flight_offers = flight_offers_search(access_token, book_comp, book_flight, book_date, book_from, book_to)
            if ret == False:
                break

            ret = flight_offers_booking(access_token, flight_offers, book_travelers)
            if ret == False:
                break
            #
            # end = time.time()
            # print(end - start)
            #
            # # ret = flight_offers_seatmap(access_token, elem)
            # # if ret == False:
            # #     continue
            #
            # # ret = flight_offers_price(access_token, elem)
            # # if ret == False:
            # #     continue
            #
            #
            # blist = []
            # for i in range(branch_size):
            #     blist.append(
            #         {
            #             "access_token": access_token,
            #             "flight_offers": flight_offers,
            #             "book_travelers": book_travelers
            #         }
            #     )
            #
            # pool = threadpool.ThreadPool(branch_size)
            # reqs = threadpool.makeRequests(booking, blist)
            # for req in reqs:
            #     pool.putRequest(req)
            #     time.sleep(1 / branch_size)
            # pool.wait()

            break


        if myflag.get_flag_relogin() == True:
            continue

        break

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
