#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'largerat'
__author__ = 'tinykay'
__mtime__ = '9/26/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import pymysql as mysql


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


# 检查是否仍存在wallet有余额的用户
def signal():
    sql = "select count(1) as ct from wallet where balance>=0.01"
    result = db_tool(sql)[0]['ct']
    return result


# 对单个用户进行转移wallet余额
def transaction(member_id):
    execute_list = list()
    # step 0, initialize variables
    initialize_sql = ("select @wallet_id:=0,@wallet_balance:=0,@wallet_records_id:=0,"
                      "@account_balance:=0,@account_id:=0 from dual;")
    execute_list.append(initialize_sql)
    # step 1,query wallet information
    query_wallet_sql = ("select @wallet_id:=id as id,@wallet_balance:=truncate(balance,2) as balance"
                        " from wallet where member_id={member_id} for update;".format(member_id=member_id))
    execute_list.append(query_wallet_sql)
    # step 2,insert wallet_records
    insert_wallet_records_sql = ("INSERT INTO wallet_records (`member_id`,`amount`,`type`,`pay_order_no`,"
                                 "`status`,`notice`,`gmt_created`,`gmt_modified`) VALUES "
                                 "('{member_id}',@wallet_balance,'2','','2','转出到余额'"
                                 ",now(),now());".format(member_id=member_id))
    execute_list.append(insert_wallet_records_sql)
    # step 3,query wallet_records_id
    query_wallet_records_id_sql = "SELECT @wallet_records_id:=LAST_INSERT_ID();"
    execute_list.append(query_wallet_records_id_sql)
    # step 4,insert wallet_running
    insert_wallet_running_sql = ("INSERT INTO wallet_running (`wallet_id`,`member_id`,`wallet_records_id`,"
                                 "`subject`,`balance`,`income`,`outlay`,`notice`,`gmt_created`,`gmt_modified`)"
                                 " VALUES (@wallet_id,'{member_id}',@wallet_records_id,'17','0','0',"
                                 "@wallet_balance,'钱包转出',NOW(),NOW());".format(member_id=member_id))
    execute_list.append(insert_wallet_running_sql)
    # step 5,update wallet
    update_wallet_sql = ("update wallet set balance=0,total_out=total_out+@wallet_balance,gmt_modified=NOW() "
                         "where member_id={member_id};".format(member_id=member_id))
    execute_list.append(update_wallet_sql)
    # step 6,query account
    query_account_sql = ("select @account_balance:=balance as balance,@account_id:=id as id "
                         "from account where member_id={member_id} for update;".format(member_id=member_id))
    execute_list.append(query_account_sql)
    # step 7,insert account_running
    insert_account_running_sql = ("INSERT INTO account_running (`account_id`,`pay_order_no`,`subject`,"
                                  "`balance`,`income`,`notice`,`gmt_created`,`gmt_modified`) VALUES"
                                  " (@account_id,'','17',@wallet_balance+@account_balance,@wallet_balance,"
                                  "'日薪宝转出成功',NOW(),NOW());")
    execute_list.append(insert_account_running_sql)
    # step 8,update account
    update_account_sql = ("UPDATE account set balance=@wallet_balance+@account_balance,"
                          "gmt_modified=NOW() where member_id={member_id};".format(member_id=member_id))
    execute_list.append(update_account_sql)
    # step 9,execute sql,if failed then rollback
    db_tool_m(execute_list)


# begin to steal rice
rat = 1
while rat > 0:
    query_exist_sql = "select member_id from wallet where balance>=0.01 limit 1;"
    exist_member_id = db_tool(query_exist_sql)[0]['member_id']
    transaction(exist_member_id)
    rat = signal()
print("Game Over!!")
