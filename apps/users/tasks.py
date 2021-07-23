import datetime
import logging
from django.conf import settings as django_settings


from common.error_codes import CODE_OK, CODE_SERVER_ERROR, CODE_INVALID_PARAMS
from common.utils import create_or_update

from users.models import User, Session

logger = logging.getLogger(__name__)


def storeUserOpenid(wx_openid):
    # 保存openid到user表
    try:
        obj = User.objects.get(wx_openid=wx_openid)
    except User.DoesNotExist:
        obj = User(**{
            "wx_openid": wx_openid,
        })
        obj.save()
    return User.objects.get(wx_openid=wx_openid)


def storeWxSession(userid, session_key, token):
    # 保存session_key， openid， token到session表
    # Todo：前期token先存到数据库，后期考虑使用redis进行缓存优化
    t_expiration = datetime.date.today() + datetime.timedelta(hours=2)
    try:
        obj = Session.objects.get(userid=userid)
        obj.session_key = session_key
        obj.token = token
        obj.t_expiration = t_expiration
        obj.save()
    except Session.DoesNotExist:
        obj = Session(**{
            "userid": userid,
            "session_key": session_key,
            "token": token,
            "t_expiration": t_expiration
        })
        obj.save()
    return True


def updateUserInfoTask(**userinfo):
    userid = userinfo.get("userid")
    try:
        create_or_update(model=User, uniq_condition={"id": userid}, data_kwargs=userinfo)
        res = {"ok": True, "code": CODE_OK, "msg": "success", "data": userinfo}
        logger.info("更新用户信息成功, userid: %s" % userid)
    except Exception as ex:
        logger.error("更新用户信息失败, userid: %s ，报错原因%s" % (userid, ex))
        res = {"ok": False, "code": CODE_SERVER_ERROR, "msg": "success", "data": userinfo}
    return res
