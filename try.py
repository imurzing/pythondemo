#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhang'
__mtime__ = '5/11/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃       ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import hashlib
import random
import time
import datetime
from dateutil.relativedelta import relativedelta
import math
import os
import pymysql as mysql
import time


config = {
    'host': '192.168.1.105',
    'port': 3306,
    'user': "root",
    'passwd': "!QAZ2wsx",
    'db': "qsdjf",
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
    cursor = db_cnt.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql_list)
    db_cnt.commit()
    db_cnt.close()


sql = ("SELECT me.id as memid,act.id as actid,me.channel,me.device_type"
       " from  member me LEFT JOIN account act on "
       "act.member_id=me.id  "
       "where act.id!=''and act.id IS not null and me.channel>0 and me.channel <150 ")
res = db_tool(sql)
e = 0
lens = len(res)
print(lens)
pay_order_no = 2045829668047980
for i in range(9999):
    member_id = res[e]['memid']
    account_id = res[e]['actid']
    channel = res[e]['channel']
    device_type = res[e]['device_type']
    pay_order_no1 = str(pay_order_no)
    sql1 = ("INSERT INTO `qsdjf`.`pay_order` (`account_id`, `member_id`,"
            " `to_account_id`, `pay_order_no`, `out_order_no`, `bank_code`,"
            " `bank_name`, `type`, `channel`, `amount`, `status`, `device_type`,"
            " `notice`, `gmt_created`, `gmt_modified`, `biz_order_no`, "
            "`edition`, `flow_type`, `pay_type`, `refund_status`) VALUES "
            "({aid}, {mid}, {aid}, {pay_order_no},"
            " NULL, 'PAB', '平安银行', '3', '1', '888.00', '1', {device_type},"
            " '', now(), now(),"
            " '', '1', '1', '2', '1')").format(
        aid=account_id,
        mid=member_id,
        device_type=device_type,
        pay_order_no=pay_order_no1)
    db_tool_m(sql1)
    pay_order_no += 200
    e = e + 1
    if e == 146:
        e = 0


def secret(snake):
    god = hashlib.md5(snake.encode(encoding='utf-8'))
    return god.hexdigest()

cc = hash('123456789'.encode(encoding='utf-8'))
dd = hashlib.sha512('123456789'.encode(encoding='utf-8')).hexdigest()
print(cc)
print(secret('Dx9Ric8RBRjynJ00FhMN'))
print(dd)

print(int(4.56))


def fuck(fn):
    print("fuck %s!" % fn.__name__[::-1].upper())


@fuck
def wfg():
    pass


def generate_verification_code():
    code_list = [str(element) for element in range(10)]
    my_slice = random.sample(code_list, 6)
    verification_code = ''.join(my_slice)
    return verification_code


print(generate_verification_code())
print([i for i in range(int(0))])
for i in range(3):
    print(i)

print(time.strftime('%Y-%m'))
print(type(time.strftime('%Y-%m')))

start_time = time.strftime('%Y-%m') + '-01'
end_time = datetime.datetime.strftime(datetime.datetime.strptime(time.strftime('%Y-%m-%d'), "%Y-%m-%d")
                                      + relativedelta(days=1), '%Y-%m-%d')
print(start_time)
print(end_time)
agent = "%s is delicious, we must protect them"
agent = agent % 'ant'
print(agent)
print(math.floor(0.3+0.3+0.3+0.1))

b = 108000
a = 0
for i in range(11):
    a += b*0.11/12
    print(a)
    b += b*0.11/12
    b -= 9810
    print(b)
print(a, b)

# file = open('logs/gg.csv', 'w')
# file.write('"设备","渠道","首投并复投金额"')
# file.close()
# os.remove('logs/gg.csv')

l = [1, 2, 3, 4, 5, 6, 7]
l = sum(l)
print(l)

