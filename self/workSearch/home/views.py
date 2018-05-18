from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import User,taskTable,spiderkeyTable
from .common import getRandom,sendEmail,getPasswdHash,getNow,int_c,pushworkLimit,pageNum
from .tasks import spider_key
import json
import datetime


def login(request):
    msg = ""
    user = ""
    if request.method == "POST":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        print(email, passwd)

        if email and passwd:
            peopleObj = User.objects.filter(email=email)
            if peopleObj:
                peopleObj = peopleObj[0]
                if peopleObj.password == getPasswdHash(passwd.encode('utf-8')):
                    request.session['logind'] = {"email": email}
                    return redirect('/home/index/')
                else:
                    msg = "密码不正确"
            else:
                msg = "账户不存在"
        else:
            msg = "email 或 密码不能为空"

        return render(request, "login.html", {'msg': msg})

    else:
        return render(request, "login.html", {'msg': msg})




def register(request):
    msg = ""
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            UserObj = User.objects.filter(email=email)
            if UserObj:
                UserObj = UserObj[0]
                if UserObj.registerStatus == 1:
                    msg = "账号已经注册成功，请直接登陆"
                else:
                    randString = getRandom()
                    UserObj.sendEmailRandom = randString
                    UserObj.save()

                    mailText = """
                          <p>站点小搜搜欢迎你</p>
                          <p><a href="http://192.168.164.40:9000/home/setPassword/?mail=%s&randString=%s">请点击这个链接完成账户任务！</a></p>
                          """ % (email, randString)

                    sendEmailResult = sendEmail(email, mailText)
                    if sendEmailResult:
                        msg = "email发送成功，请登陆到邮箱，完成后续的操作"
                    else:
                        msg = "email发送失败，请核实您的邮箱或设置邮箱的代理开启"
            else:
                randString = getRandom()
                user_obj = User(
                    email=email,
                    sendEmailRandom=randString,
                )
                user_obj.save()
                mailText = """ 
                          <p>站点小搜搜欢迎你</p>
                          <p><a href="http://192.168.164.40:9000/home/setPassword/?mail=%s&randString=%s">请点击这个链接完成账户注册任务！</a></p>
                          """ % (email, randString)

                sendEmailResult = sendEmail(email, mailText)

                if sendEmailResult:
                    msg = "email发送成功，请登陆到邮箱，完成后续的操作"
                else:
                    msg = "email发送失败，请核实您的邮箱或设置邮箱的代理开启"
                ##发送邮件

        else:
            msg = "email不能为空"

        return render(request, "register.html", {"msg": msg})
    else:
        return render(request, "register.html",{"msg":msg})

def setPassword(request):
    msg = ""
    if request.method == "POST":
        email = request.POST.get('mail', None)
        passwd1 = request.POST.get('passwd1', None)
        passwd2 = request.POST.get('passwd2', None)
        print(passwd1, passwd2, email)
        if email and passwd1 and passwd1 == passwd2:
            passwdMd5 = getPasswdHash(passwd1.encode('utf-8'))

            peopleObj = User.objects.get(email=email)
            peopleObj.password = passwdMd5
            peopleObj.registerStatus = 1
            peopleObj.successCreateTime = getNow()
            peopleObj.save()

            return redirect('/home/login/')

        else:
            msg = "2次密码不匹配/2次密码不能为空"

            return render(request, "searchPassword.html", {"mail": email, "msg": msg})

    else:
        email = request.GET.get('mail', None)
        randString = request.GET.get('randString', None)
        if email and randString:
            sendEmailRandom = User.objects.filter(email=email).values('sendEmailRandom')
            print(sendEmailRandom)
            if sendEmailRandom:
                sendEmailRandom = sendEmailRandom[0].get('sendEmailRandom')
                print(email, randString, sendEmailRandom)
                if sendEmailRandom and randString == sendEmailRandom:
                    return render(request, "setPassword.html", {"mail": email})
                else:
                    return HttpResponse("你的地址有误...")
            else:
                return HttpResponse("你的地址有误,请到官方网站完成注册")
        else:
            return HttpResponse("你的地址有误,请到官方网站完成注册")


def index(request):
    msg=""
    logind=request.session.get('logind',None)
    if logind!=None:
        msg=True
    else:
        msg=False
    pushworks=taskTable.objects.all()

    return render(request,'index.html',{"pushworks":pushworks,"msg":msg})





def checklogin(func):

    def gaveFunc(request,*args, **kwargs):
        loginStatus=request.session.get('logind',None)
        if loginStatus!=None:
            return func(request,*args, **kwargs)
        else:
            return redirect('/home/login/')
    return gaveFunc



@checklogin
def workPush(request,*args, **kwargs):
    email=request.session.get('logind')['email']
    userObj=User.objects.get(email=email)
    if request.method=="POST":
        starturl = request.POST.get("startUrl")
        domain = request.POST.get("domain")
        keyword = request.POST.get('keyword')


        status = True
        msg = ""

        limitResult, msg = pushworkLimit(starturl, domain, keyword)
        print (limitResult, msg)
        if limitResult==0:
            taskObj = taskTable(
                user=userObj,
                url = starturl,
                domain = domain,
                keyword = keyword,

                taskCreateDate =getNow(),

            )
            taskObj.save()
            spider_key.delay(starturl, domain, keyword, str(taskObj.id))
            msg="任务发布成功"
            return render(request,'workPush.html',{"msg":msg})
        elif limitResult==1:
            return redirect('/home/index/')
        else:
            return render(request,'workPush.html',{"msg":msg})
    else:
        return render(request,'workPush.html')


def showResult(request,*args, **kwargs):
    pager_num = request.COOKIES.get('pager_num', 10)
    getNum = int_c(pager_num, 10)

    sortTyle=request.COOKIES.get('sortTyle', 'keyWordNum')
    sortTyle="-"+sortTyle


    taskid=request.GET.get('taskid')
    taskObj=taskTable.objects.get(id=taskid)

    keyWord = taskObj.keyword
    domain = taskObj.domain

    spiderResult=spiderkeyTable.objects.filter(taskId=int(taskid))
    dataCount=len(spiderResult)

    if dataCount<getNum:
        getNum=dataCount

    spiderResult=spiderResult.order_by(sortTyle)[0:getNum]

    data={
        "keyWord":keyWord,
        "domain":domain,
        "spiderResults":spiderResult,
        "dataCount":dataCount,
        "taskid":taskid,
    }

    return render(request,'resultShow.html',data)

@checklogin
def myWorkPush(request):
    email = request.session.get('logind')['email']
    userObj = User.objects.get(email=email)

    pushworks = taskTable.objects.filter(user=userObj)
    return render(request,"myWorkPush.html",{"pushworks":pushworks})

@checklogin
def mySubscribe(request):
    email = request.session.get('logind')['email']
    userObj = User.objects.get(email=email)

    pushworks = taskTable.objects.filter(user=userObj,subscribeStatus=1)
    return render(request, "mySubscribe.html", {"pushworks": pushworks})


@checklogin
def logout(request):
    del request.session['logind']
    return redirect('/home/login/')


"""
 "taskID": taskID,
					"status":status,
"""
@checklogin
def setSubscribe(request):
    if request.method=="POST":
        taskid=request.POST.get('taskID')
        status=request.POST.get('status')
        print (taskid,status)

        taskObj=taskTable.objects.get(id=taskid)
        if status=="true":
            taskObj.subscribeStatus = 1
        else:
            taskObj.subscribeStatus = 0
        taskObj.save()

        return HttpResponse(json.dumps({"status":True}))

@checklogin
def getSubscribe(request):
    if request.method=="POST":
        taskid=request.POST.get('pushworkId')
        taskObj = taskTable.objects.get(id=taskid)
        # print (taskid,taskObj.subscribeStatus)
        if taskObj.subscribeStatus == 1:
            return HttpResponse(json.dumps({"status": True}))
        else:
            return HttpResponse(json.dumps({"status": False}))