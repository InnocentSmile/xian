import json
import logging

from django.forms import model_to_dict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.error_codes import CODE_OK, CODE_SERVER_ERROR
from common.utils import create_or_update
from .models import Activity, Signupsheet

from django.conf import settings as django_settings
logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["GET"])
def activityInfo(request):
    activity_qs=Activity.objects.filter(is_on_shelf=True)
    json_list = []
    res_dict = {}
    for obj in activity_qs:
        json_data = model_to_dict(obj)
        json_data["into_img"] = django_settings.XIANFILEPATH + json_data["into_img"].name if json_data["into_img"] else None
        json_data["master_img"] = django_settings.XIANFILEPATH + json_data["master_img"].name if json_data["master_img"] else None
        json_list.append(json_data)
    res_dict.update({"activity_list": json_list})
    return Response(res_dict)


@csrf_exempt
@api_view(["GET", "POST"])
def signupsheet(request):
    user_id = request.jwt_user.id
    if request.method == "GET":
        appointment_qs = Signupsheet.objects.filter(user_id=user_id)
        if appointment_qs:
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": {"is_signupsheet": True}}
        else:
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": {"is_signupsheet": False}}
    else:
        signupsheet_dict = {}
        signupsheet_dict.update({"user_id": user_id})
        for k, v in request.POST.items():
            if hasattr(Signupsheet(), k):
                signupsheet_dict.update({k: v})
        try:
            create_or_update(model=Signupsheet, uniq_condition=signupsheet_dict, data_kwargs=signupsheet_dict)
            res = {"ok": True, "code": CODE_OK, "msg": "success", "data": signupsheet_dict}
        except Exception as ex:
            logger.error("提交活动, userid: %s ，报错原因%s" % (user_id, ex))
            res = {"ok": False, "code": CODE_SERVER_ERROR, "msg": "success", "data": signupsheet_dict}
        logger.info("提交活动此时的rd_dict为%s" % signupsheet_dict)
    return Response(res)


