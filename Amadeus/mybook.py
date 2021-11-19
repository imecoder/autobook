import time
import threadpool
from mylog import *
import myfile
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

website = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp?SITE=LOGINURL&LANGUAGE=GB'

ret, base_config = myfile.get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = myfile.get_config("config.book.json")
if ret == False :
    exit(0)

browser = webdriver.Chrome()
browser.get(website)

def limit():
    # 2021-11-20 00:00 此处分发给员工时， 可以自行修改， 修改后编译即可
    # pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-30 00:00', '%Y-%m-%d %H:%M'):
        logger.warning("试用期限已到...")
        return True
    return False

def wait_element(element, string) :
    while True :
        time.sleep(1)

        try:
            browser.find_element_by_xpath("//*[@id='w2_firstInput']/span/input")
        except NoSuchElementException as e:
            print('等待加载' + string + '页面')
            continue
        break

    print('登录' + string + '加载完成')

def login() :

    wait_element("//*[@id='w2_firstInput']/span/input", '登录')

    browser.find_element_by_xpath("//*[@id='cookiebanner_cookiebanner_cookieBannerAcceptButton']/button").click()
    browser.find_element_by_xpath("//*[@id='w2_firstInput']/span/input").send_keys('WXIAONAN')
    browser.find_element_by_xpath("//*[@id='w2_officeId']/span/input").send_keys('LOSN82312')
    browser.find_element_by_xpath("//*[@id='w2_passwordInput']/span/input").send_keys('Tut@2020')

# time.sleep(1)
# browser.find_element_by_xpath("//*[@id='w7']/button/span/span[2]/span").click()
# time.sleep(4)
# browser.find_element_by_xpath("//*[@id='w7']/button/span/span[2]/span").click()
# print('click over')
#
#
# for i in range(10) :
#     time.sleep(1)
#     try:
#         element = browser.find_element_by_xpath("//*[@id='w2_otpInput']/label")
#     except NoSuchElementException as e:
#         print('等待出现一次性密码')
#         continue
#
#     print('得到结果 = ', element.text)
#     onecode = input('请输入一次性密码 ：')
#     break
#
# if onecode != '' :
#     browser.find_element_by_xpath("//*[@id='w2_firstInput']/span/input").send_keys('WXIAONAN')
#     browser.find_element_by_xpath("//*[@id='w2_officeId']/span/input").send_keys('LOSN82312')
#     browser.find_element_by_xpath("//*[@id='w2_passwordInput']/span/input").send_keys('Tut@2020')
#     browser.find_element_by_xpath("//*[@id='w2_otpInput']/span/input").send_keys(onecode)
#
#
# time.sleep(1)
# browser.find_element_by_xpath("//*[@id='w7']/button/span/span[2]/span").click()
# time.sleep(4)
# browser.find_element_by_xpath("//*[@id='w7']/button/span/span[2]/span").click()
# print('click over')
#
#
#

def start_cmd_page() :
    while True :
        time.sleep(1)

        try:
            cmdbutton = browser.find_element_by_xpath("//*[@id='etoolbar_toolbarSection_newcommandpagebtn_id']")
        except NoSuchElementException as e:
            print('等待加载主页面')
            continue
        break


    print('主页面加载完成, 启动5个页面 ...')
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='cookiebanner_cookiebanner_cookieBannerAcceptButton']/button").click()
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='ngb-popover-1']/div[2]/div/button").click()
    time.sleep(2)
    for i in range(5) :
        time.sleep(1)
        cmdbutton.click()

        while True :
            time.sleep(1)

            try:
                xpath = "//*[@id=cryptics'" + str(i) + "_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput']"
                browser.find_element_by_xpath(xpath)
            except NoSuchElementException as e:
                print('等待加载' + str(i) + '命令页面')
                continue
            break

        print('命令页面' + str(i) + '加载完成')

    print('全部命令页面加载完成')



def execute_instruction(page, cmd):
    logger.warning("命令 = " + cmd)
    js = 'var ucode = document.getElementById("cryptics' + str(page) + '_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"); ucode.value=arguments[0]'
    return browser.execute_script(js,cmd)






if __name__ == '__main__':

    branch_size = base_config["branch_size"]

    login()
    start_cmd_page()
    execute_instruction(1, "AN02DECLOSFRA/ALH")
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

# //*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]
# //*[@id="cryptics2_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]
# //*[@id="cryptics3_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]

browser.find_element_by_xpath("//*[@id='eusermanagement_logout_logo_logout_id']").click()
browser.find_element_by_xpath("//*[@id='uicAlertBox_ok']").click()

