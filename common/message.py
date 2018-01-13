# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Message Module For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import pika
from common import configutil


class CommandMessage(object):
    """
    命令消息类
    """
    def __init__(self, module_name=None, class_name=None, func_name=None,
                 parameters=None, job=None):
        """
        命令消息类构造方法
        :param module_name: 预执行python代码的模块名
        :param class_name: 预执行python代码的类名
        :param func_name: 预执行python代码的函数名
        :param parameters: 预执行python代码的参数
        :param job: 当前执行的job
        """
        self.module_name = module_name
        self.class_name = class_name
        self.func_name = func_name
        self.parameters = parameters
        self.job = job


class MessageQueue(object):
    """
    消息队列类
    """
    connection = None
    channel = None

    @staticmethod
    def init():
        """
        初始化消息队列
        :return: None
        """
        if (not MessageQueue.connection) or (not MessageQueue.channel):
            conf = configutil.get_items_in_section('common.conf', 'MESSAGE_QUEUE')
            credentials = pika.PlainCredentials(conf['user'], conf['password'])
            MessageQueue.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=conf['host'], credentials=credentials))
            MessageQueue.channel = MessageQueue.connection.channel()

    @staticmethod
    def close():
        """
        关闭消息队列连接
        :return: None
        """
        MessageQueue.channel.close()
        MessageQueue.connection.close()

    @staticmethod
    def send_message(exchange_name, routing_key, message):
        """
        向指定exchange发送指定routing_key的消息
        :param exchange_name: exchange名称
        :param routing_key: routing_key名称
        :param message: 消息内容
        :return: None
        """
        MessageQueue.channel.basic_publish(exchange=exchange_name,
                                           routing_key=routing_key, body=message)

# try:
#     MessageQueue.init()
# except Exception as e:
#     raise RuntimeError('init mq connection failed!')

