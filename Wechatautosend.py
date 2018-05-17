# -*- coding: utf-8 -*-
import itchat
import requests
import datetime
import re
import random
import time
from threading import Timer


word_compile = re.compile(r'', re.S)
add_friend_compile = re.compile(r'')


def get_news():
    url = "http://open.iciba.com/dsapi"
    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation


def send_news():
    try:
        my_friend = itchat.search_friends(name=u'Tinykay')[0]["UserName"]
        content = get_news()
        message1 = str(content[0])
        message2 = str(content[1][5:])
        message3 = "啊哈"
        itchat.send(message1, toUserName=my_friend)
        itchat.send(message2, toUserName=my_friend)
        itchat.send(message3, toUserName=my_friend)
        Timer(86400, send_news).start()
    except:
        message4 = u"sfgsdf"
        target = itchat.search_friends(name=u'Tinykay')[0]["UserName"]
        itchat.send(message4, toUserName=target)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def reply(msg):
    group_list = []
    group_name = []
    for group in group_list:
        chat = itchat.search_chatrooms(name=group)
        if len(chat) > 0:
            group_name.append(chat[0]['UserName'])
    result = word_compile.search(msg['Content'])
    if result is not None:
        if result.group() is not None:
            for group in group_name:
                itchat.send('%s' % (msg['Content']), toUserName=group)


@itchat.msg_register(itchat.content.FRIENDS)
def deal_with_friend(msg):
    if add_friend_compile.search(msg['Content']) is not None:
        itchat.add_friend(**msg['Text'])
        time.sleep(random.randint(1, 3))
        itchat.send_msg('', msg['RecommendInfo']['UserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_msg('', msg['RecommendInfo']['UserName'])


@itchat.msg_register(itchat.content.TEXT)
def deal_with_message(msg):
    text = msg['Content']
    if text == u'':
        time.sleep(random.randint(1, 3))
        itchat.add_member_into_chatroom(get_group_id(""), [{'UserName': msg['FromUserName']}], useInvitation=True)
    elif text == u'':
        time.sleep(random.randint(1, 3))
        return u''
    elif text == u'':
        time.sleep(random.randint(1, 3))
        itchat.send_image('', msg['FromUserName'])
    elif text == u'':
        time.sleep(random.randint(1, 3))
        itchat.send_msg('', msg['FromUserName'])
    else:
        time.sleep(random.randint(1, 3))


def get_group_id(group_name):
    group_list = itchat.search_chatrooms(name=group_name)
    return group_list[0]['UserName']


if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    itchat.run()
    send_news()



# #不要抄下源码就运行，你需要改动几个地方

# from __future__ import unicode_literals
# from threading import Timer
# from wxpy import *
# import requests


# #bot = Bot()
# bot = Bot(console_qr=2,cache_path="botoo.pkl")   　　　　#这里的二维码是用像素的形式打印出来！，如果你在win环境上运行，替换为  bot=Bot()


# def get_news1():
# 　　#获取金山词霸每日一句，英文和翻译
#     url = "http://open.iciba.com/dsapi/"
#     r = requests.get(url)
#     contents = r.json()['content']
#     translation= r.json()['translation']
#     return contents,translation

# def send_news():
#     try:
#         my_friend = bot.friends().search(u'徒手敬岁月')[0]    #你朋友的微信名称，不是备注，也不是微信帐号。
#         my_friend.send(get_news1()[0])
#         my_friend.send(get_news1()[1][5:])
#         my_friend.send(u"来自爸爸的心灵鸡汤！")
#         t = Timer(86400, send_news)　　 　　　　　　　　　　　　#每86400秒（1天），发送1次，不用linux的定时任务是因为每次登陆都需要扫描二维码登陆，很麻烦的一件事，就让他一直挂着吧
#         t.start()
#     except:
#         my_friend = bot.friends().search('常念')[0]       　　#你的微信名称，不是微信帐号。
#         my_friend.send(u"今天消息发送失败了")
        

    
# if __name__ == "__main__":
#     send_news()
