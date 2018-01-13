# coding:utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
String Utils For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import time
from urllib2 import quote


def get_current_time_str():
    """
    得到当前时间字符串
    :return: 年月日时分秒格式的时间字符串
    """
    timestr = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return timestr


def get_current_timestamp_str():
    """
    得到当前时间戳字符串
    :return: 字符串时间戳
    """
    timestr = str(time.time()*1000)
    return timestr


def urlencode(urlstr):
    """
    对目标串进行url编码
    :param urlstr: 待编码的字符串
    :return:
    """
    if isinstance(urlstr, unicode):
        return quote(urlstr.encode('utf8'))
    return quote(urlstr)


def get_class_name(name):
    """
    将下划线式写法的名称转换为驼峰式写法的类名（未使用）
    :param name: 下划线名称
    :return: 驼峰名称
    """
    names = name.split("_")
    class_name = names[0].capitalize() + names[1].capitalize()
    return class_name
