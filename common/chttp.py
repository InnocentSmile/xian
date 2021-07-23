# -*- coding: utf8 -*-

import datetime
import hashlib
import json

import requests
from django.core.serializers.json import DjangoJSONEncoder

from common.error_codes import CODE_OK, CODE_SERVER_ERROR, CODE_INVALID_PARAMS


class Base(object):
    def __init__(self, host, user="", password=""):
        self.host = host
        self.user = user
        self.password = password

    @staticmethod
    def __format_response(response: requests.Response):
        status_code = response.status_code
        if status_code != 200 or status_code != 201:
            return HTTPResponse(ok=False, body=response.text, status_code=status_code)
        return HTTPResponse(ok=True, body=response.text, status_code=status_code)

    def url(self, path):
        return '{}{}'.format(self.host, path)

    def get(self, path, data=None, headers=None, verify=False):
        """

        :param path:
        :param data:
        :param headers:
        :param verify: 默认不去校验https的证书
        :return:
        """
        url = self.url(path)
        if headers is None:
            headers = self.default_headers()
        if data is not None:
            params = self.update_data(data)
        else:
            params = None
        rsp = requests.get(url=url, params=params, headers=headers)
        return self.__format_response(response=rsp)

    def post(self, path, data=None, headers=None, verify=False):
        """

        :param path:
        :param data:
        :param headers:
        :param verify:  默认不去校验https的证书
        :return:
        """
        url = self.url(path)
        if headers is None:
            headers = self.default_headers()

        if data is not None:
            data = self.update_data(data)

        if isinstance(data, dict):
            data = json.dumps(data, cls=DjangoJSONEncoder)  # 引入DjangoJSONEncoder解决datetime序列化的问题
        rsp = requests.post(url=url, data=data, headers=headers, verify=verify)
        return self.__format_response(response=rsp)

    def patch(self, path, data=None, headers=None):
        url = self.url(path)
        if headers is None:
            headers = self.default_headers()

        if data is not None:
            data = self.update_data(data)

        if isinstance(data, dict):
            data = json.dumps(data, cls=DjangoJSONEncoder)  # 引入DjangoJSONEncoder解决datetime序列化的问题
        rsp = requests.patch(url=url, data=data, headers=headers)
        return self.__format_response(response=rsp)

    def default_headers(self):
        headers = {
        }
        return headers

    def update_data(self, data):
        """define specific logic according to different cases"""
        return data

    def sign(self, data):
        """different external api has different sign functions"""
        return ""

    @staticmethod
    def md5(ori_string):
        if isinstance(ori_string, str):
            m = hashlib.md5()
            m.update(ori_string.encode("utf-8"))
            return m.hexdigest()
        else:
            return ''


class HTTPResponse(object):
    def __init__(self, ok, body, status_code):
        if isinstance(body, dict):
            d = {"code": status_code, "msg": "", "data": body}
        if isinstance(body, list):
            d = {"code": status_code, "msg": "", "data": body}

        elif isinstance(body, (bytes, bytearray, str)):
            body = body.decode('utf-8') if isinstance(body, (bytes, bytearray)) else body
            try:
                _body = json.loads(body)
                if isinstance(_body, list):
                    d = {"code": status_code, "msg": "", "data": _body}

                else:
                    d = {"code": status_code, "msg": "", "data": _body}
            except Exception as ex:  # body 不能被json.load的情况
                d = {'code': CODE_OK, 'msg': '', 'data': body}

        else:
            d = {'code': CODE_SERVER_ERROR, 'msg': 'error return', 'data': {}}

        if str(status_code).startswith("4") or str(status_code).startswith("5"):
            d.update({"code": status_code})
        else:
            d.update({"code": CODE_OK})  # 只要不是4xx或者5xx错误，则认为是http请求正常

        self._body = d
        self._code = d.get('code', CODE_OK)
        self._msg = d.get('msg', '')
        self._data = d.get('data', {})
        self._ok = True if self.code == CODE_OK else False

    @property
    def ok(self):
        return self._ok

    @ok.setter
    def ok(self, ok):
        self._ok = ok

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body


InvalidParamsHttpResponse = HTTPResponse(ok=False,
                                         body={'code': CODE_INVALID_PARAMS, 'msg': 'invalid params', 'data': {}},
                                         status_code=500)
