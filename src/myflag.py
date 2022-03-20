#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading

# 舱位占有标志
flag_occupied = False
mutex_occupied = threading.Lock()

def set_flag_occupied(flag) :
    with mutex_occupied :
        global flag_occupied
        flag_occupied = flag

def get_flag_occupied() :
    with mutex_occupied :
        global flag_occupied
        return flag_occupied


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
