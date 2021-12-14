#!/usr/bin/python

import socket
import ssl
import select
import time
import os
import _thread
import urllib3
from io import BytesIO
from http.client import HTTPResponse
import queue
import requests
import http

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
        self.response_data = b''
        self.response_status = 0
        self.response_header_length = 0
        self.response_content_length = 0

    def fileno(self):
        return self.sock.fileno()


def limit():
    # 2021-11-20 00:00 我是
    # pyinstaller.exe -F -p venv/Lib/site-packages/ booking.py
    if datetime.datetime.now() > datetime.datetime.strptime('2021-12-30 23:59', '%Y-%m-%d %H:%M'):
        logger.warning("试用期限已到...")
        return True
    return False



def net_request(url, command_json) :
    try:
        response = requests.post(url, json=command_json, timeout=100)
        if base_config["debug"] :
            logger.warning(response.text)
    except requests.exceptions.ReadTimeout as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {}
    except urllib3.exceptions.ReadTimeoutError as e:
        logger.warning('网络错误 : ' + str(e))
        return False, {}

    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        return False, {}

    return True, response_json



def execute_instruction(sessionid, arg):
    logger.warning("命令 = " + arg)
    command_json = {"sessionId": sessionid, "command": arg, "allowEnhanced": True}
    ret, response_json = net_request(book_url, command_json)

    if response_json["success"] == False:
        return False, {}

    if "message" not in response_json :
        return False, {}

    return True, response_json['message']




def three_i_command(sessionid) :
    execute_instruction(sessionid, 'I')
    execute_instruction(sessionid, 'I')
    execute_instruction(sessionid, 'I')



# 登录
def login():
    # 此处分发给员工时， 可以自行修改， 修改后编译即可
    # pyinstaller.exe -F -p venv/Lib/site-packages/ booking.py
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
        ret, response_json = net_request(login_url, login_config, "sessionId")
        if ret == False :
            logger.warning('登录失败, 请确认您的登录账户信息 ...')
            time.sleep(1)
            continue

        logger.warning('登录成功')

        if 'sessionId' not in response_json :
            continue

        sessionid = response_json['sessionid']

        three_i_command(sessionid)

        return sessionid


class SocketBytesIO:
    def __init__(self, content):
        self.handle = BytesIO(content)

    def makefile(self, mode):
        return self.handle

def get_response_header(data):
    sock = SocketBytesIO(data)
    response = HTTPResponse(sock)
    response.begin()
    header_length = len(data.split(b'\r\n\r\n')[0]) + 4
    return response.status, header_length, int(response.getheader('Content-Length'))

def get_response_body(data):
    sock = SocketBytesIO(data)
    response = HTTPResponse(sock)
    response.begin()
    return urllib3.HTTPResponse.from_httplib(response).data

def get_response_body_json(data):
    sock = SocketBytesIO(data)
    response = HTTPResponse(sock)
    response.begin()
    data = urllib3.HTTPResponse.from_httplib(response).data

    try:
        body_json  = json.loads(data)
        return True, body_json
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        return False, {}

    return False, {}




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



def all_N(space_list, line_end_location) :

    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != line_end_location and status != 'N':
            return False

    return True






def query_ticket(item) :

    book_config = item['book_config']

    data = {
        "sessionId": item['sessionid'],
        "command": 'A' + book_config["date"] + book_config["from"] + book_config["to"] + '/' + book_config["comp"],
        "allowEnhanced": True
    }

    item['data'] = json.dumps(data)
    item['callback_for_success'] = callback_for_query_ticket

    send_queue.put(item)



def occupy_ticket(item, book_space, line) :

    data = {
        "sessionId": item['sessionid'],
        "command": '01' + book_space + line,
        "allowEnhanced": True
    }

    item['data'] = json.dumps(data)
    item['callback_for_success'] = callback_for_occupy_ticket

    send_queue.put(item)



def quick_booking(item) :

    book_config = item['book_config']

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
        "sessionId": item['sessionid'],
        "command": cmd,
        "allowEnhanced": True
    }

    item['data'] = json.dumps(data)
    item['callback_for_success'] = callback_for_quick_booking

    send_queue.put(item)




def callback_for_query_ticket(item, message):

    book_config = item['book_config']

    # 航班过去，重新回去刷票
    if 'DEPARTED' in message["text"]:
        logger.warning("请确认是否航班已经过期 ...")
        set_run_status(RunStatus.QUERY)
        return

    # 掉线，重新回去登录和刷票
    if 'SYSTEM ERROR' in message["text"] \
            or 'Session does not exist' in message["text"]:
        logger.warning('掉线重新登录')
        set_run_status(RunStatus.LOGIN_QUERY)
        return

    attrlist = message["masks"]["special"]["attrList"]

    # 查询匹配的航班，失败重新回去刷票
    ret, line, comp_flight_location = parse_flight(
        attrlist,
        book_config['comp'],
        book_config['flight']
    )
    if ret == False:
        set_run_status(RunStatus.QUERY)
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
    if all_N( space_list,line_end_location ) == True:
        set_run_status(RunStatus.QUERY)
        return

    # 处理所有的占座及订座

    # 处理有座状态
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == line_end_location or status == 'N':
            continue

        # 有位置, 立即占票及订票
        if status >= "1" and status <= "9":
            logger.warning("航班 [" + book_config["comp"] + book_config["flight"] + "] 有票 : " + attrlist[location]["text"])

            occupy_ticket(
                item,
                book_space,
                line
            )
            return


    # 刷票+占票模式，不进行快速预定，重新去刷票
    if base_config["mode"] == 0:
        set_run_status(RunStatus.QUERY)
        return

    # 刷票+占票+快速预定模式下，处理带有C状态的票
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == line_end_location or status == 'N':
            continue

        # 找到了对应仓位，但候补关闭，刷票+占票+快速预定模式下，执行快速预订
        if status == 'C':
            quick_booking(item)
            return

    # 候补状态，L, 0 等等重新刷票



def callback_for_occupy_ticket(item, message) :

    if 'UNABLE - DUPLICATE SEGMENT' in message['text']:
        logger.warning('前期占票命令已经执行...')
        set_run_status(RunStatus.OCCUPIED)
        return

    # 占票失败，重新回去刷票
    if 'HL' in message["text"] or \
            'LL' in message["text"]:
        logger.warning('占票失败')
        three_i_command(item['sessionid'])
        set_run_status(RunStatus.QUERY)
        return

    if 'HS' not in message["text"]:
        logger.warning('占票失败')
        set_run_status(RunStatus.QUERY)
        return

    # HS
    logger.warning('占票成功')
    set_run_status(RunStatus.OCCUPIED)

    if base_config["manual"] == True:
        return True

    auto_booking(item)




def callback_for_quick_booking(item, message):

    # 失败，重新回去刷票
    if 'text' not in message:
        logger.warning('快速预定失败')
        set_run_status(RunStatus.QUERY)
        return

    # 掉线，重新回去登录刷票
    if 'SYSTEM ERROR' in message["text"] \
            or 'Session does not exist' in message["text"]:
        logger.warning('掉线重新登录')
        set_run_status(RunStatus.LOGIN_QUICKBOOK)
        return

    # 票面关闭，重新快速预定
    if '*0 AVAIL/WL CLOSED*' in message["text"]:
        logger.warning('票面关闭中')
        set_run_status(RunStatus.QUICKBOOK)
        return

    # 票面禁止销售
    if '*SELL RESTRICTED*' in message["text"]:
        logger.warning('票面禁止销售')
        set_run_status(RunStatus.QUICKBOOK)
        return

    # 产生了HL LL错误，重新回去刷票
    if 'HL' in message["text"] or \
            'LL' in message["text"]:
        set_run_status(RunStatus.QUERY)
        return


    if 'HS' not in message["text"]:
        logger.warning('快速预定失败')
        set_run_status(RunStatus.QUERY)
        return

    # HS
    logger.warning('快速预定成功')
    set_run_status(RunStatus.OCCUPIED)

    if base_config["manual"] == True:
        return

    auto_booking(item)




def auto_booking(item):
    sessionid = item['sessionid']
    book_config = item['book_config']

    # 客户姓名
    while True :
        ret, message = execute_instruction(sessionid, book_config["user"])
        if ret == False :
            continue

        if 'text' in message and 'INVALID NAME - DUPLICATE ITEM' in message["text"]:
            logger.warning('前期客户姓名命令已经执行...')

        break


    # 客户手机
    while True :
        ret, message = execute_instruction(sessionid, book_config["contact"])
        if ret == False :
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户电话命令已经执行...')

        break


    # 客户email
    while True :
        ret, message = execute_instruction(sessionid, book_config["email"])
        if ret == False :
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户邮箱命令已经执行...')

        break


    # R.PEI
    while True :
        ret, message = execute_instruction(sessionid, "R.PEI")
        if ret == False:
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期R.PEI命令已经执行...')

        break



    # T.T*
    while True :
        ret, message = execute_instruction(sessionid, "T.T*")
        if ret == False:
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期T.T*命令已经执行...')

        break



    # ER
    while True :
        ret, message = execute_instruction(sessionid, "ER")
        if ret == False:
            continue

        break


    if 'HK' not in message["text"]:
        return False, message["text"]


    name = book_config["user"].strip('N.').replace('/','')
    id = message["text"].split('\n')[0].split('/')[0]
    logger.warning("存档 : " + name + '-' + id)
    myfile.save(name + '-' + id, message["text"])
    logger.warning('订票存档成功 !!!')
    os.system(r"start /b BookInfo.exe")

    three_i_command(item['sessionid'])

    set_run_status(RunStatus.OVER)

    return True, ''



def do_send():
    while True:
        if get_run_status() == RunStatus.OVER:
            send_queue.queue.clear()
            return

        try:
            item = send_queue.get(timeout=1)

            if get_run_status() == RunStatus.OCCUPIED :
                continue

        except:
            continue

        content = \
            (
                "POST /TWS/TerminalCommand HTTP/1.1\r\n"
                "Host: webagentapp.tts.com\r\n"
                "Accept: application/json, text/javascript, */*; q=0.01\r\n"
                "Cache-Control: no-cache\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: %d\r\n"
                "Connection: keep-alive\r\n\r\n"
                "%s"
            ) % (len(item['data']), item['data'])

        try:
            sock = ssl.wrap_socket(socket.socket())
            sock.connect(('webagentapp.tts.com', 443))
            logger.warning('------ send ------ ')
            sock.sendall(content.encode("utf-8"))

            logger.warning(content)
                
            read_list.append(HttpRequest(sock, item))
            logger.warning('添加socket=%d'%(sock.fileno()))

        except BlockingIOError as e:
            logger.warning('错误产生')
            logger.warning(json.dumps(item))

def do_recv():
    while True:
        if get_run_status() == RunStatus.OVER:
            read_list.clear()
            return

        if not read_list:
            time.sleep(1)
            continue

        for http_req in read_list :
            if get_run_status() == RunStatus.OCCUPIED :
                http_req.sock.close()
                read_list.remove(http_req)
                continue

            http_req.read_count += 1

            if http_req.read_count >= 30:  # 如果经过了30次的select轮询，依旧没有连接成功，则说明连接出现了问题。关闭此连接
                http_req.sock.close()
                read_list.remove(http_req)
                continue


        if not read_list :
            time.sleep(1)
            continue

        logger.warning("------ select read ------")
        r, _, _ = select.select([read_list[0]], [], [], 1)
        for http_request in r:
            """请求得到响应，接收数据"""

            if 'callback_for_failure' in http_request.item :
                callback_for_failure = http_request.item['callback_for_failure']
            if 'callback_for_success' in http_request.item :
                callback_for_success = http_request.item['callback_for_success']


            http_request.response_data += http_request.sock.recv(60000)
            logger.warning('socket=%d' % http_request.sock.fileno())
            logger.warning(http_request.response_data)

            # 判断是否获取过http状态
            if http_request.response_status != 200 :

                # 获取http状态
                http_request.response_status, \
                http_request.response_header_length, \
                http_request.response_content_length = \
                    get_response_header(http_request.response_data)

                if http_request.response_status != 200:
                    http_request.sock.close()
                    read_list.remove(http_request)

                    logger.warning(
                        'socket=%d, http响应状态=%d' %
                        (
                            http_request.sock.fileno(),
                            http_request.response_status
                        )
                    )

                    if callback_for_failure:
                        _thread.start_new_thread(callback_for_failure, (http_request.item))
                    continue


            logger.warning(
                'socket=%d, data.length=%d, header_length=%d, content_length=%d' %
                (
                    http_request.sock.fileno(),
                    len(http_request.response_data),
                    http_request.response_header_length,
                    http_request.response_content_length
                )
            )

            # 尚未接收完整
            if len(http_request.response_data) != http_request.response_header_length + http_request.response_content_length  :

                continue

            # 数据接收完整了
            http_request.sock.close()
            read_list.remove(http_request)

            ret, body_json = get_response_body_json(http_request.response_data)
            if ret == False :
                if callback_for_failure:
                    _thread.start_new_thread(callback_for_failure, (http_request.item))
                continue


            if body_json["success"] == False:
                logger.warning('返回状态非success')
                if callback_for_failure:
                    _thread.start_new_thread(callback_for_failure, (http_request.item))
                continue

            if 'message' not in body_json:
                logger.warning('返回数据中未发现message信息')
                if callback_for_failure:
                    _thread.start_new_thread(callback_for_failure, (http_request.item))
                continue


            _thread.start_new_thread(callback_for_success, (http_request.item, body_json['message']))




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



def munual_booking(sessionid, book_config):
    logger.warning("进入命令行, 进行手动订票...")
    while True:
        cmd = input("\n> ")

        if cmd.strip('') == '' :
            continue

        if cmd == "loop":
            break

        if cmd == "exit":
            exit(0)

        ret, message = execute_instruction(sessionid, cmd)
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


def main() :

    branch_size = base_config["branch_size"]

    for book_config in book_config_list:

        logger.warning('')
        logger.warning('')
        logger.warning('开始订票 = ' + json.dumps(book_config))

        sth = sendThread()
        rth = readThread()
        rth.start()
        sth.start()
        logger.warning('读写线程已启动 ...')

        
        set_run_status(RunStatus.LOGIN_QUERY)

        sessionid = ''
        while True:

            if limit() == True:
                exit(0)

            if get_run_status() == RunStatus.LOGIN_QUERY:
                sessionid = login()
                set_run_status(RunStatus.QUERY)
                query_ticket({'sessionid': sessionid, 'book_config': book_config})
                time.sleep(1 / branch_size)
                continue

            if get_run_status() == RunStatus.QUERY:
                query_ticket({'sessionid': sessionid, 'book_config': book_config})
                time.sleep(1 / branch_size)
                continue

            if get_run_status() == RunStatus.OCCUPIED:
                if base_config["manual"] == True:
                    munual_booking(sessionid)
                    break

                # 自动情况下，已经占票成功，什么也不做，等待订票成功退出
                time.sleep(1 / branch_size)
                continue

            if get_run_status() == RunStatus.QUICKBOOK:
                quick_booking({'sessionid': sessionid, 'book_config': book_config})
                time.sleep(1 / branch_size)
                continue

            if get_run_status() == RunStatus.LOGIN_QUICKBOOK:
                sessionid = login()
                set_run_status(RunStatus.QUICKBOOK)
                quick_booking({'sessionid': sessionid, 'book_config': book_config})
                time.sleep(1 / branch_size)
                continue

            if get_run_status() == RunStatus.OVER:
                break

        logger.warning('等待读写线程退出 ...')
        sth.join()
        rth.join()

    logger.warning ("退出主线程")



if __name__ == '__main__':
    main()
