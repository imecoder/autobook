#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading

# 舱位记录标志
flagSpace = True
mutexSpace = threading.Lock()

def set_flag_space(flag) :
    with mutexSpace :
        global flagSpace
        flagSpace = flag

def get_flag_space() :
    with mutexSpace :
        global flagSpace
        return flagSpace

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
