import time
import threadpool
from selenium.webdriver.common.keys import Keys

from mylog import *
import myfile
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, JavascriptException

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

def wait_fun(element, string) :
    time.sleep(1)

    try:
        logger.warning('element = ' + element)
        browser.find_element_by_xpath(element)
    except NoSuchElementException as e:
        logger.warning('等待加载 ' + string)
        return False

    return True

def wait_element(element, string, times) :
    if times == 0 :
        while not wait_fun(element, string):
            pass

        logger.warning(string + ' 加载完成')
        return

    for i in range(times) :
        if wait_fun(element, string) == True :
            logger.warning(string + ' 加载完成')
            break

    logger.warning(string + ' 未能加载完成')


def login() :

    element = '//*[@id="w1_firstInput"]/span/input'
    wait_element(element, '登录页面', 0)
    browser.find_element_by_xpath(element).clear()
    browser.find_element_by_xpath(element).send_keys('WXIAONAN')

    element = '//*[@id="w1_officeId"]/span/input'
    wait_element(element, '登录页面', 0)
    browser.find_element_by_xpath(element).clear()
    browser.find_element_by_xpath(element).send_keys('LOSN82312')

    element = '//*[@id="w1_passwordInput"]/span/input'
    wait_element(element, '登录页面', 0)
    browser.find_element_by_xpath(element).clear()
    browser.find_element_by_xpath(element).send_keys('Tut@2020')


def start_cmd_page(size) :
    logger.warning('启动 ' + str(size) + ' 个命令页面 ...')

    new_cmdpage_element = "//*[@id='etoolbar_toolbarSection_newcommandpagebtn_id']"
    wait_element(new_cmdpage_element, '新命令页按钮', 0)

    for i in range(size) :
        time.sleep(1)
        browser.find_element_by_xpath(new_cmdpage_element).click()

        cmdline_element = "//*[@id='cryptics" + str(i+1) + "_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput']"
        wait_element(cmdline_element, '命令页'+str(i+1), 0)

    logger.warning('全部命令页面加载完成')



def execute_instruction(page, cmd):
    try :
        page_element = '//*[@id="etaskmgr_taskBar"]/ul[2]/li['+ str(page+2) +']'
        browser.find_element_by_xpath(page_element).click()

        cmdline_element = "//*[@id='cryptics" + str(page) + "_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput']"
        wait_element(cmdline_element, '命令页'+str(page), 0)
        browser.find_element_by_xpath(cmdline_element).send_keys(cmd, Keys.ENTER)

    except JavascriptException as e :
        logger.warning('命令 = ' + cmd)
        logger.warning('错误 = ' + str(e))

if __name__ == '__main__':

    branch_size = base_config["branch_size"]

    login()
    start_cmd_page(branch_size)
    execute_instruction(1, "AN02DECLOSFRA/ALH")
    execute_instruction(2, "AN02DECLOSFRA/ALH")
    #
    # book_list = []
    # for i in range(branch_size):
    #     book_list.append({"sessionid": sessionid, "config": book_config})
    #
    # pool = threadpool.ThreadPool(branch_size)
    # reqs = threadpool.makeRequests(occupy, book_list)
    # for req in reqs:
    #     pool.putRequest(req)
    #     time.sleep(1 / branch_size)
    # pool.wait()

