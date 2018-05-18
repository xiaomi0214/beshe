from django.test import TestCase
import datetime
# Create your tests here.
t1=b'Mon, 14 May 2018 08:56:06 GMT'
# modifiedDate = datetime.datetime.strptime(t1.decode(), "%a, %d %b %Y %H:%M:%S %Z")
# modifiedDateStr = datetime.datetime.strftime(modifiedDate, "%Y-%m-%d %H:%M:%S")
# print (modifiedDateStr)

import requests
import re
import chardet
url="http://www.dingbian.gov.cn/"

response=requests.get(url=url)
print (response.encoding)
response.encoding=chardet.detect(response.content)['encoding']
print (response.encoding)
# print (response.text)
print (response.history)
result=re.findall(r'全市第一季度行业扶贫点评暨问题整改工作推进会召开',response.text)
print (result)
pass


