import xadmin
from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ['name', 'add_time', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'add_time', 'desc']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','click_nums','fav_nums','image','address','city','add_time',]
    search_fields = ['name', 'desc','click_nums','fav_nums','image','address','city']
    list_filter = ['name', 'desc','click_nums','fav_nums','image','address','city','add_time']


class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time','org' ]
    search_fields = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'org' ]
    list_filter = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time','org' ]


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)