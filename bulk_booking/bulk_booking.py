#!/usr/bin/python
# -*- coding: UTF-8 -*-


import queue

from mylimit import *
from mynet import *
from myfile import *
from myflag import *
from mylog import *
from myrandname import *


login_url = 'https://webagentapp.tts.com/TWS/Login'


pnr_queue = queue.Queue()

ret, base_config = get_config("config.base.json")
if ret == False :
    exit(0)

# 登录
def login(debug = False):
    # 此处分发给员工时， 可以自行修改， 修改后编译即可
    # pyinstaller.exe -F -p venv/Lib/site-packages/ bulk_booking.py
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
        ret, response = net_request(login_url, user)
        if ret == False :
            continue

        ret, response_json = json_parse(response)
        if ret == False:
            logger.warning('登录失败, 请确认您的登录账户信息 ...')
            time.sleep(1)
            continue

        if response_json["success"] == False:
            logger.warning('返回状态非success')
            break

        if 'sessionId' not in response_json:
            logger.warning('返回数据中未发现 [sessionId] 信息')
            break

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
    logger.warning('[' + book_comp + book_flight + '] 行 = [' + line + ']')
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
        end_location = lineplus_start_location - 1

    return end_location






def occupy_ticket(session_id, book_space, status, line) :

    command = '0' + status + book_space + line
    ret, msg = execute_instruction(session_id, command, base_config['debug'])
    if ret == False:
        logger.warning('占票失败')
        return False

    if get_flag_relogin() == True:
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

            logger.warning('[' + book_config['comp'] + book_config['flight'] + '] --> [' + book_space + status + ']')
            break

    return space_list


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


def auto_booking(session_id, book_config, status):
    for i in range(int(status)) :
        # 客户姓名
        while True :
            user = 'N.' + random_name()

            ret, message = execute_instruction(session_id, user)
            if ret == False :
                logger.warning(message)
                continue

            if 'text' in message and 'INVALID NAME - DUPLICATE ITEM' in message["text"]:
                logger.warning('前期客户姓名命令已经执行...')

            break


    # 客户手机
    while True :
        ret, message = execute_instruction(session_id, book_config["contact"])
        if ret == False :
            logger.warning(message)
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户电话命令已经执行...')

        break


    # 客户email
    while True :
        ret, message = execute_instruction(session_id, book_config["email"])
        if ret == False :
            logger.warning(message)
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户邮箱命令已经执行...')

        break


    # R.PEI
    while True :
        ret, message = execute_instruction(session_id, "R.PEI")
        if ret == False:
            logger.warning(message)
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期R.PEI命令已经执行...')

        break



    # T.T*
    while True :
        ret, message = execute_instruction(session_id, "T.T*")
        if ret == False:
            logger.warning(message)
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期T.T*命令已经执行...')

        break



    # ER
    while True :
        ret, message = execute_instruction(session_id, "ER")
        if ret == False:
            logger.warning(message)
            continue

        break


    if 'CHECK' in message["text"]:
        logger.warning('请确认是否在对已经订票成功的客户，进行重复订票')
        return False

    if 'HK' not in message["text"]:
        logger.warning('请确认是否在对已经订票成功的客户，进行重复订票')
        return False

    result_pnr = message["text"]

    pnr = result_pnr.split('\n')[0].split('/')[0]

    logger.warning('添加输出任务 = ' + pnr )
    pnr_queue.put(pnr)


    three_i_command(session_id)

    return True


def get_input( message ):

    while True :
        content = input(message + " > ")

        if content.strip('') == '' :
            continue

        if content == "exit":
            exit(0)

        return content.upper()


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


class BookingThread(threading.Thread):

    def __init__(self, session_id, book_config, debug = False):
        threading.Thread.__init__(self)
        self.session_id = session_id
        self.book_config = book_config
        self.debug = debug
        self.name = 'BookingT'

    def run(self):
        while True :
            # 查询匹配的航线
            ret, attrlist = query_airline(self.session_id, self.book_config)
            if ret == False :
                if get_flag_relogin() == True:
                    return
                continue

            # 查询匹配的航班
            ret, line, comp_flight_location = parse_flight(attrlist, self.book_config)
            if ret == False :
                continue

            # 航班行的开始位置
            line_start_location = comp_flight_location+2

            # 查找匹配的航班结束的位置，即text: line + 1 位置
            line_end_location = parse_space_end_location(attrlist, line, comp_flight_location)

            # 查找 book_config["space"] 的位置, 及状态
            space_list = parse_space(self.book_config, attrlist, line_start_location, line_end_location)

            # 如果所有仓位状态都是N，重新循环刷票
            if space_status_all_N(space_list) == True :
                continue

            # 处理所有的占座及订座
            for book_space in space_list:
                location = space_list[book_space]["location"]
                status = space_list[book_space]["status"]
                if location == -1 or status == 'N' :
                    continue

                # 有位置, 立即占票及订票
                if not (status >= "1" and status <= "9"):
                    continue

                # 有位置, 立即占票及订票
                logger.warning("准备占票 [" + self.book_config["comp"] + self.book_config["flight"] + "] [" + attrlist[location]["text"] + "]")

                # 占票
                ret = occupy_ticket(self.session_id, book_space, status, line)
                if ret == False :
                    if get_flag_relogin() == True:
                        return
                    continue

                auto_booking(self.session_id, self.book_config, status)

                if get_flag_relogin() == True:
                    return


class OutputThread(threading.Thread):

    def __init__(self, session_id, debug = False):
        threading.Thread.__init__(self)
        self.session_id = session_id
        self.debug = debug
        self.name = 'OutputT'

    def run(self):
        while True:

            # 循环监听任务命令
            try:
                pnr = pnr_queue.get(timeout=1)
            except:
                continue

            logger.warning("存档 : " + pnr)

            while True :
                # *PNR
                ret, message = execute_instruction(self.session_id, "*"+pnr, base_config['debug'])
                if ret == False:
                    if message == 'relogin' :
                        set_flag_relogin(True)
                        return
                    logger.warning(message)
                    continue

                result_pnr = message["text"]

                # *VR
                ret, message = execute_instruction(self.session_id, "*VR", base_config['debug'])
                if ret == False:
                    if message == 'relogin' :
                        set_flag_relogin(True)
                        return
                    logger.warning(message)
                    continue

                result_vr = message["text"]
                if 'ADTK' not in result_vr :
                    time.sleep(1)
                    continue

                save_excel_result(result_pnr, result_vr)

                logger.warning('订票存档成功 !!!')
                # os.system(r"start /b BookInfo.exe")

                break





def main() :
    if limit() == True:
        exit(0)

    book_config = {}

    book_config["from"]     = get_input('请输入起点')
    book_config["to"]       = get_input('请输入终点')
    book_config["date"]     = get_input('请输入日期')
    book_config["comp"]     = get_input('请输入航司')
    book_config["flight"]   = get_input('请输入航班')
    book_config["space"]    = get_input('请输入座舱').split(',')
    book_config["contact"]  = get_input('请输入联系方式')
    book_config["email"]    = get_input('请输入邮箱')

    logger.warning('')
    logger.warning('')
    logger.warning('开始订票 = ' + json.dumps(book_config))

    session_id = ''
    set_flag_relogin(True)

    while True:
        if limit() == True:
            return

        if get_flag_relogin() == True:
            session_id = login(base_config['debug'])

        set_flag_relogin(False)

        booking_thread = BookingThread(session_id, book_config, base_config['debug'])
        output_thread = OutputThread(session_id, base_config['debug'])

        booking_thread.start()
        output_thread.start()

        booking_thread.join()
        output_thread.join()





if __name__ == '__main__':
    main()
