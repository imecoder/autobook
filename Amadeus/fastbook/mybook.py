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

cookies_incap_ses_636_2643603 = 'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
cookies_visid_incap_1943992 = 'visid_incap_1943992=L3jfGEbERZ2pGmu1e+58M8EejWEAAAAAQUIPAAAAAAD6gqJ5YVvMa7sgZ7VLH2pX; '
cookies_lss_loc_id = 'lss_loc_id=AB18C4C9837457E8DA92D0FB479DD25EC60F281A6B28B7452E15D6A97CFD36D4; '

cookies_70f2_key = '70f276b919ac6ed3c8047ca07019200a='
cookies_prxCookie_key = 'prxCookie=!'


# cookies = (
#     'JSID=false;'
#     'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il;'
#     'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd;'
#     '_ga=GA1.2.208667559.1638024099'
#     'nlbi_1658442=zOG2Z9FO2nwxLqMpy0qGMAAAAACMxjNv/fYSxRZ41V9iuEFt;'
#     'nlbi_1658442_2147483646=V+ZhLzIJWSMR+Yhfy0qGMAAAAABKJ5LuiS9iRVoFmWrbRSZb;'
#     'incap_ses_1511_1658442=x2qPOb6nvXzeYxMxpib4FPMIoWEAAAAAbtV2UNbxknyV4e+5t35sBw;'
#     'incap_ses_460_2643603=8vk6bxe9PFRPL8WKC0BiBvMIoWEAAAAA//KVNU61gZfID0Ydho4Ntg'
# )
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


session = requests.session()

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

        response = session.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        if base_config['debug']:
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

    return True, response


def netoption(url, params, headers=headers_base, payload=''):
    try:
        if base_config['debug']:
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('payload = ' + payload)
        logger.warning('headers = ' + json.dumps(headers))

        response = session.get(url=url, params=params, headers=headers, data=payload, timeout=100)

        if base_config['debug']:
            logger.info('response.headers >>>\n')
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''

    return True, response


def netpost(url, params, headers=headers_base, payload=''):
    try:
        if base_config['debug']:
            logger.warning('url = ' + url)

        logger.warning('params = ' + json.dumps(params))
        logger.warning('payload = ' + payload)
        logger.warning('headers = ' + json.dumps(headers))

        response = session.post(url=url, params=params, headers=headers, data=payload, timeout=100)
        if base_config['debug']:
            logger.info('response.headers >>>\n')
            logger.info(response.raw.headers)
            logger.info('response.text >>>\n' + response.text)

    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络超时 : ' + str(e))
        return False, ''

    return True, response


def find_cookie(set_cookies, key, filter) :
    for coo in set_cookies:
        if key in coo:
            value = coo.split(key)[1].split(filter)[0]
            logger.warning(key+value)
            return value

    logger.warning('未找到cookie : ' + key)
    return '; '


def main_page_loginjsp():

    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp'

    params = {
        'SITE': 'LOGINURL',
        'LANGUAGE': 'GB'
    }
    # headers = headers_base.copy()
    # headers['sec-fetch-dest'] = 'document'
    # headers['sec-fetch-mode'] = 'navigate'
    # headers['sec-fetch-site'] = 'none'
    # headers['sec-fetch-user'] = '?1'
    # headers['upgrade-insecure-requests'] = '1'
    # headers['cookies'] = (
    #     'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
    #     'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
    #     '_ga=GA1.2.208667559.1638024099; '
    # )

    ret, response = netget(url=url, params=params)
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

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning('set_cookies = ')
    logger.warning(set_cookies)
    cookies_prxCookie_value = find_cookie(set_cookies, cookies_prxCookie_key, 'path=')

    return True, sessionid, cookies_prxCookie_value


def main_page_XMLRequestHandler(cookies_prxCookie_value):

    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.sellingplatformconnect.amadeus.com/LoginService-static/aria/modules/requestHandler/XMLRequestHandler-1ya0zpy.js'

    params = {
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'
    headers['cookies'] = (
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        '70f276b919ac6ed3c8047ca07019200a=a6300a65565dea32689c2d7b36df2492; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
    )
    headers['cookies'] = headers['cookies'] + \
                         cookies_prxCookie_key + cookies_prxCookie_value

    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)
    cookies_prxCookie_value = find_cookie(set_cookies, cookies_prxCookie_key, 'path=')

    return True, cookies_prxCookie_value





def main_page_init(sessionid, cookies_prxCookie_value):

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
    headers['cookies'] = (
        'lss_loc_id=AB18C4C9837457E8DA92D0FB479DD25EC60F281A6B28B7452E15D6A97CFD36D4; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        '70f276b919ac6ed3c8047ca07019200a=a6300a65565dea32689c2d7b36df2492; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
    )
    headers['cookies'] = headers['cookies'] + \
                         cookies_prxCookie_key + cookies_prxCookie_value

    payload = 'data=' + json.dumps({
        'supportMode': False,
        'loginPagePath': '/LoginService/login.jsp'
    })

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
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

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)
    cookies_prxCookie_value = find_cookie(set_cookies, cookies_prxCookie_key, 'path=')

    return True, model, cookies_prxCookie_value


def main_page_embedUiLess():

    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.accounts.sellingplatformconnect.amadeus.com/LoginService/embedUiLess'

    params = {'v': '1.1'}
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'script'
    headers['sec-fetch-mode'] = 'no-cors'
    headers['sec-fetch-site'] = 'same-site'

    headers['cookies'] = (
        'visid_incap_1943992=L3jfGEbERZ2pGmu1e+58M8EejWEAAAAAQUIPAAAAAAD6gqJ5YVvMa7sgZ7VLH2pX; '
        'lss_loc_id=453F2C3A6B6EDA69956B2B9BF55D6A71C3E0ABFD7641A10AB368B19071A5AEC4; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'nlbi_1943992=Wk3GOVMN0yjy1mYj+eFteAAAAADszxj+XlF/EbtmX98ayjCo; '
        'accessToken_SECO=95bXQhhCVqKPX4Q6R7jJtA; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
        'accessToken_AAM=5lLBj39k6botopHikaSEAw; '
        'sso_t=eyJhbGciOiJSU0ExXzUiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwieDV1Ijoic3NvX2ludHJhX2Vudi53d3cuYWNjb3VudHMuYW1hZGV1cy5jb20ifQ.kYjzWCUVOyOc_ktKQA1NTyE9o1eqshaeTAL6mISjuvrb49UqcjpHQ25Zkwh5PWJEQR2PUKyop3kAODCLsUS3ZCLcu0qZHQ3Rj40T-4PCh90gSTWhQJoAAyxPWD4pwvCVudLKzT7oN5M5Sxx6dh5HRGVM426OQ7O9MhfKtHBPhNSyCKybGfIBWXmymfFE8R7WW6rZBFyj-jjjX-wAP6Usfiu7vW7kN8gUeuIWDxeNMjUwPRc2WcE_GEkQBok9_TGaHHFEKAhbotjovUknOXSwDD4trycYJqYaHo4sAuvR-dSvCrIDI7i5DnD4DqDP62xjG3YABg_aV44nk7W3R4HQuA.z__ZGjbmtGgXhPpTW-qrDw.XCl5-Ex2yqoI1AbXequkvZDcZN08iEfX24VMuR75HpmfdY387qXLdtu-ZkUpGD7LD43PA62zqNEnRTroS142PcGbfmEGZiRbgYHDHxmk7EFllcHAVm1d8wAqZ7Og4-jhdu4mFSQWT3xveJGOZ7Eku4RFMoa_d95e8wZUXrg2fpLE4G8xeelkF-77EdxnqwaAKspOQ5f4GKLGZs1Ne0cxGsbJ5edfwG9-X6LmwEathvyPtNdNn0otwbDkGrkUdYOgHD4P8oKx3FbahDUgak36DEGh1pIT7TssMte7QZo5VDuLuIYDcTmYJjsJQ4Kj1M7tqCS0rE7FuzGj5-DUq5OcKs57jyXj6igFGC5K1TgfebvjYXgprvmlwTBNuvDcTB7HDu7HKAF-WOc_7d945jvhPxxmg4OCu5Ki0cjBIDXuhawjBbWYdLB1WS6hMkEuGlycN1ZIRk73LzVmwRsDNFLXgdT228KoPsfBsnwP-VTe1ZyR-YBpUysWBjxFm8RLdLgzLnMmHvKHJ70UmDD4BOUVdUuYYuj14ZH73Q0nyzJhMigQBWKS_USatKnP4_GWEJh0iWoGMcj9UMvrJEar1we3kVEgiTu_WUazKJD9crlxEQUkZYDgDQt2UaAUA5MoOmDj4lJ0y4mDbIIuAgagqpdhiDYe2J0c5NaD8vfyBdQbhvSYqq6qd46VMQUnj20ztAxjoFifE8hN-VgA4VPN2SD9IoRdhIXwYknpr3kx6Mzhij8fyt9qcp5Ue5eI4r4NyBPnl-bXWwzKXhKIUMdR-aK71f4Tb-8I7igxdsNZ5kXUKwF-_AoAkjZ_l7MNsUJZ9c7fdDeb3-Buvv7on1aMIn6-wBcpDLvNvsNFOkO_QLO4vWgAHNvhhluC7Ef6T2SMH5h6Jlpe0PTzdh_hBm8JKImEY_l350YEWrmo3uRoAtEiFV3TQReEtJuwCF8FPj42nwZ-Z4uyP57by8PG-tKD7sGyv3RTX3RYR4HndmNQqO9b7FQZW989EkrEgJnSyk_IgdiUNPpu4vodup42N7420c6dHR4ZRCb-w1fuUBReMxkW4cRDiSgYkQUxfqBvkrwg3UwXWJDsdxAuriUOdrFk0eA1_mxQC4VwiGQ9OymTVA2HWKk.USMORIpSqtdwIvOcKEpK-4VmJAi4-lbA_VVgaOBPE6Q; '
        'accessToken_ASH=EkSmNpPRDF-oE_yhVZdCWA; '
        'incap_ses_407_1943992=borEDEcrhEUtSBTngfSlBVFVpGEAAAAAHjH3UjK6xRKfNDZu2zK8dQ==; '
    )

    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

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
    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True, lid


def login_page_init(model, lid):
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


    headers['cookies'] = (
        'visid_incap_1943992=L3jfGEbERZ2pGmu1e+58M8EejWEAAAAAQUIPAAAAAAD6gqJ5YVvMa7sgZ7VLH2pX; '
        'lss_loc_id=453F2C3A6B6EDA69956B2B9BF55D6A71C3E0ABFD7641A10AB368B19071A5AEC4; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'nlbi_1943992=Wk3GOVMN0yjy1mYj+eFteAAAAADszxj+XlF/EbtmX98ayjCo; '
        'accessToken_SECO=95bXQhhCVqKPX4Q6R7jJtA; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
        'accessToken_AAM=5lLBj39k6botopHikaSEAw; '
        'sso_t=eyJhbGciOiJSU0ExXzUiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwieDV1Ijoic3NvX2ludHJhX2Vudi53d3cuYWNjb3VudHMuYW1hZGV1cy5jb20ifQ.kYjzWCUVOyOc_ktKQA1NTyE9o1eqshaeTAL6mISjuvrb49UqcjpHQ25Zkwh5PWJEQR2PUKyop3kAODCLsUS3ZCLcu0qZHQ3Rj40T-4PCh90gSTWhQJoAAyxPWD4pwvCVudLKzT7oN5M5Sxx6dh5HRGVM426OQ7O9MhfKtHBPhNSyCKybGfIBWXmymfFE8R7WW6rZBFyj-jjjX-wAP6Usfiu7vW7kN8gUeuIWDxeNMjUwPRc2WcE_GEkQBok9_TGaHHFEKAhbotjovUknOXSwDD4trycYJqYaHo4sAuvR-dSvCrIDI7i5DnD4DqDP62xjG3YABg_aV44nk7W3R4HQuA.z__ZGjbmtGgXhPpTW-qrDw.XCl5-Ex2yqoI1AbXequkvZDcZN08iEfX24VMuR75HpmfdY387qXLdtu-ZkUpGD7LD43PA62zqNEnRTroS142PcGbfmEGZiRbgYHDHxmk7EFllcHAVm1d8wAqZ7Og4-jhdu4mFSQWT3xveJGOZ7Eku4RFMoa_d95e8wZUXrg2fpLE4G8xeelkF-77EdxnqwaAKspOQ5f4GKLGZs1Ne0cxGsbJ5edfwG9-X6LmwEathvyPtNdNn0otwbDkGrkUdYOgHD4P8oKx3FbahDUgak36DEGh1pIT7TssMte7QZo5VDuLuIYDcTmYJjsJQ4Kj1M7tqCS0rE7FuzGj5-DUq5OcKs57jyXj6igFGC5K1TgfebvjYXgprvmlwTBNuvDcTB7HDu7HKAF-WOc_7d945jvhPxxmg4OCu5Ki0cjBIDXuhawjBbWYdLB1WS6hMkEuGlycN1ZIRk73LzVmwRsDNFLXgdT228KoPsfBsnwP-VTe1ZyR-YBpUysWBjxFm8RLdLgzLnMmHvKHJ70UmDD4BOUVdUuYYuj14ZH73Q0nyzJhMigQBWKS_USatKnP4_GWEJh0iWoGMcj9UMvrJEar1we3kVEgiTu_WUazKJD9crlxEQUkZYDgDQt2UaAUA5MoOmDj4lJ0y4mDbIIuAgagqpdhiDYe2J0c5NaD8vfyBdQbhvSYqq6qd46VMQUnj20ztAxjoFifE8hN-VgA4VPN2SD9IoRdhIXwYknpr3kx6Mzhij8fyt9qcp5Ue5eI4r4NyBPnl-bXWwzKXhKIUMdR-aK71f4Tb-8I7igxdsNZ5kXUKwF-_AoAkjZ_l7MNsUJZ9c7fdDeb3-Buvv7on1aMIn6-wBcpDLvNvsNFOkO_QLO4vWgAHNvhhluC7Ef6T2SMH5h6Jlpe0PTzdh_hBm8JKImEY_l350YEWrmo3uRoAtEiFV3TQReEtJuwCF8FPj42nwZ-Z4uyP57by8PG-tKD7sGyv3RTX3RYR4HndmNQqO9b7FQZW989EkrEgJnSyk_IgdiUNPpu4vodup42N7420c6dHR4ZRCb-w1fuUBReMxkW4cRDiSgYkQUxfqBvkrwg3UwXWJDsdxAuriUOdrFk0eA1_mxQC4VwiGQ9OymTVA2HWKk.USMORIpSqtdwIvOcKEpK-4VmJAi4-lbA_VVgaOBPE6Q; '
        'accessToken_ASH=EkSmNpPRDF-oE_yhVZdCWA; '
        'incap_ses_407_1943992=borEDEcrhEUtSBTngfSlBVFVpGEAAAAAHjH3UjK6xRKfNDZu2zK8dQ==; '
    )

    payload = 'data=' + \
              json.dumps({
                  'configurationToken': model['configToken']
              }) + \
              '&lid=' + lid

    ret, response = netpost(url=url, params=params, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True


def login_page_indentify(model, lid):
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
        return False, ''

    del headers['access-control-request-headers']
    del headers['access-control-request-method']
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['x-requested-with'] = 'XMLHttpRequest'


    headers['cookies'] = (
        'visid_incap_1943992=L3jfGEbERZ2pGmu1e+58M8EejWEAAAAAQUIPAAAAAAD6gqJ5YVvMa7sgZ7VLH2pX; '
        'lss_loc_id=453F2C3A6B6EDA69956B2B9BF55D6A71C3E0ABFD7641A10AB368B19071A5AEC4; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'nlbi_1943992=Wk3GOVMN0yjy1mYj+eFteAAAAADszxj+XlF/EbtmX98ayjCo; '
        'accessToken_SECO=95bXQhhCVqKPX4Q6R7jJtA; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
        'accessToken_AAM=5lLBj39k6botopHikaSEAw; '
        'sso_t=eyJhbGciOiJSU0ExXzUiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwieDV1Ijoic3NvX2ludHJhX2Vudi53d3cuYWNjb3VudHMuYW1hZGV1cy5jb20ifQ.kYjzWCUVOyOc_ktKQA1NTyE9o1eqshaeTAL6mISjuvrb49UqcjpHQ25Zkwh5PWJEQR2PUKyop3kAODCLsUS3ZCLcu0qZHQ3Rj40T-4PCh90gSTWhQJoAAyxPWD4pwvCVudLKzT7oN5M5Sxx6dh5HRGVM426OQ7O9MhfKtHBPhNSyCKybGfIBWXmymfFE8R7WW6rZBFyj-jjjX-wAP6Usfiu7vW7kN8gUeuIWDxeNMjUwPRc2WcE_GEkQBok9_TGaHHFEKAhbotjovUknOXSwDD4trycYJqYaHo4sAuvR-dSvCrIDI7i5DnD4DqDP62xjG3YABg_aV44nk7W3R4HQuA.z__ZGjbmtGgXhPpTW-qrDw.XCl5-Ex2yqoI1AbXequkvZDcZN08iEfX24VMuR75HpmfdY387qXLdtu-ZkUpGD7LD43PA62zqNEnRTroS142PcGbfmEGZiRbgYHDHxmk7EFllcHAVm1d8wAqZ7Og4-jhdu4mFSQWT3xveJGOZ7Eku4RFMoa_d95e8wZUXrg2fpLE4G8xeelkF-77EdxnqwaAKspOQ5f4GKLGZs1Ne0cxGsbJ5edfwG9-X6LmwEathvyPtNdNn0otwbDkGrkUdYOgHD4P8oKx3FbahDUgak36DEGh1pIT7TssMte7QZo5VDuLuIYDcTmYJjsJQ4Kj1M7tqCS0rE7FuzGj5-DUq5OcKs57jyXj6igFGC5K1TgfebvjYXgprvmlwTBNuvDcTB7HDu7HKAF-WOc_7d945jvhPxxmg4OCu5Ki0cjBIDXuhawjBbWYdLB1WS6hMkEuGlycN1ZIRk73LzVmwRsDNFLXgdT228KoPsfBsnwP-VTe1ZyR-YBpUysWBjxFm8RLdLgzLnMmHvKHJ70UmDD4BOUVdUuYYuj14ZH73Q0nyzJhMigQBWKS_USatKnP4_GWEJh0iWoGMcj9UMvrJEar1we3kVEgiTu_WUazKJD9crlxEQUkZYDgDQt2UaAUA5MoOmDj4lJ0y4mDbIIuAgagqpdhiDYe2J0c5NaD8vfyBdQbhvSYqq6qd46VMQUnj20ztAxjoFifE8hN-VgA4VPN2SD9IoRdhIXwYknpr3kx6Mzhij8fyt9qcp5Ue5eI4r4NyBPnl-bXWwzKXhKIUMdR-aK71f4Tb-8I7igxdsNZ5kXUKwF-_AoAkjZ_l7MNsUJZ9c7fdDeb3-Buvv7on1aMIn6-wBcpDLvNvsNFOkO_QLO4vWgAHNvhhluC7Ef6T2SMH5h6Jlpe0PTzdh_hBm8JKImEY_l350YEWrmo3uRoAtEiFV3TQReEtJuwCF8FPj42nwZ-Z4uyP57by8PG-tKD7sGyv3RTX3RYR4HndmNQqO9b7FQZW989EkrEgJnSyk_IgdiUNPpu4vodup42N7420c6dHR4ZRCb-w1fuUBReMxkW4cRDiSgYkQUxfqBvkrwg3UwXWJDsdxAuriUOdrFk0eA1_mxQC4VwiGQ9OymTVA2HWKk.USMORIpSqtdwIvOcKEpK-4VmJAi4-lbA_VVgaOBPE6Q; '
        'accessToken_ASH=EkSmNpPRDF-oE_yhVZdCWA; '
        'incap_ses_407_1943992=borEDEcrhEUtSBTngfSlBVFVpGEAAAAAHjH3UjK6xRKfNDZu2zK8dQ==; '
    )


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
        return False, ''

    try:
        accessToken = json.loads(response.text)['accessToken']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('accessToken = ' + accessToken)
    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True, accessToken


def login_page_authenticate(model, lid, accessToken, oneTimePassword=''):
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
        return False, ''

    del headers['access-control-request-headers']
    del headers['access-control-request-method']
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['x-requested-with'] = 'XMLHttpRequest'


    headers['cookies'] = (
        'visid_incap_1943992=L3jfGEbERZ2pGmu1e+58M8EejWEAAAAAQUIPAAAAAAD6gqJ5YVvMa7sgZ7VLH2pX; '
        'lss_loc_id=453F2C3A6B6EDA69956B2B9BF55D6A71C3E0ABFD7641A10AB368B19071A5AEC4; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'nlbi_1943992=Wk3GOVMN0yjy1mYj+eFteAAAAADszxj+XlF/EbtmX98ayjCo; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
        'accessToken_AAM=5lLBj39k6botopHikaSEAw; '
        'sso_t=eyJhbGciOiJSU0ExXzUiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwieDV1Ijoic3NvX2ludHJhX2Vudi53d3cuYWNjb3VudHMuYW1hZGV1cy5jb20ifQ.kYjzWCUVOyOc_ktKQA1NTyE9o1eqshaeTAL6mISjuvrb49UqcjpHQ25Zkwh5PWJEQR2PUKyop3kAODCLsUS3ZCLcu0qZHQ3Rj40T-4PCh90gSTWhQJoAAyxPWD4pwvCVudLKzT7oN5M5Sxx6dh5HRGVM426OQ7O9MhfKtHBPhNSyCKybGfIBWXmymfFE8R7WW6rZBFyj-jjjX-wAP6Usfiu7vW7kN8gUeuIWDxeNMjUwPRc2WcE_GEkQBok9_TGaHHFEKAhbotjovUknOXSwDD4trycYJqYaHo4sAuvR-dSvCrIDI7i5DnD4DqDP62xjG3YABg_aV44nk7W3R4HQuA.z__ZGjbmtGgXhPpTW-qrDw.XCl5-Ex2yqoI1AbXequkvZDcZN08iEfX24VMuR75HpmfdY387qXLdtu-ZkUpGD7LD43PA62zqNEnRTroS142PcGbfmEGZiRbgYHDHxmk7EFllcHAVm1d8wAqZ7Og4-jhdu4mFSQWT3xveJGOZ7Eku4RFMoa_d95e8wZUXrg2fpLE4G8xeelkF-77EdxnqwaAKspOQ5f4GKLGZs1Ne0cxGsbJ5edfwG9-X6LmwEathvyPtNdNn0otwbDkGrkUdYOgHD4P8oKx3FbahDUgak36DEGh1pIT7TssMte7QZo5VDuLuIYDcTmYJjsJQ4Kj1M7tqCS0rE7FuzGj5-DUq5OcKs57jyXj6igFGC5K1TgfebvjYXgprvmlwTBNuvDcTB7HDu7HKAF-WOc_7d945jvhPxxmg4OCu5Ki0cjBIDXuhawjBbWYdLB1WS6hMkEuGlycN1ZIRk73LzVmwRsDNFLXgdT228KoPsfBsnwP-VTe1ZyR-YBpUysWBjxFm8RLdLgzLnMmHvKHJ70UmDD4BOUVdUuYYuj14ZH73Q0nyzJhMigQBWKS_USatKnP4_GWEJh0iWoGMcj9UMvrJEar1we3kVEgiTu_WUazKJD9crlxEQUkZYDgDQt2UaAUA5MoOmDj4lJ0y4mDbIIuAgagqpdhiDYe2J0c5NaD8vfyBdQbhvSYqq6qd46VMQUnj20ztAxjoFifE8hN-VgA4VPN2SD9IoRdhIXwYknpr3kx6Mzhij8fyt9qcp5Ue5eI4r4NyBPnl-bXWwzKXhKIUMdR-aK71f4Tb-8I7igxdsNZ5kXUKwF-_AoAkjZ_l7MNsUJZ9c7fdDeb3-Buvv7on1aMIn6-wBcpDLvNvsNFOkO_QLO4vWgAHNvhhluC7Ef6T2SMH5h6Jlpe0PTzdh_hBm8JKImEY_l350YEWrmo3uRoAtEiFV3TQReEtJuwCF8FPj42nwZ-Z4uyP57by8PG-tKD7sGyv3RTX3RYR4HndmNQqO9b7FQZW989EkrEgJnSyk_IgdiUNPpu4vodup42N7420c6dHR4ZRCb-w1fuUBReMxkW4cRDiSgYkQUxfqBvkrwg3UwXWJDsdxAuriUOdrFk0eA1_mxQC4VwiGQ9OymTVA2HWKk.USMORIpSqtdwIvOcKEpK-4VmJAi4-lbA_VVgaOBPE6Q; '
        'accessToken_ASH=EkSmNpPRDF-oE_yhVZdCWA; '
        'accessToken_SECO=z27TUZPnQmA2O9niuZsiGA; '
        'incap_ses_407_1943992=72JVHIcQ8BHXDyTngfSlBVZ6pGEAAAAAwmPcdAkE6Yq2x3LIa3ABgA==; '
    )
    headers['cookies'] = headers['cookies'] + \
                         'accessToken_SECO=' + accessToken

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
        return False, ''

    try:
        responsejson = json.loads(response.text)
        responseStatus = json.dumps(responsejson['responseStatus'])
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('responseStatus >>> ' + responseStatus)
    logger.warning('accessToken >>> ' + accessToken)

    if responseStatus != '[]' :
        logger.warning(sys._getframe().f_code.co_name + ' 验证登录失败')
        return False, ''

    try:
        accessToken = responsejson['accessToken']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True, accessToken


def user_page_login(model, accessToken):
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

    headers['cookies'] = (
        'lss_loc_id=38215F612AB13F4247DB801C5DA977F44C332E4B3BD4158E147779BE6DB89E59; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        'aria_user_profile={"pref":{"LOGIN_TYPE":"STANDARD","OFFICE_ID":"LOSN82312","ACTIVE_OFFICE_ID":"LOSN82312","IS_GUEST_MODE":false,"AGENT_SIGN":"1012","AGENT_INITIALS":"WX","DUTY_CODE":"GS","USER_ALIAS":"WXIAONAN","ORGANIZATION":"NMC-NIGERI","FIRST_NAME":"WANG","LAST_NAME":"XIAONAN","PHONE_NUMBER":"+2348039943766","LANGUAGE_PREF":"EN","OCTX":"","ENABLE_CUST_NAME":false,"SERVICEMENU_AVAILABLE":true,"LIST_OFFICES":[{"officeId":"LOSN82312","customName":null}],"is_a_logout":"logout"},"firstName":"","lastName":"","gender":""}; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'um_jst=F7C91C446413AFD9E70F8AE640C6A377EFE0A7D5FB9D728616EFD0E4372DB81A; '
        '455368185956a8f748fd35f7d905a930=570f002eacd14a580ae521c04c20db1a; '
        'incap_ses_636_2643603=HD/RWxixLRlZJIiHDIfTCHYspGEAAAAAk2yP3ChNH/a3IkEN1YmHDA==; '
        '5bb6f21dabcc922fce10d96f5b36a932=b1f53d8e647f6f1e166516aaa0ce93f5; '
        'prxCookie=!CxNtAm9GbXP1GP3PUK3QNIFO+llyZ3bfYYuW8SSTatb5bYelGYPmhtI0W4cOmKmm++CWZOdoWx2ekp29EgCI95Z9YIeXmT/1cR/f29s=; '
    )
    headers['cookies'] = headers['cookies'] + \
                         'accessToken_SECO=' + accessToken

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

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True, sessionid

def user_page_CreateMonoSession(sessionid ):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/do/sellweb_home.taskmgr/CreateMonoSession;jsessionid=' + sessionid

    params = {
        "flowExKey": "e5s1",
        "initialAction": "createMain",
        "aria.target": "body.main.main",
        "aria.sprefix": "",
        "noloader": "true",
        "persoUpdateDateInMillis": "undefined",
        "LANGUAGE": "CN",
        "SITE": "J0CCJ0CC",
        "aria.panelId": "1"
    }

    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'

    headers['cookies'] = (
        'lss_loc_id=38215F612AB13F4247DB801C5DA977F44C332E4B3BD4158E147779BE6DB89E59; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        'aria_user_profile={"pref":{"LOGIN_TYPE":"STANDARD","OFFICE_ID":"LOSN82312","ACTIVE_OFFICE_ID":"LOSN82312","IS_GUEST_MODE":false,"AGENT_SIGN":"1012","AGENT_INITIALS":"WX","DUTY_CODE":"GS","USER_ALIAS":"WXIAONAN","ORGANIZATION":"NMC-NIGERI","FIRST_NAME":"WANG","LAST_NAME":"XIAONAN","PHONE_NUMBER":"+2348039943766","LANGUAGE_PREF":"EN","OCTX":"","ENABLE_CUST_NAME":false,"SERVICEMENU_AVAILABLE":true,"LIST_OFFICES":[{"officeId":"LOSN82312","customName":null}],"is_a_logout":"logout"},"firstName":"","lastName":"","gender":""}; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'um_jst=F7C91C446413AFD9E70F8AE640C6A377EFE0A7D5FB9D728616EFD0E4372DB81A; '
        '455368185956a8f748fd35f7d905a930=570f002eacd14a580ae521c04c20db1a; '
        '5bb6f21dabcc922fce10d96f5b36a932=b1f53d8e647f6f1e166516aaa0ce93f5; '
        'incap_ses_636_2643603=9c0/Im9e2x6YiwKIDIfTCMWIpGEAAAAAwIPrC/5vOD2BCVm0caQTSA==; '
        'nlbi_1658442=Mqi0GQgH6XpvOMFey0qGMAAAAACM327zpocb1AY//I1KyMs/; '
        'incap_ses_894_1658442=GCaGTItWnVb74uWXriBoDBWopGEAAAAAm4IemQ/4bZ+gAdtODCoYmg==; '
        'prxCookie=!ScJ6m/pUJ/Fzy2/PUK3QNIFO+llyZ0mVnCJjdzF8RxoG72MFsDhkbq4zw/5VYvt6fgqSKX2G7LDV9AZn0JMPP0yZ8qygPlw7uVa7umo=; '
    )


    ret, response = netget(url=url, params=params, headers=headers)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False

    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True


def user_page_UMCreateSessionKey(sessionid ):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/do/sellweb_home.taskmgr/UMCreateSessionKey;jsessionid=' + sessionid

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/do/sellweb_home.taskmgr/UMCreateSessionKey;jsessionid=' + sessionid + '?flowExKey=e5s1&&tabType=CMD&persoUpdateDateInMillis=undefined&initialAction=createCMD&LANGUAGE=CN&SITE=J0CCJ0CC&aria.target=body&aria.panelId=2'
    # params = {
    #     "flowExKey": "e5s1",
    #     "tabType": "CMD",
    #     "persoUpdateDateInMillis": "undefined",
    #     "initialAction": "createCMD",
    #     "LANGUAGE": "CN",
    #     "SITE": site,
    #     "aria.target": "body",
    #     "aria.panelId": "1"
    # }
    params = {}
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'

    headers['cookies'] = (
        'lss_loc_id=38215F612AB13F4247DB801C5DA977F44C332E4B3BD4158E147779BE6DB89E59; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        'aria_user_profile={"pref":{"LOGIN_TYPE":"STANDARD","OFFICE_ID":"LOSN82312","ACTIVE_OFFICE_ID":"LOSN82312","IS_GUEST_MODE":false,"AGENT_SIGN":"1012","AGENT_INITIALS":"WX","DUTY_CODE":"GS","USER_ALIAS":"WXIAONAN","ORGANIZATION":"NMC-NIGERI","FIRST_NAME":"WANG","LAST_NAME":"XIAONAN","PHONE_NUMBER":"+2348039943766","LANGUAGE_PREF":"EN","OCTX":"","ENABLE_CUST_NAME":false,"SERVICEMENU_AVAILABLE":true,"LIST_OFFICES":[{"officeId":"LOSN82312","customName":null}],"is_a_logout":"logout"},"firstName":"","lastName":"","gender":""}; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'um_jst=F7C91C446413AFD9E70F8AE640C6A377EFE0A7D5FB9D728616EFD0E4372DB81A; '
        '455368185956a8f748fd35f7d905a930=570f002eacd14a580ae521c04c20db1a; '
        '5bb6f21dabcc922fce10d96f5b36a932=b1f53d8e647f6f1e166516aaa0ce93f5; '
        'incap_ses_636_2643603=9c0/Im9e2x6YiwKIDIfTCMWIpGEAAAAAwIPrC/5vOD2BCVm0caQTSA==; '
        'nlbi_1658442=Wqv+dnf7ty6eFqtdy0qGMAAAAACHQftm454DOg/HhhAT8d3m; '
        'incap_ses_894_1658442=N1NidIvB9jd1IMiXriBoDF+KpGEAAAAAoVbqrDKa9Kz3PXMh5wvsrA==; '
        'prxCookie=!ovbFQ0+vHGTBUDbPUK3QNIFO+llyZ/D7z7UO0hqCoJ4EvKTXCpqBPlJ1eEHqg81ZtgUnqkZGsXWKHTPoFDztAJXho3fKM70d/D+5aYk=; '
    )


    ret, response = netget(url=url, params=params, headers=headers)
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
    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True, ENC, ENCT


def user_page_loginNewSession(ENC, ENCT):
    logger.warning('')
    logger.warning('')
    logger.warning(sys._getframe().f_code.co_name)

    url = 'https://www.booking1.sellingplatformconnect.amadeus.com/app_sell2.0/apf/do/loginNewSession.UM/login'

    params = {
        "LANGUAGE": ["CN", "CN"],
        "J0CCJ0CC": "",
        "persoUpdateDateInMillis": "undefined",
        "MARKETS": "OID_losn82312",
        "initialAction": "createCMD",
        "tabType": "CMD",
        "aria.target": "body.main.s1",
        "aria.sprefix": "s1",
        "ENC": '9CF4DB476AFDC338DFAEFBC1F91605C0F59013A316868D7ADB3407A08AF65ABC09E41C18F1842D11A2E87AE050CCF027CEFEF757ECF809742F3FEA99666F2168AD2A77C297D0CFCD985774C2695FC10FB000F7B0AF37D02391E2F31B3B94B9021893A2322DE65196965E5A982AA12D72E9F5D5E84C7C1CF5DED57CD973AA4D83F2928C5DC9537EE01AF87850227463479CED7C8E752855409EF66E0DD267534D8AF6441587B0991EE0350BFE9913620BE3D8C3E3191FE393FDFF8DA9AC1B4E8423CE77243E794D02269C6158EB2F1DBB72C9C749FA50D5FE0B01A027520AE5BE7E47A3834D5A87F47F5B6760788DEBD2B34B7AECCB6879C2C2F7F06A7EA4E01E8BF7BD0FF0E7688005E4A53BC8CC29D32F8FEC461C40CD46DC7D5F7F6DD06A13F347434B9A7CA9F6826FF4F180F238DA8D9C988D023C64BD597CA1BC9FE6AE6A2ED01D54A5730447642913974F4B358DEBE57C1220097C11A0DC95B169B22D306CB3F748D5F6A2CE7A447D9266263EF3B4450F0A6B4B90DC2D217F069488C8B3A4D780381FA977139F3CAF6A1AF2BF35A27F5F5C0B1BF596CC554A333D5F805B030A3EDDBCF4F184ABA48C9E5BF5308CF16D0064EBE7A60EB507BD2897FE1F86E1D975D32780E4B57807CA0BEF7563009DB4796CE077204B74E20AC90DDDBA329AD386CCD982DEED8F5660AF838E20C39FD98B395CC490B02E89CC86302474ECB4B5D3F69076D18FD1673316B7737E93E486FA473369C862CE172AD7E75A9BE9B47E8D3B006CC5503CBD2F176A23AC39539A23B5E71006D5C9D08DA8CC6F50C89EAFF4C8CB3120FF202AE9648A9E828771D3D2B5CDE65EDBB6368118AC2B831E6A5118CB48A47966FF6A27E7C16F095B761C6137AF98A194C447B5B6FBD23067D8F3FF1D6077B16715A913D682EC752229F42D9B8B5AE20FF9150438BE3B7E0788B5A703CF47053A9252DB44B5FA68C50BDC377D801BAEBCE7D56575FDE7D02C11C720948398B609B5386D8770AB5C03E7433E33EEDC33FD568BAA1087B0123E8820B850351324226F1134BC27D860A242187B6F8EB38A54596DA9949E08612CC583EA2A6693F4726DD2A5C90381B5A07760ACC854BBF20C1E6CDDE00894C2CB3D1CE4B3132B163FD3B3081B79935D25B075C444A48B0E6C218FD7E27105FD31848FA868555C28F3493267AAAD26D1FAFAC392AAA53B181E6FD2716BC6F871453360A4B33201DC68C796954DBA284C92FAC542B2A748F2F261818FFDABB9DD57',
        "ENCT": 1,
        "SITE": "J0CCJ0CC",
        "aria.panelId": "2"
    }
    headers = headers_base.copy()
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['x-requested-with'] = 'XMLHttpRequest'

    headers['cookies'] = (
        'lss_loc_id=38215F612AB13F4247DB801C5DA977F44C332E4B3BD4158E147779BE6DB89E59; '
        'visid_incap_2643603=DjOoKdUJQaS83l28R4BclZQgjWEAAAAAQUIPAAAAAADB3QNy7MQ4WzMSU1Iho2Il; '
        'visid_incap_1658442=OR9nS+auQ36uz4lZTq3aepUgjWEAAAAAQUIPAAAAAACoWkGaU1onx+XRGOggqwmd; '
        'aria_user_profile={"pref":{"LOGIN_TYPE":"STANDARD","OFFICE_ID":"LOSN82312","ACTIVE_OFFICE_ID":"LOSN82312","IS_GUEST_MODE":false,"AGENT_SIGN":"1012","AGENT_INITIALS":"WX","DUTY_CODE":"GS","USER_ALIAS":"WXIAONAN","ORGANIZATION":"NMC-NIGERI","FIRST_NAME":"WANG","LAST_NAME":"XIAONAN","PHONE_NUMBER":"+2348039943766","LANGUAGE_PREF":"EN","OCTX":"","ENABLE_CUST_NAME":false,"SERVICEMENU_AVAILABLE":true,"LIST_OFFICES":[{"officeId":"LOSN82312","customName":null}],"is_a_logout":"logout"},"firstName":"","lastName":"","gender":""}; '
        '_ga=GA1.2.208667559.1638024099; '
        'JSID=false; '
        'um_jst=F7C91C446413AFD9E70F8AE640C6A377EFE0A7D5FB9D728616EFD0E4372DB81A; '
        '455368185956a8f748fd35f7d905a930=570f002eacd14a580ae521c04c20db1a; '
        '5bb6f21dabcc922fce10d96f5b36a932=b1f53d8e647f6f1e166516aaa0ce93f5; '
        'nlbi_1658442=Mqi0GQgH6XpvOMFey0qGMAAAAACM327zpocb1AY//I1KyMs/; '
        'incap_ses_894_1658442=GCaGTItWnVb74uWXriBoDBWopGEAAAAAm4IemQ/4bZ+gAdtODCoYmg==; '
        'incap_ses_636_2643603=xn+NcF9hpzaJ2yKIDIfTCFeopGEAAAAAF0iVSNq5FigI7WmNZ8vAGA==; '
        'prxCookie=!GmVkvCFUqZEfJwbPUK3QNIFO+llyZ87ju77sDraTkwUInPkuTPfa5Tj74cBlOr4+n2J1xd7Z9X9baSI/5OHP2cd5T09so2to+T2qwLI=; '
    )

    ret, response = netget(url=url, params=params, headers=headers)
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
    set_cookies = response.raw.headers.getlist('Set-Cookie')
    logger.warning(set_cookies)

    return True, newsessionid, contextId


def shell_page_cryptic_execute_instruction(newsessionid, contextId, command, site):
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
    # headers['cookies'] = cookies
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
        return False, ''

    try:
        result = json.loads(response.text)['model']['output']['crypticResponse']['response']
    except json.decoder.JSONDecodeError as e:
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

        ret, sessionid, cookies_prxCookie_value = main_page_loginjsp()
        if ret == False:
            exit(-1)

        ret, cookies_prxCookie_value = main_page_XMLRequestHandler( cookies_prxCookie_value )
        if ret == False:
            exit(-1)

        ret, model, cookies_prxCookie_value = main_page_init(sessionid, cookies_prxCookie_value)
        if ret == False:
            exit(-1)

        ret, lid = main_page_embedUiLess()
        if ret == False:
            exit(-1)

        ret = login_page_init(model, lid)
        if ret == False:
            exit(-1)

        ret, accessToken = login_page_indentify(model, lid)
        if ret == False:
            exit(-1)

        while True:
            oneTimePassword = input('\noneTimePassword > ')

            if oneTimePassword.strip('') != '':
                break

    # oneTimePassword=''
    ret, newAccessToken = login_page_authenticate(model, lid, accessToken, oneTimePassword.strip(' '))
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

            ret = user_page_CreateMonoSession(sessionid)
            # if ret == False :
            #     continue


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
