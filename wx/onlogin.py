# -*- coding: utf8 -*-

import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common import error_codes

from django.conf import settings as django_settings

from XiAn.django_jwt_session_auth import jwt_login
from users.tasks import storeUserOpenid, storeWxSession
from wx.utils import wxLogin

logger = logging.getLogger(__name__)


@csrf_exempt
def onLogin(request):
    code = request.POST.get("code")
    if code is None:
        res = {
            "code": error_codes.CODE_WX_LOGIN_FAILED,
            "msg": "code is None",
            "ok": False,
            "data": {}
        }
        logger.error("微信登录失败，code 不能为空")
        return JsonResponse(res)
    rsp = wxLogin(code)
    logger.info("微信登录结果%s" % (rsp))
    if not rsp.ok:
        res = {
            "code": error_codes.CODE_WX_LOGIN_FAILED,
            "msg": "weixin login failed",
            "ok": False,
            "data": {}
        }
        logger.error("用户登录失败， 失败原因：请求微信接口失败")
        return JsonResponse(res)
    else:
        data = rsp.data
        openid = data.get("openid")
        session_key = data.get("session_key")
        if openid is None:
            errmsg = data.get("errmsg")
            res = {
                "code": error_codes.CODE_WX_LOGIN_FAILED,
                "msg": "get openid failed: %s" % errmsg,
                "ok": False,
                "data": {}
            }
            logger.error("用户登录失败, 失败原因: %s" % errmsg)
            return JsonResponse(res)
        user_obj = storeUserOpenid(openid)  # 保存用户wx_openid 信息
        token = jwt_login(user_obj, request, expire=django_settings.WX_SESSION_EXPIRE_TIME)  # 产生token
        storeWxSession(userid=user_obj.id, session_key=session_key, token=token)  # 存下来，后面会用到sessionkey解锁微信的加密过的信息
        data.update({"token": token})
        data.pop("session_key")  # 不要返回session_key给前端
        res = {
            "code": error_codes.CODE_OK,
            "msg": "login success",
            "ok": True,
            "data": data
        }
        logger.info("用户(user_id=%s)微信登录成功, openid为%s" % (user_obj.id, openid))
        return JsonResponse(res)
