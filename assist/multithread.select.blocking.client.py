''''
select 异步socket客户端实例
把请求连接、监听发送队列、监听接收队列放到不同的线程中里。
这是短连接模式。即收发送消息，收到消息就断开连接。
如果是长链接模式，此模型并不适用。
'''


import socket
import select
import time
import threading


class HttpRequest:
    def __init__(self, sock, item):
        self.sock = sock
        self.item = item
        self.write_count = 0
        self.read_count = 0

    def fileno(self):
        return self.sock.fileno()


list_read = []

def doconnect(item):
    try:
        sock = socket.socket()
        sock.connect((item['host'], 80,))
        host = item['host']
        url = item['url']
        content = 'GET %s HTTP/1.0\r\nHost:%s\r\n\r\n' % (url, host)
        print('send ' + host)
        sock.sendall(content.encode("utf-8"))

        list_read.append(HttpRequest(sock, item))
    except BlockingIOError as e:
        print("-------------- error ---------------")



def dorecv():
    while True:
        if not list_read:
            time.sleep(1)
            continue


        for elem in list_read :
            elem.write_count += 1
            if elem.write_count >= 30 :     # 如果经过了30次的select轮询，依旧没有连接成功，则说明连接出现了问题。关闭此连接
                elem.sock.close()
                list_read.remove(elem)

        if not list_read :
            time.sleep(1)
            continue

        print("------ select read ------")
        r, _, _ = select.select(list_read, [], [], 1)
        for http_request in r:
            """请求得到响应，接收数据"""
            print('recv ' + http_request.item['host'])
            data = http_request.sock.recv(8096)
            http_request.sock.close()
            http_request.item['callback'](data)  # 回调
            list_read.remove(http_request)


def callback(data):
    print(data)
    print('')


list_url = [
    {"host": "www.baidu.com", "url": "/", "callback": callback},
    {"host": "www.bing.com", "url": "/", "callback": callback},
    {"host": "www.cnblogs.com", "url": "/staff/p/13139545.html", "callback": callback},
]


class connectThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for item in list_url:
            doconnect(item)
            time.sleep(2)


class readThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dorecv()


# 创建新线程
connectthread = connectThread()
readthread = readThread()


# 开启新线程
readthread.start()
connectthread.start()

connectthread.join()
readthread.join()

print ("退出主线程")

