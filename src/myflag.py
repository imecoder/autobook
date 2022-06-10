#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading

# 掉线重新登录标志
flag_relogin = False
mutex_relogin = threading.Lock()

def set_flag_relogin(flag) :
    with mutex_relogin :
        global flag_relogin
        flag_relogin = flag

def get_flag_relogin() :
    with mutex_relogin :
        global flag_relogin
        return flag_relogin


# 预订个数
condition = 5
occupied = 0
mutex_occupied = threading.Lock()

def set_condition(_condition) :
    with mutex_occupied :
        global condition
        condition = _condition

def occupied_append() :
    with mutex_occupied :
        global occupied
        occupied = occupied+1

def is_occupied_over() :
    with mutex_occupied :
        global occupied
        global condition
        return occupied >= condition