'''
这是select读写基本使用，这是个是客户端实例
'''


import socket
import select


class HttpRequest:
    def __init__(self, sock, item):
        self.sock = sock
        self.item = item

    def fileno(self):
        return self.sock.fileno()


class AsyncHttp:
    def __init__(self):
        self.list_connections = []
        self.list_sockets = []

    def start(self, item):
        try:
            sock = socket.socket()
            sock.setblocking(False)   # 设置为不阻塞的socket，这样sockt的通信不能自动完成
            sock.connect((item['host'], 80,))
        except BlockingIOError as e:
            self.list_sockets.append(HttpRequest(sock, item))
            self.list_connections.append(HttpRequest(sock, item))

    def run(self):
        while True:
            """循环监测，返回值r，w。
            w有值代表连接成功，可以发请求了。
            r有值代表请求已经得到响应了，可以收数据了。
            传的参数是被监控的[socket0, socket1, socket2]列表
            """
            print("------ select ------")
            r, w, x = select.select(self.list_connections, self.list_sockets, [], 0.05)
            for http_request in w:
                """连接成功了，可以发请求了"""
                print('------ send ------')
                host = http_request.item['host']
                url = http_request.item['url']
                content = 'GET %s HTTP/1.0\r\nHost:%s\r\n\r\n' % (url, host)
                http_request.sock.sendall(content.encode("utf-8"))
                self.list_sockets.remove(http_request)
            for http_request in r:
                """请求得到响应，接收数据"""
                print('------ recv ------')
                data = http_request.sock.recv(8096)
                http_request.sock.close()
                http_request.item['callback'](data)  # 回调
                self.list_connections.remove(http_request)
            if len(self.list_connections) == 0:
                break


def callback(data):
    print(data)


# 调用方式
ep_io = AsyncHttp()

list_url = [
    {"host": "www.baidu.com", "url": "/", "callback": callback},
    {"host": "www.bing.com", "url": "/", "callback": callback},
    {"host": "www.cnblogs.com", "url": "/staff/p/13139545.html", "callback": callback},
]

for item in list_url:
    print(item)
    ep_io.start(item)

ep_io.run()
