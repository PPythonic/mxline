from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password
import json

from pure_pagination import Paginator,EmptyPage,PageNotAnInteger


from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin
from apps.operation.models import UserCourse, UserMessage, UserFavorite
from apps.organization.models import CourseOrg, Teacher
from courses.models import Course


# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    # 继承的view自动帮我们完成request.method的方法调用，get和post方法
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg':'用户还未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form':login_form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))
        # return redirect(request,'index.html')


# 一般类命名加view，用于表明这是处理前端请求的view类
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':'用户名已被注册'})
            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            # 写入欢迎注册消息
            user_msg = UserMessage()
            user_msg.user = user_profile
            user_msg.message = '欢迎注册慕学在线网'
            user_msg.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
             return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email':email})
        else:
             return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email':email, 'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form':modify_form})


class UserInfoView(LoginRequireMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse(json.dumps(user_info_form.errors))

class UserCourseView(LoginRequireMixin, View):
    '''
    我的课程
    '''
    def get(self,request):
        courses = UserCourse.objects.filter(user_id=request.user)
        return render(request, 'usercenter-mycourse.html',{
            'courses': courses,
        })


class MyFavOrgView(LoginRequireMixin, View):
    '''
    我收藏的课程机构
    '''
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequireMixin, View):
    '''
    我收藏的讲师
    '''
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for teacher in fav_teachers:
            teacher_id = teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequireMixin, View):
    '''
    我收藏的课程
    '''
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for course in fav_courses:
            course_id = course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
        })


class UserMsgView(LoginRequireMixin, View):
    '''
    我的消息
    '''
    def get(self, request):
        all_msgs = UserMessage.objects.filter(user=request.user.id)

        # 用戶進入消息中心后清除未讀的消息提示
        all_unread_msgs = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_msg in all_unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_msgs, 6, request=request)
        msgs = p.page(page)
        return render(request, 'usercenter-message.html', {
            'msgs': msgs,
        })


class UploadImageView(LoginRequireMixin, View):
    '''
    用户上传图像
    '''
    def post(self,request):
        image_form = UploadImageForm(request.POST, request.FILES) # 这样就把图片保存到内存中来了
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'fail', 'msg':'上传头像错误'})


class UpdataPwdView(LoginRequireMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return JsonResponse({'status':'fail','msg':'密码不一致'})
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return JsonResponse({'status':'success','msg':'密码修改成功'})
        else:
            return JsonResponse(json.dumps(modify_form.errors))


class UpdateEmailView(LoginRequireMixin, View):
    def post(self, request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        excited_record = EmailVerifyRecord.objects.filter(email=email, code=code,send_type='update')
        if excited_record:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'email':'验证码错误'})



class SendEmailView(LoginRequireMixin, View):
    '''
    发送邮箱验证码
    '''
    def get(self, request):
        email = request.GET.get('email', '')
        # 判断邮箱是否已经注册
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email':"邮箱已经存在"})
        # 调用发送邮件函数
        send_register_email(email, 'update')
        return JsonResponse({'status':'success'})


class IndexView(View):
    '''
    首页
    '''
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs':course_orgs,
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code =404
    return response

def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response

def no_permission(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('403.html',{})
    response.status_code = 403
    return response