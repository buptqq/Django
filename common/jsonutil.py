# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Json Utils For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import json
import logging
logger = logging.getLogger('appLogger')


def object2dict(obj):
    """
    转换对象到字典
    :param obj: 待转换的对象
    :return: 转换对象得到的字典
    """
    d = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
    d.update(obj.__dict__)
    return d


def dict2object(d):
    """
    字典转换为对象
    :param d: 待转换的字典
    :return: 转换字典得到的对象
    """
    # convert dict to object
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name, fromlist=True)
        # print 'the module is:', module
        class_ = getattr(module, class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items())  # get args
        # print 'the atrribute:', repr(args)
        inst = class_(**args)  # create new instance
    else:
        inst = d
    return inst


def object2json(obj):
    """
    对象转换为json串
    :param obj: 待转换的对象
    :return: 转换对象得到的json串
    """
    obj_json = None
    try:
        obj_dict = object2dict(obj)
        obj_json = json.dumps(obj_dict)
    except Exception as e:
        logger.exception("Convert obj to json failed!The exception is: %s" % e.message)
    return obj_json


def json2object(obj_json):
    """
    json串转换为对象
    :param obj_json: 待转换的json串
    :return: 转换json串得到的对象
    """
    obj = None
    try:
        obj_dict = json.loads(obj_json)
        obj = dict2object(obj_dict)
    except Exception as e:
        logger.exception("Convert json to obj failed!The exception is: " % e.message)
    return obj
