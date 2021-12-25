# coding:utf-8

from xlrd import open_workbook
from xlutils.copy import copy

rexcel = open_workbook("collection.xls")  # 用wlrd提供的方法读取一个excel文件
rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
values = ["1", "2", "3"]
row = rows
for value in values:
    table.write(row, 0, value)  # xlwt对象的写方法，参数分别是行、列、值
    table.write(row, 1, "haha")
    table.write(row, 2, "lala")
    row += 1
excel.save("collection.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel