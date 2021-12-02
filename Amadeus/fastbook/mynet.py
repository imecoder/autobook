import requests
import urllib3
import json
from mylog import *


def get(url, params={}, headers={}, payload='', debug=False):
    try:
        if debug == True :
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('headers = ' + json.dumps(headers))
        logger.warning('payload = ' + payload)

        response = requests.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        if debug == True :
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text + '\n')

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except requests.exceptions.ConnectionError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''

    logger.warning(response.raw.headers.getlist('Set-Cookie'))

    return True, response


def option(url, params={}, headers={}, payload='', debug=False):
    try:
        if debug == True :
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('headers = ' + json.dumps(headers))
        logger.warning('payload = ' + payload)

        response = requests.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        if debug == True :
            logger.info('response.headers >>>\n')
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''

    # logger.warning(response.raw.headers.getlist('Set-Cookie'))

    return True, response


def post(url, params={}, headers={}, payload='', debug=False):
    try:
        if debug == True :
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('headers = ' + json.dumps(headers))
        logger.warning('payload = ' + payload)

        response = requests.post(url=url, params=params, headers=headers, data=payload, timeout=100)
        if debug == True :
            logger.info('response.headers >>>\n')
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''

    # logger.warning(response.raw.headers.getlist('Set-Cookie'))

    return True, response
