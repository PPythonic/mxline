from django.conf.urls import url
from users.views import UserInfoView, UserCourseView, MyFavCourseView, UserMsgView, UploadImageView, UpdataPwdView, SendEmailView, UpdateEmailView, MyFavOrgView, MyFavTeacherView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='usercenter_info'),
    # 我的课程
    url(r'^course/$', UserCourseView.as_view(), name='usercenter_course'),
    # 我收藏的机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 我收藏的讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 用户消息
    url(r'^msg/$', UserMsgView.as_view(), name='usercenter_msg'),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户中心修改密码
    url(r'^update/pwd/$', UpdataPwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailView.as_view(), name='email_code'),
    # 发送用户邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

]