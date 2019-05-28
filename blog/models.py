from django.db import models


# Create your models here.
class cls(models.Model):
    name = models.CharField(max_length=30, unique=True)
    start = models.DateField()
    progress = models.CharField(max_length=50)
    teachers=models.CharField(max_length=30, null=True, blank=True, default="无")
    remark = models.CharField(max_length=100, null=True, blank=True, default="无")
    def __str__(self):
        return self.name


class student(models.Model):
    name=models.CharField(max_length=20)
    cls=models.ForeignKey(cls,models.SET_NULL,null=True)
    sex=models.CharField(max_length=5,null=True,blank=True,default="不明")
    age=models.IntegerField()
    phonenum=models.CharField(max_length=11,unique=True)
    qq=models.CharField(max_length=15,null=True,blank=True,default="未留")
    school=models.CharField(max_length=30,null=True,blank=True,default="未留")
    homeaddr=models.CharField(max_length=30,null=True,blank=True,default="未留")
    addr=models.CharField(max_length=50)
    progress=models.CharField(max_length=50,null=True,blank=True,default="未留")
    job = models.CharField(max_length=30, null=True, blank=True, default="未就业")
    remark=models.CharField(max_length=100, null=True, blank=True, default="无")
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (("name", "sex", "age"),)


class teacher(models.Model):
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=5, null=True, blank=True, default="不明")
    phonenum = models.CharField(max_length=11)
    classes=models.ManyToManyField(cls)
    def __str__(self):
        return self.name
    class Meta:
        unique_together=(("name","sex","phonenum"),)


class usrid(models.Model):
    identity=models.CharField(max_length=10)


class usrinfo(models.Model):
    usr=models.CharField(max_length=30)
    pwd=models.CharField(max_length=16)
    uid=models.ForeignKey(to=usrid,on_delete=models.CASCADE,null=True,default="1")


class leave(models.Model):
    name=models.ForeignKey(student,models.CASCADE)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    reson=models.CharField(max_length=50)


class area(models.Model):
    codeid=models.IntegerField()
    parentid=models.IntegerField()
    cityName=models.CharField(max_length=180)
    def __str__(self):
        return self.cityName












