#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from mylog import *


from enum import Enum

class RunStatus(Enum):
    LOGIN_QUERY = '登录与刷票'
    QUERY = '刷票'
    OCCUPIED = '占票'
    QUICKBOOK = '快速预定'
    LOGIN_QUICKBOOK = '登录与快速预定'
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
