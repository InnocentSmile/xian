# -*- coding: utf8 -*-


import datetime

from rest_framework import authentication
from rest_framework import exceptions


def user_to_payload(user):
    exp = datetime.datetime.now() + datetime.timedelta(seconds=3600 * 7)
    return {
        'userid': user.id,
        'exp': exp
    }


def payload_to_user(payload):
    if not payload:
        return None
    userid = payload.get('userid')
    try:
        from users.models import User
        user = User.objects.get(id=userid)
    except:
        return None
    return user


# 自定义rest-framework验证器
class WechatUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not request.jwt_user:
            msg = u'用户不存在或用户未获得登录授权'
            raise exceptions.AuthenticationFailed(msg)
        return (request.jwt_user, None)
