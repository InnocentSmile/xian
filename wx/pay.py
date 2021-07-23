# # -*- coding: utf8 -*-
#
# import logging
# import hashlib
# import time
# import json
# import uuid
# import xml.etree.ElementTree as ET
#
# import requests
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# from django.conf import settings as django_settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# from backend.utils import genOrderNo, getOrderTypeCode, getProductPrice
# from backend.tasks import initNewMemberTask, upgradeMemberLevelTask, phonebillChargeGetBonusTask, createWxPayTicket, \
#     updateUserBenefitPoint
# from backend.models import Order, User, WxForm
# from promo.models import M1, RelM1M2, Activity, Mission, M2
# from promo.tasks import initNewMemberFromPromoTask, handle_inviteRewardTask, pushForwardTask, handle_aiqiyi_reward_task
# from common.error_codes import CODE_OK
# from common.utils import getModelObj, create_or_update, decrypt_info
# from tools.get_formid import get_form_id
# from wx.utils import wxSendMsg
#
# logger = logging.getLogger(__name__)
#
#
# def request(url, data):
#     '''
#     请求
#     :param url:
#     :param data:
#     :return:
#     '''
#     rsp = requests.post(url, data, headers={'Content-Type': 'application/xml'})
#     return rsp.text
#
#
# def get_nonce_str():
#     '''
#     获取随机字符串
#     :return:
#     '''
#     return str(uuid.uuid4()).replace('-', '')
#
#
# def dict_to_xml(dict_data):
#     '''
#     dict to xml
#     :param dict_data:
#     :return:
#     '''
#     xml = ["<xml>"]
#     for k, v in dict_data.items():
#         xml.append("<{0}>{1}</{0}>".format(k, v))
#     xml.append("</xml>")
#     return "".join(xml)
#
#
# def xml_to_dict(xml_data):
#     '''
#     xml to dict
#     :param xml_data:
#     :return:
#     '''
#     xml_dict = {}
#     root = ET.fromstring(xml_data)
#     for child in root:
#         xml_dict[child.tag] = child.text
#     return xml_dict
#
#
# class WxPay(object):
#
#     def __init__(self, merchant_key, *args, **kwargs):
#         self.url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
#         self.merchant_key = merchant_key
#         self.pay_data = kwargs
#         super(WxPay, self).__init__()
#
#     def create_sign(self, pay_data):
#         '''
#         生成签名
#         :return:
#         '''
#         stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
#         stringSignTemp = '{0}&key={1}'.format(stringA, self.merchant_key)
#         sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
#         return sign.upper()
#
#     def get_pay_info(self):
#         '''
#         获取支付信息
#         :param xml_data:
#         :return:
#         '''
#         sign = self.create_sign(self.pay_data)
#         self.pay_data['sign'] = sign
#         xml_data = dict_to_xml(self.pay_data)
#         response = request(url=self.url, data=xml_data.encode("utf-8"))
#         if response:
#             prepay_id = xml_to_dict(response).get('prepay_id')
#             paySign_data = {
#                 'appId': self.pay_data.get('appid'),
#                 'timeStamp': str(int(time.time())),
#                 'nonceStr': self.pay_data.get('nonce_str'),
#                 'package': 'prepay_id={0}'.format(prepay_id),
#                 'signType': 'MD5'
#             }
#             paySign = self.create_sign(paySign_data)
#             paySign_data.pop('appId')
#             paySign_data['paySign'] = paySign
#             return paySign_data
#         return False
#
#
# @csrf_exempt
# @api_view(["POST"])
# def createWxpay(request):
#     '''
#     请求支付
#     :return:
#     '''
#     paytype = request.POST.get("paytype")  # 订单类型
#     payinfo = request.POST.get("payinfo")
#     # wx_openid = request.POST.get("wx_openid")
#     wx_openid = request.jwt_user.wx_openid
#     order_name = request.POST.get("order_name", paytype)  # 商品描述
#     attach = "暂无内容"  # 附加信息, 待定, 但是不能为"", 否则微信支付时会报INVALID错误
#     trade_type = 'JSAPI'  # 交易类型
#     try:
#         kwargs = json.loads(payinfo)
#         total_fee = getProductPrice(paytype, **kwargs)  # 总金额
#         order_type_code = getOrderTypeCode(paytype, **kwargs)
#         order_number = genOrderNo(order_type_code=order_type_code)
#     except Exception as ex:
#         logger.error(ex)
#         logger.error("用户(%s)微信下单失败，订单类型有误： 商品%s, 附加信息%s" % (wx_openid, paytype, payinfo))
#         return Response(data={'code': 40001, 'msg': '下单失败，订单类型有误', 'data': {}, 'ok': False})
#     data = {
#         'appid': django_settings.APP_ID,
#         'mch_id': django_settings.MCH_ID,
#         'nonce_str': get_nonce_str(),
#         'body': order_name,  # 商品描述
#         'out_trade_no': order_number,  # 商户订单号
#         'total_fee': total_fee,
#         'spbill_create_ip': django_settings.SPBILL_CREATE_IP,
#         'notify_url': django_settings.NOTIFY_URL,
#         'attach': attach,
#         'trade_type': trade_type,
#         'openid': wx_openid
#     }
#     logger.info(data)
#     wxpay = WxPay(django_settings.MERCHANT_KEY, **data)
#     pay_info = wxpay.get_pay_info()
#     logger.info(pay_info)
#     if pay_info:
#         pay_info.update({"orderNo": order_number})
#         try:
#             prepay_id = pay_info["package"].split("=")[1]
#         except:
#             prepay_id = None
#         createWxPayTicket(wx_openid=wx_openid, order_number=order_number, order_name=order_name,
#                           total_fee=total_fee, paytype=paytype, payinfo=payinfo, status="unpaid", prepay_id=prepay_id)
#         logger.info(
#             "用户(%s)微信下单成功： 商品%s, 附加信息%s, 价格%s元, 订单号%s" % (wx_openid, paytype, payinfo, total_fee / 100, order_number))
#         return Response(data={'code': CODE_OK, 'msg': '下单成功', 'data': pay_info, 'ok': True})
#     else:
#         logger.error("用户(%s)微信下单失败： 商品%s, 附加信息%s, 价格%s, 订单号%s" % (wx_openid, paytype, payinfo, total_fee, order_number))
#         return Response(data={'code': 40001, 'msg': '下单失败', 'data': {}, 'ok': False})
#
#
# @csrf_exempt
# def wxpayNotify(request):
#     '''
#     支付回调通知， 当微信支付成功后通知该接口
#     :return:
#     '''
#     if request.method == 'POST':
#         try:
#             rsp_data = xml_to_dict(request.body)
#             return_code = rsp_data.get("return_code")
#         except Exception as e:
#             logger.error("微信回调解析。。。。" + str(e))
#             logger.error(request.body)
#             rsp_data = None
#             return_code = 'FAILED'
#         if return_code == "SUCCESS":
#             # Todo 到微信后台查询一下订单是否存在，如果不存在，则直接return。 防止恶意用户模拟微信回调。
#             logger.info("微信支付成功， 返回数据: %s" % rsp_data)
#             # 调用初始化会员信息接口
#             wx_openid = rsp_data.get("openid")
#             order_number = rsp_data.get("out_trade_no")
#             res = getModelObj(Order, {"order_number": order_number})
#             if res.get("ok"):
#                 order_obj = res["data"]
#             else:
#                 return res
#             if order_obj:
#                 # 微信支付成功回调将 order_obj.prepay_id 存入formid中
#                 data = {
#                     "wx_openid": wx_openid,
#                     "form_id": order_obj.prepay_id,
#                     "times": 3,
#                     "source": "微信支付回调"
#                 }
#                 try:
#                     create_or_update(WxForm, {"wx_openid": wx_openid, "form_id": order_obj.prepay_id}, data)
#                 except:
#                     pass
#                 if order_number.startswith("KK"):  # 开卡订单
#                     logger.info("开卡订单，正在初始化会员信息...")
#                     card_type = order_obj.type
#                     try:
#                         _payinfo = order_obj.payinfo
#                         payinfo = json.loads(_payinfo)
#                         invite_id = payinfo.get("invite_id")
#                         source = payinfo.get("source")  # 新用户开卡入口或者来源
#                     except Exception as ex:
#                         logger.warning("获取和反序列化订单的payinfo出错: %s" % ex)
#                         invite_id = None
#                         source = None
#                     if source in ["xcx_ticket_m2", "xcx_ticket_m1"]:  # 从m2页面开通的时候会附加给m1用户送里程， 或者m1开通会员时
#                         res = initNewMemberFromPromoTask(wx_openid, card_type, invite_id, source)
#                     else:
#                         res = initNewMemberTask(wx_openid, card_type)
#                         if source == 'invite_friends':
#                             handle_inviteRewardTask(wx_openid, invite_id, activity_name=source)
#
#                     order_name = django_settings.PRODUCT_INFOS[card_type]["name"]
#                     if res.get("ok"):  # 更新微信订单的状态，初始化会员直接返回结果
#                         order_obj.status = "success"
#                         order_obj.name = order_name
#                         order_obj.save()
#                         if source and source.startswith("aiqiyi"):
#                             handle_aiqiyi_reward_task(order_type=order_obj.type, wx_openid=wx_openid)
#                     else:
#                         logger.error(res)
#                         order_obj.status = "failed"
#                         order_obj.desc = res["msg"]
#                         order_obj.name = order_name
#                         order_obj.save()
#                 elif order_number.startswith("UP"):  # 升级订单
#                     logger.info("升级订单，正在更新会员信息...")
#                     card_type = order_obj.type
#                     order_name = django_settings.PRODUCT_INFOS[card_type]["name"]
#                     try:
#                         _payinfo = order_obj.payinfo
#                         payinfo = json.loads(_payinfo)
#                         invite_id = payinfo.get("invite_id")
#                         source = payinfo.get("source")  # 新用户开卡入口或者来源
#                     except Exception as ex:
#                         logger.warning("获取和反序列化订单的payinfo出错: %s" % ex)
#                         invite_id = None
#                         source = None
#                     if source in ["xcx_ticket_m2", "xcx_ticket_m1"]:  # 从m2页面开通的时候会附加给m1用户送里程， 或者m1开通会员时
#                         res = initNewMemberFromPromoTask(wx_openid, card_type, invite_id, source, upgrade=True)
#                     else:
#                         res = upgradeMemberLevelTask(wx_openid, card_type)
#                         if source == 'invite_friends':
#                             handle_inviteRewardTask(wx_openid, invite_id, activity_name=source)
#                     if res.get("ok"):  # 更新微信订单的状态
#                         order_obj.status = "success"
#                         order_obj.name = order_name
#                         order_obj.save()
#                         if source and source.startswith("aiqiyi") or order_obj.type == "UP01-02":
#                             handle_aiqiyi_reward_task(order_type=order_obj.type, wx_openid=wx_openid)
#                     else:
#                         order_obj.status = "failed"
#                         order_obj.desc = res["msg"]
#                         order_obj.name = order_name
#                         order_obj.save()
#                 elif order_number.startswith("PB"):  # 话费充值订单
#                     logger.info("话费充值订单，正在为的用户充值话费...")
#                     product = order_obj.type
#                     payinfo = order_obj.payinfo
#                     try:
#                         payment = django_settings.PRODUCT_INFOS[product]["price"]
#                         order_name = django_settings.PRODUCT_INFOS[product]["name"]
#                         deserialized_payinfo = json.loads(payinfo)
#                         phone_number = deserialized_payinfo["phone_number"]
#                         payment = int(payment)
#                         phonebillChargeGetBonusTask(phone_number=phone_number, payment=payment, wx_openid=wx_openid,
#                                                     order_number=order_number)
#                         # 这里要重新获取新的订单对象， 否则会把旧对象的信息会把新的订单信息覆盖
#                         res = getModelObj(Order, {"order_number": order_number})
#                         order_obj = res["data"]
#                         order_obj.name = order_name
#                         order_obj.type = "phonebill"  # type原有的类型是paytype，比如phonebill_of_50之类, 这里更新type统一为phonebill，主要是方便后统计话费等
#                         order_obj.status = "paid"  # 支付成功
#                         order_obj.source = "微信支付"
#                         order_obj.save()
#                         # 结果需要以第三方充值结果为准，等待回调更新
#                     except Exception as ex:
#                         logger.error("参数有误，无法正常为用户充值话费, err: %s" % ex)
#                 elif order_number.startswith("HT"):  # 酒店订单
#                     logger.info("酒店订单，正在为的用户更新预订记录...")
#                     # 这里要重新获取新的订单对象， 否则会把旧对象的信息会把新的订单信息覆盖
#                     payinfo = order_obj.payinfo
#                     res = getModelObj(Order, {"order_number": order_number})
#                     order_obj = res["data"]
#                     # order_obj.name = "预订酒店"
#                     order_obj.type = "hotel"  # 原有类型为HT1#1的方式，这里的type统一修改为hotel，方便后期进行检索
#                     order_obj.status = "confirming"  # 修改状态 待支付 -->  确认中
#                     order_obj.save()
#                     # 更新用户权益点数, 预订了几间夜，就用掉几个点数，如果订单关闭了，则点数退回
#                     kwargs = json.loads(payinfo)
#                     stay_days = kwargs.get("stay_days")
#                     room_cnt = kwargs.get("room_cnt")
#                     point_change = -(int(stay_days) * int(room_cnt))
#                     updateUserBenefitPoint(wx_openid=wx_openid, benefit="hotel", point_change=point_change)
#                 elif order_number.startswith("JF"):  # 集福订单
#                     try:
#                         _payinfo = order_obj.payinfo
#                         # 只存邀请码，activity_name和mission_name 默认为{"invite_id":"jifu-xxxxxx"}
#                         payinfo = json.loads(_payinfo)
#                         invite_id = payinfo.get("invite_id")
#                         user = User.objects.get(wx_openid=wx_openid)
#                         m1_obj = M1.objects.get(invite_id=invite_id)
#                         m1_user = User.objects.get(id=m1_obj.user_id)
#                         # 保存m2   存入m1和m2关系  m1 奖励加1
#                         pushForwardTask(m2_wx_openid=wx_openid, invite_id=invite_id, activity_name="jifu")
#                         order_obj.status = "success"
#                         order_obj.save()
#                         # M1第一次参加活动,微信通知和短信通知
#                         try:
#                             #### 给m2发微信通知
#                             page = "/pages/assemble-m2/assemble-m2?activity_name=jifu&mission_name=jifu"
#                             # 取完formid  可用次数减1
#                             formid = get_form_id(wx_openid)
#
#                             content_dict = {
#                                 "keyword1": {"value": "你已帮好友%s集福成功！" % m1_user.wx_nickname},
#                                 "keyword2": {"value": "好友回送了你1次全国高铁贵宾休息厅，春运不再拥挤，限时免费，快来领取吧！"}
#                             }
#                             errorcode = wxSendMsg.delay(wx_openid, page, formid, django_settings.WX_JF_HELP_TO_M2,
#                                                   **content_dict)
#                             logger.info("m2助力成功给m2发微信通知完毕errorcode为0则发送成功,目前errorcode为" + str(errorcode))
#                             #### 给m1发微信通知
#                             page = "/pages/assemble-m2/assemble-m2?activity_name=jifu&mission_name=jifu"
#                             # 取完formid  将其可用次数减一
#                             formid = get_form_id(m1_user.wx_openid)
#
#                             phone_number = decrypt_info(user.phone_number)
#                             phone_number = phone_number[:3] + '*' * 4 + phone_number[7:]
#                             content_dict = {
#                                 "keyword1": {"value": phone_number},
#                                 "keyword2": {"value": "哇，你人缘超好！你的好友帮你助力了一次，距离领取免费高铁贵宾厅又近了一步！快去看看领取进度呗！"}
#                             }
#                             errorcode = wxSendMsg.delay(m1_user.wx_openid, page, formid, django_settings.WX_JF_HELP_TO_M1,
#                                                   **content_dict)
#                             logger.info("m2助力成功给m1发微信通知完毕errorcode为0则发送成功,目前errorcode为" + str(errorcode))
#                             # print("**************M1第一次参加活动微信通知完毕")
#                         except Exception as e:
#                             errmsg = "m2助力成功,微信通知和短信通知" + str(e)
#                             logger.warning(errmsg)
#
#                     except Exception as e:
#                         logger.error("集福订单微信回调处理发生异常%s" % e)
#
#                     pass
#                 else:
#                     pass
#
#             else:
#                 pass
#             result_data = {
#                 'return_code': 'SUCCESS',
#                 'return_msg': 'OK'
#             }
#             return HttpResponse(dict_to_xml(result_data), content_type="application/xml")
#         else:
#             logger.error("微信支付失败, 返回数据: %s" % rsp_data)
