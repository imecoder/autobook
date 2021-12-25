#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

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


def save_excel_result(message) :
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    sheet_name = datetime.datetime.now().strftime('%Y-%m-%d')

    read_workbook = open_workbook("result.xls")  # 用wlrd提供的方法读取一个excel文件
    write_workbook = copy(read_workbook)

    sheets = read_workbook.sheets()

    for read_sheet in sheets :
        if read_sheet.name != sheet_name :
            continue

        rows = read_sheet.nrows
        write_sheet = write_workbook.sheet_by_name(sheet_name)
        write_sheet.write(rows, 0, message)  # xlwt对象的写方法，参数分别是行、列、值
        write_sheet.write(rows, 1, current_datetime)
        write_workbook.save("result.xls")  # xlwt对象的保存方法，这时便覆盖掉
        return

    write_sheet = write_workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    write_sheet.write(0, 0, message)  # xlwt对象的写方法，参数分别是行、列、值
    write_sheet.write(0, 1, current_datetime)
    write_workbook.save("result.xls")  # xlwt对象的保存方法，这时便覆盖掉
