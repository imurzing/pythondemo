#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'transformer'
__author__ = 'tinykay'
__mtime__ = '9/13/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import os
import xlrd
import re
import time


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
        input("Press Enter to Exit:")
        exit(1)


def match_time(columns):
    for element in range(columns):
        try:
            value = xlrd.xldate.xldate_as_datetime(table.cell(1, element).value, 0).strftime('%Y-%m-%d %H:%M:%S')
        except:
            value = table.cell(1, element).value
        result = re.match(r'^20\d{2}-', str(value))
        if result:
            return element


def match_idfa(columns):
    for element in range(columns):
        value = table.cell(1, element).value
        result = re.match(r'^\w{8}-\w{4}-', str(value))
        if result:
            return element


def match_ip(columns):
    for element in range(columns):
        value = table.cell(1, element).value
        result = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(value))
        if result:
            return element


list1 = file_name('logs')
check_file(list1)
today = time.strftime('%Y%m%d')
channel = input("请输入渠道(username):")
attachment = open('out/{today}{channel}.csv'.format(today=today, channel=channel), 'w')
attachment2 = open('out/log{today}{channel}.txt'.format(today=today, channel=channel), 'a')
attachment.write('"IDFA","时间","IP"\n')
for list2 in list1:
    data = xlrd.open_workbook(list2)
    table = data.sheets()[0]
    rows = table.nrows
    cols = table.ncols
    attachment2.write(list2 + '\n')
    attachment2.write(str(rows) + ' 行记录\n')
    res_time = match_time(cols)
    res_idfa = match_idfa(cols)
    res_ip = match_ip(cols)
    if res_idfa is None:
        print('idfa not found!!')
        exit(1)
    insert_ip = '127.0.0.1'
    start_signal = 1
    for ele in range(cols):
        check_title = table.cell(0, ele).value
        check_result = re.match(r'^\w{8}-\w{4}-', str(check_title))
        if check_result:
            start_signal = 0
    for i in range(start_signal, rows):
        if res_ip:
            insert_ip = table.cell(i, res_ip).value
        try:
            active_time = (xlrd.xldate.xldate_as_datetime(table.cell(i, res_time).value, 0).
                           strftime('%Y-%m-%d %H:%M:%S'))
        except:
            active_time = table.cell(i, res_time).value
        if not table.cell(i, res_idfa).value:
            continue
        attachment.write('"'+table.cell(i, res_idfa).value+'"," '+active_time+'","'+insert_ip+'"\n')
attachment.close()
attachment2.close()
