import json
import logging
from django.conf import settings as django_settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.error_codes import CODE_OK, CODE_SERVER_ERROR
from common.utils import create_or_update
from courses.models import Course
from operation.models import UserFavorite, Resource, RDUser, Appointment
from projects.models import Project, ProBanner

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["POST"])
def userfav(request):
    userfav_dict = {}
    user_id = request.jwt_user.id
    userfav_dict.update({"user_id": user_id})
    for k, v in request.POST.items():  # request.POST返回的是QueryDict的形式，值都会带上[]， 比如first_name_pinyin: ["gao"]
        if hasattr(UserFavorite(), k):
            userfav_dict.update({k: v})
    try:
        create_or_update(model=UserFavorite, uniq_condition=userfav_dict, data_kwargs=userfav_dict)
        res = {"ok": True, "code": CODE_OK, "msg": "success", "data": userfav_dict}
    except Exception as ex:
        logger.error("用户收藏, userid: %s ，报错原因%s" % (user_id, ex))
        res = {"ok": False, "code": CODE_SERVER_ERROR, "msg": "success", "data": userfav_dict}
    logger.info("此时的userfav_dict为%s" % userfav_dict)
    return Response(res)


@csrf_exempt
@api_view(["GET"])
def resourceList(request):
    resource_qs = Resource.objects.filter(is_on_shelf=True).order_by("index")
    ###########分页
    page = request.GET.get("page", None)
    if page:
        page = int(page)
    paginator = Paginator(resource_qs, 6)
    try:
        resource_qs = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        resource_qs = paginator.page(1)  # 提取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        resource_qs = paginator.page(paginator.num_pages)  # 提取最后一页的记录
    number = resource_qs.number
    next = number + 1 if resource_qs.has_next() else None
    previous = number - 1 if resource_qs.has_previous() else None
    count = paginator.count
    paginator_info = {"next": next, "count": count, "previous": previous}
    #############分页之后的查询集
    json_list = []
    res_dict = paginator_info  # 初始化
    for i in resource_qs:
        json_data = model_to_dict(i)
        json_data["img"] = django_settings.XIANFILEPATH + json_data["img"].name if json_data["img"] else None
        json_data["download"] = django_settings.XIANFILEPATH + json_data["download"].name if json_data[
            "download"] else None
        # 最后添加到列表中
        json_list.append(json_data)
    res_dict.update({"pro_list": json_list})
    return Response(res_dict)


# 资料下载表单
@csrf_exempt
@api_view(["GET", "POST"])
def rdUser(request):
    user_id = request.jwt_user.id
    if request.method == "GET":
        rd_qs = RDUser.objects.filter(user_id=user_id)
        if rd_qs:
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": {"isrd": True}}
        else:
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": {"isrd": False}}
    else:
        rd_dict = {}
        user_id = request.jwt_user.id
        rd_dict.update({"user_id": user_id})
        for k, v in request.POST.items():  # request.POST返回的是QueryDict的形式，值都会带上[]， 比如first_name_pinyin: ["gao"]
            if hasattr(RDUser(), k):
                if k in ("is_subscribe"):
                    v = json.loads(v)
                rd_dict.update({k: v})
        try:
            create_or_update(model=RDUser, uniq_condition=rd_dict, data_kwargs=rd_dict)
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": rd_dict}
        except Exception as ex:
            logger.error("资料下载表单, userid: %s ，报错原因%s" % (user_id, ex))
            res = {"ok": False, "code": CODE_SERVER_ERROR, "msg": "success", "data": rd_dict}
        logger.info("资料下载表单此时的rd_dict为%s" % rd_dict)
    return Response(res)


# 预约品鉴
@csrf_exempt
@api_view(["GET", "POST"])
def appointment(request):
    user_id = request.jwt_user.id
    if request.method == "GET":
        appointment_qs = Appointment.objects.filter(user_id=user_id)
        if appointment_qs:
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": {"isappointment": True}}
        else:
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": {"isappointment": False}}
    else:
        appointment_dict = {}
        user_id = request.jwt_user.id
        appointment_dict.update({"user_id": user_id})
        for k, v in request.POST.items():  # request.POST返回的是QueryDict的形式，值都会带上[]， 比如first_name_pinyin: ["gao"]
            if hasattr(Appointment(), k):
                if k in ("is_subscribe"):
                    v = json.loads(v)
                appointment_dict.update({k: v})
        try:
            create_or_update(model=Appointment, uniq_condition=appointment_dict, data_kwargs=appointment_dict)
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": appointment_dict}
        except Exception as ex:
            logger.error("预约品鉴, userid: %s ，报错原因%s" % (user_id, ex))
            res = {"ok": False, "code": CODE_SERVER_ERROR, "msg": "success", "data": appointment_dict}
        logger.info("预约品鉴此时的rd_dict为%s" % appointment_dict)
    return Response(res)


@csrf_exempt
@api_view(["GET"])
def myfav(request):
    # (1, '项目'),
    # (2, '课程'),
    user_id = request.jwt_user.id
    fav_type = request.GET.get("fav_type", 1)
    page = request.GET.get("page", None)
    user_fav_qs = UserFavorite.objects.filter(user_id=user_id, fav_type=fav_type)
    fav_id_list = [i.fav_id for i in user_fav_qs]
    if int(fav_type) == 1:
        pro_qs = Project.objects.filter(id__in=fav_id_list)
        ###########分页
        if page:
            page = int(page)
        paginator = Paginator(pro_qs, 6)
        try:
            pro_qs = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            pro_qs = paginator.page(1)  # 提取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            pro_qs = paginator.page(paginator.num_pages)  # 提取最后一页的记录
        number = pro_qs.number
        next = number + 1 if pro_qs.has_next() else None
        previous = number - 1 if pro_qs.has_previous() else None
        count = paginator.count
        paginator_info = {"next": next, "count": count, "previous": previous}
        #############分页之后的查询集
        json_list = []
        res_dict = paginator_info  # 初始化
        for p in pro_qs:
            json_data = model_to_dict(p)
            json_data["logo_img"] = django_settings.XIANFILEPATH + json_data["logo_img"].name if json_data[
                "logo_img"] else None
            json_data["gif_img"] = django_settings.XIANFILEPATH + json_data["gif_img"].name if json_data[
                "gif_img"] else None
            json_data["country"] = p.country.name
            # 轮播图
            banner_list = ProBanner.objects.filter(project=p).values("name", "img", "url")
            for b in banner_list:
                b["img"] = django_settings.XIANFILEPATH + b["img"] if b["img"] else None
            json_data["banner_list"] = banner_list
            # 最后添加到列表中
            json_list.append(json_data)
        res_dict.update({"pro_list": json_list})
        return Response(res_dict)

    else:
        course_qs = Course.objects.filter(id__in=fav_id_list)
        ###########分页
        if page:
            page = int(page)
        paginator = Paginator(course_qs, 6)
        try:
            course_qs = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            course_qs = paginator.page(1)  # 提取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            course_qs = paginator.page(paginator.num_pages)  # 提取最后一页的记录
        number = course_qs.number
        next = number + 1 if course_qs.has_next() else None
        previous = number - 1 if course_qs.has_previous() else None
        count = paginator.count
        paginator_info = {"next": next, "count": count, "previous": previous}
        #############分页之后的查询集
        json_list = []
        res_dict = paginator_info  # 初始化
        for c in course_qs:
            json_data = model_to_dict(c)
            json_data["video"] = django_settings.XIANFILEPATH + json_data["video"].name if json_data["video"] else None
            json_data["img"] = django_settings.XIANFILEPATH + json_data["img"].name if json_data["img"] else None
            json_data["audio"] = django_settings.XIANFILEPATH + json_data["audio"].name if json_data["audio"] else None

            # 最后添加到列表中
            json_list.append(json_data)
        res_dict.update({"course_list": json_list})
        return Response(res_dict)

@csrf_exempt
def myssl(request):
    return HttpResponse("201905210225363qbs17ll2p0uabzpgbny9ajtt2qdmbj99n4mungsjp2q1f0898")