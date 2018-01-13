# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Demo App For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import os


def test(parameters):
    """
    Demo for function in module
    :param parameters:
    :return:
    """
    print 'test , parameters is: ' + str(parameters) + " pid is: " + str(os.getpid())


class TestClass(object):
    """
    Demo class
    """
    def __init__(self, test=''):
        self.test = test

    def test(self, parameters):
        """
        Demo method in class
        :param parameters:
        :return:
        """
        print 'TestClass.test , parameters is: ' + str(parameters) + ' , test is: ' + self.test
