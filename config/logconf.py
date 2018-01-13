# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Logging Conf For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import logging
from logging import handlers
from common import pathutil
import os


# formatter
fmt = '[%(asctime)s] - [%(levelname)s] - [%(name)s] - [module: %(module)s] - ' \
      '[func: %(funcName)s] - %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
app_formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)


# handler
app_log_file_name = 'app_%s.log' % str(os.getpid())
app_log_file_path = pathutil.get_log_file_path(app_log_file_name)
app_handler = handlers.TimedRotatingFileHandler(app_log_file_path, when='D',
                                                backupCount=30, encoding='UTF-8')
app_handler.setFormatter(app_formatter)


# logger
app_logger = logging.getLogger('appLogger')
app_logger.propagate = 0
app_logger.setLevel(logging.DEBUG)
app_logger.addHandler(app_handler)
