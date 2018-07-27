#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Aquaman'
__author__ = 'Tinykay'
__mtime__ = '07/26/2018'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
# 平行债转，不产生出入金额
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
        account_id=account_id
        )
    res = db_tool(sql)[0]['balance']
    return res


# 查询用户在投金额
def query_account_investing(account_id):
    sql = "select investing_principal from account where id={account_id}".format(
        account_id=account_id
        )
    res= db_tool(sql)[0]['investing_principal']
    return res


# 查询用户account信息
def query_account_info(account_id):
    sql = "select * from account where id={account_id}".format(account_id=account_id)
    res = db_tool(sql)
    print(
        "余额:{balance},总提现{total_withdraw},总充值{total_recharge},"
        "在投总额{investing_principal},待收收益{investing_interest},"
        "已投资{invested},已收收益{interest}".format(
            balance=res[0]['balance'],
            total_recharge=res[0]['total_recharge'],
            total_withdraw=res[0]['total_withdraw'],
            investing_interest=res[0]['investing_interest'],
            investing_principal=res[0]['investing_principal'],
            invested=res[0]['invested'],
            interest=res[0]['interest']
            )
        )


# 查询有效在投订单
def query_valid_order(member_id):
    sql = (
        "SELECT order_no,pay_order_no,use_banlance,invest_amount,"
        "red_envelope_discount,debt_title,date_format(end_date,'%Y-%m-%d') as end_date"
        " FROM `order` "
        "WHERE member_id={member_id} and end_date>='2018-07-16' "
        "and `status`=1 "
        ).format(
            member_id=member_id
            )
    res = db_tool(sql)
    if res:
        return res
    else:
        print("不存在有效在投订单!!")
        exit(1)


# 查询是否为未结清订单
def query_uncleared_order(order_no):
    sql = (
        "SELECT count(1) as ct "
        "FROM `order_interest` "
        "WHERE `status`= 0 "
        "and `payable_principal`> 0 "
        "and `payable_principal`> IFNULL(`real_pay_principal`, 0) "
        "and `order_no`= '{order_no}'"
        ).format(
            order_no=order_no
            )
    res = db_tool(sql)
    return res[0]['ct']


# 备份表
def backup(member_id, table_name):
    try:
        current = time.strftime('%Y%m%d%S')
        # sql = "DROP TABLE IF EXISTS {db}.{member_id}_{table_name}_{current}".format(
        #     table_name=table_name, member_id=member_id, current=current, db=db)
        # db_tool_m(sql)
        sql1 = (
            "create table /*!32312 IF NOT EXISTS*/"
            " skyeye.{member_id}_{table_name}_{current} "
            "select * from `{table_name}` where member_id={member_id}"
            ).format(
                table_name=table_name,
                member_id=member_id,
                current=current
                )
        db_tool_m(sql1)
    except:
        print("备份{member_id}.{table_name}失败!".format(
            member_id=member_id, table_name=table_name))
        exit(1)


# 更新account表统计信息
def modify_census(member_id):
    sql = """UPDATE account SET investing_interest = ifnull((SELECT SUM(payable_interest) 
        FROM order_interest WHERE member_id ={member_id} AND `status` = 0 ),0), 
        investing_principal = ifnull(( SELECT SUM(payable_principal)-SUM(real_pay_principal) FROM order_interest 
        WHERE member_id ={member_id} AND `status` = 0 ),0), 
        invested = ifnull(( SELECT SUM(payable_principal) FROM order_interest 
        WHERE member_id ={member_id}),0), interest = ifnull((SELECT SUM(payable_interest) 
        FROM order_interest WHERE member_id ={member_id} ),0),
        total_recharge=ifnull((SELECT SUM(amount) 
        FROM pay_order WHERE type = 1 AND `status` = 2 AND member_id ={member_id} ),0), 
        total_withdraw = ifnull((SELECT SUM(amount) FROM pay_order WHERE type = 3 
        AND `status` = 2 
        AND member_id ={member_id}),0) WHERE member_id ={member_id};""".format(
            member_id=member_id
            )
    db_tool_m(sql)


# 数据检查
from_user = input("输入转移的用户名(username):").strip()
print(from_user)
to_user = input("输入接收的用户名(username):").strip() or '18758079426'
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
print("有效在投订单详情如下：\n")
for idx, element in enumerate(valid_order):
    print(
        idx,
        element['debt_title'],
        element['order_no'],
        element['invest_amount'],
        element['end_date']
        )
# 确认需要转让的订单
transfer_order = input("请输入需转让的订单(999表示全部)：")
remain_list = list(map(int,transfer_order.split()))
if remain_list[0] == 999:
    pass
else:
    valid_order = [valid_order[i] for i in remain_list]
print("需转移订单如下:\n")
for element in valid_order:
    print(
        element['debt_title'],
        element['order_no'],
        element['invest_amount'],
        element['end_date']
        )
check = input("确认输入yes: ").strip()
if check != 'yes':
    exit(1)
sum_interest_payed = 0
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
    # 检查是否还有未还本金
    check_remain_principal = query_uncleared_order(order_no)
    if check_remain_principal == 0:
        print("该订单已无未还本金,无法转移。")
        continue
    # 修改pay_order表
    if invest_amount > (use_balance + red_envelope_discount):
        print("存在充值订单{pay_order_no}".format(pay_order_no=pay_order_no))
        modify_pay_order_sql = (
            "update `pay_order` set to_account_id={to_account_id},"
            "member_id={to_member_id} where "
            "pay_order_no='{pay_order_no}'"
            ).format(
                to_account_id=to_account_id,
                to_member_id=to_member_id,
                pay_order_no=pay_order_no
                )
        execute_list.append(modify_pay_order_sql)
        print("已修改pay_order表{pay_order_no}为接收人充值订单！".format(
            pay_order_no=pay_order_no))
    else:
        print("不存在充值订单!!")
    # 修改red_envelope表
    if red_envelope_discount > 0:
        print("存在使用了红包{red_envelope_discount}元!".format(
            red_envelope_discount=red_envelope_discount))
        modify_red_envelope_sql = (
            "update red_envelope set member_id={to_member_id} "
            "where order_no={order_no}").format(
                to_member_id=to_member_id,
                order_no=order_no
                )
        execute_list.append(modify_red_envelope_sql)
        print("已修改红包为接收人使用红包!!")
    else:
        print("该订单未使用红包!")
    # 修改order表
    print("开始修改order表!!")
    modify_order_sql = (
        "update `order` set member_id={to_member_id},"
        "username='{to_user}' "
        "where order_no={order_no}"
        ).format(
            to_member_id=to_member_id,
            to_user=to_user,
            order_no=order_no
            )
    execute_list.append(modify_order_sql)
    print("已修改order表{order_no}为接收人投资订单".format(order_no=order_no))
    # 修改order_interest表
    modify_order_interest_sql = (
        "update order_interest "
        "set member_id={to_member_id} "
        "where order_no={order_no}").format(
            to_member_id=to_member_id,
            order_no=order_no
            )
    execute_list.append(modify_order_interest_sql)
    print("已修改order_interest表{order_no}".format(order_no=order_no))
    # 修改order_record表
    modify_order_record_sql = (
        "update order_record "
        "set member_id={to_member_id} "
        "where identification_no={order_no}"
        ).format(
            to_member_id=to_member_id,
            order_no=order_no
            )
    execute_list.append(modify_order_record_sql)
    print("已修改order_record表{order_no}".format(order_no=order_no))
    # 查询两个用户的当前余额
    current_from_account = query_account_investing(from_account_id)
    current_to_account = query_account_investing(to_account_id)
    print("当前{from_user}在投金额为:{money}".format(
        from_user=from_user,
        money=current_from_account)
        )
    print("当前{to_user}在投金额为:{money}".format(
        to_user=to_user,
        money=current_to_account)
        )
    # 修改account_running表
    # 修改转出用户account_running
    # 查询对应的account_running_id
    query_account_running_id_sql = (
        "select id from account_running "
        "where account_id={account_id} and "
        "pay_order_no='{pay_order_no}'"
        ).format(
            account_id=from_account_id,
            pay_order_no=pay_order_no
            )
    query_account_running_id = db_tool(query_account_running_id_sql)[0]['id']
    # 添加备注信息
    modify_account_running_sql = (
        "update account_running set"
        " `notice` = concat(`notice`, ',该订单已转给{to_member_id}')"
        " where id={running_id}"
        ).format(
            to_member_id=to_member_id,
            running_id=query_account_running_id
            )
    execute_list.append(modify_account_running_sql)
    # 查询是否有已收收益
    query_interest_sql = (
        "select ifnull(SUM(real_pay_interest),0) as payed_interest,"
        "ifnull(SUM(real_pay_principal),0) as payed_principal,"
        "count(if(real_pay_interest>0,true,null)) as ct "
        "FROM `order_interest` WHERE order_no={order_no}"
        ).format(
            order_no=order_no
            )
    interest = db_tool(query_interest_sql)
    if interest[0]['payed_interest'] or interest[0]['payed_principal']:
        print("存在已收收益!!")
        sum_interest_payed += interest[0]['payed_interest'] + interest[0]['payed_principal']
        modify_account_running_interest = (
            "update account_running set "
            "subject=21,"
            "`notice`=concat(`notice`,'(债转,已收收益)')"
            "where account_id={account_id} "
            "and `notice`='{notice}'"
            ).format(
                account_id=from_account_id,
                notice=debt_title
                )
        execute_list.append(modify_account_running_interest)
    else:
        print("无已收收益!!")
    # 判断是否有已收利息
    if interest[0]['payed_interest'] or interest[0]['payed_principal']:
        # 在订单中备注哪几期利息未给接收帐户
        update_order_sql = (
            "update `order` set "
            "`notice`=concat(`notice`,',{notice}') "
            "where order_no={order_no}"
            ).format(
                order_no=order_no,
                notice=(
                    str(interest[0]['ct']) + "期利息" +
                    str(interest[0]['payed_interest']) + "元" + 
                    str(interest[0]['payed_principal']) + "元本金" +
                    "给债权转出用户{from_member_id}".format(
                        from_member_id=from_member_id
                        )
                    )
        )
        execute_list.append(update_order_sql)
    # 统一执行sql，失败回滚
    print(execute_list)
    db_tool_m(execute_list)
    print("订单{order_no}转移结束!".format(order_no=order_no))
    print("--------------------------------------\n")
# 更新account表统计信息
modify_census(from_member_id)
modify_census(to_member_id)
print("更新account表统计信息成功!")
print(
    "已成功转移用户{from_user}的有效在投订单至{to_user}用户名下!".format(
        from_user=from_user,
        to_user=to_user
        )
    )
print("该批订单组已收收益为:{payed_interest}".format(payed_interest=sum_interest_payed))
print("#########################################\n")
print("现在{from_user}用户的帐户信息为:".format(from_user=from_user))
query_account_info(from_account_id)
print("现在{to_user}用户的帐户信息为:".format(to_user=to_user))
query_account_info(to_account_id)
