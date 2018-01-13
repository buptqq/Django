# coding:utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Time Utils For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import time


def get_current_timestamp():
    """
    得到当前时间戳（未指定时区）
    :return: 当前时间戳
    """
    timestamp = time.time()*1000
    return timestamp
