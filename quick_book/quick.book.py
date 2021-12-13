#!/usr/bin/python

import socket
import ssl
import select
import time
import threading
import urllib3
from io import BytesIO
from http.client import HTTPResponse
import queue
import requests

from mylog import *
from myflag import *
import myfile
import json



login_url = 'https://webagentapp.tts.com/TWS/Login'
book_url = 'https://webagentapp.tts.com/TWS/TerminalCommand'

ret, base_config = myfile.get_config("config.base.json")
if ret == False :
    exit(0)

ret, book_config_list = myfile.get_config("config.book.json")
if ret == False :
    exit(0)


send_queue = queue.Queue()
read_list = []



class HttpRequest:
    def __init__(self, sock, item):
        self.sock = sock
        self.item = item
        self.read_count = 0

    def fileno(self):
        return self.sock.fileno()


def limit():
    # 2021-11-20 00:00 我是
    # pyinstaller.exe -F -p venv/Lib/site-packages/ quick_booking.book.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-12-12 23:59', '%Y-%m-%d %H:%M'):
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
    # pyinstaller.exe -F -p venv/Lib/site-packages/ quick_booking.book.py
    login_config = {"son": "Z7LJ2/WX", "pcc": "7LJ2", "pwd": "LLP0605", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/WP", "pcc": "7LJ2", "pwd": "BANANA12", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/FG", "pcc": "7LJ2", "pwd": "PLANTAIN12", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/LL", "pcc": "7LJ2", "pwd": "PLL0605", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/PX", "pcc": "7LJ2", "pwd": "FRUITS01", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/YJ", "pcc": "7LJ2", "pwd": "FRUITS02", "gds": "Galileo"}
    # login_config = {"son": "Z7LJ2/SS", "pcc": "7LJ2", "pwd": "FRUITS03", "gds": "Galileo"}


    logger.warning('')
    logger.warning('')
    logger.warning('登录账户 = ' + json.dumps(login_config['son']))

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


def brush_ticket(sessionid, book_config) :

    data = {
        "sessionId": sessionid,
        "command": 'A' + book_config["date"] + book_config["from"] + book_config["to"] + '/' + book_config["comp"],
        "allowEnhanced": True
    }

    item = {
        'sessionid': sessionid,
        'book_config': book_config,
        'data': json.dumps(data),
        "callback": brush_ticket_callback
    }

    send_queue.put(item)



def brush_ticket_callback(item, data):
    logger.warning('response >>>')
    response = response_from_bytes(data)
    logger.warning(response.headers)
    logger.warning(response.data)

    msg = response.data
    # set_flag_relogin(True)
    # if 'text' not in msg:
    #     logger.warning('刷票失败')
    # else:
    #     logger.warning('发现错误 : ' + msg["text"])
    # return False, []

    sessionid = item['sessionid']
    book_config = item['book_config']

    # 刷票失败，重新回去刷票
    if 'text' not in msg:
        logger.warning('刷票失败')
        return

    # 航班过去，重新回去刷票
    if 'DEPARTED' in msg["text"]:
        logger.warning("请确认是否航班已经过期 ...")
        return

    # 掉线，重新回去登录和刷票
    if 'SYSTEM ERROR' in msg["text"] \
            or 'Session does not exist' in msg["text"]:
        logger.warning('掉线重新登录')
        set_run_status(RunStatus.LOGIN)
        return

    attrlist = msg["masks"]["special"]["attrList"]

    # 查询匹配的航班，失败重新回去刷票
    ret, line, comp_flight_location = parse_flight(
        attrlist,
        book_config['comp'],
        book_config['flight']
    )
    if ret == False:
        return

    # 航班行的开始位置
    line_start_location = comp_flight_location + 2

    # 查找匹配的航班结束的位置，即text: line + 1 位置
    line_end_location = parse_space_end_location(
        attrlist,
        line,
        comp_flight_location
    )

    # 查找 book_space_list 的位置, 及状态
    space_list = parse_space(
        attrlist,
        book_config["space"],
        line_start_location,
        line_end_location,
        book_config["comp"],
        book_config["flight"]
    )

    # 如果所有仓位状态都是N，重新回去刷票
    if all_N(
            space_list,
            line_end_location,
            book_config["comp"],
            book_config["flight"]
    ) == True:
        return

    # 处理所有的占座及订座

    # 处理有座状态
    has_ticket = False
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == line_end_location or status == 'N':
            continue

        # 有位置, 立即占票及订票
        if status >= "1" and status <= "9":
            occupy_ticket(
                item['sessionid'],
                attrlist,
                book_config["comp"],
                book_config["flight"],
                line_end_location,
                book_space,
                line)
            return


    # 刷票+占票模式，不进行快速预定，重新去刷票
    if base_config["mode"] == 0:
        return

    # 刷票+占票+快速预定模式下，处理带有C状态的票
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == line_end_location or status == 'N':
            continue

        # 找到了对应仓位，但候补关闭，刷票+占票+快速预定模式下，执行快速预订
        if status == 'C':
            ret = quick_booking(
                item['sessionid'],
                book_config["comp"],
                book_config["flight"],
                book_config["space"],
                book_config["date"],
                book_config["from"],
                book_config["to"])
            if ret == True:
                return

            if get_flag_relogin() == True:
                return

            break

    # 候补状态，L, 0 等等重新刷票





def parse_flight(attrlist, book_comp, book_flight) :
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

def occupy_ticket(sessionid, attrlist, book_comp, book_flight, space_location, book_space, line) :

    # logger.warning("space_location = %d" % space_location )
    # logger.warning("text = " + attrlist[space_location]["text"])

    logger.warning("航班 [" + book_comp + book_flight + "] 有票 : " + attrlist[space_location]["text"])

    occupy_ticket_cmd = '01' + book_space + line
    ret, msg = execute_instruction(sessionid, occupy_ticket_cmd)
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
    set_flag_occupied(True)

    if base_config["manual"] == True:
        return True

    ret, msg = auto_booking(sessionid)
    if ret == True:
        return True

    if msg == '':
        logger.warning("请检查订票配置文件 [ config.book.json ] ...")
        return False

    logger.warning('')
    logger.warning('')
    logger.warning(msg)
    return False



def quick_booking(sessionid, book_config) :

    cmd = (
        'N {}{} {} {} {}{} NN1',
    ).format(
        book_config['comp'],
        book_config['flight'],
        book_config['space'],
        book_config['date'],
        book_config['from'],
        book_config['to']
    )

    data = {
        "sessionId": sessionid,
        "command": cmd,
        "allowEnhanced": True
    }

    item = {
        'sessionid': sessionid,
        'book_config': book_config,
        'data': json.dumps(data),
        "callback": quick_booking_callback
    }

    send_queue.put(item)



def quick_booking_callback(item, data):
    logger.warning('response >>>')
    response = response_from_bytes(data)
    logger.warning(response.headers)
    logger.warning(response.data)

    msg = response.data
    # if ret == False:
    #     logger.warning('快速预定失败')
    #     continue


    sessionid = item['sessionid']
    book_config = item['book_config']


    # 失败，重新回去刷票
    if 'text' not in msg:
        logger.warning('快速预定失败')
        set_run_status(RunStatus.BRUSH)
        return

    # 掉线，重新回去登录刷票
    if 'SYSTEM ERROR' in msg["text"] \
            or 'Session does not exist' in msg["text"]:
        logger.warning('掉线重新登录')
        set_run_status(RunStatus.LOGIN)
        return

    # 票面关闭，重新快速预定
    if '*0 AVAIL/WL CLOSED*' in msg["text"]:
        logger.warning('票面关闭中')
        set_run_status(RunStatus.QUICKBOOK)
        return

    # 票面禁止销售
    if '*SELL RESTRICTED*' in msg["text"]:
        logger.warning('票面禁止销售')
        set_run_status(RunStatus.QUICKBOOK)
        return

    # 产生了HL LL错误，重新回去刷票
    if 'HL' in msg["text"] or \
            'LL' in msg["text"]:
        set_run_status(RunStatus.BRUSH)
        return

    # HS
    if 'HS' in msg["text"]:
        logger.warning('占票成功')
        set_run_status(RunStatus.OCCUPIED)

        if base_config["manual"] == True:
            return

        auto_booking(sessionid, book_config)
        return



def quick_booking(sessionid, book_comp, book_flight, book_space, book_date, book_from, book_to) :
    logger.warning("航班 [" + book_comp + book_flight + "] 不可候补, 执行快速预订")

    while True:
        quick_bookinging_cmd = 'N ' + book_comp + book_flight + ' ' + book_space + ' ' + book_date + ' ' + book_from + book_to + ' NN1'
        ret, msg = execute_instruction(sessionid, quick_bookinging_cmd)





def parse_space(attrlist, book_space_list, line_start_location, line_end_location, book_comp, book_flight) :
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

    return space_list



def all_N(space_list, line_end_location, book_comp, book_flight) :

    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != line_end_location and status != 'N':
            return False

        logger.warning('找到航班 [' + book_comp + book_flight + ']的座舱类型[' + book_space + status + ']')

    return True





def auto_booking_user(sessionid, book_config):

    data = {
        "sessionId": sessionid,
        "command": book_config["user"],
        "allowEnhanced": True
    }

    item = {
        'type':'user',
        'sessionid': sessionid,
        'book_config': book_config,
        'data': json.dumps(data),
        "callback": brush_ticket_callback
    }

    send_queue.put(item)




def auto_booking_contact(sessionid, book_config):

    data = {
        "sessionId": sessionid,
        "command": book_config["contact"],
        "allowEnhanced": True
    }

    item = {
        'type': 'user',
        'sessionid': sessionid,
        'book_config': book_config,
        'data': json.dumps(data),
        "callback": brush_ticket_callback
    }

    send_queue.put(item)










        # 客户姓名
        ret, msg = execute_instruction(sessionid, book_config["user"])
        if ret == False :
            if get_flag_relogin() == True:
                return
            logger.warning(msg)
            continue

        if 'text' in msg and 'INVALID NAME - DUPLICATE ITEM' in msg["text"]:
            logger.warning('前期客户姓名命令已经执行...')

        break


        if msg == '':
            logger.warning("请检查订票配置文件 [ config.book.json ] ...")
            return False


    # 客户手机
    while True :
        ret, msg = execute_instruction(sessionid, book_config["contact"])
        if ret == False :
            if get_flag_relogin() == True:
                return
            logger.warning(msg)
            continue

        if 'text' in msg and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in msg["text"]:
            logger.warning('前期客户电话命令已经执行...')

        break


    # 客户email
    while True :
        ret, msg = execute_instruction(sessionid, book_config["email"])
        if ret == False :
            if get_flag_relogin() == True:
                return
            logger.warning(msg)
            continue

        if 'text' in msg and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in msg["text"]:
            logger.warning('前期客户邮箱命令已经执行...')

        break


    # R.PEI
    while True :
        ret, msg = execute_instruction(sessionid, "R.PEI")
        if ret == False:
            if get_flag_relogin() == True:
                return
            logger.warning(msg)
            continue

        if 'text' in msg and 'SINGLE ITEM FIELD' in msg["text"]:
            logger.warning('前期R.PEI命令已经执行...')

        break



    # T.T*
    while True :
        ret, msg = execute_instruction(sessionid, "T.T*")
        if ret == False:
            if get_flag_relogin() == True:
                return
            logger.warning(msg)
            continue

        if 'text' in msg and 'SINGLE ITEM FIELD' in msg["text"]:
            logger.warning('前期T.T*命令已经执行...')

        break



    # ER
    while True :
        ret, msg = execute_instruction(sessionid, "ER")
        if ret == False:
            if get_flag_relogin() == True:
                return
            logger.warning(msg)
            continue

        break


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



class BytesIOSocket:
    def __init__(self, content):
        self.handle = BytesIO(content)

    def makefile(self, mode):
        return self.handle

def response_from_bytes(data):
    sock = BytesIOSocket(data)

    response = HTTPResponse(sock)
    response.begin()

    return urllib3.HTTPResponse.from_httplib(response)






def do_send():
    while True:

        item = send_queue.get()
        content = \
            (
                "POST TWS/TerminalCommand HTTP/1.1\r\n"
                "Host: webagentapp.tts.com\r\n"
                "Accept: application/json, text/javascript, */*; q=0.01\r\n"
                "Cache-Control: no-cache\r\n"
                "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n"
                "Content-Length: %d\r\n"
                "Connection: keep-alive\r\n\r\n"
                "%s"
            ) % (len(item['data']), item['data'])

        try:
            sock = ssl.wrap_socket(socket.socket())
            sock.connect(('webagentapp.tts.com', 443))
            logger.warning('------ send ------ ')
            sock.sendall(content.encode("utf-8"))
            read_list.put(HttpRequest(sock, item))
            logger.warning('添加socket=%d'%(sock.fileno()))

        except BlockingIOError as e:
            logger.warning('错误产生')
            logger.warning(json.dumps(item))




def do_recv():
    while True:
        if not read_list:
            time.sleep(1)
            continue

        for elem in read_list :
            elem.write_count += 1
            if elem.write_count >= 30 :     # 如果经过了30次的select轮询，依旧没有连接成功，则说明连接出现了问题。关闭此连接
                elem.sock.close()
                read_list.remove(elem)

        if not read_list :
            time.sleep(1)
            continue

        logger.warning("------ select read ------")
        r, _, _ = select.select(read_list, [], [], 1)
        for http_request in r:
            """请求得到响应，接收数据"""
            logger.warning(http_request.sock)
            data = http_request.sock.recv(8096)
            http_request.sock.close()
            http_request.item['callback'](http_request.item, data)  # 回调
            read_list.remove(http_request)


def callback(item, data):
    logger.warning('response >>>')
    response = response_from_bytes(data)
    logger.warning(response.headers)
    logger.warning(response.data)







class sendThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        do_send()






class readThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        do_recv()


class taskThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        branch_size = base_config["branch_size"]

        for book_config in book_config_list :

            logger.warning('')
            logger.warning('')
            logger.warning('开始订票 = ' + json.dumps(book_config))

            set_flag_relogin(True)
            set_flag_occupied(False)

            sessionid = ''
            while True :

                if limit() == True:
                    exit(0)

                if get_flag_relogin() == True:
                    sessionid = login()

                brush_ticket(sessionid, book_config)

                time.sleep(1/branch_size)

                if get_flag_relogin() == True:
                    continue

                if get_flag_occupied() == False:
                    break

                if base_config["manual"] == True:
                    if munual_booking(sessionid) == True:
                        break

                    exit(0)

                break


def munual_booking(sessionid):
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


def main() :

    # 创建新线程
    sth = sendThread()
    rth = readThread()
    tth = taskThread()


    # 开启新线程
    rth.start()
    sth.start()
    tth.start()

    tth.join()
    sth.join()
    rth.join()

    logger.warning ("退出主线程")



if __name__ == '__main__':
    main()
