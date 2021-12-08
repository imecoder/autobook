import time
from selenium.webdriver.common.keys import Keys

from mylog import *
import myfile
import myflag
import json
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import UnexpectedAlertPresentException

website = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp?SITE=LOGINURL&LANGUAGE=GB'


xpath_login_username = '//*[@id="w1_firstInput"]/span/input'
xpath_login_office = '//*[@id="w1_officeId"]/span/input'
xpath_login_password = '//*[@id="w1_passwordInput"]/span/input'
xpath_login_button = '//*[@id="w6"]/button'

xpath_new_shell_button = '//button[@id="etoolbar_toolbarSection_newcommandpagebtn_id"]'
xpath_shell_page = '//*[@id="etaskmgr_taskBar"]/ul[2]/li[3]'

xpath_shell = '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cshell"]/div[3]/span[2]/div/textarea[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]'
xpath_shell = '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]'
xpath_shell_result = '//*[@class="cmdResponse"]/span/div/div/pre'
xpath_shell_result = '//*[@class="cmdResponse"]/span/div/div/pre[@class="speedModePanel"]'
xpath_shell_error_result = '//div[@class="command cmdBlock"]/div[2]/span/div/div/span[1]/div/span/pre[1]/span[1]'

xpath_alert_dialog = '//*[@id="uicAlertBox"]/div[1]/div/div'
xpath_alert_ok_button = '//*[@id="uicAlertBox_ok"]'



ret, base_config = myfile.get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = myfile.get_config("config.book.json")
if ret == False :
    exit(0)



try :
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:6001")
    browser = webdriver.Chrome(options=options)
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



def wait_fun(xpath) :
    try:
        element = browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False, {}, 'NoSuchElementException'
    except UnexpectedAlertPresentException:
        return False, {}, 'UnexpectedAlertPresentException'

    return True, element, ''



def wait_element(xpath, prompt, times=0) :
    logger.warning('等待 ' + prompt + ', xpath = ' + xpath)

    if times == 0 :
        while True:
            ret, element, error = wait_fun(xpath)
            if ret == True:
                logger.warning('加载完成. element.text = ' + element.text + '\n')
                return True, element

            time.sleep(1)

    for i in range(times) :
        ret, element, error = wait_fun(xpath)
        if ret == True :
            logger.warning('加载完成. element.text = ' + element.text + '\n')
            return True, element

        time.sleep(1)

    logger.warning('未能加载完成 ' + error)
    return False, {}


def login() :

    while True :
        _, element = wait_element(xpath_login_username, '登录页面')
        element.clear()
        element.send_keys('WXIAONAN')

        _, element = wait_element(xpath_login_office, '登录页面')
        element.clear()
        element.send_keys('LOSN82312')

        _, element = wait_element(xpath_login_password, '登录页面')
        element.clear()
        element.send_keys('Tut@2020')

        time.sleep(3)

        _, element = wait_element(xpath_login_button, '登录页面')
        element.click()

        ret, element = wait_element(xpath_new_shell_button, '新命令页按钮', 10)
        if ret == True :
            break


def start_terminal() :
    _, element = wait_element(xpath_new_shell_button, '登录页面')
    element.click()

    wait_element(xpath_shell_page, '命令页 1')

    wait_element(xpath_shell, '命令行 ')

    logger.warning('命令页面加载完成')



def execute_instruction(cmd, times=0):
    try :
        if base_config["debug"] == True :
            logger.warning('cmd = ' + cmd)

        while True :
            _, element = wait_element(xpath_shell, '命令行', times)
            if element.is_displayed() == False :
                time.sleep(1)
                continue

            break

        element.send_keys(cmd, Keys.ENTER)

    except JavascriptException as e :
        logger.warning('命令 = ' + cmd)
        logger.warning('错误 = ' + str(e))




def analysis(text, sub='') :
    if 'HK1' not in text :
        return False

    if sub != '' and sub not in text :
        return False

    return True




def fast_prebook(book_comp, book_flight, book_space, book_date, book_from, book_to ) :

    execute_instruction('RT')

    while True :
        _, element = wait_element(xpath_shell_error_result,'占票')
        if len(element.text.strip()) == 0 :
            time.sleep(1)
            continue

        if 'INVALID' not in element.text :
            return analysis(element.text)

        break


    instruction = 'SS ' + book_comp + book_flight + ' ' + book_space + ' ' + book_date + ' ' + book_from + book_to + ' NN1'
    execute_instruction(instruction)
    _, element = wait_element(xpath_shell_result,'占票')

    return analysis(element.text)



def autobook(book_user, book_contact) :

    # 客户姓名
    execute_instruction(book_user)
    _, element = wait_element(xpath_shell_result,'订票')
    if analysis(element.text, book_user[3:]) == False :
        return False

    # 客户联系方式
    execute_instruction(book_contact)
    _, element = wait_element(xpath_shell_result,'订票')
    if analysis(element.text, book_contact[2:]) == False :
        return False

    # 日期
    instruction = 'TKTL/' + book_date
    execute_instruction(instruction)
    _, element = wait_element(xpath_shell_result,'订票')
    if analysis(element.text, book_date) == False :
        return False

    # 固定命令
    execute_instruction('RFPEI')
    _, element = wait_element(xpath_shell_result,'订票')
    if analysis(element.text) == False :
        return False

    # 固定命令
    execute_instruction('ER')
    _, element = wait_element(xpath_shell_result,'订票')
    if analysis(element.text) == False :
        return False

    name = book_user.strip('NM1').replace('/', '')
    id = element.text.split('\n')[1][-6:]
    logger.warning("存档 : " + name + '-' + id)
    myfile.save(name + '-' + id, element.text)
    logger.warning('订票存档成功 !!!')
    os.system(r"start /b BookInfo.exe")

    return True, ''


if __name__ == '__main__':

    myflag.set_flag_relogin(True)

    for book_config in book_config_list :

        while True :
            if limit() == True:
                exit(0)

            logger.warning('\n\n开始订票为 : ' + json.dumps(book_config))

            book_date = book_config["date"]
            book_from = book_config["from"]
            book_to = book_config["to"]
            book_comp = book_config["comp"]
            book_flight = book_config["flight"]
            book_space = book_config["space"][0]
            book_user = book_config["user"]
            book_contact = book_config["contact"]

            if myflag.get_flag_relogin() == True:
                login()
                start_terminal()
                myflag.set_flag_relogin(False)

            # 快速预定失败的话， 继续进行下一个用户的订票
            if fast_prebook(book_comp, book_flight, book_space, book_date, book_from, book_to ) == False :
                continue

            # 开始执行订票流程
            if autobook(book_user, book_contact) == True :
                break


    logger.warning('程序退出 ...\n\n')