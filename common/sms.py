#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oakvip.settings.local')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import django
# django.setup()  # django.setup() may only be called once.

from django.conf import settings as django_settings

import requests
import json


logger = logging.getLogger(__name__)

singleurl = 'https://sms.yunpian.com/v2/sms/single_send.json'


@task
def send_sms(apikey, mobile, text, **kwargs):
    """
    :param mobile:
    :param text:
    :param kwargs:
    :return: {'code': 0, 'msg': '发送成功', 'count': 4, 'fee': 0.2, 'unit': 'RMB', 'mobile': '15717929717', 'sid': 31679531708}
    """
    print(kwargs)

    parmas = {
        'apikey': apikey,
        'mobile': mobile,
        'text': text.format(**kwargs)
    }
    print("模板是:", text)
    print(parmas)
    reaponse = requests.post(singleurl, data=parmas)
    re_dict = json.loads(reaponse.text)
    # logger.info("发短信的一些信息=========", parmas)
    print(re_dict)

    return re_dict


if __name__ == '__main__':
    # APIKEY = "0a73328bcd095c656c41f8a5243f9396"
    mobile = "15717929717"
    # send_sms(mobile, django_settings.HOTEL_SUCCESS_TEMPLATE_TEXT,
    #          **{"hotel_name": "顺德喜来登酒店", "checkin_date": "2018年12月08号", "checkout_date": "2018年12月09号", "room_cnt": "1",
    #             "bed_type": "豪华城景大床房", "price": "299",
    #             "breakfast_type": "无早", "cn_name": "廖鸿胤",
    #             "confirm_num": "75401602"})
    # send_sms(django_settings.YUNPIAN_MARKET_API_KEY, mobile, django_settings.KK00_TEMPLATE_TEXT)

    # res = send_sms(django_settings.YUNPIAN_MARKET_API_KEY, mobile,
    #                django_settings.MILEAGE_START_TEMPLATE_TEXT,
    #                **{"wx_nickname": "zfdz", "mileage": 2000, "fraction": "1/3"})

    res = send_sms(django_settings.YUNPIAN_NORMAL_API_KEY, "17688784800",
                   "【橡树黑卡】尊敬的橡树黑卡会员何珍娣，您在1月9日预订的顺德喜来登酒店，1间豪华城景大床房于2月6日入住，2月7日退房；预订失败。如需变更房型请联系橡树黑卡微信客服或致电0755-33176698。感谢你对橡树黑卡的信任与支持。", )
