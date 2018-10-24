import pymysql as mysql
import zipfile
import codecs
import sys
import subprocess
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from apscheduler.schedulers.blocking import BlockingScheduler
import config


#database configuration
config = {
    'host': '192.168.1.105',
    'port': 3306,
    'user': "root",
    'passwd': "!QAZ2wsx",
    'db': "skyeye",
    'charset': "utf8"
}


# email configuration
send_from = ''
smtp_server = "smtp.126.com"
smtp_server_port = 25
email_passsword = ''
send_to_mail_list = ['kai.zhang@qsdjr.com', 'xiaoqiang.huang@qsdjr.com', 'junfang.zuo@qsdjr.com', ]


attachment_title = '"设备","渠道","首投并复投金额"\n'
attachment_detail = '"'+element['设备']+'","'+element['渠道']+'","' + str(element['首投并复投金额'])+'"\n'


# Select使用方法
def db_tool(sql):
    dbs = mysql.connect(**config)
    c = dbs.cursor(mysql.cursors.DictCursor)
    c.execute(sql)
    ones = [i for i in c.fetchall()]
    dbs.commit()
    dbs.close()
    return ones


# Insert及Update使用方法
def db_tool_m(sql):
    db_cnt = mysql.connect(**config)
    cursor = db_cnt.cursor(mysql.cursors.DictCursor)
    effect_rows = cursor.execute(sql)
    db_cnt.commit()
    db_cnt.close()
    return effect_rows


# 用于邮件发送
def mail(mail_to_list, title, *args):
    # set variables
    my_sender = send_from
    my_mail_to_list = mail_to_list
    my_title = title
    my_content = args[0]
    try:
        msg = MIMEMultipart()
        if len(args) > 1:
            attachment = MIMEApplication(open('transfer/'+args[1], 'rb').read())
            attachment["Content-Type"] = 'application/octet-stream'
            attachment["Content-Disposition"] = 'attachment; filename="'+args[1]+'"'
            msg.attach(attachment)
        pure_text = MIMEText(my_content, 'plain', 'utf-8')
        msg.attach(pure_text)
        msg['From'] = formataddr(["Agent", my_sender])
        msg['To'] = ";".join(my_mail_to_list)
        msg['Subject'] = my_title
        server = smtplib.SMTP(smtp_server, smtp_server_port)
        server.login(my_sender, email_passsword)
        server.sendmail(my_sender, my_mail_to_list, msg.as_string())
        server.quit()
    except Exception:
        raise Exception




# 自动提取数据发邮件
def lily_liu():
    current_date = time.strftime('%Y%m%d')
    ant = ''
    attachment = codecs.open('transfer/attach.csv', 'w', 'utf_8_sig')
    attachment.write(attachment_title)
    res = db_tool(ant)
    for element in res:
        attachment.write(attachment_detail)
    attachment.close()
    if sys.platform[:5] == 'linux':
        subprocess.call(['zip', '-rjP', 'Yummy666', 'transfer/attach.zip', 'transfer/attach.csv'])
    else:
        zip_file = zipfile.ZipFile('transfer/attach.zip', 'w', zipfile.ZIP_DEFLATED)
        zip_file.write('transfer/attach.csv', 'attach.csv')
        zip_file.close()
    content = '上周首投并复投金额'
    title = '[DATA]上周首投并复投金额'
    file = 'attach.zip'
    mail(config.business_mail_list, title, content, file)
    os.remove('transfer/attach.csv')
    os.remove('transfer/attach.zip')


if __name__ == "__main__":
    # 创建计划任务
    scheduler = BlockingScheduler()
    # 数据需求定时任务
    scheduler.add_job(lily_liu, 'cron', hour='7')
    scheduler.start()
