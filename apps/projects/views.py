import json

from django.conf import settings as django_settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from operation.models import UserFavorite
from .models import Project, ProBanner, ProVideo, ProApartment, Country


@csrf_exempt
@api_view(["POST"])
def proInfo(request):
    user_id = request.jwt_user.id
    filterParams = {}
    query_params = dict(request.POST.items())
    for k, v in query_params.items():
        if hasattr(Project, k):
            if k in ("is_detail_recommend", "is_index_recommend", "is_on_shelf"):
                v = json.loads(v)
            filterParams.update({k: v})
    project_qs = Project.objects.filter(**filterParams).order_by("index")
    if filterParams.get("is_detail_recommend") or filterParams.get("is_detail_recommend"):
        pro_id = filterParams.pop("id")
        project_qs = Project.objects.filter(**filterParams).exclude(id=pro_id).order_by("index")
    ###########分页
    page = query_params.get("page", None)
    if page:
        page = int(page)
    paginator = Paginator(project_qs, 6)
    try:
        project_qs = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        project_qs = paginator.page(1)  # 提取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        project_qs = paginator.page(paginator.num_pages)  # 提取最后一页的记录
    number = project_qs.number
    next = number + 1 if project_qs.has_next() else None
    previous = number - 1 if project_qs.has_previous() else None
    count = paginator.count
    paginator_info = {"next": next, "count": count, "previous": previous}
    #############分页之后的查询集
    json_list = []
    res_dict = paginator_info  # 初始化
    for p in project_qs:
        json_data = model_to_dict(p)
        json_data["logo_img"] = django_settings.XIANFILEPATH + json_data["logo_img"].name if json_data[
            "logo_img"] else None
        json_data["gif_img"] = django_settings.XIANFILEPATH + json_data["gif_img"].name if json_data[
            "gif_img"] else None
        json_data["country"] = p.country.name
        # 视频
        video_list = ProVideo.objects.filter(project=p).values("name", "video", "url")
        for v in video_list:
            v["video"] = django_settings.XIANFILEPATH + v["video"] if v["video"] else None
        json_data["video_list"] = video_list
        # 轮播图
        banner_list = ProBanner.objects.filter(project=p).order_by("index").values("name", "img", "url")
        for b in banner_list:
            b["img"] = django_settings.XIANFILEPATH + b["img"] if b["img"] else None
        json_data["banner_list"] = banner_list
        # 户型
        apartment_list = ProApartment.objects.filter(project=p).order_by("index").values("name", "apartment_img", "url",
                                                                                         "house_area")
        for a in apartment_list:
            a["apartment_img"] = django_settings.XIANFILEPATH + a["apartment_img"] if a["apartment_img"] else None
        json_data["apartment_list"] = apartment_list
        # 最后添加到列表中
        json_data["is_fav"] = False
        user_fav_qs = UserFavorite.objects.filter(user_id=user_id, fav_type=1, fav_id=json_data["id"])
        if user_fav_qs:
            json_data["is_fav"] = True
        json_list.append(json_data)
    country = Country.objects.values("id", "name")
    res_dict.update({"pro_list": json_list, "country": country})
    return Response(res_dict)
