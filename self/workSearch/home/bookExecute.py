#coding=utf-8
import pymysql
from tasks import spider_key

MYSQL_HOST="192.168.164.40"
MYSQL_USER="test"
MYSQL_PASSWD="redhat"
MYSQL_DBNAME="spider"

conn=pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD,database=MYSQL_DBNAME,charset="utf8")

cur=conn.cursor()
"""
spider_key.delay(starturl, domain, keyword, str(taskObj.id))
"""
sql="select url,domain,keyword,id from pushTask where subscribeStatus=1;"
try:
    cur.execute(sql)
    excuteResult=cur.fetchall()
    for eachResult in excuteResult:
        # print (eachResult[0],eachResult[1],eachResult[2],str(eachResult[3]))
        spider_key.delay(eachResult[0],eachResult[1],eachResult[2],str(eachResult[3]))
    # print (excuteResult,type(excuteResult))

except Exception as e:
    print(e)
    exit(1)

