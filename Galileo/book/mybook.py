#!/usr/bin/python

import time
import requests
import threadpool
import urllib3

from mylog import *
import myflag
import myfile
import json
import os

login_url = 'https://webagentapp.tts.com/TWS/Login'
book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'

ret, base_config = myfile.get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = myfile.get_config("config.book.json")
if ret == False :
    exit(0)


def limit():
    # 2021-11-20 00:00 我是
    # pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-30 00:00', '%Y-%m-%d %H:%M'):
        logger.warning("试用期限已到...")
        return True
    return False

def netaccess(url, js, key) :
    try:
        response = requests.post(url, json=js, timeout=100)
        if base_config["debug"] :
            logger.info(response.text)
    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {}
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {}

    try:
        thejson = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        # logger.warning('-------------------------------\n' + response.text)
        return False, {}

    if thejson["success"] == False:
        return False, {}

    if key not in thejson :
        return False, {}

    return True, thejson[key]

# 登录
def login():
    # 此处分发给员工时， 可以自行修改， 修改后编译即可
    # pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py
    # login_config = {"son": "Z7LJ2/WX", "pcc": "7LJ2", "pwd": "LLP0605", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/WP", "pcc": "7LJ2", "pwd": "BANANA12", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/FG", "pcc": "7LJ2", "pwd": "PLANTAIN12", "gds": "Galileo"}
    login_config = {"son": "Z7LJ2/LL", "pcc": "7LJ2", "pwd": "PLL0605", "gds": "Galileo"}

    logger.warning('')
    logger.warning('')
    logger.warning('登录账户 = ' + json.dumps(login_config))

    while True :
        ret, sessionid = netaccess(login_url, login_config, "sessionId")
        if ret == False :
            logger.warning('登录失败, 请确认您的登录账户信息 ...')
            time.sleep(3)
            continue

        logger.warning('登录成功')

        execute_instruction(sessionid, "I")
        execute_instruction(sessionid, "I")
        execute_instruction(sessionid, "I")

        return sessionid

def execute_instruction(sessionid, arg):
    logger.warning("命令 = " + arg)
    cmd = {"sessionId": sessionid, "command": arg, "allowEnhanced": True}
    return netaccess(book_url, cmd, "message")

def query_airline(book_date, book_from, book_to, book_comp) :
    scan_cmd = 'A' + book_date + book_from + book_to + '/' + book_comp
    ret, msg = execute_instruction(sessionid, scan_cmd)
    if ret == False:
        myflag.set_flag_relogin(True)
        if 'text' not in msg:
            logger.warning('刷票失败')
        else:
            logger.warning('发现错误 : ' + msg["text"])
        return False, []

    if 'text' not in msg:
        logger.warning('刷票失败')
        return False, []

    if 'DEPARTED' in msg["text"]:
        logger.warning("请确认是否航班已经过期 ...")
        return False, []

    if 'SYSTEM ERROR' in msg["text"] \
            or 'Session does not exist' in msg["text"]:
        logger.warning('掉线重新登录')
        myflag.set_flag_relogin(True)
        return False, []

    attrlist = msg["masks"]["special"]["attrList"]
    return True, attrlist

def query_flight(attrlist, book_comp, book_flight) :
    # 查找 book_comp, book_flight
    comp_flight_location = len(attrlist)
    for i in range(len(attrlist)):
        # logger.warning(str(i) + ' ' + attrlist[i]["text"] + attrlist[i+1]["text"])
        if "text" in attrlist[i] \
                and attrlist[i]["text"] == book_comp \
                and "text" in attrlist[i + 1] \
                and attrlist[i + 1]["text"].strip() == book_flight:
            comp_flight_location = i
            break

    if comp_flight_location >= len(attrlist):
        logger.warning('未找到航班 [' + book_comp + book_flight + ']')
        return False, 0, 0

    line = attrlist[comp_flight_location - 8]["text"]
    # logger.warning("comp_flight_location = %d" % comp_flight_location )
    logger.warning('找到航班 [' + book_comp + book_flight + ']，位于行 [' + line + ']')
    return True, line, comp_flight_location

def query_space_end_location(attrlist, line, comp_flight_location) :
    lineplus = str(int(line) + 1)
    lineplus_start_location = comp_flight_location
    for i in range(comp_flight_location, len(attrlist)):
        if "text" in attrlist[i] and attrlist[i]["text"] == lineplus:
            lineplus_start_location = i
            break

    end_location = len(attrlist)
    if lineplus_start_location < len(attrlist):
        # logger.warning("lineplus_start_location = %d" % lineplus_start_location)
        # logger.warning('找到第二个航班')
        end_location = lineplus_start_location - 1

    return end_location

def deal_ticket(attrlist, book_comp, book_flight, space_location, book_space, line) :

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

def quick_booking(book_comp, book_flight, book_space, book_date, book_from, book_to) :
    logger.warning("航班 [" + book_comp + book_flight + "] 不可候补, 执行快速预订")

    while True:
        quick_booking_cmd = 'N ' + book_comp + book_flight + ' ' + book_space + ' ' + book_date + ' ' + book_from + book_to + ' NN1'
        ret, msg = execute_instruction(sessionid, quick_booking_cmd)
        if ret == False:
            logger.warning('占票失败')
            continue

        if 'text' not in msg:
            logger.warning('占票失败')
            return False

        if 'SYSTEM ERROR' in msg["text"] \
                or 'Session does not exist' in msg["text"]:
            logger.warning('掉线重新登录')
            myflag.set_flag_relogin(True)
            return False

        if '*0 AVAIL/WL CLOSED*' in msg["text"]:
            logger.warning('票面关闭中')
            continue

        if '*SELL RESTRICTED*' in msg["text"]:
            logger.warning('票面禁止销售')
            continue

        if 'HL' in msg["text"] or \
                'LL' in msg["text"]:
            logger.warning(msg['text'])
            return False

        # HS
        if 'HS' in msg["text"]:
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

    return True

def query_space(attrlist, book_space_list, line_start_location, line_end_location, book_comp, book_flight) :
    space_list = {}

    # 枚举所有的座舱类型
    for book_space in book_space_list:

        space_list[book_space] = {
            "location": line_end_location,
            "status": 'N'
        }

        # 查找座舱所在位置, 以及座舱的状态
        for i in range(line_start_location, line_end_location):

            if "extended" not in attrlist[i]:
                continue

            if "bic" not in attrlist[i]["extended"]:
                continue

            if attrlist[i]["extended"]["bic"] != book_space:
                continue

            space_list[book_space]["location"] = i
            status = attrlist[i]["extended"]["status"]
            space_list[book_space]["status"] = status

            logger.warning('找到航班 [' + book_comp + book_flight + ']的座舱[' + book_space + status + ']')
            break


def all_N(space_list, line_end_location, book_comp, book_flight) :

    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != line_end_location and status != 'N':
            return False

        logger.warning('找到航班 [' + book_comp + book_flight + ']的座舱类型[' + book_space + status + ']')

    return True




# 占票
def occupy(book_list):
    sessionid = book_list["sessionid"]
    book_config = book_list["config"]

    book_date = book_config["date"]
    book_from = book_config["from"]
    book_to = book_config["to"]
    book_comp = book_config["comp"]
    book_flight = book_config["flight"]
    book_space_list = book_config["space"]

    while True:
        # logger.warning(sessionid)

        if limit() == True:
            return

        if myflag.get_flag_occupied() == True:
            logger.warning("其他刷票分支已占票, 当前刷票分支退出.")
            return

        if myflag.get_flag_relogin() == True:
            logger.warning("其他刷票分支出错, 当前刷票分支退出.")
            return

        # 查询匹配的航线
        ret, attrlist = query_airline(book_date, book_from, book_to, book_comp)
        if ret == False :
            return

        # 查询匹配的航班
        ret, line, comp_flight_location = query_flight(attrlist, book_comp, book_flight)
        if ret == False :
            return

        # 航班行的开始位置
        line_start_location = comp_flight_location+2

        # 查找匹配的航班结束的位置，即text: line + 1 位置
        line_end_location = query_space_end_location(attrlist, line, comp_flight_location)

        # 查找 book_space_list 的位置, 及状态
        space_list = query_space(attrlist, book_space_list, line_start_location, line_end_location, book_comp, book_flight)

        # 如果所有仓位状态都是N，重新循环刷票
        if all_N(space_list, line_end_location, book_comp, book_flight) == True :
            continue

        # 处理所有的占座及订座

        # 处理有座状态
        has_ticket = False
        for book_space in space_list:
            location = space_list[book_space]["location"]
            status = space_list[book_space]["status"]
            if location == line_end_location or status == 'N' :
                continue

            # 有位置, 立即占票及订票
            if status >= "1" and status <= "9":
                has_ticket = True
                ret = deal_ticket(attrlist, book_comp, book_flight, line_end_location, book_space, line)
                if ret == True :
                    return

                # 有位置， 但占票或订票失败，此时应当重新去刷票
                break # ------------------------


        # 有位置的情况下， 但未能占票或订票成功，重新去刷票
        if has_ticket == True :
            continue

        # 刷票+占票模式，不进行快速预定，重新去刷票
        if base_config["mode"] == 0:
            continue

        # 刷票+占票+快速预定模式下，处理带有C状态的票
        for book_space in space_list:
            location = space_list[book_space]["location"]
            status = space_list[book_space]["status"]
            if location == line_end_location or status == 'N':
                continue

            # 找到了对应仓位，但候补关闭，刷票+占票+快速预定模式下，执行快速预订
            if status == 'C' :
                ret = quick_booking(book_comp, book_flight, book_space, book_date, book_from, book_to)
                if ret == True :
                    return

                if myflag.get_flag_relogin() == True :
                    return

                break

        # 候补状态，L, 0 等等重新刷票



def munual_book(sessionid):
    logger.warning("进入命令行, 进行手动订票...")
    while True:
        cmd = input("\n> ")

        if cmd.strip('') == '' :
            continue

        if cmd == "loop":
            break

        if cmd == "exit":
            exit(0)

        ret, msg = execute_instruction(sessionid, cmd)
        if ret == False:
            logger.warning(msg)
            continue

        text = msg["text"]
        print()
        print(text)
        print(flush=True)


        if 'UNABLE - DUPLICATE SEGMENT' in text:
            logger.warning('前期占票命令已经执行...')
            continue

        if 'INVALID NAME - DUPLICATE ITEM' in text:
            logger.warning('前期客户姓名命令已经执行...')
            continue

        if 'SINGLE ITEM FIELD' in text and "R.PEI" in text:
            logger.warning('前期R.PEI命令已经执行...')
            continue

        if 'SINGLE ITEM FIELD' in text and "T.T*" in text:
            logger.warning('前期T.T*命令已经执行...')
            continue

        if cmd == "ER":
            if "SELL OPTION HAS EXPIRED - CHECK ITINERARY" in text :
                continue

            if 'NEED RECEIVED' in text:
                continue

            if 'MODIFY BOOKING' in text:
                continue

            name = book_config["user"].strip('N.').replace('/','')
            id = text.split('\n')[0].split('/')[0]
            logger.warning("存档 : " + name + '-' + id)
            myfile.save(name + '-' + id, text)
            logger.warning('订票存档成功 !!!')
            os.system(r"start /b BookInfo.exe")

    return True

def auto_book(sessionid):
    # 客户姓名
    ret, msg = execute_instruction(sessionid, book_config["user"])
    if ret == False :
        logger.warning(msg)
        return False, ''

    if 'text' in msg and 'INVALID NAME - DUPLICATE ITEM' in msg["text"]:
        logger.warning('前期客户姓名命令已经执行...')


    # 客户联系方式
    ret, msg = execute_instruction(sessionid, book_config["contact"])
    if ret == False :
        logger.warning(msg)
        return False, ''

    if 'text' in msg and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in msg["text"]:
        logger.warning('前期客户电话命令已经执行...')

    # R.PEI
    ret, msg = execute_instruction(sessionid, "R.PEI")
    if ret == False:
        logger.warning(msg)
        return False, ''

    if 'text' in msg and 'SINGLE ITEM FIELD' in msg["text"]:
        logger.warning('前期R.PEI命令已经执行...')

    # T.T*
    ret, msg = execute_instruction(sessionid, "T.T*")
    if ret == False:
        logger.warning(msg)
        return False, ''

    if 'text' in msg and 'SINGLE ITEM FIELD' in msg["text"]:
        logger.warning('前期T.T*命令已经执行...')

    # ER
    ret, msg = execute_instruction(sessionid, "ER")
    if ret == False:
        logger.warning(msg)
        return False, ''

    if 'HK' not in msg["text"]:
        return False, msg["text"]

    name = book_config["user"].strip('N.').replace('/','')
    id = msg["text"].split('\n')[0].split('/')[0]
    logger.warning("存档 : " + name + '-' + id)
    myfile.save(name + '-' + id, msg["text"])
    logger.warning('订票存档成功 !!!')
    os.system(r"start /b BookInfo.exe")

    execute_instruction(sessionid, "I")
    execute_instruction(sessionid, "I")
    execute_instruction(sessionid, "I")

    return True, ''


if __name__ == '__main__':

    branch_size = base_config["branch_size"]

    for book_config in book_config_list :

        logger.warning('')
        logger.warning('')
        logger.warning('开始订票 = ' + json.dumps(book_config))

        while True :
            if limit() == True:
                exit(0)

            myflag.set_flag_relogin(False)
            myflag.set_flag_occupied(False)

            sessionid = login()

            book_list = []
            for i in range(branch_size):
                book_list.append({"sessionid" : sessionid, "config" : book_config })

            pool = threadpool.ThreadPool(branch_size)
            reqs = threadpool.makeRequests(occupy, book_list)
            for req in reqs:
                pool.putRequest(req)
                time.sleep(1 / branch_size)
            pool.wait()

            if myflag.get_flag_relogin() == True:
                continue

            if myflag.get_flag_occupied() == False:
                break

            if base_config["manual"] == True:
                if munual_book(sessionid) == True :
                    break

                exit(0)

            break

    logger.warning('程序退出 ...')
    logger.warning('')
    logger.warning('')
