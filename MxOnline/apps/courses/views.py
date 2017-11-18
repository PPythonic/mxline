from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse
from courses.models import Course, CourseResourse
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from apps.operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequireMixin
from django.db.models import Q

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-students')[0:3]

        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(tag__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_course = all_course.order_by('-click_nums')
        elif sort == 'students':
            all_course = all_course.order_by('-students')

        # 对课程进行分页，分页这一块儿代码可以重复使用
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_course': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        # 判断是否登录，是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 相关推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request,'course-detail.html', {
            'course': course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseInfoView(LoginRequireMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        all_resourses = CourseResourse.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resourses': all_resourses,
            'relate_courses':relate_courses,
        })


class CourseCommentView(View):
    '''
    课程评论
    '''
    def get(self, requeset, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resourses = CourseResourse.objects.filter(course=course)
        comments = CourseComment.objects.filter(course_id=course_id)
        return render(requeset, 'course-comment.html', {
            'course': course,
            'comments': comments,
            'all_resourses': all_resourses,
        })


class AddCommentView(View):
    '''
    用户添加课程评论
    '''
    def post(self,request):
        # 判断用户是否登录
        if not request.user.is_authenticated():
            return JsonResponse({'status':'fail','msg':'用户未登录'})

        # 将数据保存到数据库
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) >0 and comments:
            course_comments = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comment = comments
            course_comments.user = request.user
            course_comments.save()
            return JsonResponse({'status':'success','msg':'添加成功'})
        else:
            return JsonResponse({'status':'fail', 'msg':'添加失败'})

