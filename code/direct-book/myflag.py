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
