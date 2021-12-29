#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import urllib3
import json

from mylog import *

book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'

session = requests.Session()

def net_request(url, command_json, debug=False):
    try:

        response = session.post(url, json=command_json, timeout=30)
        if debug:
            logger.info(response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {'message':'网络错误'}
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {'message':'网络错误'}
    except urllib3.exceptions.NewConnectionError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {'message':'网络错误'}
    except urllib3.exceptions.MaxRetryError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {'message':'网络错误'}
    except requests.exceptions.ConnectionError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {'message':'网络错误'}

    return True, response



def json_parse(response) :
    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        return False, {'message':'解析json失败'}

    return True, response_json




def execute_instruction(session_id, arg, debug=False):
    logger.warning("命令 = " + arg)
    command_json = {"sessionId": session_id, "command": arg, "allowEnhanced": True}
    ret, response = net_request(book_url, command_json, debug)
    if ret == False :
        return False, 'relogin'

    ret, response_json = json_parse(response)
    if ret == False :
        return False, ''

    if response_json["success"] == False:
        return False, ''

    if "message" not in response_json:
        return False, ''

    return True, response_json['message']



def three_i_command(session_id, debug = False):
    execute_instruction(session_id, 'I', debug)
    execute_instruction(session_id, 'I', debug)
    execute_instruction(session_id, 'I', debug)

