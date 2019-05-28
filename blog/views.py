from django.shortcuts import render,redirect,HttpResponse
from django import views
from blog import models
import json


# Create your views here.
def test(req):
    # obj = models.teacher.objects.all().last().classes.add(498)
    # obj = models.teacher.objects.all().last().classes.add(models.cls.objects.get(name=""))
    # ret=models.student.objects.get(id=2).cls  #一对多时的正反向查找
    #
    # ret = models.cls.objects.get(id=6).student_set.all()[0].name
    # print(666999,ret)

    # models.usrinfo.objects.filter(usr="").update(usr="")
    # ret=models.usrinfo.objects.filter(usr="")
    # ret1=models.usrinfo.objects.get(usr="")
    # print(1,ret,2,ret1)
    # for i in ret:
    #     print(666,i)
    # 可以用name去改信息，但主要是下面还要用id去设置多对多或者一对多
    return render(req, "base.html")


class student(views.View):
    def get(self, request, *args, **kwargs):
        if not request.session.get("login",None):
            return redirect("/login/")
        students = models.student.objects.all()
        models.student.objects.filter(name="乙").update(cls=models.cls.objects.get(name="自动化2班"))
        models.student.objects.filter(name="丙").update(cls=models.cls.objects.get(name="自动化2班"))
        models.student.objects.filter(name="丁").update(cls=models.cls.objects.get(name="自动化2班"))
        models.student.objects.filter(name="小王").update(cls=models.cls.objects.get(name="自动化2班"))
        return render(request, "student.html", {"usrname": request.session["usr"], "addwhich":"student", "students":students})


class teacher(views.View):
    def get(self, request, *args, **kwargs):
        if not request.session.get("login", None):
            return redirect("/login/")
        page = int(kwargs["page"].split(".")[0])
        start = (page - 1) * 20
        end = start + 20
        teacheres = models.teacher.objects.all()
        pages = teacheres.count()
        teacheres_ = teacheres[start:end]

        intpage, ynum = divmod(teacheres.count(), 20)
        # print(classes.count())
        # print(len(classes))
        # print(intpage)
        pagenum = []
        step = 0
        if page < 4:
            pagestart = 2
            if intpage >= 5:
                pageend = 5
                step = 1
            else:
                pageend = intpage
                step = 2
        elif page < intpage - 1:
            pagestart = page - 2
            pageend = page + 2
            step = 3
        else:
            step = 4
            if ynum != 0:
                pagestart = page - 3
                pageend = intpage + 1
            else:
                pagestart = page - 4
                pageend = intpage

        if page != 1:
            pagenum.append("<a style='width:60px' href='/teacher/%d.html/'>上一页</a>" % (page - 1,))
            pagenum.append("<a href='/teacher/1.html/'>1</a>")
        else:
            pagenum.append("<a style='background:gold' href='/teacher/1.html/'>1</a>")
        # if step > 1:
        #     pagenum.append("<a>...</a>")

        for i in range(pagestart, pageend + 1):
            if i == page:
                pagenum.append("<a style='background:gold' href='/teacher/%d.html/'>%d</a>" % (i, i))
            else:
                pagenum.append("<a href='/teacher/%d.html/'>%d</a>" % (i, i))

        # if step > 0 and step <= 3:
        #     pagenum.append("<a>...</a>")
        if page != (intpage + 1):
            pagenum.append("<a style='width:60px' href='/teacher/%d.html/'>下一页</a>" % (page + 1,))
        numshow = "".join(pagenum)
        # print(teacheres_)
        return render(request, "teacher.html", {"usrname": request.session["usr"],"addwhich":"teacher","teachers":teacheres_,"pagenum":numshow})

class cls(views.View):
    def get(self, request, *args, **kwargs):
        if not request.session.get("login", None):
            return redirect("/login/")
        # for i in range(1,100):
        #     models.cls.objects.create(
        #         name="自动化"+str(i)+"班",
        #         start='2018-06-15',
        #         progress="毕设"
        #     )
        page = int(kwargs["page"].split(".")[0])
        start = (page - 1) * 20
        end = start + 20
        classes = models.cls.objects.all()
        pages = classes.count()
        clss = classes[start : end]
        intpage, ynum = divmod(classes.count(), 20)

        pagenum=[]
        step=0
        if page<4:
            pagestart=2
            if intpage>=5:
                pageend=5
                step = 1
            else:
                pageend=intpage
                step=2
        elif page < intpage-1:
                pagestart=page-2
                pageend=page+2
                step=3
        else:
            step=4
            if ynum!=0:
                pagestart=page-3
                pageend=intpage+1
            else:
                pagestart = page - 4
                pageend = intpage


        if page!=1:
            pagenum.append("<a style='width:60px' href='/cls/%d.html/'>上一页</a>" % (page - 1,))
            pagenum.append("<a href='/cls/1.html/'>1</a>")
        else:
            pagenum.append("<a style='background:gold' href='/cls/1.html/'>1</a>")
        if step > 1:
            pagenum.append("<a>...</a>")

        for i in range(pagestart,pageend+1):
            if i==page:
                pagenum.append("<a style='background:gold' href='/cls/%d.html/'>%d</a>" % (i, i))
            else:
                pagenum.append("<a href='/cls/%d.html/'>%d</a>"%(i,i))

        if step > 0 and step <= 3:
            pagenum.append("<a>...</a>")
        if page != (intpage+1):
            pagenum.append("<a style='width:60px' href='/cls/%d.html/'>下一页</a>" % (page + 1,))
        numshow = "".join(pagenum)
        print(numshow)
        return render(request, "cls.html", {"usrname": request.session["usr"],"addwhich":"cls","classes":clss,"pagenum":numshow})


from django.db import connection
def clsOperation(req):
    op = req.POST.get('op',None)
    if op == 'del':
        clsname=req.POST.get('name',None)
        try:
            # models.cls.objects.raw(" delete from study_cls where name='全栈16班'")
            # with connection.cursor() as cursor:
            #     cursor.execute("delete from blog_cls where name=%s",[clsname])
            models.cls.objects.get(name=clsname).delete()
        except Exception as e:
            return HttpResponse(e)
        return  HttpResponse("ok")
    elif op == 'edit':
        formData = req.POST.get("formdata", None)
        formObj = json.loads(formData)
        # print(formObj)
        try:
            models.cls.objects.filter(id=formObj['id']).update(name=formObj['clsname'], start=formObj['start'],
                                      progress=formObj['progress'], remark=formObj['remark'])
            teacherList = []
            for i in formObj['teacherList']:
                teacherList.append(models.teacher.objects.get(name=i))
            models.cls.objects.get(id=formObj['id']).teacher_set.set(teacherList)
        except Exception as e:
            print(e)
            return HttpResponse("err")
        return HttpResponse("ok")
    elif op == 'preGet':
        teacherList = models.teacher.objects.raw("select * from blog_teacher")
        L = []
        for i in teacherList:
            L.append(i.name)
        clsname = req.POST.get('name', None)
        ret = models.cls.objects.get(name=clsname)
        josndata = json.dumps({"teachers": L, "id": ret.id})
        # teachers=",".join(L)
        return HttpResponse(josndata)

from django.db import connection
def teacherOperation(req):
    op = req.POST.get('op',None)
    if op == 'del':
        studentname=req.POST.get('name',None)
        try:
            # models.teacher.objects.filter(name=teachername).cls.clear()
            # models.cls.objects.raw(" delete from study_cls where name='全栈16班'")
            # with connection.cursor() as cursor:
            #     print(5555555555)
            #     cursor.execute("delete from blog_teacher where name=%s",[teachername])
            models.teacher.objects.filter(name=studentname).delete()
            # print(models.teacher.objects.get(name="xiao9"))
        except Exception as e:
            return HttpResponse(e)
        return  HttpResponse("ok")
    elif op == 'edit':
        formData = req.POST.get("formdata", None)
        formObj = json.loads(formData)
        # print(formObj)
        try:
            models.teacher.objects.filter(id=formObj['id']).update(name=formObj['name'], sex=formObj['sex'],
                                      phonenum=formObj['phonenum'])
            clsList = []
            for i in formObj['clsList']:
                clsList.append(models.cls.objects.get(name=i))
            print(clsList)
            models.teacher.objects.get(id=formObj['id']).classes.set(clsList)
        except Exception as e:
            return HttpResponse("err")
        return HttpResponse("ok")
    elif op == 'preGet':
        clsList = models.cls.objects.raw("select * from blog_cls")
        L = []
        for i in clsList:
            L.append(i.name)
        teachername = req.POST.get('name', None)
        ret = models.teacher.objects.get(name=teachername)
        josndata = json.dumps({"clses": L, "id": ret.id})
        # teachers=",".join(L)
        return HttpResponse(josndata)


from django.db import connection
def studentOperation(req):
    op = req.POST.get('op',None)
    if op == 'del':
        studentname=req.POST.get('name',None)
        try:
            models.student.objects.get(name=studentname).delete()
        except Exception as e:
            return HttpResponse(e)
        return  HttpResponse("ok")
    elif op == 'edit':
        formData = req.POST.get("formdata", None)
        formObj = json.loads(formData)
        print("<<", formObj)
        try:
            models.cls.objects.filter(id=formObj['id']).update(name=formObj['clsname'], start=formObj['start'],
                                      progress=formObj['progress'], remark=formObj['remark'])
            teacherList = []
            for i in formObj['teacherList']:
                teacherList.append(models.teacher.objects.get(name=i))
            models.cls.objects.get(id=formObj['id']).teacher_set.set(teacherList)
        except Exception as e:
            print(e)
            return HttpResponse("err")
        return HttpResponse("ok")
    elif op == 'preGet':
        teacherList = models.teacher.objects.raw("select * from blog_teacher")
        L = []
        for i in teacherList:
            L.append(i.name)
        clsname = req.POST.get('name', None)
        ret = models.cls.objects.get(name=clsname)
        josndata = json.dumps({"teachers": L, "id": ret.id})
        # teachers=",".join(L)
        return HttpResponse(josndata)


class login(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")
    def post(self, request, *args, **kwargs):
        usr_data = request.POST.get("usr", None)
        pwd_data = request.POST.get("pwd", None)
        id_data = request.POST.get("id", None)
        try:
            models.usrinfo.objects.get(usr=usr_data, pwd=pwd_data, uid=id_data)
        except Exception:
            return render(request, "login.html", {"errinfo":"登陆失败，请检查您的用户名密码或身份"})
        request.session["login"] = True
        request.session["usr"] = usr_data
        request.session["id"] = id_data
        # request.session.set_expiry()
        # return HttpResponse(iddata)
        return redirect("/student/")

def blank(req):
    return redirect("/login/")


def articlas(req,y):
    return HttpResponse("123"+y)

proid=0
def add(req,which):
    if req.session.get("id",None):
        if which == "property":
            if req.session.get("id", None) == '3':
                return HttpResponse("ok")
            else:
                return HttpResponse("err")
        else:
            if which!="student":
                return  render(req, "base.html")
            if which == "student":

                global proid
                classes=models.cls.objects.all()
                # b=models.cls.objects.get(id=3)
                # models.student.objects.filter(id=5).update(cls=b)
                # models.student.objects.filter(id=5).delete()
                # a = models.student.objects.get(id=2).cls
                # print(111,a)
                proviences = models.area.objects.filter(parentid=0)


                cityname = req.POST.get("pro", None)
                if req.POST.get("pro", None):
                    cityname = req.POST.get("pro", None)
                    codeid = models.area.objects.get(cityName=cityname, parentid=0).codeid
                    proid = codeid
                elif req.POST.get("city", None):
                    cityname = req.POST.get("city", None)
                    codeid = models.area.objects.get(cityName=cityname, parentid=proid).codeid
                if cityname:
                    cities = models.area.objects.filter(parentid=codeid)
                    citystr = ""
                    for i in cities:
                        citystr = citystr + i.cityName + ","
                    return HttpResponse(citystr)

                cityname_ = req.POST.get("pro_", None)
                if req.POST.get("pro_", None):
                    cityname_ = req.POST.get("pro_", None)
                    codeid = models.area.objects.get(cityName=cityname_, parentid=0).codeid
                    proid = codeid
                elif req.POST.get("city_", None):
                    # global proid
                    print(req.POST.get("city_", None))
                    cityname_= req.POST.get("city_", None)
                    codeid = models.area.objects.get(cityName=cityname_, parentid=proid).codeid
                if cityname_:
                    cities = models.area.objects.filter(parentid=codeid)
                    citystr = ""
                    for i in cities:
                        citystr = citystr + i.cityName + ","
                    return HttpResponse(citystr)
                return render(req,"add.html",{"cls":classes,"provinces": proviences,"addwhich":which})
    else:
        return render(req,"login.html")


def clsedit(req):
    if req.session.get("id", None) == '3':
        return HttpResponse("ok")
    else:
        return HttpResponse("err")

