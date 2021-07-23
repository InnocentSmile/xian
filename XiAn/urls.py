"""XiAn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import xadmin
from XiAn import views
from users import views as users_view
from projects import views as pro_view
from courses import views as course_view
from operation import views as opera_view
from activity import views as activity_view

from wx import onlogin

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    # wx related
    path('wx/onlogin', onlogin.onLogin),

    path('api/updateUserInfo', users_view.updateUserInfo),
    path('api/indexBanner', users_view.indexBanner),
    path('api/companyInfo', users_view.companyInfo),
    # 项目
    path('api/proInfo', pro_view.proInfo),
    # 课程
    path('api/courseInfo', course_view.courseInfo),
    # 用户操作
    path('api/userfav', opera_view.userfav),
    path('api/resourceList', opera_view.resourceList),
    path('api/rdUser', opera_view.rdUser),
    path('api/appointment', opera_view.appointment),
    path('api/myfav', opera_view.myfav),
    path('api/activityInfo', activity_view.activityInfo),
    path('api/signupsheet', activity_view.signupsheet),


    path('.well-known/pki-validation/fileauth.txt', opera_view.myssl),


    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),

    # path('test', views.test),
    path('test', views.test),
    path('healthz', views.healthz),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
