#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from mylog import *


from enum import Enum

class RunStatus(Enum):
    LOGIN = '登录'
    QUERY = '刷票'
    QUICKBOOK = '快速预定'
    OCCUPIED = '占票'
    OVER = '订票完成'

# 运行状态

run_statue = RunStatus.QUERY
mutex_run_status = threading.Lock()

def set_run_status(flag) :
    with mutex_run_status :
        global run_statue
        run_statue = flag
        logger.warning('设置状态 = %s' % flag.value )


def get_run_status() :
    with mutex_run_status :
        global run_statue
        return run_statue
