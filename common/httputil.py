# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Config Utils For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import httplib2


def request(url, method, data):
    """
    发出http请求
    :param url: 请求url
    :param method: 请求方法
    :param data: 请求数据
    :return: 响应头, 响应体
    """
    # 获取HTTP对象
    h = httplib2.Http()

    # 发出同步请求，并获取内容
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    resp, content = h.request(url, method=method, body=data, headers=headers)
    return resp, content
