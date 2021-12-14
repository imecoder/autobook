#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading

# 舱位占有标志
flagOccupied = False
mutexOccupied = threading.Lock()

def set_flag_occupied(flag) :
    with mutexOccupied :
        global flagOccupied
        flagOccupied = flag

def get_flag_occupied() :
    with mutexOccupied :
        global flagOccupied
        return flagOccupied


# 掉线重新登录标志
flagRelogin = False
mutexRelogin = threading.Lock()

def set_flag_relogin(flag) :
    with mutexRelogin :
        global flagRelogin
        flagRelogin = flag

def get_flag_relogin() :
    with mutexRelogin :
        global flagRelogin
        return flagRelogin


from enum import Enum

class RunStatus(Enum):
    LOGIN = 1
    QUERY = 2
    OCCUPIED = 3
    QUICKBOOK = 4
    OVER = 5

# 运行状态

run_statue = RunStatus.QUERY
mutex_run_status = threading.Lock()

def set_run_status(flag) :
    with mutex_run_status :
        global run_statue
        run_statue = flag

def get_run_status() :
    with mutex_run_status :
        global run_statue
        return run_statue
