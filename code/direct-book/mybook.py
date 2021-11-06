#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import requests
import threadpool
from mylog import *
import myflag
import myfile

login_url = 'https://webagentapp.tts.com/TWS/Login'
book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'

ret, base_config = myfile.get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = myfile.get_config("config.book.json")
if ret == False :
    exit(0)


def limit():
    if datetime.datetime.now() > datetime.datetime.strptime('2021-11-8 00:00', '%Y-%m-%d %H:%M'):
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
            # logger.warning('登录超时，重新登录 ...')
            continue

        break

    resjson = response.json()
    if resjson["success"] == True:
        logger.warning('登录成功')
        return True, resjson['sessionId']
    else:
        logger.warning('登录失败, 请检查登录配置文件 [ config.login.json ] ...')
        return False, ''

def dofilter(js) :
    if "addOns" in js :
        del js["aaa"]

    if "syncData" in js :
        del js["syncData"]

    if "enablePageDown" in js :
        del js["enablePageDown"]

    # msg = js["message"]
    # if "masks" in msg:
    #     del msg["masks"]

    logger.info(js)
    return js

def execute_instruction(sessionid, arg):
    logger.warning("命令 = " + arg)
    cmd = {"sessionId": sessionid, "command": arg, "allowEnhanced": True}
    try :
        response = requests.post(book_url, json=cmd, timeout=10)
    except :
        logger.warning('指令执行请求超时 ...')
        return False, {}

    simple = dofilter(response.json())
    msg = simple["message"]
    if simple["success"] == False:
        return False, msg

    # msg = response.json()["message"]
    # if response.json()["success"] == False:
    #     return False, msg

    return True, msg

# 占票
def occupy(book_list):
    sessionid = book_list["sessionid"]
    book_config = book_list["config"]
    while True:
        # logger.warning(sessionid)

        if limit() == True:
            return

        if myflag.get_flag_occupied() == True:
            logger.warning("其他刷票分支已占票, 当前刷票分支退出.")
            return

        if int(book_config["date"][:2]) < int(time.strftime("%d", time.localtime())):
            logger.warning("请确认 [ config.book.json ] 中的日期 ...")
            exit(0)

        # 查航线
        scan_cmd = 'A' + book_config["date"] + book_config["from"] + book_config["to"] + '*' + book_config["comp"];
        ret, msg = execute_instruction(sessionid, scan_cmd)
        if ret == False:
            continue

        if 'text' in msg and 'DEPARTED' in msg["text"] :
            logger.warning("请确认是否航班已经过期 ...")
            return

        attrlist = msg["masks"]["special"]["attrList"]

        # 查找 book_config["comp"], book_config["flight"]
        comp_flight_location = len(attrlist)
        for i in range(len(attrlist)):
            # logger.warning(str(i) + ' ' + attrlist[i]["text"] + attrlist[i+1]["text"])
            if "text" in attrlist[i] \
                    and attrlist[i]["text"] == book_config["comp"] \
                    and "text" in attrlist[i+1] \
                    and attrlist[i+1]["text"].strip() == book_config["flight"] :
                comp_flight_location = i
                break

        if comp_flight_location >= len(attrlist) :
            logger.warning('未找到航班 [' + book_config["comp"] + book_config["flight"] + ']')
            return

        line = attrlist[comp_flight_location-8]["text"]
        # logger.warning("comp_flight_location = %d" % comp_flight_location )
        logger.warning('找到航班 [' + book_config["comp"] + book_config["flight"] + ']，位于行 [' + line + ']')


        # 查找 text: line + 1 位置
        lineplus = str(int(line) +1)
        lineplus_start_location = comp_flight_location
        for i in range(comp_flight_location, len(attrlist)):
            if "text" in attrlist[i] and attrlist[i]["text"] == lineplus :
                lineplus_start_location = i
                break


        end_location = len(attrlist)
        if lineplus_start_location < len(attrlist) :
            # logger.warning("lineplus_start_location = %d" % lineplus_start_location)
            # logger.warning('找到第二个航班')
            end_location = lineplus_start_location-1

        # 查找 space 的位置, 及状态
        space_start_location = comp_flight_location+2
        space_location = end_location
        space = book_config["space"]

        for i in range(space_start_location, end_location):
            if "extended" in attrlist[i] :
                if "bic" in attrlist[i]["extended"] :
                    if attrlist[i]["extended"]["bic"] == space :
                        space_location = i
                        status = attrlist[space_location]["extended"]["status"]

                        # 有位置, 立即占票
                        if status >= "1" and status <= "9":
                            # logger.warning("space_location = %d" % space_location )
                            # logger.warning("text = " + attrlist[space_location]["text"])

                            logger.warning("航班 [" + book_config["comp"] + book_config["flight"] + "] 有票 : " + attrlist[space_location]["text"])

                            occupy_cmd = '01' + book_config["space"] + line
                            ret, msg = execute_instruction(sessionid, occupy_cmd)
                            if ret == False:
                                logger.warning('占票失败')
                                break

                            if 'text' not in msg:
                                logger.warning('占票失败')
                                break

                            if 'HL' in msg["text"] or \
                                    'LL' in msg["text"] :
                                logger.warning('占票失败')
                                execute_instruction(sessionid, 'I')
                                execute_instruction(sessionid, 'I')
                                execute_instruction(sessionid, 'I')
                                break

                            if 'HS' not in msg["text"] :
                                logger.warning('占票失败')
                                break

                            # HS
                            logger.warning('占票成功')
                            myflag.set_flag_occupied(True)

                            ret, msg = auto_book(sessionid)
                            if ret == True:
                                return

                            if msg == '':
                                logger.warning("请检查订票配置文件 [ config.book.json ] ...")
                                return

                            logger.warning('\n\n' + msg)
                            break


                        # 不可候补状态，执行快速预订
                        elif status == 'C' :
                            # logger.warning("航班 [" + book_config["comp"] + book_config["flight"] + "] 不可候补，执行快速预订 : " + attrlist[space_location]["text"])
                            logger.warning("航班 [" + book_config["comp"] + book_config["flight"] + "] 不可候补, 执行快速预订")

                            while True:
                                quick_booking_cmd = 'N ' + \
                                                    book_config["comp"] + \
                                                    book_config["flight"] + \
                                                    ' ' + \
                                                    book_config["space"] + \
                                                    ' ' + \
                                                    book_config["date"] + \
                                                    ' ' + \
                                                    book_config["from"] + \
                                                    book_config["to"] + \
                                                    ' NN1'
                                ret, msg = execute_instruction(sessionid, quick_booking_cmd)
                                if ret == False:
                                    logger.warning('占票失败')
                                    continue

                                # HS
                                if 'text' not in msg :
                                    logger.warning('占票失败')
                                    break

                                if '*0 AVAIL/WL CLOSED*' in msg["text"] :
                                    logger.warning('票面关闭中')
                                    continue

                                if 'HL' in msg["text"] or \
                                        'LL' in msg["text"] :
                                    break

                                if 'HS' in msg["text"]:
                                    logger.warning('占票成功')
                                    myflag.set_flag_occupied(True)

                                    ret, msg = auto_book(sessionid)
                                    if ret == True:
                                        return

                                    if msg == '':
                                        logger.warning("请检查订票配置文件 [ config.book.json ] ...")
                                        return

                                    logger.warning('\n\n' + msg)
                                    break

                            break

                        # 候补状态，L, 0 重新刷票
                        break





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

    execute_instruction(sessionid, "I")
    execute_instruction(sessionid, "I")
    execute_instruction(sessionid, "I")

    return True, ''


if __name__ == '__main__':

    branch_size = base_config["branch_size"]

    ret, sessionid = login()
    if ret == False:
        exit(0)

    execute_instruction(sessionid, 'I')
    execute_instruction(sessionid, 'I')
    execute_instruction(sessionid, 'I')

    for book_config in book_config_list :

        if limit() == True:
            exit(0)

        book_list = []
        for i in range(branch_size):
            book_list.append({"sessionid" : sessionid, "config" : book_config })

        pool = threadpool.ThreadPool(branch_size)
        reqs = threadpool.makeRequests(occupy, book_list)
        for req in reqs:
            pool.putRequest(req)
            time.sleep(1 / branch_size)
        pool.wait()

        if myflag.get_flag_occupied() == False:
            exit(0)

        if base_config["manual"] == True:
            munual_book(sessionid)
            exit(0)
