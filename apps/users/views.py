import logging

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as django_settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import User, Banner, Company
from users.tasks import updateUserInfoTask

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["POST"])
def updateUserInfo(request):
    userinfo = {}
    userid = request.jwt_user.id
    userinfo.update({"userid": userid})
    for k, v in request.POST.items():  # request.POST返回的是QueryDict的形式，值都会带上[]， 比如first_name_pinyin: ["gao"]
        if hasattr(User(), k):
            userinfo.update({k: v})
    logger.info("此时的userinfo为%s" % userinfo)
    res = updateUserInfoTask(**userinfo)
    return Response(data=res)


@csrf_exempt
@api_view(["GET"])
def indexBanner(request):
    banner_qs = Banner.objects.filter(is_on_shelf=True).order_by("index")
    banner_list_dict = banner_qs.values("image", "title", "project_id")
    for i in banner_list_dict:
        i["image"] = django_settings.XIANFILEPATH + i["image"] if i["image"] else None
    return Response(banner_list_dict)


@csrf_exempt
@api_view(["GET"])
def companyInfo(request):
    company_qs = Company.objects.all()
    company_list_dict = company_qs.values("logo_img", "video", "description", "bottom")
    for i in company_list_dict:
        i["logo_img"] = django_settings.XIANFILEPATH + i["logo_img"] if i["logo_img"] else None
        i["video"] = django_settings.XIANFILEPATH + i["video"] if i["video"] else None
    return Response(company_list_dict)
