''''
select 异步socket客户端实例
把请求连接、监听发送队列、监听接收队列放到不同的线程中里。
'''


import socket
import select
import time
import threading


class HttpRequest:
    def __init__(self, sock, item):
        self.sock = sock
        self.item = item

    def fileno(self):
        return self.sock.fileno()


list_read = []
list_write = []

def doconnect(item):
    try:
        sock = socket.socket()
        sock.setblocking(False)   # 设置为不阻塞的socket，这样sockt的通信不能自动完成
        sock.connect((item['host'], 80,))
    except BlockingIOError as e:
        list_write.append(HttpRequest(sock, item))
        list_read.append(HttpRequest(sock, item))


def dosend():
    while True:
        if not list_write :
            time.sleep(1)
            continue

        print("------ select write ------")
        _, w, _ = select.select([], list_write, [], 1)
        for http_request in w:
            """连接成功了，可以发请求了"""
            host = http_request.item['host']
            url = http_request.item['url']
            content = 'GET %s HTTP/1.0\r\nHost:%s\r\n\r\n' % (url, host)
            print('send ' + host )
            http_request.sock.sendall(content.encode("utf-8"))
            list_write.remove(http_request)


def dorecv():
    while True:
        if not list_read:
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


class writeThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dosend()


class readThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dorecv()


# 创建新线程
connectthread = connectThread()
writethread = writeThread()
readthread = readThread()


# 开启新线程
writethread.start()
time.sleep(0.01)
readthread.start()
connectthread.start()

connectthread.join()
writethread.join()
readthread.join()

print ("退出主线程")

