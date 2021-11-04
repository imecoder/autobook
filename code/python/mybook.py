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

def get_space(flight):
    flight_airtype = myfile.get_config("config.flight.airtype.json")
    if flight not in flight_airtype:
        logger.info("未找到为航班" + flight + "配置的飞机类型 .")
        return False, []

    airtype = flight_airtype[flight]
    if airtype == "":
        logger.info("未找到为航班" + flight + "配置的飞机类型 .")
        return False, []

    airtype_space = myfile.get_config("config.airtype.space.json")
    if airtype not in airtype_space:
        logger.info("未找到为机型" + airtype + "配置的舱位 .")
        return False, []

    space = airtype_space[airtype]
    if space == []:
        logger.info("未找到为机型" + airtype + "配置的舱位 .")
        return False, []

    return True, space

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

        if myflag.get_flag_space() == False:
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
        flight = attrlist[16]["text"] + attrlist[17]["text"].strip()
        logger.info('查询到航班' + flight)

        # 确定本地舱位配置
        ret, space = get_space(flight)
        if ret == False:
            myflag.set_flag_space(False)
            logger.info("尚未配置舱位, 请退出后, 联系开发人员进行配置...")
            return

        # 查找带票仓位
        flagHasTicket = False
        for i in range(len(space)):
            if "extended" not in attrlist[space[i]] :
                logger.info("配置舱位有误, 请退出后, 联系开发人员进行配置...")
                return

            if "status" not in attrlist[space[i]]["extended"] :
                logger.info("配置舱位有误, 请退出后, 联系开发人员进行配置...")
                return

            status = attrlist[space[i]]["extended"]["status"]
            if (status >= "1" and status <= "9"):
                flagHasTicket = True

        if flagHasTicket == False:
            logger.info("航班无票")
            continue

        logger.info("航班" + flight + "有票")

        if myflag.get_flag_occupied() == True:
            logger.info("其他刷票分支已占票, 当前刷票分支退出.")
            return

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

    if myflag.get_flag_space() == False:
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





