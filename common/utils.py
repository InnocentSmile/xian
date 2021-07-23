# -*- coding: utf8 -*-

import datetime
import copy
import logging
import os
import time
import functools

import requests
from xpinyin import Pinyin
from django.conf import settings as django_settings
from django.db import transaction




logger = logging.getLogger(__name__)


def create_or_update(model, uniq_condition, data_kwargs, enable_encrypt=False, encrypt_fields=list()):
    try:
        obj = getattr(getattr(model, "objects"), "get")(**uniq_condition)
        for key, value in data_kwargs.items():
            # if enable_encrypt:  # 允许对某些字段进行加密后存储
            #     if key in encrypt_fields:
            #         value_to_save = aes_encrypt(message=value, key=django_settings.AES_KEY, iv=django_settings.AES_IV)
            #     else:
            #         value_to_save = value
            # else:
            #     value_to_save = value
            value_to_save = value
            setattr(obj, key, value_to_save)
        obj.save()
    except model.DoesNotExist:
        obj = model(**data_kwargs)
        obj.save()


def update_with_lock(model, uniq_condition, data_kwargs, version_field, limit_field=None):
    """

    :param model:
    :param uniq_condition:
    :param data_kwargs:
    :param version_field: 指定版本检查的字段
    :param limit_field: 额外的限制条件， 比如对比库存值，比如要减少的数量大于库存值，则事务回滚， 默认为None
    :return: True or False

    """
    data_kwargs_copy = copy.deepcopy(data_kwargs)
    # 采用乐观锁+事务的模式更新数据, 可以指定版本检查的字段
    sid = transaction.savepoint()  # 开始事务
    try:
        obj = getattr(getattr(model, "objects"), "get")(**uniq_condition)
        first_value = getattr(obj, version_field)

        if limit_field:
            limit_field_value = data_kwargs_copy[limit_field]  # 要求limit field可比较的，且在data_kwargs之中
            new_limit_field_value = getattr(obj, limit_field) + limit_field_value  # 原始值加上要增加/减少的值，要减少的值要负数表示
            data_kwargs_copy.update({limit_field: new_limit_field_value})

        for key, value in data_kwargs_copy.items():
            setattr(obj, key, value)
        second_obj = getattr(getattr(model, "objects"), "get")(**uniq_condition)
        cur_value = getattr(second_obj, version_field)

        if limit_field:
            cur_limit_field_value = abs(getattr(second_obj, limit_field))
            if data_kwargs[limit_field] < 0:  # 传入的值为负数，说明是要减少库存值，要判断库存值是否足够
                if abs(data_kwargs[limit_field]) > cur_limit_field_value:  # 要求limit field可比较的，且在data_kwargs之中
                    logger.warning("%s(提交值为%s) 大于数据库现有值%s，不提交事务。" % (
                        limit_field, abs(data_kwargs[limit_field]), cur_limit_field_value))
                    transaction.savepoint_rollback(sid)
                    return False
                else:
                    pass
            else:
                pass
        else:
            pass

        if first_value == cur_value:  # 如果前后两次的值一致，说明数据没有被另外一个线程修改, 下一步可以提交更新了
            obj.save()
            transaction.savepoint_commit(sid)  # 成功更新，提交事务
            return True
        else:
            transaction.savepoint_rollback(sid)
            logger.warning("%s: 事务冲突（可能有另外一个线程正在修改表数据), 执行回滚操作" % model.__name__)
            return False
    except model.DoesNotExist:
        transaction.savepoint_rollback(sid)
        errmsg = "%s对象不存在%s" % (model.__name__, uniq_condition)
        logger.error(errmsg)
        return False


def shortUrlToLong(shorturl):
    r = requests.get(shorturl)
    if r.ok:
        return r.url
    else:
        return ""


def timestamp_to_datatime(value):
    format = '%Y-%m-%d %H:%m:%S'
    # format = '%Y-%m-%d %H:%M:%S'
    # value 为时间戳值,如:1460073600.0
    dt = datetime.datetime.fromtimestamp(value)
    return dt


def datetime_to_timestamp(dt):
    # time.strptime(dt,'%Y-%m-%d %H:%m:%s')
    # s = time.mktime(time.strptime(dt,'%Y-%m-%d %H:%M'))
    s = time.mktime(dt.timetuple())
    return int(s)


# def decrypt_info(crypted_value):
#     try:
#         decrypted_value = aes_decrypt(crypted_value, key=django_settings.AES_KEY, iv=django_settings.AES_IV)
#         return decrypted_value
#     except Exception as ex:
#         logger.warning("对字符串[%s]解密失败: %s" % (crypted_value, ex))
#         return crypted_value


def convert_to_pinyin(var_string):
    # 橡树  ->  xiangshu
    p = Pinyin()
    return p.get_pinyin(var_string, "")


def getCurrentSystemTime():
    return int(time.time()) * 1000


def datetime_to_ms_timestamp(dt):
    # time.strptime(dt,'%Y-%m-%d %H:%m:%s')
    # s = time.mktime(time.strptime(dt,'%Y-%m-%d %H:%M'))
    s = time.mktime(dt.timetuple())
    return int(s * 1000)


def msg_wrapper(msg, **extra_info):
    pypkg = extra_info.get("pypkg")
    wx_openid = extra_info.get("wx_openid")
    wrapped_msg = "[%s][%s]%s" % (pypkg, wx_openid, msg)
    return wrapped_msg


def rsp_wrapper(ok, code, msg, data):
    res = {
        "msg": msg,
        "code": code,
        "data": data,
        "ok": ok
    }
    return res


def store_wx_headimg(wx_headimg, wx_openid):
    if wx_headimg is None or wx_headimg == "null":  # 头像url为空时
        pass
    else:
        headimg_dir = os.path.join(django_settings.MEDIA_ROOT, "wx_headimg/").replace("\\", '/')
        headimg_file = os.path.join(headimg_dir, '%s.png' % wx_openid)
        if not os.path.exists(headimg_file):  # 如果不存在则保存文件到本地
            rsp = requests.get(wx_headimg)
            with open(headimg_file, "wb") as f:
                f.write(rsp.content)
            # 修改头像文件权限
            # os.chmod(headimg_file, stat.S_IROTH)
    return True


def to_local_wx_headimg(wx_headimg, wx_openid, use_reverse_proxy=False):
    """转换成本地的wx_headimg的url"""
    if use_reverse_proxy:  # 使用反向代理
        if wx_headimg is None or wx_headimg == "null":
            return django_settings.DOMAIN + "/static/images/anonymous_headimg.jpeg"
        else:
            return wx_headimg.replace("https://wx.qlogo.cn", "%s/wxServer" % django_settings.DOMAIN)
    else:
        # 返回本地缓存的微信头像的url
        if wx_headimg is None or wx_headimg == "null":
            return django_settings.CDN_DOMAIN + "/static/images/anonymous_headimg.jpeg"
        else:
            return django_settings.CDN_DOMAIN + "/media/wx_headimg/%s.png" % wx_openid


def calc_run_time(debug=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if debug:
                start = time.time()
                ret = func(*args, **kw)
                end = time.time()
                duration = end - start
                logger.info("运行函数%s, 花费了%s秒" % (func.__name__, duration))
            else:
                ret = func(*args, **kw)
            return ret

        return wrapper

    return decorator


def tuple_to_dict(tuple_data):
    return dict(tuple_data)


def mask_phone_number(phone_number):
    # 给手机号打码 131****4444
    return phone_number[:3] + '*' * 4 + phone_number[7:]
