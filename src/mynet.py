import requests
import urllib3
import json
from mylog import *

def get(session, url, params={}, headers={}, payload='', debug=True):
    try:
        logger.warning("-------------- request --------------")

        if debug == True :
            logger.warning('url = ' + url)
            logger.warning('params = ' + json.dumps(params))
            logger.warning('headers = ' + json.dumps(headers))
            logger.warning('payload = ' + payload)

        response = session.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        logger.warning("-------------- response --------------")

        if debug == True :
            logger.warning('response.headers >>>')
            logger.warning(response.raw.headers)
            logger.warning('get Set-Cookie >>>')
            logger.warning(response.raw.headers.getlist('Set-Cookie'))
            logger.info('response.text >>>\n' + response.text.strip('\n').strip(' ') + '\n')

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except requests.exceptions.ConnectionError as e:
        logger.warning('网络连接失败 : ' + str(e))
        return False, ''

    return True, response


def option(session, url, params={}, headers={}, payload='', debug=True):
    try:
        logger.warning("-------------- request --------------")

        if debug == True :
            logger.warning('url = ' + url)
            logger.warning('params = ' + json.dumps(params))
            logger.warning('headers = ' + json.dumps(headers))
            logger.warning('payload = ' + payload)

        response = session.options(url=url, params=params, headers=headers, data=payload, timeout=100)

        logger.warning("-------------- response --------------")

        if debug == True :
            logger.warning('response.headers >>>')
            logger.warning(response.raw.headers)
            logger.warning('option Set-Cookie >>>')
            logger.warning(response.raw.headers.getlist('Set-Cookie'))
            logger.info('response.text >>>\n' + response.text.strip('\n').strip(' ') + '\n')

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except requests.exceptions.ConnectionError as e:
        logger.warning('网络连接失败 : ' + str(e))
        return False, ''


    return True, response


def post(session, url, params={}, headers={}, payload='', debug=True):
    try:
        logger.warning("-------------- request --------------")

        if debug == True :
            logger.warning('url = ' + url)
            logger.warning('params = ' + json.dumps(params))
            logger.warning('headers = ' + json.dumps(headers))
            logger.warning('payload = ' + payload)

        response = session.post(url=url, params=params, headers=headers, data=payload, timeout=100)

        logger.warning("-------------- response --------------")

        if debug == True :
            logger.warning('response.headers >>>')
            logger.warning(response.raw.headers)
            logger.warning('post Set-Cookie >>>')
            logger.warning(response.raw.headers.getlist('Set-Cookie'))
            logger.info('response.text >>>\n' + response.text.strip('\n').strip(' ') + '\n')

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.NewConnectionError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, ''
    except urllib3.exceptions.MaxRetryError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, ''
    except requests.exceptions.ConnectionError as e:
        logger.warning('网络连接失败 : ' + str(e))
        return False, ''

    return True, response.text



def execute_instruction(session_id, arg, debug=False):
    logger.warning("命令 = " + arg)
    command_json = {"sessionId": session_id, "command": arg, "allowEnhanced": True}
    ret, response_json = net_post(book_url, command_json, debug)
    if ret == False :
        return False, {}

    if response_json["success"] == False:
        return False, {}

    if "message" not in response_json:
        return False, {}

    return True, response_json['message']



def three_i_command(session_id, debug = False):
    execute_instruction(session_id, 'I', debug)
    execute_instruction(session_id, 'I', debug)
    execute_instruction(session_id, 'I', debug)

