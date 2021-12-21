import http
from http.client import HTTPResponse
from io import BytesIO
import urllib3
import json
import requests

from mylog import *


book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'


def net_request(url, command_json, debug=False):
    try:

        response = requests.post(url, json=command_json, timeout=100)
        if debug:
            logger.info(response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {}
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {}

    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        return False, {}

    return True, response_json


def execute_instruction(session_id, arg, debug=False):
    logger.warning("命令 = " + arg)
    command_json = {"sessionId": session_id, "command": arg, "allowEnhanced": True}
    ret, response_json = net_request(book_url, command_json, debug)

    if response_json["success"] == False:
        return False, {}

    if "message" not in response_json:
        return False, {}

    return True, response_json['message']


def three_i_command(session_id, debug = False):
    execute_instruction(session_id, 'I', debug)
    execute_instruction(session_id, 'I', debug)
    execute_instruction(session_id, 'I', debug)



class SocketBytesIO:
    def __init__(self, content):
        self.handle = BytesIO(content)

    def makefile(self, mode):
        return self.handle


def get_response_header(data):
    sock = SocketBytesIO(data)
    response = HTTPResponse(sock)
    response.begin()
    header_length = len(data.split(b'\r\n\r\n')[0]) + 4
    return response.status, header_length, int(response.getheader('Content-Length'))


def get_response_body(data):
    sock = SocketBytesIO(data)
    response = HTTPResponse(sock)
    response.begin()
    return urllib3.HTTPResponse.from_httplib(response).data


def get_response_body_json(data):
    try:
        sock = SocketBytesIO(data)
        response = HTTPResponse(sock)
        response.begin()

        data = urllib3.HTTPResponse.from_httplib(response).data
        body_json = json.loads(data)

        return True, body_json
    except http.client.RemoteDisconnected as e:
        logger.warning('远程断开了链接 : ' + str(e))
        return False, {}
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        return False, {}

    return False, {}
