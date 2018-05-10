#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhang'
__mtime__ = '4/9/2018'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import urllib.request
import pymysql as mysql, json, threading
from queue import Queue


# 数据库配置
config = {
    'host': '192.168.1.105',
    'port': 3306,
    'user': "root",
    'passwd': "!QAZ2wsx",
    'db': "qsdjf",
    'charset': "utf8"
}
# 查询上限次数配置
remain_times = 100


# 查询方法
def db_tool(sql):
    try:
        dbs = mysql.connect(**config)
        c = dbs.cursor(mysql.cursors.DictCursor)
        c.execute(sql)
        ones = [et for et in c.fetchall()]
        dbs.commit()
        dbs.close()
        return ones
    except:
        db_tool(sql)


# Insert及Update使用方法
def db_tool_m(sql_list):
    try:
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
    except:
        pass


# multithreading
class MyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while not self.queue.empty():
            member_id = self.queue.get()
            member_id_queue.task_done()
            update_ip_address(member_id)


# query ip address
def check_ip_address(ip):
    if not ip:
        return {
            'status': 0,
            'address': '查询失败'
        }
    else:
        url = 'https://api.map.baidu.com/location/ip?ip=' + ip + '&ak=rpRoDSGYvzK72meGKBFIhIXjGcdlIt14'
        try:
            req = urllib.request.Request(url)
            content = urllib.request.urlopen(req).read().decode('utf-8')
            # 不用.decode('utf-8'）会报错the JSON object must be str, not 'bytes'
            res = json.loads(content)
        except:
            res = {
                'status': 1
            }
        if not isinstance(res, dict) or res['status'] != 0:
            return {
                'status': 0,
                'address': '查询失败'
            }
        else:
            return {
                'status': 1,
                'address':
                    res['content']['address_detail']['province'] + ',' +
                    res['content']['address_detail']['city']
            }


# update two columns in table member
def update_ip_address(member_id):
    query_ip_address = "select last_login_ip,register_ip from member where id={id}".format(id=member_id)
    res = db_tool(query_ip_address)
    res = isinstance(res, list) and res[0] or ''
    register_ip = isinstance(res, dict) and res.get('register_ip') or ''
    last_login_ip = isinstance(res, dict) and res.get('last_login_ip') or ''
    if register_ip.find(',') > 1:
        register_ip = register_ip[:register_ip.find(',')]
    if last_login_ip.find(',') > 1:
        last_login_ip = last_login_ip[:last_login_ip.find(',')]
    register_ip_address = check_ip_address(register_ip)
    last_login_ip_address = check_ip_address(last_login_ip)
    update_address_sql = 'update member set gender=gender'
    if register_ip_address['status'] == 1:
        update_address_sql += ",registered_address='{registered_address} '".format(
            registered_address=register_ip_address['address']
        )
    if last_login_ip_address['status'] == 1:
        update_address_sql += ",login_address='{login_address}'".format(
            login_address=last_login_ip_address['address']
        )
    update_address_sql += " where id={id}".format(
        id=member_id
    )
    db_tool_m(update_address_sql)


# check how many iters remainning
def signal():
    sql = "select count(1) as ct from member where registered_address='' and login_address=''"
    result = db_tool(sql)[0]['ct']
    return result


# main flow
mark = 1
member_id_queue= Queue()
while remain_times > 0 and mark > 0:
    query_exist_sql = "select id from member where registered_address='' and login_address='' limit 10000"
    exist_member_id = [i['id'] for i in db_tool(query_exist_sql)]
    print('The range is {min} to {max},length {len}'.format(
        min=min(exist_member_id),
        max=max(exist_member_id),
        len=len(exist_member_id)
    ))
    for exist_member in exist_member_id:
        member_id_queue.put(exist_member)
        remain_times -= 2
    th1 = MyThread(member_id_queue)
    th2 = MyThread(member_id_queue)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    member_id_queue.join()
    mark = signal()
print('The task has been completed today.')
