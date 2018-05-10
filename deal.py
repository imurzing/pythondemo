#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'deal'
__author__ = 'Tinykay'
__mtime__ = '9/05/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
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
        exit(1)
    db_cnt.close()


# 查询用户member_id
def query_member_id(username):
    sql = "select id from member where username={username}".format(username=username)
    member_id = db_tool(sql)
    if member_id:
        return member_id[0]['id']
    else:
        print("用户不存在!!")
        exit(1)


# 查询用户account_id
def query_account_id(member_id):
    sql = "select id from account where member_id={member_id}".format(member_id=member_id)
    account_id = db_tool(sql)
    if account_id:
        return account_id[0]['id']
    else:
        print("帐户不存在!!")
        exit(1)


# 查询用户余额
def query_account_balance(account_id):
    sql = "select balance from account where id={account_id}".format(
        account_id=account_id)
    res = db_tool(sql)[0]['balance']
    return res


# 查询用户account信息
def query_account_info(account_id):
    sql = "select * from account where id={account_id}".format(account_id=account_id)
    res = db_tool(sql)
    print("余额:{balance},总提现{total_withdraw},总充值{total_recharge},"
          "在投总额{investing_principal},待收收益{investing_interest},"
          "已投资{invested},已收收益{interest}".format(
                                        balance=res[0]['balance'],
                                        total_recharge=res[0]['total_recharge'],
                                        total_withdraw=res[0]['total_withdraw'],
                                        investing_interest=res[0]['investing_interest'],
                                        investing_principal=res[0]['investing_principal'],
                                        invested=res[0]['invested'],
                                        interest=res[0]['interest']))


# 查询有效在投订单
def query_valid_order(member_id):
    sql = ("SELECT order_no,pay_order_no,use_banlance,invest_amount,"
           "red_envelope_discount,debt_title"
           " FROM `order` "
           "WHERE member_id={member_id} and end_date>CURRENT_DATE "
           "and `status`=1 ").format(member_id=member_id)
    res = db_tool(sql)
    if res:
        return res
    else:
        print("不存在有效在投订单!!")
        exit(1)


# 备份表
def backup(member_id, table_name):
    try:
        current = time.strftime('%Y%m%d%S')
        # sql = "DROP TABLE IF EXISTS {db}.{member_id}_{table_name}_{current}".format(
        #     table_name=table_name, member_id=member_id, current=current, db=db)
        # db_tool_m(sql)
        sql1 = ("create table /*!32312 IF NOT EXISTS*/"
                " skyeye.{member_id}_{table_name}_{current} "
                "select * from `{table_name}` where member_id={member_id}").format(
            table_name=table_name, member_id=member_id, current=current)
        db_tool_m(sql1)
    except:
        print("备份{member_id}.{table_name}失败!".format(
            member_id=member_id, table_name=table_name))
        exit(1)


# 更新account表统计信息
def modify_census(member_id):
    sql = """UPDATE account SET investing_interest = ifnull((SELECT SUM(payable_interest) 
    FROM order_interest WHERE member_id ={member_id} AND `status` = 0 ),0), 
    investing_principal = ifnull(( SELECT SUM(payable_principal) FROM order_interest 
    WHERE member_id ={member_id} AND `status` = 0 ),0), 
    invested = ifnull(( SELECT SUM(payable_principal) FROM order_interest 
    WHERE member_id ={member_id}),0), interest = ifnull((SELECT SUM(payable_interest) 
    FROM order_interest WHERE member_id ={member_id} ),0),
    total_recharge=ifnull((SELECT SUM(amount) 
    FROM pay_order WHERE type = 1 AND `status` = 2 AND member_id ={member_id} ),0), 
    total_withdraw = ifnull((SELECT SUM(amount) FROM pay_order WHERE type = 3 
    AND `status` = 2 
    AND member_id ={member_id}),0) WHERE member_id ={member_id};""".format(
        member_id=member_id)
    db_tool_m(sql)


# 数据检查
from_user = input("输入转移的用户名(username):")
print(from_user)
to_user = input("输入接收的用户名(username):")
print(to_user)
from_member_id = query_member_id(from_user)
from_account_id = query_account_id(from_member_id)
print("转移用户member_id为:{from_member_id}".format(
    from_member_id=from_member_id))
to_member_id = query_member_id(to_user)
to_account_id = query_account_id(to_member_id)
print("接收用户member_id为:{to_member_id}".format(
    to_member_id=to_member_id))
# 查询有效在投订单
valid_order = query_valid_order(from_member_id)
# 查询接收用户的帐户余额是否充足
query_balance_sql = "select balance from account where member_id={member_id}".format(
    member_id=to_member_id)
query_balance = db_tool(query_balance_sql)[0]['balance']
sum_interest_payed = 0
sum_valid_order = sum([i['invest_amount'] for i in valid_order])
if query_balance < sum_valid_order:
    print("接收方用户余额不足!!")
    exit(1)
else:
    print("需转移总额为:{sum_valid_order}".format(
        sum_valid_order=sum_valid_order))
print("当前{from_user}用户的帐户信息为:".format(from_user=from_user))
query_account_info(from_account_id)
print("当前{to_user}用户的帐户信息为:".format(to_user=to_user))
query_account_info(to_account_id)
print("------------------------------------\n\n\n")
# 备份各个表信息
backup(from_member_id, "order")
backup(from_member_id, "order_interest")
backup(from_member_id, "pay_order")
backup(from_member_id, "red_envelope")
backup(from_member_id, "order_record")
backup(from_member_id, "account")
backup(to_member_id, "account")
# 转移流程开始
for element in valid_order:
    execute_list = list()
    order_no = element['order_no']
    pay_order_no = element['pay_order_no']
    use_balance = element['use_banlance']
    red_envelope_discount = element['red_envelope_discount']
    invest_amount = element['invest_amount']
    debt_title = element['debt_title']
    print("开始转移订单{order_no}".format(order_no=order_no))
    # 修改pay_order表
    if invest_amount > (use_balance + red_envelope_discount):
        print("存在充值订单{pay_order_no}".format(pay_order_no=pay_order_no))
        modify_pay_order_sql = ("update `pay_order` set type=1 where  "
                                "pay_order_no='{pay_order_no}'").format(
            pay_order_no=pay_order_no)
        execute_list.append(modify_pay_order_sql)
        print("已修改pay_order表{pay_order_no}为充值订单！".format(
            pay_order_no=pay_order_no))
    else:
        print("不存在充值订单!!")
    # 修改red_envelope表
    if red_envelope_discount > 0:
        print("存在使用了红包{red_envelope_discount}元!".format(
            red_envelope_discount=red_envelope_discount))
        modify_red_envelope_sql = ("update red_envelope set use_date=null,`status`=3,"
                                   "order_no=0,debt_title=null "
                                   "where order_no={order_no}").format(
            order_no=order_no)
        execute_list.append(modify_red_envelope_sql)
        print("已修改红包为过期红包!!")
    else:
        print("该订单未使用红包!")
    # 修改order表
    print("开始修改order表!!")
    modify_order_sql = ("update `order` set member_id={to_member_id},"
                        "use_banlance=invest_amount,red_envelope_discount=0,"
                        "username={to_user},pay_amount=invest_amount "
                        "where order_no={order_no}").format(
        to_member_id=to_member_id, to_user=to_user, order_no=order_no)
    execute_list.append(modify_order_sql)
    print("已修改order表{order_no}".format(order_no=order_no))
    # 修改order_interest表
    modify_order_interest_sql = ("update order_interest "
                                 "set member_id={to_member_id} "
                                 "where order_no={order_no}").format(
        to_member_id=to_member_id, order_no=order_no)
    execute_list.append(modify_order_interest_sql)
    print("已修改order_interest表{order_no}".format(order_no=order_no))
    # 修改order_record表
    modify_order_record_sql = ("update order_record "
                               "set member_id={to_member_id} "
                               "where identification_no={order_no}").format(
        to_member_id=to_member_id, order_no=order_no)
    execute_list.append(modify_order_record_sql)
    print("已修改order_record表{order_no}".format(order_no=order_no))
    # 查询两个用户的当前余额
    current_from_account = query_account_balance(from_account_id)
    current_to_account = query_account_balance(to_account_id)
    print("当前{from_user}余额为:{money}".format(
        from_user=from_user, money=current_from_account))
    print("当前{to_user}余额为:{money}".format(
        to_user=to_user, money=current_to_account))
    new_to_balance = current_to_account - invest_amount
    new_from_balance = current_from_account + invest_amount
    # 修改account_running表
    # 修改转出用户account_running
    # 查询对应的account_running_id
    query_account_running_id_sql = ("select id from account_running "
                                    "where account_id={account_id} and "
                                    "pay_order_no='{pay_order_no}'").format(
        account_id=from_account_id, pay_order_no=pay_order_no)
    query_account_running_id = db_tool(query_account_running_id_sql)[0]['id']
    # 判断是否有充值
    if invest_amount > (use_balance + red_envelope_discount):
        print("该笔订单有充值，改投资流水为充值流水!")
        modify_account_running_sql = ("update account_running set "
                                      "subject=1,income={income},"
                                      "balance=balance+{balance},"
                                      "outlay=null,notice='支付成功'  where account_id={account_id} "
                                      "and pay_order_no='{pay_order_no}' "
                                      "and id={running_id}").format(
            income=invest_amount-red_envelope_discount-use_balance,
            balance=invest_amount-red_envelope_discount,
            account_id=from_account_id,
            pay_order_no=pay_order_no,
            running_id=query_account_running_id)
        execute_list.append(modify_account_running_sql)
        # 给后续流水的balance全加上充值金额
        update_account_running_sql = ("update account_running set "
                                      "balance=balance+{balance} where "
                                      "account_id={account_id}"
                                      " and id>{running_id}").format(
            balance=invest_amount-red_envelope_discount,
            account_id=from_account_id,
            running_id=query_account_running_id)
        execute_list.append(update_account_running_sql)
    else:
        print("该笔订单未使用银行卡支付,删除投资流水!!")
        modify_account_running_sql = ("delete from  account_running  "
                                      " where account_id={account_id} "
                                      "and pay_order_no='{pay_order_no}' "
                                      "and id={running_id}").format(
           account_id=from_account_id,
           pay_order_no=pay_order_no,
           running_id=query_account_running_id)
        execute_list.append(modify_account_running_sql)
        # 给后续流水的balance全加上充值金额
        update_account_running_sql = ("update account_running set "
                                      "balance=balance+{balance} where "
                                      "account_id={account_id}"
                                      " and id>{running_id}").format(
            balance=invest_amount - red_envelope_discount,
            account_id=from_account_id,
            running_id=query_account_running_id)
        execute_list.append(update_account_running_sql)
    # 如果有红包，加一笔红包收益
    if red_envelope_discount > 0:
        insert_from_account_running = ("insert into account_running "
                                       "(account_id,pay_order_no,"
                                       "subject,balance,income,outlay,"
                                       "`notice`,gmt_created,"
                                       "gmt_modified) values ({account_id},"
                                       "'',"
                                       "21,{balance},{income},"
                                       "null,'订单{order_no}红包(债转)',"
                                       "now(),now());").format(
                account_id=from_account_id,
                balance=new_from_balance,
                income=red_envelope_discount,
                order_no=order_no)
        execute_list.append(insert_from_account_running)
    # 查询是否有已收收益
    query_interest_sql = ("select SUM(real_pay_interest) as payed,"
                          "count(if(real_pay_interest>1,true,null)) as ct "
                          "FROM `order_interest` WHERE order_no={order_no}").format(
        order_no=order_no)
    interest = db_tool(query_interest_sql)
    if interest[0]['payed']:
        print("存在已收收益!!")
        sum_interest_payed += interest[0]['payed']
        modify_account_running_interest = ("update account_running set "
                                           "subject=21,"
                                           "`notice`=concat(`notice`,'(债转,已收收益)')"
                                           "where account_id={account_id} "
                                           "and `notice`='{notice}'").format(
            account_id=from_account_id, notice=debt_title)
        execute_list.append(modify_account_running_interest)
    else:
        print("无已收收益!!")
    # 新增接收用户account_running
    insert_in_account_running = ("insert into account_running (account_id,pay_order_no,"
                                 "subject,balance,income,outlay,`notice`,gmt_created,"
                                 "gmt_modified) values ({to_account_id},'{pay_order_no}',"
                                 "3,{new_to_balance},null,{invest_amount},"
                                 "'投资成功(债转)',now(),now());").format(
        to_account_id=to_account_id, pay_order_no=pay_order_no,
        invest_amount=invest_amount, new_to_balance=new_to_balance)
    execute_list.append(insert_in_account_running)
    # 判断是否有已收利息
    if interest[0]['payed']:
        # new_to_balance += interest[0]['payed']
        # insert_in_account_running_sql = ("insert into account_running (account_id,"
        #                                  "subject,balance,income,outlay,notice,"
        #                                  "gmt_created,"
        #                                  "gmt_modified) values ({to_account_id},"
        #                                  "14,{new_to_balance},{income},null,"
        #                                  "'{debt_title}债转收益',now(),now());").format(
        #     to_account_id=to_account_id,
        #     new_to_balance=new_to_balance,
        #     income=interest[0]['payed'],
        #     debt_title=debt_title)
        # execute_list.append(insert_in_account_running_sql)
        # 在订单中备注哪几期利息未给接收帐户
        update_order_sql = ("update `order` set "
                            "`notice`=concat(`notice`,',{notice}') "
                            "where order_no={order_no}").format(
            order_no=order_no,
            notice=(str(interest[0]['ct']) + "期利息" +
                    str(interest[0]['payed']) + "元给债权转出用户")
        )
        execute_list.append(update_order_sql)
    # 修改account表
    update_to_account_sql = ("update account set "
                             "balance={new_to_balance} "
                             "where id={to_account_id}").format(
        new_to_balance=new_to_balance, to_account_id=to_account_id)
    execute_list.append(update_to_account_sql)
    update_from_account_sql = ("update account set "
                               "balance={new_from_balance} where "
                               "id={from_account_id}").format(
        new_from_balance=new_from_balance, from_account_id=from_account_id)
    execute_list.append(update_from_account_sql)
    # 统一执行sql，失败回滚
    db_tool_m(execute_list)
    print("{from_user}当前余额为:{new_from_balance}".format(
        from_user=from_user, new_from_balance=new_from_balance))
    print("{to_user}当前余额为:{new_to_balance}".format(
        to_user=to_user, new_to_balance=new_to_balance))
    print("订单{order_no}转移结束!".format(order_no=order_no))
    print("--------------------------------------\n")
# 更新account表统计信息
modify_census(from_member_id)
modify_census(to_member_id)
print("更新account表统计信息成功!")
print("已成功转移用户{from_user}的有效在投订单至{to_user}用户名下!".format(
    from_user=from_user, to_user=to_user))
print("该批订单组已收收益为:{payed_interest}".format(payed_interest=sum_interest_payed))
print("#########################################\n")
print("现在{from_user}用户的帐户信息为:".format(from_user=from_user))
query_account_info(from_account_id)
print("现在{to_user}用户的帐户信息为:".format(to_user=to_user))
query_account_info(to_account_id)
