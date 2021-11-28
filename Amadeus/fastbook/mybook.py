#!/usr/bin/python
import sys
import time
import requests
import threadpool
import urllib3

from mylog import *
import myflag
import myfile
import json
import os


login_url = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp?SITE=LOGINURL&LANGUAGE=GB'
cookies_base = 'JSID=false; visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; nlbi_1658442=zOG2Z9FO2nwxLqMpy0qGMAAAAACMxjNv/fYSxRZ41V9iuEFt; nlbi_1658442_2147483646=V+ZhLzIJWSMR+Yhfy0qGMAAAAABKJ5LuiS9iRVoFmWrbRSZb; incap_ses_1511_1658442=x2qPOb6nvXzeYxMxpib4FPMIoWEAAAAAbtV2UNbxknyV4e+5t35sBw; incap_ses_460_2643603=8vk6bxe9PFRPL8WKC0BiBvMIoWEAAAAA//KVNU61gZfID0Ydho4Ntg'
headers_base = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

ret, base_config = myfile.get_config('config.base.json')
if ret == False:
    exit(0)

ret, book_config_list = myfile.get_config('config.book.json')
if ret == False:
    exit(0)


def limit():
    # 2021-11-20 00:00 我是
    # pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-30 00:00', '%Y-%m-%d %H:%M'):
        logger.warning('试用期限已到...')
        return True
    return False


def netget(url, params, headers=headers_base, payload=''):
    try:
        if base_config['debug']:
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('payload = ' + payload)
        logger.warning('headers = ' + json.dumps(headers))

        response = requests.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        if base_config['debug']:
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text + '\n')

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False

    return True, response


def netoption(url, params, headers=headers_base, payload=''):
    try:
        if base_config['debug']:
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('payload = ' + payload)
        logger.warning('headers = ' + json.dumps(headers))

        response = requests.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        if base_config['debug']:
            logger.info('response.headers >>>\n')
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False

    return True, response


def netpost(url, params, headers=headers_base, payload=''):
    try:
        if base_config['debug']:
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('payload = ' + payload)
        logger.warning('headers = ' + json.dumps(headers))

        response = requests.post(url=url, params=params, headers=headers, data=payload, timeout=100)
        if base_config['debug']:
            logger.info('response.headers >>>\n')
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False

    return True, response


def loginjsp_sessionid():
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp'

    params = {
        'SITE': 'LOGINURL',
        'LANGUAGE': 'GB',
        'event': 'LOGIN_LOGOUT'
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'document'
    headers['sec-fetch-mode'] = 'navigate'
    headers['sec-fetch-site'] = 'none'
    headers['sec-fetch-user'] = '?1'
    headers['upgrade-insecure-requests'] = '1'
    # headers['cookies'] = cookies_base

    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    if 'aria.modules.RequestMgr.session.id' not in response.text:
        logger.warning('获取sessionid失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False
    # response.raw.headers.getlist('Set-Cookie')

    lines = response.text.split('\n')
    for line in lines:
        if 'aria.modules.RequestMgr.session.id' in line:
            sessionid = line.strip(' ').strip('aria.modules.RequestMgr.session.id = ').strip(';').strip('"')
            break

    logger.warning('sessionid = ' + sessionid)

    return True, sessionid


def init_model(sessionid):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.sellingplatformconnect.amadeus.com/LoginService/apfplus/modules/usermanagement/init;jsessionid=' + sessionid

    params = {
        'LANGUAGE': 'GB',
        'SITE': 'LOGINURL'
    }
    headers = headers_base.copy()
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base
    payload = 'data=' + json.dumps({
        'supportMode': False,
        'loginPagePath': '/LoginService/login.jsp'
    })

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    lines = response.text.split('\n')
    data = ''
    for line in lines:
        if 'switchOfficeAllowed' in line:
            data = line
            break

    try:
        model = json.loads(data)['model']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    logger.warning('clpUrl = ' + model['clpUrl'])
    logger.warning('nonce = ' + model['nonce'])
    logger.warning('sessionToken = ' + model['sessionToken'])
    logger.warning('configToken = ' + model['configToken'])

    return True, model


def initWelcome():
    pass


def embedUiLess_lid():
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.accounts.sellingplatformconnect.amadeus.com/LoginService/embedUiLess'

    params = {'v': '1.1'}
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'script'
    headers['sec-fetch-mode'] = 'no-cors'
    headers['sec-fetch-site'] = 'same-site'
    # headers['cookies'] = cookies_base

    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    if 'window._clp_lid' not in response.text:
        logger.warning('获取lid失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    lines = response.text.split('\n')
    for line in lines:
        if 'window._clp_lid' in line:
            lid = line.strip(' ').strip('window._clp_lid = ').strip(';').strip('"')
            break

    logger.warning('lid = ' + lid)

    return True, lid


def aptjs():
    pass


def init_option_post(model, lid):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.accounts.sellingplatformconnect.amadeus.com/LoginService/services/rs/auth2.0/init'

    params = {
        'service': 'SECO',
        'nonce': model['nonce']
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['access-control-request-headers'] = 'x-requested-with'
    headers['access-control-request-method'] = 'POST'

    ret, response = netoption(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    del headers['access-control-request-headers']
    del headers['access-control-request-method']
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base
    payload = 'data=' + \
              json.dumps({
                  'configurationToken': model['configToken']
              }) + \
              '&lid=' + lid

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True


def identify_option_post_accessToken(model, lid):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.accounts.sellingplatformconnect.amadeus.com/LoginService/services/rs/auth2.0/identify'

    params = {
        'service': 'SECO',
        'nonce': model['nonce']
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['access-control-request-headers'] = 'x-requested-with'
    headers['access-control-request-method'] = 'POST'

    ret, response = netoption(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    del headers['access-control-request-headers']
    del headers['access-control-request-method']
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base
    payload = 'data=' + \
              json.dumps({
                  'configurationToken': model['configToken'],
                  'officeId': 'LOSN82312',
                  'userAlias': 'WXIAONAN',
                  'language': 'zh_cn',
                  'authMode': 'HOS'
              }) + \
              '&lid=' + lid

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    try:
        accessToken = json.loads(response.text)['accessToken']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    logger.warning('accessToken = ' + accessToken)

    return True, accessToken


def authenticate_option_post(model, lid, accessToken, oneTimePassword=''):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.accounts.sellingplatformconnect.amadeus.com/LoginService/services/rs/auth2.0/authenticate'

    params = {
        'service': 'SECO',
        'nonce': model['nonce']
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['access-control-request-headers'] = 'x-requested-with'
    headers['access-control-request-method'] = 'POST'

    ret, response = netoption(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    del headers['access-control-request-headers']
    del headers['access-control-request-method']
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base + ';accessToken_SECO=' + accessToken
    payload = 'data=' + \
              json.dumps({
                  'configurationToken': model['configToken'],
                  'accessToken': accessToken,
                  'authenticationFactors': {
                      'password': 'Tut@2020',
                      'oneTimePassword': oneTimePassword,
                      'uba': '{}'
                  },
                  'language': 'zh_cn',
                  'authMode': 'HOS'
              }) + \
              '&lid=' + lid

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    try:
        responsejson = json.loads(response.text)
        responseStatus = json.dumps(responsejson['responseStatus'])
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    logger.warning('responseStatus >>> ' + responseStatus)
    logger.warning('accessToken >>> ' + accessToken)

    if responseStatus != '[]' :
        logger.warning(sys._getframe().f_code.co_name + ' 验证登录失败')
        return False

    try:
        accessToken = responsejson['accessToken']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True, accessToken


def login_sessionid_site(model, accessToken):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/init/login'

    params = {
        'SITE': 'LOGINURL',
        'LANGUAGE': 'CN',
        'refreshOnError': 'true'
    }

    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'document'
    headers['sec-fetch-mode'] = 'navigate'
    headers['sec-fetch-site'] = 'same-site'
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['sec-fetch-user'] = '?1'
    headers['upgrade-insecure-requests'] = '1'
    # headers['cookies'] = cookies_base
    payload = 'ACTION=UMSignInByAccessToken&ACCESS_TOKEN=' + accessToken + '&ID_TOKEN=' + model[
        'configToken'] + '&NONCE=' + model['nonce']

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    lines = response.text.split('\n')
    for line in lines:
        if 'aria.modules.RequestMgr.session' in line:
            sessionid = line.split("aria.modules.RequestMgr.session = {id:'")[1].split("',paramName:'jsessionId'};")[0]
            break

    logger.warning('newsessionid = ' + sessionid)

    return True, sessionid, 'J0CCJ0CC'


def UMCreateSessionKey_ENC(sessionid, site ):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/do/sellweb_home.taskmgr/UMCreateSessionKey;jsessionid=' + sessionid

    params = {
        "flowExKey": "e5s1",
        "tabType": "CMD",
        "persoUpdateDateInMillis": "undefined",
        "initialAction": "createCMD",
        "LANGUAGE": "CN",
        "SITE": site,
        "aria.target": "body",
        "aria.panelId": "1"
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base

    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    if '{"ENC":"' not in response.text:
        logger.warning('获取 ENC 失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    lines = response.text.split('\n')
    for line in lines:
        if '{"ENC":"' in line:
            thejson = json.loads(line.strip(' '))
            ENC = thejson['ENC']
            ENCT = thejson['ENCT']
            break

    logger.warning('ENC = ' + ENC)
    logger.warning('ENCT = ' + ENCT)

    return True, ENC, ENCT


def loginNewSession_login_sessionid_contextid(ENC, ENCT, site):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/do/loginNewSession.UM/login'

    params = {
        "LANGUAGE": ["CN", "CN"],
        site: "",
        "persoUpdateDateInMillis": "undefined",
        "MARKETS": "OID_losn82312",
        "initialAction": "createCMD",
        "tabType": "CMD",
        "aria.target": "body.main.s1",
        "aria.sprefix": "s1",
        "ENC": ENC,
        "ENCT": ENCT,
        "SITE": site,
        "aria.panelId": "4"
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base

    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    if '<aria-response jsessionid=' not in response.text:
        logger.warning('获取新的 jsessionid 失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    newsessionid = ''
    contextId = ''
    lines = response.text.split('\n')
    for line in lines:
        if '<aria-response jsessionid=' in line:
            newsessionid = line.split('<aria-response jsessionid="')[1].split('" viewSetId="')[0]
            contextId = line.split('"dcxid":"')[1].split('","speedModeActivated":')[0]
            break

    logger.warning('newsessionid = ' + newsessionid)
    logger.warning('contextId = ' + contextId)

    return True, newsessionid, contextId


def cryptic_execute_instruction(newsessionid, contextId, command, site):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = '"https://www.booking1.sellingplatformconnect.amadeus.com/cryptic/apfplus/modules/cryptic/cryptic'

    params = {
        "LANGUAGE": "CN",
        "SITE": site,
        "OCTX": "OID_losn82312"
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['cookies'] = cookies_base
    payload = 'data=' + \
              json.dumps({
                  "jSessionId": newsessionid,
                  "contextId": contextId,
                  "userId": "WXIAONAN",
                  "organization": "NMC-NIGERI",
                  "officeId": "LOSN82312",
                  "gds": "AMADEUS",
                  "isStatelessCloneRequired": False,
                  "tasks": [
                      {
                          "type": "CRY",
                          "command": {
                              "command": command,
                              "prohibitedList": "SITE_JCPCRYPTIC_PROHIBITED_COMMANDS_LIST_2"
                          }
                      },
                      {
                          "type": "PAR",
                          "parserType": "screens.ScreenTypeParser"
                      },
                      {
                          "type": "PAR",
                          "parserType": "screens.ScreenTypeParser"
                      },
                      {
                          "type": "ACT",
                          "actionType": "speedmode.SpeedModeAction",
                          "args": {
                              "argsType": "speedmode.SpeedModeActionArgs",
                              "obj": {}
                          }
                      },
                      {
                          "type": "PAR",
                          "parserType": "pnr.PnrParser"
                      }
                  ]
              })

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    try:
        result = json.loads(response.text)['model']['output']['crypticResponse']['response']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    logger.warning('response = ' + result )

    if 'HK1' not in result :
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True, result



def rt(sessionid, contextId, book_comp, book_flight, book_space, book_date, book_from, book_to):
    logger.warning('查询航班 [' + book_comp + book_flight + '] 执行快速预订结果')

    ret, msg = cryptic_execute_instruction(sessionid, contextId, 'RT')
    if ret == False:
        logger.warning('未查到快速预定成功的结果')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    if book_comp+book_flight+' '+book_space+' '+book_date not in msg or \
        book_from+book_to not in msg :
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True


def quick_prebook(sessionid, contextId, book_comp, book_flight, book_space, book_date, book_from, book_to):
    logger.warning('航班 [' + book_comp + book_flight + '] 执行快速预订')

    quick_booking_cmd = 'SS ' + book_comp + book_flight + ' ' + book_space + ' ' + book_date + ' ' + book_from + book_to + ' NN1'
    ret, msg = cryptic_execute_instruction(sessionid, contextId, quick_booking_cmd)
    if ret == False:
        logger.warning('快速预定失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    if book_comp+book_flight+' '+book_space+' '+book_date not in msg or \
        book_from+book_to not in msg :
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True



def auto_book(sessionid):
    # 客户姓名
    ret, msg = cryptic_execute_instruction(sessionid, 'NM1'+book_config['user'])
    if ret == False:
        logger.warning(msg)
        return False

    if book_config['user'] not in msg :
        logger.warning('AP'+book_config['user'] + ' 运行失败')
        return False

    # 客户联系方式
    ret, msg = cryptic_execute_instruction(sessionid, 'AP'+book_config['contact'])
    if ret == False:
        logger.warning(msg)
        logger.warning('AP'+book_config['contact'] + ' 运行失败')
        return False

    if book_config['user'] not in msg :
        logger.warning('AP'+book_config['contact'] + ' 运行失败')
        return False

    # TKTL/
    ret, msg = cryptic_execute_instruction(sessionid, 'TKTL/'+book_config['date'])
    if ret == False:
        logger.warning(msg)
        logger.warning('TKTL/'+book_config['date'] + ' 运行失败')
        return False

    # RFPEI
    ret, msg = cryptic_execute_instruction(sessionid, 'RFPEI')
    if ret == False:
        logger.warning(msg)
        logger.warning('RFPEI 运行失败')
        return False


    # ER
    ret, msg = cryptic_execute_instruction(sessionid, 'ER')
    if ret == False:
        logger.warning(msg)
        logger.warning('ER 运行失败')
        return False

    name = book_config['user'].strip('N.').replace('/', '')
    id = msg['text'].split('\n')[0].split('/')[0]
    logger.warning('存档 : ' + name + '-' + id)
    myfile.save(name + '-' + id, msg['text'])
    logger.warning('订票存档成功 !!!')
    os.system(r'start /b BookInfo.exe')

    cryptic_execute_instruction(sessionid, 'I')
    cryptic_execute_instruction(sessionid, 'I')
    cryptic_execute_instruction(sessionid, 'I')

    return True


def login() :

    model = {}
    lid = ''
    oneTimePassword = ''
    accessToken = ''

    if myflag.get_flag_relogin() == False :

        ret, sessionid = loginjsp_sessionid()
        if ret == False:
            exit(-1)

        ret, model = init_model(sessionid)
        if ret == False:
            exit(-1)

        ret, lid = embedUiLess_lid()
        if ret == False:
            exit(-1)

        ret = init_option_post(model, lid)
        if ret == False:
            exit(-1)

        ret, accessToken = identify_option_post_accessToken(model, lid)
        if ret == False:
            exit(-1)

        while True:
            oneTimePassword = input('\noneTimePassword > ')

            if oneTimePassword.strip('') != '':
                break

    ret, newAccessToken = authenticate_option_post(model, lid, accessToken, oneTimePassword.strip(' '))
    if ret == False:
        exit(-1)

    return model, newAccessToken

def main():
    pass


if __name__ == '__main__':


    branch_size = base_config['branch_size']

    for book_config in book_config_list:

        logger.warning('')
        logger.warning('')
        logger.warning('开始订票 = ' + json.dumps(book_config))

        while True:
            if limit() == True:
                exit(0)

            myflag.set_flag_relogin(False)
            myflag.set_flag_occupied(False)

            model, accessToken = login()

            ret, sessionid, site = login_sessionid_site(model, accessToken)
            if ret == False :
                continue

            ret, ENC, ENCT = UMCreateSessionKey_ENC(sessionid, site)
            if ret == False :
                continue

            ret, sessionid, contextId = loginNewSession_login_sessionid_contextid(ENC, ENCT)
            if ret == False :
                continue

            ret = rt(sessionid, contextId, book_comp, book_flight, book_space, book_date, book_from, book_to)
            if ret == False :
                continue

            ret = quick_prebook(sessionid, contextId, book_comp, book_flight, book_space, book_date, book_from, book_to)
            if ret == False :
                continue

            auto_book(sessionid)

            if myflag.get_flag_relogin() == True:
                continue

            if myflag.get_flag_occupied() == False:
                break

                exit(0)

            break

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
