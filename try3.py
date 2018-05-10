#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhang'
__mtime__ = '10/16/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import pymysql as mysql
import random


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
    # try:
        cursor = db_cnt.cursor(mysql.cursors.DictCursor)
        if isinstance(sql_list, list):
            for sql in sql_list:
                cursor.execute(sql)
        else:
            cursor.execute(sql_list)
        db_cnt.commit()
        db_cnt.close()
    # except mysql.Error:
    #     db_cnt.rollback()
    #     print('执行失败，回滚!!!')
    # db_cnt.close()


member_id = 9282869289
for i in range(19999):
    execute_list = list()
    member_id1 = str(member_id)
    sql1 = ("INSERT INTO `qsdjf`.`wallet` (`member_id`, `balance`, `interest`, `total_in`,"
            " `total_out`, `gmt_created`, `gmt_modified`) VALUES ('{member_id}', '{balance}', "
            "'0', '0', '0', now(), now());").format(
            member_id=member_id1,
            balance=str(random.randint(0, 10000000)/100))
    execute_list.append(sql1)
    sql2 = ("INSERT INTO `qsdjf`.`account` (`member_id`, `out_account_id`, "
            "`balance`, `withdraw_frozen`, `transfer_in_frozen`, `invest_frozen`, `frozen`, "
            "`invested`, `interest`, `total_recharge`, `total_withdraw`, `gmt_created`, `gmt_modified`, "
            "`investing_interest`, `investing_principal`, `custody_balance`, `custody_frozen_balance`) VALUES "
            "('{member_id}', NULL, '0', '0', '0', '0', '0', '0', '0', '0', '0', now(), now(), '0', "
            "'0', '0', '0');").format(member_id=member_id1)
    execute_list.append(sql2)
    db_tool_m(execute_list)
    member_id = int(member_id) + 1
