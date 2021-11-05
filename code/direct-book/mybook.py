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
        logger.warning("试用期限已到...")
        return True
    return False

# 登录
def login():
    ret, config = myfile.get_config("config.login.json")
    if ret == False :
        return False, {}

    while True :
        try:
            response = requests.post(login_url, json=config, timeout=10)
        except :
            logger.warning('登录超时，重新登录 ...')
            continue

        break

    resjson = response.json()
    if resjson["success"] == True:
        logger.warning('登录成功')
        return True, resjson['sessionId']
    else:
        logger.warning('登录失败, 请检查登录配置文件 [ config.login.json ] ...')
        return False, ''

def myprint(j) :
    if "addOns" in j :
        del j["addOns"]

    if "syncData" in j:
        del j["syncData"]

    if "enablePageDown" in j:
        del j

    msg = j["message"]
    if "masks" in msg:
        del msg["masks"]

    logger.info(j)

    return j

def execute_instruction(sessionid, arg):
    cmd = {"sessionId": sessionid, "command": arg, "allowEnhanced": True}
    try :
        response = requests.post(book_url, json=cmd, timeout=10)
    except :
        logger.warning('指令执行请求超时 ...')
        return False, {}

    logger.info(response.json())
    msg = myprint(response.json())["message"]
    if response.json()["success"] == False:
        return False, msg
    logger.info
    return True, msg

# 占票
def occupy(sessionid):
    while True:
        # logger.warning(sessionid)

        if limit() == True:
            return

        if myflag.get_flag_occupied() == True:
            logger.warning("其他刷票分支已占票, 当前刷票分支退出.")
            return

        ret, msg = execute_instruction(sessionid, book_config["cmd"])
        if ret == False:
            logger.warning('占票失败')
            continue

        if 'text' in msg :
            if 'UNABLE' in msg["text"] or 'FINISH OR IGNORE TRANSACTION' in msg["text"] :
                logger.warning('前期占票命令已经执行...')
                return

        logger.warning('占票成功')
        myflag.set_flag_occupied(True)
        return



def munual_book(sessionid):
    logger.warning("进入命令行, 进行手动订票...")
    while True:
        cmd = input("\n> ")

        if cmd.strip('') == '' :
            continue

        if cmd == "exit":
            exit(0)

        ret, msg = execute_instruction(sessionid, cmd)
        if ret == False:
            logger.warning(msg)
            continue

        result = msg["text"]
        print()
        print(result)
        print(flush=True)


        if 'UNABLE - DUPLICATE SEGMENT' in result:
            logger.warning('前期占票命令已经执行...')
            continue

        if 'INVALID NAME - DUPLICATE ITEM' in result:
            logger.warning('前期客户姓名命令已经执行...')
            continue

        if 'SINGLE ITEM FIELD' in result and "R.PEI" in result:
            logger.warning('前期R.PEI命令已经执行...')
            continue

        if 'SINGLE ITEM FIELD' in result and "T.T*" in result:
            logger.warning('前期T.T*命令已经执行...')
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
            logger.warning("存档 : " + name + '-' + id)
            myfile.save(name + '-' + id, result)
            logger.warning('订票存档成功 !!!')

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

    if 'SELL OPTION HAS EXPIRED - CHECK ITINERARY' in msg["text"]:
        return False, 'SELL OPTION HAS EXPIRED - CHECK ITINERARY'

    name = book_config["user"].strip('N.').replace('/','')
    id = msg["text"].split('\n')[0].split('/')[0]
    logger.warning("存档 : " + name + '-' + id)
    myfile.save(name + '-' + id, msg["text"])
    logger.warning('订票存档成功 !!!')

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
    reqs = threadpool.makeRequests(occupy, session_list)
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
            logger.warning("请检查订票配置文件 [ config.book.json ] ...")
        else :
            logger.warning(msg)





