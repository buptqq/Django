# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Path Utils For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import sys
import os

CONF_DIR_NAME = 'config'
LOG_DIR_NAME = 'logs'


def get_current_run_path():
    """
    得到当前运行的python文件所在的目录
    :return: 当前运行的python文件所在的目录
    """
    current_run_path = sys.path[0]
    return current_run_path


def get_current_code_path():
    """
    得到当前执行的代码块所在的目录
    :return: 当前执行的代码块所在的目录
    """
    current_code_path = os.path.split(os.path.realpath(__file__))[0]
    return current_code_path


def get_app_root_path():
    """
    得到当前app的根目录
    :return: 当前app的根目录
    """
    current_path = get_current_code_path()
    app_root = os.path.dirname(current_path)
    return app_root


def get_app_dir_path(dir_name):
    """
    得到app下指定目录名称的路径
    :param dir_name: 目录名称
    :return: app下目录名称路径
    """
    dir_path = None
    if dir_name:
        app_root = get_app_root_path()
        dir_path = os.path.join(app_root, dir_name)
    return dir_path


def get_app_file_path(dir_name, file_name):
    """
    得到app下指定目录、指定文件名的文件路径
    :param dir_name: 目录名
    :param file_name: 文件名
    :return: 文件路径
    """
    file_path = None
    if dir_name and file_name:
        dir_path = get_app_dir_path(dir_name)
        file_path = os.path.join(dir_path, file_name)
    return file_path


def get_config_path():
    """
    得到配置文件所在的目录
    :return: 配置文件所在的目录
    """
    config_path = get_app_dir_path(CONF_DIR_NAME)
    return config_path


def get_config_file_path(config_file_name):
    """
    根据配置文件名得到配置文件的路径
    :param config_file_name: 配置文件名
    :return: 配置文件路径
    """
    config_file_path = get_app_file_path(CONF_DIR_NAME, config_file_name)
    return config_file_path


def get_log_path():
    """
    得到日志文件所在的目录
    :return: 日志文件所在的目录
    """
    log_path = get_app_dir_path(LOG_DIR_NAME)
    return log_path


def get_log_file_path(log_file_name):
    """
    根据日志文件名得到日志文件的路径
    :param log_file_name: 日志文件名
    :return: 日志文件路径
    """
    log_file_path = get_app_file_path(LOG_DIR_NAME, log_file_name)
    return log_file_path
