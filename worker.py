# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Message Worker For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/07
"""
from common import jsonutil
from common import message
from multiprocessing import Pool
from common import configutil
import logging
from config import logconf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

CONF = configutil.get_items_in_section('common.conf', 'WORKER')
# POOLSIZE = int(CONF['poolsize'])
# pool = Pool(POOLSIZE)
logger = logging.getLogger('appLogger')


def call_func_in_progress(command_message_json):
    """
    此函数子进程中调用。
    通过反射调用指定模块.类.方法或模块.函数
    （取决于command_message_json是否含有class_name）
    :param command_message_json:命令消息json串
    :return:
    """
    logger.debug(command_message_json)
    print command_message_json
    if command_message_json:
        command_message = jsonutil.json2object(command_message_json)#反序列化
        module_name = command_message.module_name
        if command_message.class_name:
            class_name = command_message.class_name
        else:
            class_name = ''
        func_name = command_message.func_name
        parameters = command_message.parameters
        module = __import__(module_name, fromlist=True)
        if class_name:
            instance = getattr(module, class_name)()
            instance_method = getattr(instance, func_name)
            instance_method(parameters)
        else:
            func = getattr(module, func_name)
            print func
            func(parameters)


def is_multiprocessing():
    """
    根据poolsize判断是否启用多进程模式
    :return: 是否多进程
    """
    if not CONF['poolsize']:
        return False
    if not CONF['poolsize'].isdigit():
        return False
    if not int(CONF['poolsize']) > 0:
        return False
    return True


def call_func(command_message_json):
    """
    使用进程池启动要执行的函数
    :param command_message_json: 命令消息json串
    :return:
    """
    logger.debug(command_message_json)
    if is_multiprocessing():
        pool.apply_async(call_func_in_progress, (command_message_json,))
    else:
        call_func_in_progress(command_message_json)


def callback(ch, method, properties, body):
    """
    消息回调
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    try:
        logger.debug(" [x] Received %r" % body)
        # time.sleep(body.count(b'.'))
        call_func(body)
        logger.debug(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.exception('Handle message: [%s] failed! Exception is: [%s]' % (body, e.message))


def receive_message():
    """
    接收指定队列消息(队列名及routing_key均为conf中的type)
    :return:
    """
    if not message.MessageQueue.channel:
        try:
            message.MessageQueue.init()
        except Exception as e:
            raise RuntimeError('Init mq connection failed!')
        # message.MessageQueue.init()
    message.MessageQueue.channel.exchange_declare(exchange=CONF['exchange'], type='direct')
    message.MessageQueue.channel.queue_declare(queue=CONF['type'], durable=True)
    message.MessageQueue.channel.queue_bind(exchange=CONF['exchange'],
                                            queue=CONF['type'], routing_key=CONF['type'])
    # print(' [*] Waiting for messages. To exit press CTRL+C')

    message.MessageQueue.channel.basic_qos(prefetch_count=1)
    message.MessageQueue.channel.basic_consume(callback, queue=CONF['type'])

    message.MessageQueue.channel.start_consuming()

if __name__ == '__main__':
    if is_multiprocessing():
        POOLSIZE = int(CONF['poolsize'])
        pool = Pool(POOLSIZE)
    receive_message()
    # call_func({'parameters':1,'module_name':'test','class_name':'','func_name':''})
