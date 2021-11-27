import time
import threadpool
from selenium.webdriver.common.keys import Keys

from mylog import *
import myfile
import myflag
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import UnexpectedAlertPresentException

website = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp?SITE=LOGINURL&LANGUAGE=GB'

ret, base_config = myfile.get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = myfile.get_config("config.book.json")
if ret == False :
    exit(0)

try :
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:6001")
    # browser = webdriver.Chrome(options=options)
    browser = webdriver.Chrome()
    browser.get(website)
    logger.warning('title = ' + browser.title)
except WebDriverException as e :
    logger.warning('发生错误 = ' + str(e) )
    exit(-1)

def limit():
    # 2021-11-20 00:00 此处分发给员工时， 可以自行修改， 修改后编译即可
    # pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-30 00:00', '%Y-%m-%d %H:%M'):
        logger.warning("试用期限已到...")
        return True
    return False

def wait_fun(xpath, prompt) :
    try:
        logger.warning('xpath = ' + xpath)
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException as e:
        logger.warning('等待加载 ' + prompt)
        return False, {}
    except UnexpectedAlertPresentException as e :
        logger.warning('等待加载 ' + prompt)
        return False, {}

    return True, browser.find_element_by_xpath(xpath)

def wait_element(xpath, prompt, times=0) :
    if times == 0 :
        while True:
            ret, element = wait_fun(xpath, prompt)
            if ret == True:
                logger.warning(prompt + ' 加载完成')
                return True, element

            time.sleep(1)

    for i in range(times) :
        ret, element = wait_fun(xpath, prompt)
        if ret == True :
            logger.warning(prompt + ' 加载完成')
            return True, element

        time.sleep(1)

    logger.warning(prompt + ' 未能加载完成')
    return False, {}


def login() :

    # while True :
    _, element = wait_element('//*[@id="w2_firstInput"]/span/input', '登录页面')
    element.clear()
    element.send_keys('WXIAONAN')

    _, element = wait_element('//*[@id="w2_officeId"]/span/input', '登录页面')
    element.clear()
    element.send_keys('LOSN82312')

    _, element = wait_element('//*[@id="w2_passwordInput"]/span/input', '登录页面')
    element.clear()
    element.send_keys('Tut@2020')

        # time.sleep(10)
        #
        # _, element = wait_element('//*[@id="w6"]/button', '登录页面')
        # element.click()
        #
        # ret, element = wait_element('//button[@id="etoolbar_toolbarSection_newcommandpagebtn_id"]', '新命令页按钮', 10)
        # if ret == True :
        #     break


def start_terminal() :
    _, element = wait_element('//button[@id="etoolbar_toolbarSection_newcommandpagebtn_id"]', '登录页面')
    element.click()

    wait_element('//*[@id="etaskmgr_taskBar"]/ul[2]/li[3]', '命令页 1')

    wait_element('//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]', '命令行 ')

    logger.warning('命令页面加载完成')

def execute_instruction(cmd, times=0):
    try :
        _, element = wait_element('//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]', '命令行', times)
        element.send_keys(cmd, Keys.ENTER)

    except JavascriptException as e :
        logger.warning('命令 = ' + cmd)
        logger.warning('错误 = ' + str(e))


def analysis_flight(text) :
    # text = 'AN02DECLOSFRA/ALH\n** AMADEUS AVAILABILITY - AN ** FRA FRANKFURT.DE               9 TH 02DEC 0000\n 1   LH 567  J9 C9 D9 Z9 P9 G9 E9 /LOS I FRA 1  2350    0620+1E0/333       6:30\n             N9 Y9 B9 M9 U9 H9 Q9 V9 W9 S9 T9 L9 K9'

    line2 = text.split('\n')[2].split(' ')
    line3 = text.split('\n')[3].split(' ')
    spaces = []

    for i in range(7, len(line2)):
        if len(line2[i]) == 2:
            spaces.append(line2[i])

    for i in range(13, len(line3)):
        if len(line3[i]) == 2:
            spaces.append(line3[i])

    return line2[4], line2[5], spaces

def brush_ticket(book_date, book_from, book_to, book_comp) :
    instruction = 'AN' + book_date + book_from + book_to + '/A' + book_comp
    execute_instruction(instruction)
    ret, element = wait_element('//*[@class="panel3270"]/span/pre/span[3]', '刷票', 5)
    if ret == True:
        logger.warning('\n' + element.text)

        if 'NO FLIGHT FOR THIS CITY PAIR' in element.text:
            logger.warning('刷票命令错误')

        return False, '', '', []

    _, element = wait_element(
        '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_commandResponse0" and @class="cmdResponse"]',
        '刷票')
    logger.warning('\n' + element.text)

    _, element = wait_element(
        '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_commandResponse0" and @class="cmdResponse"]/span/div/div/pre',
        '刷票')
    logger.warning('\n' + element.text)

    return analysis_flight(element.text)

def query_flight(book_comp, book_flight, comp, flight) :

    if book_comp != comp or book_flight != flight :
        logger.warning('航班不匹配, 要求航班为 [' + book_comp + book_flight + '], 找到航班为 [' + comp + flight + ']' )
        return False

    logger.warning('找到航班 [' + book_comp + book_flight + ']')
    return True


def occupy(space) :
    instruction = 'SS1' + space + '1'
    execute_instruction(instruction)

    _, element = wait_element(
        '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_commandResponse0" and @class="cmdResponse"]',
        '刷票')
    logger.warning('\n' + element.text)

    _, element = wait_element(
        '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_commandResponse0" and @class="cmdResponse"]/span/div/div/pre',
        '刷票')
    logger.warning('\n' + element.text)

    return element.text


def deal_ticket(book_comp, book_flight, space_location, book_space, line) :

    # logger.warning("space_location = %d" % space_location )
    # logger.warning("text = " + attrlist[space_location]["text"])

    logger.warning("航班 [" + book_comp + book_flight + "] 有票 : " + attrlist[space_location]["text"])

    occupy_cmd = '01' + book_space + line
    ret, msg = execute_instruction(sessionid, occupy_cmd)
    if ret == False:
        logger.warning('占票失败')
        return False

    if 'text' not in msg:
        logger.warning('占票失败')
        return False

    if 'HL' in msg["text"] or \
            'LL' in msg["text"]:
        logger.warning('占票失败')
        execute_instruction(sessionid, 'I')
        execute_instruction(sessionid, 'I')
        execute_instruction(sessionid, 'I')
        return False

    if 'HS' not in msg["text"]:
        logger.warning('占票失败')
        return False

    # HS

    logger.warning('占票成功')
    myflag.set_flag_occupied(True)

    if base_config["manual"] == True:
        return True

    ret, msg = auto_book(sessionid)
    if ret == True:
        return True

    if msg == '':
        logger.warning("请检查订票配置文件 [ config.book.json ] ...")
        return False

    logger.warning('')
    logger.warning('')
    logger.warning(msg)
    return False



if __name__ == '__main__':

    login()
    exit(0)

    myflag.set_flag_relogin(True)

    for book_config in book_config_list :

        if limit() == True:
            exit(0)

        logger.warning('\n\n开始订票为 : ' + json.dumps(book_config))

        book_date = book_config["date"]
        book_from = book_config["from"]
        book_to = book_config["to"]
        book_comp = book_config["comp"]
        book_flight = book_config["flight"]
        book_space_list = book_config["space"]

        if myflag.get_flag_relogin() == True:
            login()
            start_terminal()
            myflag.set_flag_relogin(False)

        comp, flight, spaces = brush_ticket(book_date, book_from, book_to, book_comp)

        # 没有找到对应的飞机，进行下一个客户的刷票
        if query_flight(book_comp, book_flight, comp, flight) == False :
            continue

        for space in spaces :
            booked_flag = False
            for book_space in book_space_list :

                # 判断座舱类型是否匹配
                if space[0] != book_space :
                    continue

                # 判断是否为有座票
                if space[1] >= '1' and space[1] <= '9' :
                    logger.warning('找到航班 [' + book_comp + book_flight + ']的座舱[' + space + ']')
                    ret, text = occupy(book_space)
                    if ret == False :
                        # 有位置， 但占票或订票失败，此时应当重新去刷票
                        break

                    # 如果手动订票，此处退出
                    if base_config["manual"] == True:
                        exit(0)

                    # 占票成功， 继续订票
                    booked_flag = True
                    exit(0)


            # 订完此票， 不再继续后续座位订票，
            if booked_flag == True :
                break       # 退出订后续座位循环，开始下一个客户的订票


    logger.warning('程序退出 ...\n\n')