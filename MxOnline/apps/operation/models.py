from datetime import datetime

from django.db import models

from courses.models import Course
from users.models import UserProfile


# Create your models here.

class UserAsk(models.Model):
    '''
    用户咨询
    '''
    name = models.CharField(max_length=20, verbose_name='用户名')
    mobile = models.CharField(max_length=11,verbose_name='手机号码')
    course_name = models.CharField(max_length=50, verbose_name='课程名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural =verbose_name


class CourseComment(models.Model):
    '''
    课程评论
    '''
    course = models.ForeignKey(Course, verbose_name='课程')
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    comment = models.CharField(max_length=200, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment


class UserFavorite(models.Model):
    '''
    用户收藏
    '''
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据id')
    fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')), default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    '''
    用户消息
    '''
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=500, verbose_name='用户消息')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    '''
    用户课程
    '''
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name



