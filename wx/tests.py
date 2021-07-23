# -*- coding: utf8 -*-


import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oakvip.settings.dev')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django

django.setup()  # django.setup() may only be called once.

from django.test import TestCase

from django.conf import settings as django_settings

from wx.utils import *


class TestWxLogin(TestCase):
    def setUp(self):
        self.appid = django_settings.APP_ID
        self.appsecret = django_settings.APP_SECRET
        self.openid = "ouyWp5VXKMV-cw0yMKXmZDycF-90"
        self.page = "pages/index/index"
        self.form_id = "wx08110929038948953620fc243195288335"
        self.template_name = "jsWAygfJgWBsQXa1Y3-5FXlrXusMRuLRn4S7aJKvVt0"
        self.content_dict = {"keyword1": {"value": "顺德喜来登酒店"}, "keyword2": {"value": "2018年11月17日"},
                             "keyword3": {"value": "2018年11月18号"}, "keyword4": {"value": "若您入住受阻，请留言，客服将第一时间为您处理。"}}

    def tearDown(self):
        pass

    def test_get_token(self):
        token = wxGetToken(appid=self.appid, appsecret=self.appsecret)
        print(token)
        self.assertEqual(token, "xxx")

    def test_wx_send_msg(self):
        res = wxSendMsg.delay(self.openid, self.page, self.form_id, self.template_name, **self.content_dict)
        expected = 0
        self.assertEqual(res, expected)

    def test_get_wx_minicode(self):
        token = wxGetToken(django_settings.APP_ID, django_settings.APP_SECRET)
        qrcode_image_file = "/Users/hackstoic/Downloads/minicode_image_file.png"
        wx_page_path = "pages/about/about"
        res = wxGetMiniCode(token, wx_page_path, qrcode_image_file)
        print(res)

    def test_get_unionid(self):
        data = wxGetUnionId()
        print(data)
