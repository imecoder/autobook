#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import time
import requests
import threadpool
from mylog import *
import myflag
import myfile

login_url = 'https://webagentapp.tts.com/TWS/Login'
book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'

ret, book_config = myfile.get_config("config.book.json")
if ret == False :
    exit(0)


def limit():
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-6 00:00', '%Y-%m-%d %H:%M'):
        logger.info("试用期限已到...")
        return True
    return False

# 登录
def login():
    ret, config = myfile.get_config("config.login.json")
    if ret == False :
        return False, {}

    try:
        response = requests.post(login_url, json=config, timeout=10)
    except :
        logger.info('请确认是否打开VPN, 如果打开请关闭 ...')
        return False, {}

    logger.debug(response.text)
    resjson = response.json()
    if resjson["success"] == True:
        logger.info('登录成功')
        return True, resjson['sessionId']
    else:
        logger.info('登录失败, 请检查登录配置文件 [ config.login.json ] ...')
        return False, ''

def execute_instruction(sessionid, arg):
    cmd = {"sessionId": sessionid, "command": arg, "allowEnhanced": True}
    try :
        response = requests.post(book_url, json=cmd, timeout=10)
    except :
        logger.info('请确认是否打开VPN, 如果打开请关闭 ...')
        return False, {}

    logger.debug(response.text)
    msg = response.json()["message"]
    if response.json()["success"] == False:
        return False, msg

    return True, msg

# 占票
def occupy(sessionid):
    ret, msg = execute_instruction(sessionid, book_config["occupy"])
    if ret == False:
        logger.info('占票失败')
        return False

    if 'text' in msg and 'UNABLE - DUPLICATE SEGMENT' in msg["text"]:
        logger.info('前期占票命令已经执行...')
        return True

    logger.info('占票成功')
    return True


# 查票
def query(sessionid):
    while True:
        # logger.info(sessionid)

        if limit() == True:
            return

        if myflag.get_flag_occupied() == True:
            logger.info("其他刷票分支已占票, 当前刷票分支退出.")
            return

        # 查航线
        cmd = 'A' + book_config["date"] + book_config["from"] + book_config["to"] + '*' + book_config["comp"];
        # logger.info(cmd)
        ret, msg = execute_instruction(sessionid, cmd)
        if ret == False:
            logger.info('航线查询失败')
            return

        attrlist = msg["masks"]["special"]["attrList"]

        # 确定航班

        # 查找 text : line 位置
        line = book_config["occupy"][3:]
        start_location = len(attrlist)
        for i in range(len(attrlist)):
            if "text" in attrlist[i] and attrlist[i]["text"] == line :
                start_location = i
                break

        if start_location >= len(attrlist) :
            logger.info('未找到任何航班')
            continue

        # logger.info("start_location = %d" % start_location )

        # 查找 text : comp 位置
        comp_start_location = start_location
        for i in range(start_location, len(attrlist)):
            if "text" in attrlist[i] and attrlist[i]["text"] == book_config["comp"] :
                comp_start_location = i
                break

        if comp_start_location >= len(attrlist) :
            logger.info('未找到任何航班')
            continue

        # logger.info("comp_start_location = %d" % comp_start_location )

        flight = attrlist[comp_start_location]["text"] + attrlist[comp_start_location+1]["text"].strip()
        logger.info('查询到航班' + flight)


        # 查找 text: line + 1 位置
        lineplus = str(int(line) +1)
        lineplus_start_location = comp_start_location
        for i in range(comp_start_location, len(attrlist)):
            if "text" in attrlist[i] and attrlist[i]["text"] == lineplus :
                lineplus_start_location = i
                break


        end_location = len(attrlist)
        if lineplus_start_location < len(attrlist) :
            # logger.info("lineplus_start_location = %d" % lineplus_start_location)
            # logger.info('找到第二个航班')
            end_location = lineplus_start_location-1

        # 查找 spacetype 的位置, 及状态
        space_start_location = comp_start_location+2
        space_location = end_location
        spacetype = book_config["occupy"][2:3]
        flagHasTicket = False

        for i in range(space_start_location, end_location):
            if "extended" in attrlist[i] :
                if "bic" in attrlist[i]["extended"] :
                    if attrlist[i]["extended"]["bic"] == spacetype :
                        space_location = i
                        status = attrlist[space_location]["extended"]["status"]
                        if status >= "1" and status <= "9":
                            flagHasTicket = True

                        break

        # logger.info("space_location = %d" % space_location )
        # logger.info("text = " + attrlist[space_location]["text"])

        if flagHasTicket == False:
            logger.info("航班" + flight + "无票")
            continue

        logger.info("航班" + flight + "有票 : ", attrlist[space_location]["text"])

        if myflag.get_flag_occupied() == True:
            logger.info("其他刷票分支已占票, 当前刷票分支退出.")
            return

        # 占票
        myflag.set_flag_occupied(occupy(sessionid))
        if myflag.get_flag_occupied() == True:
            return

def munual_book(sessionid):
    logger.info("进入命令行, 进行手动订票...")
    while True:
        cmd = input("\n> ")

        if cmd.strip('') == '' :
            continue

        if cmd == "exit":
            exit(0)

        ret, msg = execute_instruction(sessionid, cmd)
        if ret == False:
            logger.info(msg)
            continue

        result = msg["text"]
        print()
        print(result)
        print(flush=True)


        if 'UNABLE - DUPLICATE SEGMENT' in result:
            logger.info('前期占票命令已经执行...')
            continue

        if 'INVALID NAME - DUPLICATE ITEM' in result:
            logger.info('前期客户姓名命令已经执行...')
            continue

        if 'SINGLE ITEM FIELD' in result and "R.PEI" in result:
            logger.info('前期R.PEI命令已经执行...')
            continue

        if 'SINGLE ITEM FIELD' in result and "T.T*" in result:
            logger.info('前期T.T*命令已经执行...')
            continue

        if cmd == "ER":
            if "SELL OPTION HAS EXPIRED - CHECK ITINERARY" in result :
                continue

            if 'NEED RECEIVED' in result:
                continue

            if 'MODIFY BOOKING' in result:
                continue

            name = book_config["user"].strip('N.').replace('/','')
            id = result.split('\n')[0].split('/')[0]
            logger.info("存档 : " + name + '-' + id)
            myfile.save(name + '-' + id, result)
            logger.info('订票存档成功 !!!')

def auto_book(sessionid):
    # 客户姓名
    ret, msg = execute_instruction(sessionid, book_config["user"])
    if ret == False :
        logger.info(msg)
        return False, ''

    if 'text' in msg and 'INVALID NAME - DUPLICATE ITEM' in msg["text"]:
        logger.info('前期客户姓名命令已经执行...')


    # 客户联系方式
    ret, msg = execute_instruction(sessionid, book_config["contact"])
    if ret == False :
        logger.info(msg)
        return False, ''

    if 'text' in msg and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in msg["text"]:
        logger.info('前期客户电话命令已经执行...')

    # R.PEI
    ret, msg = execute_instruction(sessionid, "R.PEI")
    if ret == False:
        logger.info(msg)
        return False, ''

    if 'text' in msg and 'SINGLE ITEM FIELD' in msg["text"]:
        logger.info('前期R.PEI命令已经执行...')

    # T.T*
    ret, msg = execute_instruction(sessionid, "T.T*")
    if ret == False:
        logger.info(msg)
        return False, ''

    if 'text' in msg and 'SINGLE ITEM FIELD' in msg["text"]:
        logger.info('前期T.T*命令已经执行...')

    # ER
    ret, msg = execute_instruction(sessionid, "ER")
    if ret == False:
        logger.info(msg)
        return False, ''

    if 'SELL OPTION HAS EXPIRED - CHECK ITINERARY' in msg["text"]:
        return False, 'SELL OPTION HAS EXPIRED - CHECK ITINERARY'

    name = book_config["user"].strip('N.').replace('/','')
    id = msg["text"].split('\n')[0].split('/')[0]
    logger.info("存档 : " + name + '-' + id)
    myfile.save(name + '-' + id, msg["text"])
    logger.info('订票存档成功 !!!')

    execute_instruction(sessionid, "I")
    execute_instruction(sessionid, "I")
    execute_instruction(sessionid, "I")

    return True, ''


if __name__ == '__main__':

    if limit() == True:
        exit(0)

    ret, sessionid = login()
    if ret == False :
        exit(0)

    ret, config = myfile.get_config("config.branch.json")
    if ret == False :
        exit(0)

    size = config["size"]

    session_list = []
    for i in range(size):
        session_list.append(sessionid)

    pool = threadpool.ThreadPool(size)
    reqs = threadpool.makeRequests(query, session_list)
    for req in reqs:
        pool.putRequest(req)
        time.sleep(1 / size)
    pool.wait()

    if myflag.get_flag_occupied() == False:
        exit(0)

    if book_config["manual"] == True:
        munual_book(sessionid)
        exit(0)

    ret, msg = auto_book(sessionid)
    if ret == False:
        if msg == '' :
            logger.info("请检查订票配置文件 [ config.book.json ] ...")
        else :
            logger.info(msg)





