#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import time
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy

from mylog import *

def get_config(filename) :
    try:
        with open(filename, 'r') as thefile:
            return True, json.load(thefile)
    except:
        logger.warning("配置文件 [" + filename + "] 有误, 请重新配置 ...")
        return False, {}

def save_result(name, message):
    fo = open(name + '-' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.txt', "w")
    fo.write(message)
    fo.close()


def save_excel_result(result_pnr, result_vl, result_vr, result_si) :
    sheet_name = datetime.datetime.now().strftime('%Y.%m.%d')
    read_workbook = open_workbook("result.xls")  # 用wlrd提供的方法读取一个excel文件

    try :
        read_sheet = read_workbook.sheet_by_name(sheet_name)
        line = read_sheet.nrows
    except xlrd.biffh.XLRDError :
        line = 0

    write_workbook = copy(read_workbook)

    if line == 0 :
        write_sheet = write_workbook.add_sheet(sheet_name)
    else :
        index = write_workbook.sheet_index(sheet_name)
        write_sheet = write_workbook.get_sheet(index)

    write_sheet.write(line, 0, result_pnr)
    write_sheet.write(line, 1, result_vl)
    write_sheet.write(line, 2, result_vr)
    write_sheet.write(line, 3, result_si)


    while True :
        try :
            write_workbook.save("result.xls")  # xlwt对象的保存方法，这时便覆盖掉
            break
        except PermissionError :
            logger.warning('请关闭result.xls文档后再试.')
            time.sleep(1)
            continue

