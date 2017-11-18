from django.db import models
from datetime import datetime


# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    add_time = models.DateTimeField(default=datetime.now)
    desc = models.CharField(max_length=200, verbose_name='城市描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name='机构描述')
    tag = models.CharField(max_length=10, verbose_name='机构标签', default='谁知道呢')
    category = models.CharField(default='organ',verbose_name='机构类别',max_length=20, choices=(('organ','培训机构'),('school','高校'),('person','个人')))
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', max_length=100,null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    # 获取课程机构的教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=20, verbose_name='姓名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50,  verbose_name='工作职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    courses = models.CharField(max_length=50,verbose_name='讲授课程',null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100,null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_num(self):
        return self.course_set.all().count()


