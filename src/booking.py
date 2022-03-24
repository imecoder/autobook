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


def fun_flight_offers(access_token) :

    url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
        'ama-client-ref': json.dumps(datetime.time())
    }

    ret, payload = myfile.read_json('flight-offers-search.json')
    if ret == False:
        exit(0)

    ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, {}

    flight_offers = json.loads(response.text)['data'][0]

    return True, flight_offers


def fun_flight_orders(access_token, flight_offers) :

    url = 'https://test.api.amadeus.com/v1/booking/flight-orders'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
    }

    payload = json.dumps(mypayload.for_flight_orders(flight_offers, book_travelers))

    ret, response = mynet.post(session=session, url=url, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True


def main():
    pass


if __name__ == '__main__':

    branch_size = base_config['branch_size']
    print(branch_size)

    if mylimit.limit() == True:
        exit(0)

    ret, access_token = get_access_token()
    if ret == False :
        exit(-1)

    ret, flight_offers = fun_flight_offers(access_token)
    if ret == False:
        exit(-1)

    ret = fun_flight_orders(access_token, flight_offers)
    if ret == False:
        exit(-1)

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
