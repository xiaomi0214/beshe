from django.test import TestCase

# Create your tests here.
import requests
import json
import random
import hashlib
import string
import datetime
from .models import taskTable
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import string
import hashlib
import datetime


"""
uid = models.CharField(max_length=50)

    url = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)
    keyword = models.CharField(max_length=50)
"""
allowDomains=["sust.edu.cn",]
def pushworkLimit(starturl,domain,keyword):
    if domain in starturl:
        if domain in allowDomains:
            useTask=taskTable.objects.filter(url=starturl,domain=domain,keyword=keyword)
            if useTask:
                status = False
                msg = "已发布相同的任务，请在历史记录搜索"
            else:
                status = True
                msg = "你的任务已成功发布"
        else:
            status=False
            msg="你所输入的域名不被允许，请联系管理员"
    else:
        msg="入口url不在这个网站下，请重新输入"
        status=False

    return status,msg



def getInter(price):
    try:
        price=int(price)
    except Exception as e:
        price=100

    return price

def sendEmail(email,emailContent):
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "13772098509@163.com"  # 用户名
    mail_pass = "peng123456"  # 口令

    sender = mail_user
    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(emailContent, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receivers[0]
    print(message['From'],message['To'])
    subject = '彭芽丽民宿网站'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host,465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers[0], message.as_string())
        return True
    except Exception as e:
        return False

def getRandom(num=20):
    sting1=string.digits+string.ascii_letters
    print(sting1)
    result=""
    for i in range(num):
        result=result+random.choice(sting1)
    return result


def getPasswdHash(passwd):
    hashobj=hashlib.md5()
    hashobj.update(passwd)
    return hashobj.hexdigest()

def getNow():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")




