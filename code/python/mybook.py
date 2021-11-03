#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import time
import requests
import json
import threading
import threadpool
import sys
import logging
import msvcrt

fmt = logging.Formatter('%(asctime)s - [%(lineno)3.3d] %(threadName)-10.10s: %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(fmt)
ch.setLevel(logging.INFO)
fh = logging.FileHandler(filename="log_%s.txt"%(datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')), mode='a', encoding='utf-8')
fh.setFormatter(fmt)
fh.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(ch)
logger.addHandler(fh)


login_url = 'https://webagentapp.tts.com/TWS/Login'
book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'

flagQueryAllFlight = True
flagQueryDestFlight = True
flagSpace = True
flagBook = False
flagOccupied = False

# 读取订票配置文件
with open("config.book.json", 'r') as thefile:
    book_config = json.load(thefile)


def limit() :
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-4 00:00', '%Y-%m-%d %H:%M'):
        logger.info("试用期限已到...")
        return True
    return False

# 登录
def login():
    with open("config.login.json", 'r') as thefile:
        config = json.load(thefile)
    response = requests.post(login_url, json=config)
    logger.info(response.text)
    resjson = response.json()
    if (resjson["success"] == True):
        logger.info('')
        logger.info('登录成功')
        return resjson['sessionId']
    else:
        logger.info('登录失败, 请重新配置登录配置文件, 按任意键退出...')
        msvcrt.getch()
        exit(0)

def invoke(sessionid, arg) :
    cmd = {"sessionId": sessionid, "command": arg, "allowEnhanced": True}
    response = requests.request("POST", book_url, json=cmd)
    logger.info(response.text)
    resjson = response.json()
    if (resjson["success"] != True):
        logger.info('指令返回失败')
        return False, resjson
    return True, resjson["message"]


def save(name, message) :
    fo = open(name + '.txt', "w")
    fo.write(message)
    fo.close()

def autobook( sessionid ) :
    ret, msg = invoke(sessionid, book_config["user"] )
    if ret != True :
        logger.info('订票失败')
        return False

    ret, msg = invoke(sessionid, book_config["contact"] )
    if ret != True :
        logger.info('订票失败')
        return False

    ret, msg = invoke(sessionid, "R.PEI" )
    if ret != True :
        logger.info('订票失败')
        return False

    ret, msg = invoke(sessionid, "T.T*" )
    if ret != True :
        logger.info('订票失败')
        return False

    ret, msg = invoke(sessionid, "ER" )
    if ret != True :
        logger.info('订票失败')
        return False

    save(book_config["user"], msg["text"])


# 占票
def occupy(sessionid):
    global flagBook
    global flagOccupied

    ret, msg = invoke(sessionid, book_config["occupy"] )
    if ret != True :
        logger.info('占票失败')
        flagBook = False
        return

    if book_config["autobook"] == True :
        flagOccupied = True
        logger.info('票已占, 请继续未用户订票流程 ...')
        return

    if autobook(sessionid) == False :
        flagBook = False
        return

    logger.info('订票成功')
    flagBook = True


def get_space(flight) :
    with open("config.flight.airtype.json", 'r') as thefile:
        flight_airtype = json.load(thefile)
    if not flight_airtype.has_key(flight):
        logger.info("未找到为航班" + flight + "配置的飞机类型 .")
        return False, []

    airtype = flight_airtype[flight]
    if airtype == "" :
        logger.info("未找到为航班" + flight + "配置的飞机类型 .")
        return False, []

    with open("config.airtype.space.json", 'r') as thefile:
        airtype_space = json.load(thefile)
    if not airtype_space.has_key(airtype):
        logger.info("未找到为机型" + airtype + "配置的舱位 .")
        return False, []

    space = airtype_space[airtype]
    if space == [] :
        logger.info("未找到为机型" + airtype + "配置的舱位 .")
        return False, []

    return True, space

# 查票
def query(sessionid):
    global flagQueryAllFlight
    global flagQueryDestFlight
    global flagSpace
    global flagBook
    global flagOccupied

    # logger.info(sessionid)

    while True:
        # logger.info(sessionid)

        if limit() == True :
            return

        if flagQueryAllFlight == False or flagQueryDestFlight == False:
            logger.info("刷票分支出错, 分支退出.")
            return

        if flagSpace == False:
            logger.info("尚未配置舱位, 请退出后, 联系开发人员进行配置...")
            return

        if flagBook == True:
            logger.info("其他刷票分支已出票, 当前刷票分支退出.")
            return

        if flagOccupied == True:
            logger.info("票已占, 当前刷票分支退出.")
            return

        # 查票
        cmd = 'A'+book_config["date"]+book_config["from"]+book_config["to"]+'*'+book_config["comp"];
        ret, msg = invoke(sessionid, cmd)
        if ret != True:
            logger.info('航线查询失败')
            flagQueryAllFlight = False
            return

        attrlist = msg["masks"]["special"]["attrList"]
        # 确定航班
        flight = attrlist[16]["text"] + attrlist[17]["text"].strip()
        logger.info('查询到航班' + flight)

        # 确定舱位
        ret, space = get_space(flight)
        if ret == False :
            flagSpace == False
            logger.info("尚未配置舱位, 请退出后, 联系开发人员进行配置...")


        # 查找带票仓位
        for i in range(len(space)):
            status = attrlist[space[i]]["extended"]["status"]
            # print(space[i], status)
            if (status >= "1" and status <= "9"):
                logger.info(space[i], status, "航班有票")
                # 订票流程
                occupy(sessionid)
                return

        logger.info("航班无票")

        if flagBook == True:
            logger.info("其他刷票分支已出票, 当前刷票分支退出.")
            return

def command(sessionid) :
    logger.info("进入命令行, 进行手动订票...")
    while True :
        cmd = input("> ")
        if cmd == "exit" :
            msvcrt.getch()
            exit(0)

        ret, msg = invoke(sessionid, cmd)
        if ret != True:
            logger.info('订票失败')
            return False

        result = msg["text"]
        print(result)
        if cmd == "ER" :
            name = result.split('\n')[1].strip().strip('/')
            save(name, result)


if __name__ == '__main__':

    # 大循环启动线程
    while True:
        flagQueryAllFlight = True
        flagQueryDestFlight = True
        flagSpace = True
        flagOccupied = False

        if flagBook == True:
            logger.info("已出票, 按任意键退出")
            msvcrt.getch()
            exit(0)

        sessionid = login()

        with open("config.count.json", 'r') as thefile:
            count = json.load(thefile)["count"]

        session_list = []
        for i in range(count):
            session_list.append(sessionid)

        pool = threadpool.ThreadPool(count)
        reqs = threadpool.makeRequests(query, session_list)
        for req in reqs:
            pool.putRequest(req)
            time.sleep(1 / count)
        pool.wait()

        if flagOccupied == True :
            command(sessionid)
            msvcrt.getch()
            exit(0)

        if flagSpace == False:
            msvcrt.getch()
            exit(0)

        if limit() == True :
            msvcrt.getch()
            exit(0)
