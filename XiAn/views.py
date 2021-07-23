# -*- coding: utf8 -*-

import datetime
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse

from XiAn.django_jwt_session_auth import jwt_login
from users.models import User

logger = logging.getLogger(__name__)


@csrf_exempt
def test(request):
    userid = request.POST.get("id")
    # wx_openid = request.jwt_user.wx_openid
    print(userid)
    import json
    try:
        user_obj = User.objects.get(id=userid)
    except User.DoesNotExist:
        return JsonResponse({"msg": "没有该用户！"})
    token = jwt_login(user_obj, request, expire=3600)
    return HttpResponse(json.dumps([token], indent=2))


@csrf_exempt
def healthz(request):
    return HttpResponse("ok")
