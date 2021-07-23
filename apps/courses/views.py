import json

from django.conf import settings as django_settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from operation.models import UserFavorite
from .models import Course


@csrf_exempt
@api_view(["POST"])
def courseInfo(request):
    user_id = request.jwt_user.id
    filterParams = {}
    query_params = dict(request.POST.items())
    for k, v in query_params.items():
        if hasattr(Course, k):
            if k in ("is_detail_recommend", "is_index_recommend", "is_on_shelf"):
                v = json.loads(v)
            filterParams.update({k: v})
    course_qs = Course.objects.filter(**filterParams)
    if filterParams.get("is_detail_recommend") or filterParams.get("is_detail_recommend"):
        course_id = filterParams.get("id")
        course_qs = Course.objects.filter(**filterParams).exclude(id=course_id)
    ###########分页
    page = query_params.get("page", None)
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

        json_data["is_fav"] = False
        user_fav_qs = UserFavorite.objects.filter(user_id=user_id, fav_type=2, fav_id=json_data["id"])
        if user_fav_qs:
            json_data["is_fav"] = True
        # 最后添加到列表中
        json_list.append(json_data)
    res_dict.update({"course_list": json_list})
    return Response(res_dict)
