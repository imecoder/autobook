#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import datetime
from mylog import *

def read_json(filename) :
    try:
        with open(filename, 'r') as thefile:
            return True, json.load(thefile)
    except:
        logger.warning("json 文件 [" + filename + "] 读取有误 ...")
        return False, {}


def write_json(filename, thejson) :
    try:
        with open(filename, 'w') as thefile:
            return True, thefile.write(json.dumps(thejson, indent=4))
    except:
        logger.warning("json文件 [" + filename + "] 写入有误 ...")
        return False, {}

def save(name, message):
    fo = open(name + '-' + datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S') + '.txt', "w")
    fo.write(message)
    fo.close()