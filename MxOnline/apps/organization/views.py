from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse

from apps.organization.models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.organization.forms import UserAskForm
from courses.models import Course
from apps.operation.models import UserFavorite



# Create your views here.
class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-students')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 对机构地区进行筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构类别进行筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 对课程机构进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs =all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        org_nums = all_orgs.count()

        return render(request, 'org-list.html', {
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id': city_id,
            'category':category,
            'hot_orgs': hot_orgs,
            'sort': sort,

        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'fail','msg':'添加出错'})


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]   # 有外键的地方可以这么使用，django自带的ORM非常方便！！！
        all_teachers = course_org.teacher_set.all()[:1]  # 同上
        return render(request, 'org-detail-homepage.html', {
            'course_org': course_org,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()   # 有外键的地方可以这么使用，django自带的ORM非常方便！！！
        return render(request, 'org-detail-course.html', {
            'course_org': course_org,
            'all_courses':all_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    '''
    添加用户收藏，取消收藏
    '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户登陆状态
            return JsonResponse({'status':'fail','msg':'用户未登录'})
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            # 收藏数减一
            if int(fav_type == 1):
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type ==2):
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type ==3):
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return JsonResponse({'status':'fail','msg':'收藏'})
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return JsonResponse({'status':'success','msg':'已收藏'})
            else:
                return JsonResponse({'status':'fail','msg':'收藏出错'})

class TeacherListView(View):
    def get(self,request):
        teachers = Teacher.objects.all()
        teacher_nums = teachers.count()

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            teachers = teachers.filter(Q(name__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')

        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        # 对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(teachers, 2, request=request)
        teacher = p.page(page)
        # course = Course.objects.get(id=int(course_id))
        return render(request, 'teachers-list.html', {
            'teachers': teacher,
            # 'course': course,
            'sorted_teachers': sorted_teachers,
            'teacher_nums': teacher_nums,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self,request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teachers=teacher)
        teacher.click_nums += 1
        teacher.save()

        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3,fav_id=teacher.id):
            has_fav_teacher = True

        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2,fav_id=teacher.org.id):
            has_fav_org = True

        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org,

        })