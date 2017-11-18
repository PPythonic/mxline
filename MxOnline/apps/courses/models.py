from django.db import models
from datetime import datetime
from apps.organization.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    teachers = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=200, verbose_name='课程简介')
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(choices=(('cj','初级'),('zj','中级'),('gj','高级')), verbose_name='课程难度', max_length=20)
    learn_time = models.IntegerField(default=0, verbose_name='学习时常(分钟数)')
    chapters = models.IntegerField(default=0,verbose_name='章节数', null=True, blank=True)
    category = models.CharField(default='', max_length=30,verbose_name='课程类别',null=True, blank=True)
    tag = models.CharField(default='', verbose_name='课程标签',max_length=20)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100,null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    need_known = models.CharField(max_length=100, verbose_name='课程须知', null=True, blank=True)
    tell_you = models.CharField(max_length=100, verbose_name='老师告诉你什么', null=True, blank=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_learn_users(self):
        return self.usercourse_set.all()[0:6]

    # 获取章节课程
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    # 获取章节视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return '{0}--{1}'.format(self.course, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.URLField(max_length=200,default='', verbose_name='视频链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.name)


class CourseResourse(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resouce/%Y/%m', verbose_name='资源文件', max_length=100,null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}{}'.format(self.course, self.name)


