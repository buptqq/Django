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
import ConfigParser
import os
from common import pathutil


def get_config_parser(config_file_name):
    """
    根据配置文件名得到ConfigParser对象
    :param config_file_name: 配置文件名
    :return: ConfigParser对象
    """
    if not config_file_name:
        raise RuntimeError('Config file name: [' + config_file_name + '] is null!')
    config_file_path = pathutil.get_config_file_path(config_file_name)
    if config_file_path and os.path.exists(config_file_path):
        conf = ConfigParser.SafeConfigParser()
        conf.read(config_file_path)
        return conf
    else:
        raise RuntimeError('Config file: [%s] not exists!' % config_file_path)


def get_config_value(config_file_name, section, option, allow_null=False):
    """
    根据配置文件名及指定的配置节和选项得到配置项
    :param config_file_name: 配置文件名
    :param section: 配置节
    :param option: 选项
    :param allow_null: 是否允许为空（如不允许，且配置项为空，将抛出异常）
    :return: 配置项
    """
    conf = get_config_parser(config_file_name)
    value = conf.get(section=section, option=option)
    if not value and not allow_null:
        raise RuntimeError('Config: [%s][%s] in file: [%s] is null!'
                           % (section, option, config_file_name))
    return value


def __get_conf(conf, section, option):
    value = conf.get(section=section, option=option)
    return value


def __get_conf_not_null(conf, section, option, config_file_name='NO_FILE'):
    value = conf.get(section=section, option=option)
    if not value:
        raise RuntimeError('get config: [%s][%s] in file: [%s] failed!'
                           % (section, option, config_file_name))
    return value


def check(section, option, value, allow_null_options):
    """
    根据配置节、选项及是允许为空选项列表，检查配置项合法性
    :param section: 配置节
    :param option: 选项
    :param value: 配置项
    :param allow_null_options: 允许为空选项列表
    :return: 配置项合法性
    """
    if not value and (section, option) not in allow_null_options:
        return False
    return True


def get_items_in_section(config_file_name, section, allow_null_options=None):
    """
    根据配置文件名，配置节得到该节下所有配置项
    :param config_file_name: 配置文件名
    :param section: 配置节
    :param allow_null_options: 允许为空的选项列表（格式[(section,option),...]，如存在选项为空，且不在允许为空列表中，则抛出异常）
    :return: 配置项字典（dict[option]）
    """
    if not allow_null_options:
        allow_null_options = []
    conf = get_config_parser(config_file_name)
    item_dicts = {}
    items = conf.items(section)
    for option, value in items:
        item_dicts[option] = value
        valid = check(section, option, value, allow_null_options)
        if not valid:
            raise RuntimeError('Config: [%s][%s] in file: [%s] is null!'
                               % (section, option, config_file_name))
    return item_dicts


def get_specified_items(config_file_name, specified_options, allow_null_options=None):
    """
    根据配置文件名及指定的配置节和选项，得到配置项
    :param config_file_name: 配置文件名
    :param specified_options: 指定的配置节和选项（格式[(section, option)]）
    :param allow_null_options: 允许为空列表（格式[(section, option)]，如存在选项为空，且不在允许为空列表中，则抛出异常）
    :return: 配置项字典(dict[section][option])
    """
    if not allow_null_options:
        allow_null_options = []
    conf = get_config_parser(config_file_name)
    item_dicts = {}
    for section, option in specified_options:
        if section not in item_dicts:
            item_dicts[section] = {}
        item_dicts[section][option] = conf.get(section=section, option=option)
        valid = check(section, option, item_dicts[section][option], allow_null_options)
        if not valid:
            raise RuntimeError('Config: [%s][%s] in file: [%s] is null!'
                               % (section, option, config_file_name))
    return item_dicts


