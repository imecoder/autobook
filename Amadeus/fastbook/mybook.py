#!/usr/bin/python
import sys
import time
import requests
import threadpool
import urllib3
import json
import os

from mylog import *
import mydb
import myflag
import myfile
import mynet

ret, link_config = myfile.read_json('link.json')
if ret == False:
    exit(0)

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


def get_link_info(name) :
    logger.warning('')
    logger.warning('')
    # logger.warning(name)

    try:
        # logger.warning(link_config[name]['url'])
        # logger.warning(json.dumps(link_config[name]['params']))

        headers = link_config['headers_base']
        for key, value in link_config[name]['headers'].items() :
            headers[key] = value
        # logger.warning(json.dumps(headers))

        domain = link_config[name]['url'].split('https://')[1].split('/')[0]

    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        exit(0)
    except KeyError as e:
        logger.warning('解析json失败 : ' + str(e))
        exit(0)


    return link_config[name]['url'], link_config[name]['params'], headers, domain




def get_cookie(set_cookies) :
    cookie = {}
    for coo in set_cookies:
        key = coo.split(';')[0].split('=')[0]
        value = coo.split(';')[0].split('=')[1]
        cookie[key] = value

    return cookie



def main_page_loginjsp():

    url, params, headers, domain = get_link_info(sys._getframe().f_code.co_name)

    ret, response = mynet.get(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

    if 'aria.modules.RequestMgr.session.id' not in response.text:
        logger.warning('获取sessionid失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

    lines = response.text.split('\n')
    for line in lines:
        if 'aria.modules.RequestMgr.session.id' in line:
            sessionid = line.strip(' ').strip('aria.modules.RequestMgr.session.id = ').strip(';').strip('"')
            break

    logger.warning('sessionid = ' + sessionid)

    cookie = get_cookie(response.raw.headers.getlist('Set-Cookie'))
    mydb.save_cookie(domain=domain, cookie=cookie)

    return True, cookie['prxCookie'], sessionid


def main_page_XMLRequestHandler():

    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    ret, response = mynet.get(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''


    return True, newPrxCookie


def main_page_init(sessionid):

    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    payload = 'data=' + json.dumps({
        'supportMode': False,
        'loginPagePath': '/LoginService/login.jsp'
    })

    ret, response = mynet.post(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

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
        return False, '', ''

    logger.warning('clpUrl = ' + model['clpUrl'])
    logger.warning('nonce = ' + model['nonce'])
    logger.warning('sessionToken = ' + model['sessionToken'])
    logger.warning('configToken = ' + model['configToken'])

    return True, newPrxCookie, model


def main_page_embedUiLess():

    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    ret, response = mynet.get(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''


    if 'window._clp_lid' not in response.text:
        logger.warning('获取lid失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    lines = response.text.split('\n')
    for line in lines:
        if 'window._clp_lid' in line:
            lid = line.strip(' ').strip('window._clp_lid = ').strip(';').strip('"')
            break

    logger.warning('lid = ' + lid)

    return True, lid


def auth_page_init_option(model, lid):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    params['nonce']= model['nonce']

    ret, response = mynet.option(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True

def auth_page_init_post(model, lid):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    params['nonce']= model['nonce']

    payload = 'data=' + \
              json.dumps({
                  'configurationToken': model['configToken']
              }) + \
              '&lid=' + lid

    ret, response = mynet.post(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True


def auth_page_indentify_option(model, lid):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)
    params['nonce']= model['nonce']

    ret, response = mynet.option(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False


    return True




def auth_page_indentify_post(model, lid):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)
    params['nonce']= model['nonce']

    payload = 'data=' + \
              json.dumps({
                  'configurationToken': model['configToken'],
                  'officeId': 'LOSN82312',
                  'userAlias': 'WXIAONAN',
                  'language': 'zh_cn',
                  'authMode': 'HOS'
              }) + \
              '&lid=' + lid

    ret, response = mynet.post(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    try:
        accessToken = json.loads(response.text)['accessToken']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('accessToken = ' + accessToken)

    return True, accessToken




def auth_page_authenticate_option(model, lid, accessToken, oneTimePassword=''):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)
    params['nonce']= model['nonce']

    ret, response = mynet.option(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True



def auth_page_authenticate_post(model, lid, accessToken, oneTimePassword=''):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)
    params['nonce']= model['nonce']

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

    ret, response = mynet.post(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    try:
        responsejson = json.loads(response.text)
        responseStatus = json.dumps(responsejson['responseStatus'])
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('responseStatus >>> ' + responseStatus)

    if responseStatus != '[]' :
        logger.warning(sys._getframe().f_code.co_name + ' 验证登录失败')
        return False, ''

    try:
        newaccessToken = responsejson['accessToken']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('newaccessToken >>> ' + newaccessToken)

    exit(0)

    return True, newaccessToken



def user_page_login(model, accessToken):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    payload = 'ACTION=UMSignInByAccessToken&ACCESS_TOKEN=' + accessToken + '&ID_TOKEN=' + model[
        'configToken'] + '&NONCE=' + model['nonce']

    ret, response = mynet.post(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    lines = response.text.split('\n')
    for line in lines:
        if 'aria.modules.RequestMgr.session' in line:
            newsessionid = line.split("aria.modules.RequestMgr.session = {id:'")[1].split("',paramName:'jsessionId'};")[0]
            break

    logger.warning('newsessionid = ' + newsessionid)

    return True, newsessionid

def user_page_UMCreateSessionKey(sessionid):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)

    ret, response = mynet.get(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

    if '{"ENC":"' not in response.text:
        logger.warning('获取 ENC 失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

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


def user_page_loginNewSession(ENC, ENCT):
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)
    params['ENC'] = ENC
    params['aria.panelId'] = '2'

    ret, response = mynet.get(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

    if '<aria-response jsessionid=' not in response.text:
        logger.warning('获取新的 jsessionid 失败')
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, '', ''

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


def shell_page_cryptic_execute_instruction(newsessionid, contextId, command):
# def shell_page_cryptic_execute_instruction():
    url, params, headers = get_link_info(sys._getframe().f_code.co_name)
    payload = 'data={"jSessionId":"P5xQ0BWCMJWeO4jsxqXmxHZ0cEDXT9bwNIWBqDqs!1638335619670","contextId":"8c3e796ca1dce6ce9e46aeeeb53508f16aec49c7ec4662e8a77d425988fb3c7a","userId":"WXIAONAN","organization":"NMC-NIGERI","officeId":"LOSN82312","gds":"AMADEUS","isStatelessCloneRequired":false,"tasks":[{"type":"CRY","command":{"command":"AN02DECLOSFRA/ALH","prohibitedList":"SITE_JCPCRYPTIC_PROHIBITED_COMMANDS_LIST_2"}},{"type":"PAR","parserType":"screens.ScreenTypeParser"},{"type":"PAR","parserType":"screens.ScreenTypeParser"},{"type":"ACT","actionType":"speedmode.SpeedModeAction","args":{"argsType":"speedmode.SpeedModeActionArgs","obj":{}}},{"type":"PAR","parserType":"pnr.PnrParser"}]}'

    ret, response = mynet.post(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    try:
        result = json.loads(response.text)['model']['output']['crypticResponse']['response']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''
    except KeyError as e :
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('response = ' + result )

    if 'HK1' not in result :
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    return True, result



def rt(sessionid, contextId, book_comp, book_flight, book_space, book_date, book_from, book_to):
    logger.warning('查询航班 [' + book_comp + book_flight + '] 执行快速预订结果')

    ret, msg = shell_page_cryptic_execute_instruction(sessionid, contextId, 'RT')
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
    ret, msg = shell_page_cryptic_execute_instruction(sessionid, contextId, quick_booking_cmd)
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
    ret, msg = shell_page_cryptic_execute_instruction(sessionid, 'NM1'+book_config['user'])
    if ret == False:
        logger.warning(msg)
        return False

    if book_config['user'] not in msg :
        logger.warning('AP'+book_config['user'] + ' 运行失败')
        return False

    # 客户联系方式
    ret, msg = shell_page_cryptic_execute_instruction(sessionid, 'AP'+book_config['contact'])
    if ret == False:
        logger.warning(msg)
        logger.warning('AP'+book_config['contact'] + ' 运行失败')
        return False

    if book_config['user'] not in msg :
        logger.warning('AP'+book_config['contact'] + ' 运行失败')
        return False

    # TKTL/
    ret, msg = shell_page_cryptic_execute_instruction(sessionid, 'TKTL/'+book_config['date'])
    if ret == False:
        logger.warning(msg)
        logger.warning('TKTL/'+book_config['date'] + ' 运行失败')
        return False

    # RFPEI
    ret, msg = shell_page_cryptic_execute_instruction(sessionid, 'RFPEI')
    if ret == False:
        logger.warning(msg)
        logger.warning('RFPEI 运行失败')
        return False


    # ER
    ret, msg = shell_page_cryptic_execute_instruction(sessionid, 'ER')
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

    shell_page_cryptic_execute_instruction(sessionid, 'I')
    shell_page_cryptic_execute_instruction(sessionid, 'I')
    shell_page_cryptic_execute_instruction(sessionid, 'I')

    return True


def login() :

    model = {}
    lid = ''
    oneTimePassword = ''
    accessToken = ''

    if myflag.get_flag_relogin() == False :

        ret, sessionid = main_page_loginjsp()
        if ret == False:
            exit(-1)
        #
        # ret = main_page_XMLRequestHandler()
        # if ret == False:
        #     exit(-1)

        ret, model = main_page_init(sessionid)
        if ret == False:
            exit(-1)

        ret, lid = main_page_embedUiLess()
        if ret == False:
            exit(-1)
        #
        # ret = auth_page_init_option(model, lid)
        # if ret == False:
        #     exit(-1)
        #
        # ret = auth_page_init_post(model, lid)
        # if ret == False:
        #     exit(-1)
        #
        # ret = auth_page_indentify_option(model, lid)
        # if ret == False:
        #     exit(-1)

        ret, accessToken = auth_page_indentify_post(model, lid)
        if ret == False:
            exit(-1)

        while True:
            oneTimePassword = input('\noneTimePassword > ')

            if oneTimePassword.strip('') == 'null':
                oneTimePassword=''
                break

            if oneTimePassword.strip('') != '':
                break

    # oneTimePassword=''
    ret, newAccessToken = auth_page_authenticate_post(model, lid, accessToken, oneTimePassword.strip(' '))
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

        book_date = book_config["date"]
        book_from = book_config["from"]
        book_to = book_config["to"]
        book_comp = book_config["comp"]
        book_flight = book_config["flight"]
        book_space = book_config["space"][0]
        book_user = book_config["user"]
        book_contact = book_config["contact"]

        while True:
            if limit() == True:
                exit(0)

            myflag.set_flag_relogin(False)
            myflag.set_flag_occupied(False)

            model, accessToken = login()

            ret, sessionid = user_page_login(model, accessToken)
            if ret == False :
                continue

            # ret = user_page_CreateMonoSession(sessionid)
            # # if ret == False :
            # #     continue


            ret, ENC, ENCT = user_page_UMCreateSessionKey(sessionid)
            # if ret == False :
            #     continue

            ret, sessionid, contextId = user_page_loginNewSession(ENC, ENCT)
            # if ret == False :
            #     continue


            ret = rt(sessionid, contextId, book_comp, book_flight, book_space, book_date, book_from, book_to)
            # if ret == False :
            #     continue
            exit()

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
