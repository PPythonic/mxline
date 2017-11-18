import xadmin
from .models import Course,Lesson,Video,CourseResourse


class CourseAdmin(object):
    list_display = ['name','desc','degree','students','fav_nums','click_nums']
    search_fields = ['name','desc','detail','degree','students','fav_nums','click_nums']
    list_filter = ['name','desc','detail','degree','learn_time','students','fav_nums','click_nums']


class LessonAdmin(object):
    list_display = ['course','name', 'add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourseAdmin(object):
    list_display = ['course', 'name','download','add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name','download','add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResourse, CourseResourseAdmin)