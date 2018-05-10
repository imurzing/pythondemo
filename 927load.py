#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'tinykay'
__mtime__ = '9/27/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import os
import xlrd
import re
import time
import pymysql as mysql


config = {
    'host': '192.168.1.105',
    'port': 3306,
    'user': "root",
    'passwd': "!QAZ2wsx",
    'db': "qsdjf_cunguan",
    'charset': "utf8"
}


# 查询方法
def db_tool(sql):
    dbs = mysql.connect(**config)
    c = dbs.cursor(mysql.cursors.DictCursor)
    c.execute(sql)
    ones = [et for et in c.fetchall()]
    dbs.commit()
    dbs.close()
    return ones


# Insert及Update使用方法
def db_tool_m(sql_list):
    db_cnt = mysql.connect(**config)
    try:
        cursor = db_cnt.cursor(mysql.cursors.DictCursor)
        if isinstance(sql_list, list):
            for sql in sql_list:
                cursor.execute(sql)
        else:
            cursor.execute(sql_list)
        db_cnt.commit()
    except mysql.Error:
        db_cnt.rollback()
        print('执行失败，回滚!!!')
    db_cnt.close()


def file_name(file_dir):
    file_list = list()
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.xls' or os.path.splitext(file)[1] == '.xlsx':
                file_list.append(os.path.join(root, file))
    return file_list


def check_file(file_list):
    bad_signal = 0
    for file in file_list:
        try:
            xlrd.open_workbook(file)
        except:
            print(file+'   异常!!请检查!!')
            bad_signal += 1
    if bad_signal:
        exit(1)


list1 = file_name('logs')
check_file(list1)
for list2 in list1:
    print(list2)
    data = xlrd.open_workbook(list2)
    print(data.sheet_names())
    table = data.sheets()[1]
    table1 = data.sheets()[2]
    rows = table.nrows
    cols = table.ncols
    rows1 = table1.nrows
    cols1 = table1.ncols
    array = set()
    array2 = set()
    for i in range(3, rows):
        array.add((table.cell(i, 0).value, table.cell(i, 1).value.strip()))
    for i in range(3, rows1):
        array2.add((table1.cell(i, 0).value, table1.cell(i, 1).value.strip()))
    print(array)
    print(array2)
    minus = array - array2
    minus2 = array2 - array
    b = array & array2
    print(minus)
    print(minus2)
    print(b)
    for i in minus:
        sql = ("INSERT INTO custody_bank (`name`,`gmt_created`,`gmt_modified`,"
               "`parent_bank_id`,`support`) VALUES ('{name}',NOW(),NOW(),"
               "'{parent_id}','{support}')".format(
                name=i[1],
                parent_id=i[0],
                support='1'))
        db_tool_m(sql)
    for i in minus2:
        sql = ("INSERT INTO custody_bank (`name`,`gmt_created`,`gmt_modified`,"
               "`parent_bank_id`,`support`) VALUES ('{name}',NOW(),NOW(),"
               "'{parent_id}','{support}')".format(
                name=i[1],
                parent_id=i[0],
                support='2'))
        db_tool_m(sql)
    for i in b:
        sql = ("INSERT INTO custody_bank (`name`,`gmt_created`,`gmt_modified`,"
               "`parent_bank_id`,`support`) VALUES ('{name}',NOW(),NOW(),"
               "'{parent_id}','{support}')".format(
                name=i[1],
                parent_id=i[0],
                support='3'))
        db_tool_m(sql)
