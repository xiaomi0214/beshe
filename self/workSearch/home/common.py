#coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import string
import hashlib
import datetime
from .models import taskTable
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import string
import hashlib
import datetime
from django.utils.safestring import mark_safe

pageNum=12


allowDomains=["sust.edu.cn","dingbian.gov.cn"]
def pushworkLimit(starturl,domain,keyword):
    """


    :param starturl:
    :param domain:
    :param keyword:
    :return:
            status 1 :已发布相同的任务，请在历史记录搜索
                    0:允许发布
                    2：发布条件不满足   条件：startUrl and domain
                                           允许的域名
    """
    if domain in starturl:
        if domain in allowDomains:
            useTask=taskTable.objects.filter(url=starturl,domain=domain,keyword=keyword)
            if useTask:
                status = 1
                msg = "已发布相同的任务，请在历史记录搜索"
            else:
                status = 0
                msg = ""
        else:
            status=2
            msg="你所输入的域名不被允许，请联系管理员"
    else:
        msg="入口url不在这个网站下，请重新输入"
        status=2

    return status,msg






def getInter(price):
    try:
        price=int(price)
    except Exception as e:
        price=100

    return price

def sendEmail(email,emailContent):
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "mixiongxiong0214@163.com"  # 用户名
    mail_pass = "mixiongxiong0214"  # 口令

    sender = mail_user
    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(emailContent, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receivers[0]
    print(message['From'],message['To'])
    subject = '网站小搜搜'
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
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")





class Pager(object):
    def __init__(self, cur_page, data_all, page_each_num=2):
        """

        :param cur_page:  当前页数
        :param data_all:  取得所有数据的数目
        :param page_each_num: 每页显示数据的个数
        self.start  每页5 现在显示第5页  显示的数据为：start-end
        pageNum:总数据数目，每页显示的数目---得到要显示的总页数
        """
        self.CurPage = cur_page
        self.DataAll = data_all
        self.PageEachNum = page_each_num

    @property
    def start(self):
        return (self.CurPage - 1) * self.PageEachNum

    @property
    def end(self):
        return self.CurPage * self.PageEachNum

    @property
    def pageNum(self):
        page_num = divmod(self.DataAll, self.PageEachNum)
        if page_num[1] == 0:
            page_num = page_num[0]
        else:
            page_num = page_num[0] + 1
        return page_num


def get_page(page, page_num):
    """


    :param page:  代表当前页码
    :param page_num: 总页码
    :return:
    """
    page_str = []

    ##首页
    first_html = '<a href="/home/showResult/%s">首页</a>' % (1)
    page_str.append(first_html)

    ##上一页
    if page == 1:
        front_page_html = '<a href="#">上一页</a>'
    else:
        front_page_html = '<a href="/home/showResult/%s">上一页</a>' % (page - 1)
    page_str.append(front_page_html)

    start = page - 3
    if start < 2:
        start = 1
    end = page + 3
    if end > page_num:
        end = page_num - 1

    if page_num < 5:
        start = 0
        end = page_num
    else:
        if (page < 3):
            start = 0
            end = 5
        else:
            if (page + 2 > page_num):
                start = page_num - 5
                end = page_num
            else:
                start = page - 3
                end = page + 2
    for i in range(start, end):
        if page == i + 1:
            page_each_str = '<a class="selected"  href="/home/showResult/%s">%d</a>' % (i + 1, i + 1)
        else:
            page_each_str = '<a href="/home/showResult/%s">%d</a>' % (i + 1, i + 1)
        page_str.append(page_each_str)

    ##下一页
    if page == page_num:
        next_page_html = '<a href="#">下一页</a>'
    else:
        next_page_html = '<a href="/home/showResult/%s">下一页</a>' % (page + 1)
    page_str.append(next_page_html)

    ##尾页
    last_page_html = '<a href="/home/showResult/%s">尾页</a>' % (page_num)
    page_str.append(last_page_html)

    page_str = ' '.join(page_str)
    page_html = mark_safe(page_str)
    return page_html



def int_c(arg,default):
    """
    url输入的页数是字符型的数字，int转化为整形
                 其他         则arg=默认的整数
    """
    try:
        arg=int(arg)
    except Exception:
        arg=default
    return arg

if __name__=="__main__":
    print (getRandom())
