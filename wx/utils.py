# -*- coding: utf8 -*-

import hashlib
import base64
import json
import logging


from django.conf import settings as django_settings
import requests
# from Crypto.Cipher import AES

from common import chttp


logger = logging.getLogger(__name__)


def generate_token(openid, session_key):
    """根据openid， session_key生成token. Deprecated!该方法不再使用"""
    ori_string = "%s::%s" % (openid, session_key)
    m = hashlib.md5()
    m.update(ori_string.encode("utf-8"))
    return m.hexdigest()


def wxGetToken(appid, appsecret):
    host = "https://api.weixin.qq.com"
    path = '/cgi-bin/token'
    url = host + path
    payload = {
        "grant_type": 'client_credential',
        "appid": appid,
        "secret": appsecret
    }
    rsp = requests.get(url=url, params=payload, headers={"Content-type": "application/x-www-form-urlencoded"})
    data = json.loads(rsp.text)
    token = data.get("access_token")
    return token


def wxGetMiniCode(access_token, wx_page_path, qrcode_image_file):
    host = "https://api.weixin.qq.com"
    path = "/wxa/getwxacode?access_token=%s" % access_token
    url = host + path
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    payload = {
        "path": wx_page_path,  # 要跳转的微信页面的路径,必填不能为空，最大128字符, 示例中pages/index 需要在 app.json 的 pages 中定义
        "width": 430,  # 二维码的宽度
        "auto_color": False,  # 自动配置线条颜色，如果颜色依然是黑色，则说明不建议配置主色调
        "line_color": {"r": "0", "g": "0", "b": "0"},
        # auth_color 为 false 时生效，使用 rgb 设置颜色 例如 {"r":"xxx","g":"xxx","b":"xxx"},十进制表示
        "is_hyaline": False,  # 是否需要透明底色， is_hyaline 为true时，生成透明底色的小程序码
    }
    rsp = requests.post(url=url, data=json.dumps(payload), headers=headers)
    image_data = rsp.content  # bytes
    with open(qrcode_image_file, "wb") as f:
        f.write(image_data)
    return rsp.status_code


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        """
        :param encryptedData:
        :param iv:
        :return:
        {
            "phoneNumber": "13580006666",
            "purePhoneNumber": "13580006666",
            "countryCode": "86",
            "watermark":
            {
                "appid":"APPID",
                "timestamp": TIMESTAMP
            }
        }
        """
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
        print(decrypted)
        # if decrypted['watermark']['appid'] != self.appId:
        #     raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        res = s[:-ord(s[len(s) - 1:])]
        return res.decode("utf-8")


# 发送微信消息服务
def wxSendMsg(openid, page, form_id, template_name, **kwargs):
    data = {
        "touser": openid,
        "template_id": template_name,  # 模板ID
        "page": page,
        "form_id": form_id,
        "data": {**kwargs}
    }
    json_template = json.dumps(data)
    access_token = wxGetToken(django_settings.APP_ID, django_settings.APP_SECRET)

    url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + access_token

    respone = requests.post(url, data=json_template, timeout=50)
    # 拿到返回值
    errcode = respone.json().get("errcode")
    logger.info("消息通知发送openid=%s，form_id=%s,结果为%s" % (openid, form_id, respone.text))
    return errcode  # errcode等于0,模板消息发送成功"


# @calc_run_time(debug=django_settings.DEBUG)
def wxLogin(code):
    """
    使用 code 换取 openid 和 session_key 等信息
    :param code:
    :return:
    {
       "code": 200,
       "msg": "success",
       "ok": True,
       "data": {
            "openid": "xxx",
            "session_key": "xxx",
            "unionid": "xxx",
            "errcode": 0,  # 0 正常， -1系统繁忙， 40029 code无效，  45011  频率限制，每个用户每分钟100次
            "errmsg": "xxx" # 错误信息

       }
    }
    """
    host = "https://api.weixin.qq.com"
    path = '/sns/jscode2session'
    appid = django_settings.APP_ID
    appsecret = django_settings.APP_SECRET
    payload = {
      "grant_type": 'authorization_code',
      "appid": appid,
      "secret": appsecret,
      "js_code": code
    }
    Q = chttp.Base(host=host)
    rsp = Q.get(path=path, data=payload, headers={"Content-type": "application/x-www-form-urlencoded"})
    return rsp
