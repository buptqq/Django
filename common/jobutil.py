# coding=utf8
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Job Utils For QA Platform.

Authors: maxun(maxun@baidu.com)
Date:    2016/12/08
"""
import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from common import timeutil

engine = create_engine('mysql://root:root@10.99.199.16:8778/platform_test', encoding="utf-8")
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = None
logger = logging.getLogger('appLogger')


class Job(Base):
    """
    Job类，orm对应job表
    """
    __tablename__ = 'evaluate_job'
    id = Column(Integer, primary_key=True)
    job_name = Column(String)
    func_id = Column(Integer)
    func_name = Column(String)
    status = Column(Integer)
    create_time = Column(Integer)
    update_time = Column(Integer)


def init_session():
    """
    初始化session
    :return:
    """
    global session
    session = Session()


def close_session():
    """
    关闭session
    :return:
    """
    global session
    session.close()


def get_job_by_name(job_name):
    """
    根据job名称得到job
    :param job_name: job名称
    :return:
    """
    job = session.query(Job).filter(Job.job_name == job_name).one()
    return job


def get_job_by_id(job_id):
    """
    根据id得到job
    :param job_id: job id
    :return:
    """
    job = session.query(Job).filter(Job.id == job_id).one()
    return job


def save_job(job):
    """
    保存job
    :param job: 需要保存的job
    :return:
    """
    try:
        session.add(job)
        session.commit()
    except Exception as e:
        logger.exception('Save job: %s failed!' % job.job_name)


def update_job_status_by_name(job_name, status):
    """
    根据job名称更新job状态
    :param job_name: job名称
    :param status: job状态
    :return:
    """
    init_session()
    job = get_job_by_name(job_name)
    job.status = status
    job.update_time = timeutil.get_current_timestamp()
    save_job(job)
    close_session()


def update_job_status_by_id(job_id, status):
    """
    根据job id更新job状态
    :param job_id: job id
    :param status: job状态
    :return:
    """
    init_session()
    job = get_job_by_id(job_id)
    job.status = status
    job.update_time = timeutil.get_current_timestamp()
    save_job(job)
    close_session()

