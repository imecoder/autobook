import http
import socket
import ssl
import select
import json
import os
import _thread
import queue
import time

from mylog import *
from myflag import *
from myfile import*
from mynet import *


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


    request_body = json.dumps(user)

    request_data = \
        (
            "POST /TWS/Login HTTP/1.1\r\n"
            "Host: webagentapp.tts.com\r\n"
            "Accept: application/json, text/javascript, */*; q=0.01\r\n"
            "Cache-Control: no-cache\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: %d\r\n"
            "Connection: keep-alive\r\n\r\n"
            "%s"
        ) % (len(request_body), request_body)

    while True:
        sock = ssl.wrap_socket(socket.socket())
        sock.connect(('webagentapp.tts.com', 443))
        sock.sendall(request_data.encode("utf-8"))

        http_content = b''

        while True :
            buf = sock.recv(60000)

            if debug:
                logger.info('socket=%d 接收到数据=%s' % (sock.fileno(), str(buf)))

            http_content += buf

            # 如果不满足一个完整的http头部，回去继续接收后续数据
            if len(http_content) < 1000:
                continue

            # 获取http状态
            status, header_length, content_length = get_response_header(http_content)

            # 说明网络错误，需要重新登录
            if status != 200:
                logger.warning('socket=%d, http响应状态=%d' % (sock.fileno(), status))

                sock.close()
                break

            if debug:
                logger.info(
                    'socket=%d, data.length=%d, header_length=%d, content_length=%d' %
                    (
                        sock.fileno(),
                        len(http_content),
                        header_length,
                        content_length
                    )
                )

            # 尚未接收完整
            if len(http_content) < header_length + content_length:
                continue

            if debug:
                logger.info('socket=%d, 数据接收完成' % sock.fileno())

            ret, body_json = get_response_body_json(http_content)
            if ret == False:
                break

            if body_json["success"] == False:
                logger.warning('返回状态非success')
                break

            if 'sessionId' not in body_json:
                logger.warning('返回数据中未发现 [sessionId] 信息')
                break

            logger.warning('登录成功')

            session_id = body_json['sessionId']

            three_i_command(session_id)

            return session_id, sock



def auto_booking(session_id, book_config):
    # 客户姓名
    while True:
        ret, message = execute_instruction(session_id, book_config["user"])
        if ret == False:
            continue

        if 'text' in message and 'INVALID NAME - DUPLICATE ITEM' in message["text"]:
            logger.warning('前期客户姓名命令已经执行')

        break

    # 客户手机
    while True:
        ret, message = execute_instruction(session_id, book_config["contact"])
        if ret == False:
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户电话命令已经执行')

        break

    # 客户email
    while True:
        ret, message = execute_instruction(session_id, book_config["email"])
        if ret == False:
            continue

        if 'text' in message and 'ADD/DELETE RESTRICTED ON RETRIEVED BOOKING' in message["text"]:
            logger.warning('前期客户邮箱命令已经执行')

        break

    # R.PEI
    while True:
        ret, message = execute_instruction(session_id, "R.PEI")
        if ret == False:
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期R.PEI命令已经执行')

        break

    # T.T*
    while True:
        ret, message = execute_instruction(session_id, "T.T*")
        if ret == False:
            continue

        if 'text' in message and 'SINGLE ITEM FIELD' in message["text"]:
            logger.warning('前期T.T*命令已经执行')

        break

    # ER
    while True:
        ret, message = execute_instruction(session_id, "ER")
        if ret == False:
            continue

        break

    if 'CHECK' in message["text"]:
        logger.warning('请确认是否在对已经订票成功的客户，进行重复订票')
        return False

    if 'HK' not in message["text"]:
        logger.warning('请确认是否在对已经订票成功的客户，进行重复订票')
        return False

    name = book_config["user"].strip('N.').replace('/', '')
    id = message["text"].split('\n')[0].split('/')[0]
    logger.warning("存档 : " + name + '-' + id)
    save_result(name + '-' + id, message["text"])
    logger.warning('订票存档成功 !!!')
    os.system(r"start /b BookInfo.exe")

    three_i_command(session_id)

    set_run_status(RunStatus.OVER)

    return True


def munual_booking(session_id, book_config):
    logger.warning("进入命令行, 进行手动订票...")
    while True:
        command = input("\n> ")

        if command.strip('') == '':
            continue

        if command == "loop":
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
            logger.warning('前期占票命令已经执行')
            continue

        if 'INVALID NAME - DUPLICATE ITEM' in text:
            logger.warning('前期客户姓名命令已经执行')
            continue

        if 'SINGLE ITEM FIELD' in text and "R.PEI" in text:
            logger.warning('前期R.PEI命令已经执行')
            continue

        if 'SINGLE ITEM FIELD' in text and "T.T*" in text:
            logger.warning('前期T.T*命令已经执行')
            continue

        if command == "ER":
            if "SELL OPTION HAS EXPIRED - CHECK ITINERARY" in text:
                continue

            if 'NEED RECEIVED' in text:
                continue

            if 'MODIFY BOOKING' in text:
                continue

            name = book_config["user"].strip('N.').replace('/', '')
            id = text.split('\n')[0].split('/')[0]
            logger.warning("存档 : " + name + '-' + id)
            save_result(name + '-' + id, text)
            logger.warning('订票存档成功 !!!')
            os.system(r"start /b BookInfo.exe")

    set_run_status(RunStatus.OVER)



send_queue = queue.Queue()



class SendThread(threading.Thread):

    def __init__(self, sock, session_id, debug = False):
        threading.Thread.__init__(self)
        self.sock = sock
        self.session_id = session_id
        self.debug = debug

    def run(self):
        while True:

            # 已经占票的情况下，清除所有命令，继续等待
            if get_run_status() == RunStatus.OCCUPIED:
                send_queue.queue.clear()
                time.sleep(1)
                continue

            # 已经订票成功，清除所有命令，直接返回
            if get_run_status() == RunStatus.OVER:
                send_queue.queue.clear()
                logger.warning('发送线程退出')
                return

            # 循环监听任务命令
            try:
                command = send_queue.get(timeout=1)
            except:
                continue

            request_body = json.dumps(
                {
                    "sessionId": self.session_id,
                    "command": command,
                    "allowEnhanced": True
                }
            )

            request_data = \
                (
                    "POST /TWS/TerminalCommand HTTP/1.1\r\n"
                    "Host: webagentapp.tts.com\r\n"
                    "Accept: application/json, text/javascript, */*; q=0.01\r\n"
                    "Cache-Control: no-cache\r\n"
                    "Content-Type: application/json\r\n"
                    "Content-Length: %d\r\n"
                    "Connection: keep-alive\r\n\r\n"
                    "%s"
                ) % (len(request_body), request_body)

            try:
                self.sock.sendall(request_data.encode("utf-8"))

                logger.warning('[新任务] socket=%d command=%s' % (self.sock.fileno(), command))

                if self.debug:
                    logger.info(request_data)

            except BlockingIOError as e:
                logger.warning('错误产生')
                logger.warning(json.dumps(item))

        logger.warning('发送线程退出')


class RecvThread(threading.Thread):

    def __init__(self, sock, session_id, book_config, callback, debug = False):
        threading.Thread.__init__(self)
        self.sock = sock
        self.session_id = session_id
        self.book_config = book_config
        self.buffer = b''
        self.callback = callback
        self.debug = debug

    def run(self):
        while True:

            # 已经占票的情况下，清除所有命令
            if get_run_status() == RunStatus.OCCUPIED:
                time.sleep(1)
                continue

            # 已经订票成功，清除所有命令，直接返回
            if get_run_status() == RunStatus.OVER:
                logger.warning('接收线程退出')
                return

            if self.debug:
                logger.info("------ select ------")

            readable, _, _ = select.select([self.sock], [], [], 1)
            for read_socket in readable:
                """请求得到响应，接收数据"""

                buf = read_socket.recv(60000)

                if self.debug:
                    logger.info('socket=%d 接收到数据=%s' % (read_socket.fileno(), str(buf)))

                self.buffer += buf

                # 如果不满足一个完整的http头部，回去继续接收后续数据
                if len(self.buffer) < 1000 :
                    continue

                # 获取http状态
                status, header_length, content_length = get_response_header(self.buffer)

                # 说明网络错误，需要重新登录
                if status != 200:

                    logger.warning( 'socket=%d, http响应状态=%d' % ( read_socket.fileno(), status ) )

                    read_socket.close()
                    set_run_status(RunStatus.LOGIN)
                    return


                if self.debug:
                    logger.info(
                        'socket=%d, data.length=%d, header_length=%d, content_length=%d' %
                        (
                            read_socket.fileno(),
                            len(self.buffer),
                            header_length,
                            content_length
                        )
                    )

                # 尚未接收完整
                if len(self.buffer) < header_length + content_length :
                    continue

                if self.debug:
                    logger.info('socket=%d, 数据接收完成' % read_socket.fileno())

                # 数据接收完整了, 开始截断数据包
                http_content = self.buffer[0 : header_length + content_length]
                self.buffer = self.buffer[header_length + content_length : ]

                ret, body_json = get_response_body_json(http_content)
                if ret == False:
                    continue

                if body_json["success"] == False:
                    logger.warning('返回状态非success')
                    continue

                if 'message' not in body_json:
                    logger.warning('返回数据中未发现message信息')
                    continue

                _thread.start_new_thread(
                    self.callback,
                    (self.session_id, self.book_config, body_json['message'])
                )

        logger.warning('接收线程退出')


