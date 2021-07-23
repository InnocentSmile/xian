# -*- coding: utf8 -*-

from django.test import TestCase

from django.conf import settings as django_settings

from common.sms import send_sms


class TestCommonUtils(TestCase):
    def setUp(self):
        self.mobile = "15717929717"
        self.template_text =  django_settings.HOTEL_SUCCESS_TEMPLATE_TEXT
        self.content_dict = {"hotel_name": "顺德喜来登酒店", "checkin_date": "2018年11月17日", "checkout_date": "2018年11月18号", "room_cnt": "1",
                "bed_type": "豪华城景大床房", "price": "299",
                "breakfast_type": "无早", "cn_name": "吴遥道",
                "confirm_num": "93254846"}

    def tearDown(self):
        pass

    def test_sms(self):
        res = send_sms(self.mobile, self.template_text,**self.content_dict)
        code = res["code"]
        expected = 0
        self.assertEqual(code, expected)
