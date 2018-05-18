from django.db import models
import datetime
# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=40)
    registerStatus = models.IntegerField(default=0)
    sendEmailRandom = models.CharField(max_length=60, default="")
    successCreateTime = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "User"

class taskTable(models.Model):
    """
    subscribeStatus :订阅标志  0：不订阅
                        1：订阅
    status :0   任务未开始
            1   执行中
            2   完成
    """
    user = models.ForeignKey(User)

    url = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)
    keyword = models.CharField(max_length=50)

    taskCreateDate = models.DateTimeField()
    subscribeStatus = models.IntegerField(default=0)
    status=models.IntegerField(default=0)

    class Meta:
        db_table = "pushTask"

class spiderkeyTable(models.Model):
    taskId=models.IntegerField(default=0)

    url=models.CharField(max_length=100)
    keyWordNum=models.IntegerField()

    modifiedTime=models.CharField(max_length=50)
    startTime=models.DateTimeField()
    class Meta:
        db_table="spiderKey"


