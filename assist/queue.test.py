import queue
import threading
import time


q = queue.Queue()

print(q.maxsize)


class putThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        q.put(1)  # 进队列
        time.sleep(2)
        q.put(2)


class getThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("qsize:{}".format(q.qsize()))  # 取队列当前队列长度
        # print(q.get())  # 出队列
        print(q.get())
        print(q.get())
        print("qsize:{}".format(q.qsize()))
        # print(q.get_nowait())# 不检测队列是否为空，为空则报错



# 创建新线程
pth = putThread()
gth = getThread()


# 开启新线程
gth.start()
pth.start()

pth.join()
gth.join()

