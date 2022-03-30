#!/usr/bin/python
import sys

import requests
import json
import time

from mylog import *
import myfile
import mynet
import mylimit

session = requests.session()

ret, base_config = myfile.read_json('config.base.json')
if ret == False:
    exit(0)

def get_access_token() :
    url_token = 'https://test.travel.api.amadeus.com/v1/security/oauth2/token'

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    payload = "grant_type=client_credentials&client_id=gtAD9AaLtE8iNSNeuvrpHKZq47qucBTo&client_secret=Z2mjUGv3hkZx8oAk"

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

    url = 'https://test.travel.api.amadeus.com/v1/shopping/flight-offers'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token
    }

    import flight_offers_case1

    payload = flight_offers_case1.get_payload()

    ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, {}

    flight_offers = json.loads(response.text)['data'][0]

    return True, flight_offers


def fun_flight_orders(access_token, flight_offers_result) :

    url = 'https://test.travel.api.amadeus.com/v1/booking/flight-orders'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token ,
        'ama-client-ref': 'LOSN828UU-' + str(time.time())
    }

    import flight_orders

    payload = flight_orders.get_payload(flight_offers_result)

    ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
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

    ret, flight_offers_result = fun_flight_offers(access_token)
    if ret == False:
        exit(-1)

    ret = fun_flight_orders(access_token, flight_offers_result)
    if ret == False:
        exit(-1)

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
