#!/usr/bin/python

import time
import threadpool
import json
import os

from mylimit import *
from mynet import *
from myfile import *
from myflag import *
from mylog import *

login_url = 'https://webagentapp.tts.com/TWS/Login'

ret, base_config = get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = get_config("config.book.json")
if ret == False :
    exit(0)


# 登录
def login(debug = False):
    # 此处分发给员工时， 可以自行修改， 修改后编译即可
    # pyinstaller.exe -F -p venv/Lib/site-packages/ booking.py
    user = {"son": "Z7LJ2/WX", "pcc": "7LJ2", "pwd": "LLP0605", "gds": "Galileo"}
    # user = {"son": "Z7LJ2/WP", "pcc": "7LJ2", "pwd": "BANANA12", "gds": "Galileo"}
    # user = {"son": "Z7LJ2/FG", "pcc": "7LJ2", "pwd": "PLANTAIN12", "gds": "Galileo"}
    # user = {"son": "Z7LJ2/LL", "pcc": "7LJ2", "pwd": "PLL0605", "gds": "Galileo"}
    # user = {"son": "Z7LJ2/PX", "pcc": "7LJ2", "pwd": "FRUITS01", "gds": "Galileo"}
    # user = {"son": "Z7LJ2/YJ", "pcc": "7LJ2", "pwd": "FRUITS02", "gds": "Galileo"}
    # user = {"son": "Z7LJ2/SS", "pcc": "7LJ2", "pwd": "FRUITS03", "gds": "Galileo"}

    logger.warning('')
    logger.warning('')
    logger.warning('登录账户 = ' + json.dumps(user['son']))

    while True :
        ret, response_json = net_request(login_url, user)
        if ret == False :
            logger.warning('登录失败, 请确认您的登录账户信息 ...')
            time.sleep(3)
            continue

        if response_json["success"] == False:
            logger.warning('返回状态非success')
            break

        if 'sessionId' not in response_json:
            logger.warning('返回数据中未发现 [sessionId] 信息')
            break

        set_flag_relogin(False)
        logger.warning('登录成功')

        session_id = response_json['sessionId']

        three_i_command(session_id)

        return session_id





def parse_flight(attrlist, book_config) :
    book_comp = book_config['comp']
    book_flight = book_config['flight']

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





def parse_space_end_location(attrlist, line, comp_flight_location) :
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






def occupy_ticket(session_id, book_space, line) :
    if get_flag_occupied() == True:
        return False

    if get_flag_relogin() == True:
        return False

    command = '01' + book_space + line
    ret, msg = execute_instruction(session_id, command, base_config['debug'])
    if ret == False:
        logger.warning('占票失败')
        return False

    if 'text' not in msg:
        logger.warning('占票失败')
        return False

    if 'HL' in msg["text"] or \
            'LL' in msg["text"]:
        logger.warning('占票失败')
        three_i_command(session_id)
        return False

    if 'HS' not in msg["text"]:
        logger.warning('占票失败')
        return False

    # HS

    logger.warning('占票成功')
    set_flag_occupied(True)
    return True




def parse_space(book_config, attrlist, line_start_location, line_end_location) :

    space_list = {}

    # 枚举所有的座舱类型
    for book_space in book_config["space"]:

        space_list[book_space] = {
            "location": -1,
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

            logger.warning('找到航班 [' + book_config['comp'] + book_config['flight'] + ']的座舱[' + book_space + status + ']')
            break

    return space_list



def space_status_has_ticket(space_list):
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == -1 or status == 'N' :
            continue

        # 有位置, 立即占票及订票
        if status >= "1" and status <= "9":
            return True

    return False


def space_status_all_N(space_list):
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != -1 and status != 'N':
            return False

    return True


def space_status_has_C(space_list):
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != -1 and status == 'C':
            return True

    return False



def quick_booking(session_id, book_config, space_list) :
    logger.warning("航班 [" + book_config['comp'] + book_config['flight'] + "] 不可候补, 执行快速预订")

    # 刷票+占票+快速预定模式下，处理带有C状态的票
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == -1 or \
            status != 'C' :
            continue

        command = (
            'N {}{} {} {} {}{} NN1'
        ).format(
            book_config['comp'],
            book_config['flight'],
            book_space,
            book_config['date'],
            book_config['from'],
            book_config['to']
        )

        # 找到了对应仓位，但候补关闭，刷票+占票+快速预定模式下，执行快速预订
        while True:
            if get_flag_occupied() == True :
                return False

            if get_flag_relogin() == True :
                return False

            ret, message = execute_instruction(session_id, command, base_config['debug'])
            if ret == False:
                logger.warning('占票失败')
                continue

            if 'text' not in message:
                logger.warning('占票失败')
                continue

            if 'SYSTEM ERROR' in message["text"] \
                    or 'Session does not exist' in message["text"]:
                logger.warning('掉线重新登录')
                set_flag_relogin(True)
                return False

            if '*0 AVAIL/WL CLOSED*' in message["text"]:
                logger.warning('票面关闭中')
                continue

            if '*SELL RESTRICTED*' in message["text"]:
                logger.warning('票面禁止销售')
                continue

            if '*UNABLE - CLASS DOES NOT EXIST FOR THIS FLIGHT*' in message["text"]:
                logger.warning('票面禁止销售')
                continue

            if 'HS' not in message["text"]:
                logger.warning(message['text'])
                continue

            # HS
            logger.warning('占票成功')
            set_flag_occupied(True)
            return True

    return False



def auto_booking(session_id, book_config):
    # 客户姓名
    while True :
        ret, message = execute_instruction(session_id, book_config["user"])
        if ret == False :
            if get_flag_relogin() == True:
                return False
            logger.warning(message)
            continue

        if 'text' in message and 'INVALID NAME - DUPLICATE ITEM' in message["text"]:
            logger.warning('前期客户姓名命令已经执行...')

        break


    # 客户手机
    while True :
        ret, message = execute_instruction(session_id, book_config["contact"])
        if ret == False :
            if get_flag_relogin() == True:
                return False
            logger.warning(message)
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户电话命令已经执行...')

        break


    # 客户email
    while True :
        ret, message = execute_instruction(session_id, book_config["email"])
        if ret == False :
            if get_flag_relogin() == True:
                return False
            logger.warning(message)
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户邮箱命令已经执行...')

        break


    # R.PEI
    while True :
        ret, message = execute_instruction(session_id, "R.PEI")
        if ret == False:
            if get_flag_relogin() == True:
                return False
            logger.warning(message)
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期R.PEI命令已经执行...')

        break



    # T.T*
    while True :
        ret, message = execute_instruction(session_id, "T.T*")
        if ret == False:
            if get_flag_relogin() == True:
                return False
            logger.warning(message)
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期T.T*命令已经执行...')

        break



    # ER
    while True :
        ret, message = execute_instruction(session_id, "ER")
        if ret == False:
            if get_flag_relogin() == True:
                return False
            logger.warning(message)
            continue

        break

    if 'CHECK' in message["text"]:
        logger.warning('请确认是否在对已经订票成功的客户，进行重复订票')
        return False

    if 'HK' not in message["text"]:
        logger.warning('请确认是否在对已经订票成功的客户，进行重复订票')
        return False


    name = book_config["user"].strip('N.').replace('/','')
    id = message["text"].split('\n')[0].split('/')[0]
    logger.warning("存档 : " + name + '-' + id)
    save_result(name + '-' + id, message["text"])
    logger.warning('订票存档成功 !!!')
    os.system(r"start /b BookInfo.exe")

    three_i_command(session_id)

    return True




def munual_booking(session_id, book_config):
    logger.warning("进入命令行, 进行手动订票 ...")
    logger.warning("输入 break 停止当前用户订票 .")
    logger.warning("输入 exit 退出程序 .")

    while True:
        command = input("\n> ")

        if command.strip('') == '' :
            continue

        if command == "break":
            break

        if command == "exit":
            exit(0)

        ret, message = execute_instruction(session_id, command)
        if ret == False:
            logger.warning(message)
            continue

        text = message["text"]
        logger.warning()
        logger.warning(text)
        logger.warning(flush=True)

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

        if command == "ER":
            if "SELL OPTION HAS EXPIRED - CHECK ITINERARY" in text :
                continue

            if 'NEED RECEIVED' in text:
                continue

            if 'MODIFY BOOKING' in text:
                continue

            name = book_config["user"].strip('N.').replace('/','')
            id = text.split('\n')[0].split('/')[0]
            logger.warning("存档 : " + name + '-' + id)
            save_result(name + '-' + id, text)
            logger.warning('订票存档成功 !!!')
            os.system(r"start /b BookInfo.exe")

    return True



def query_airline(session_id, book_config ) :
    command = (
        'A{}{}{}/{}'
    ).format(
        book_config['date'],
        book_config['from'],
        book_config['to'],
        book_config['comp'],
    )

    ret, msg = execute_instruction(session_id, command, base_config['debug'])
    if ret == False:
        set_flag_relogin(True)
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
        set_flag_relogin(True)
        return False, []

    attrlist = msg["masks"]["special"]["attrList"]
    return True, attrlist



# 占票
def booking(book_list):
    session_id = book_list["session_id"]
    book_config = book_list["config"]

    while True:

        if limit() == True:
            return

        if get_flag_occupied() == True:
            logger.warning("已占票, 当前分支退出.")
            return

        if get_flag_relogin() == True:
            logger.warning("需要重新登录, 当前分支退出.")
            return

        # 查询匹配的航线
        ret, attrlist = query_airline(session_id, book_config)
        if ret == False :
            if get_flag_occupied() == True:
                logger.warning("已占票, 当前分支退出.")
                return

            if get_flag_relogin() == True:
                logger.warning("需要重新登录, 当前分支退出.")
                return
            continue

        # 查询匹配的航班
        ret, line, comp_flight_location = parse_flight(attrlist, book_config)
        if ret == False :
            if get_flag_occupied() == True:
                logger.warning("已占票, 当前分支退出.")
                return

            if get_flag_relogin() == True:
                logger.warning("需要重新登录, 当前分支退出.")
                return
            return

        # 航班行的开始位置
        line_start_location = comp_flight_location+2

        # 查找匹配的航班结束的位置，即text: line + 1 位置
        line_end_location = parse_space_end_location(attrlist, line, comp_flight_location)

        # 查找 book_config["space"] 的位置, 及状态
        space_list = parse_space(book_config, attrlist, line_start_location, line_end_location)

        # 如果所有仓位状态都是N，重新循环刷票
        if space_status_all_N(space_list) == True :
            continue

        # 处理所有的占座及订座

        # 处理有座状态
        is_have_ticket = False
        for book_space in space_list:
            location = space_list[book_space]["location"]
            status = space_list[book_space]["status"]
            if location == -1 or status == 'N' :
                continue

            # 有位置, 立即占票及订票
            if not (status >= "1" and status <= "9"):
                continue

            # 有位置, 立即占票及订票
            is_have_ticket = True
            logger.warning("航班 [" + book_config["comp"] + book_config["flight"] + "] 有票 : " + attrlist[location]["text"])

            # 占票
            ret = occupy_ticket(session_id, book_space, line)
            if ret == False :
                if get_flag_occupied() == True:
                    logger.warning("已占票, 当前分支退出.")
                    return

                if get_flag_relogin() == True:
                    logger.warning("需要重新登录, 当前分支退出.")
                    return
                break

            if base_config["manual"] == True:
                return

            ret = auto_booking(session_id, book_config)
            if ret == True:
                return

            if get_flag_relogin() == True:
                logger.warning("需要重新登录, 当前分支退出.")
                return

            break


        # 有位置的情况下， 但未能占票或订票成功，重新去刷票
        if is_have_ticket == True :
            continue

        # 刷票+占票模式，不进行快速预定，重新去刷票
        if base_config["mode"] == 0:
            continue

        # 候补状态，L, 0 等等重新刷票
        if space_status_has_C(space_list) == False :
            continue

        # C状态
        ret = quick_booking(session_id, book_config, space_list)
        if ret == False :
            if get_flag_occupied() == True:
                logger.warning("已占票, 当前分支退出.")
                return

            if get_flag_relogin() == True:
                logger.warning("需要重新登录, 当前分支退出.")
                return
            continue

        if base_config["manual"] == True:
            return

        ret = auto_booking(session_id, book_config)
        if ret == True:
            return

        if get_flag_occupied() == True:
            logger.warning("已占票, 当前分支退出.")
            return

        if get_flag_relogin() == True:
            logger.warning("需要重新登录, 当前分支退出.")
            return





def main() :
    branch_size = base_config["branch_size"]

    for book_config in book_config_list :

        logger.warning('')
        logger.warning('')
        logger.warning('开始订票 = ' + json.dumps(book_config))

        while True :
            if limit() == True:
                exit(0)

            set_flag_relogin(False)
            set_flag_occupied(False)

            session_id = login(base_config['debug'])

            book_list = []
            for i in range(branch_size):
                book_list.append({"session_id" : session_id, "config" : book_config })

            pool = threadpool.ThreadPool(branch_size)
            reqs = threadpool.makeRequests(booking, book_list)
            for req in reqs:
                pool.putRequest(req)
                time.sleep(1 / branch_size)
            pool.wait()

            if get_flag_relogin() == True:
                continue

            if get_flag_occupied() == False:
                break

            if base_config["manual"] == True:
                if munual_booking(session_id, book_config) == True :
                    break

                exit(0)

            break

    logger.warning('程序退出 ...')
    logger.warning('')


if __name__ == '__main__':
    main()
