#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import datetime
from mylog import *

def get_config(filename) :
    try:
        with open(filename, 'r') as thefile:
            return True, json.load(thefile)
    except:
        logger.info("配置文件 [" + filename + "] 有误, 请重新配置 ...")
        return False, {}

def save(name, message):
    fo = open(name + '-' + datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S') + '.txt', "w")
    fo.write(message)
    fo.close()