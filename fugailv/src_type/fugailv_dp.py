#-*- coding: UTF-8 -*-
################################################################################
#
#Copyright (c) 2016 Baidu.com, Inc. All Right Reserved
#
#
#Message Worker For QA Platfrom
#
#Author:qiuqian(qiuqian01@baidu.com)
#Date:      2016/12/23
#func:      各大行业详情覆盖率dp
##################################################################################
import MySQLdb
import sys
import json
import re
import logging
import os
import time


def init():
    curpath = os.path.abspath('.')
    global output
    outfile = curpath + '/fugailv/result/fugailv_dp.txt'
    output = open(outfile,'w')
    global log
    log = logging.getLogger('fugailv')

def main(dic):
    init()
    countrys = dic['country']
    taskid = dic['taskid']
    for country in countrys:
        log.debug('----------------country:%s---src_type:dp------taskid:%d-----------' % (country,taskid))
        sqls = [
            "select city,category1,count(distinct basic.sid) from poi_basic_dp as basic inner join t_pic_dp as pic on basic.sid = pic.sid where city = '%s' group by city,category1" % country,
            "select city,category1,count(sid) from poi_basic_dp where city = '%s' group by city,category1" % country
,
            "select city,category1,count(sid) from poi_basic_dp where city = '%s' and address is not NULL group by city,category1" % country,
            "select city,category1,count(sid) from poi_basic_dp where city = '%s' and phone is not NULL group by city,category1" % country,
            "select city,category1,count(sid) from poi_basic_dp where city = '%s' and overall_rating is not NULL group by city,category1" % (country),
            "select city,category1,count(sid) from poi_basic_dp where city = '%s' and price is not NULL group by city,category1" % (country)    
            ]
        for sql in sqls:
            execute(sql,country,taskid)
    output.close()



def execute(sql,country,taskid):
    try:
        conn = MySQLdb.connect(
                host = "10.120.28.42",
                user = "readonly",
                passwd = "readonly",
                db = "etl",
                port = 3306)
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        log.debug('execute sql :[' + sql + ']')
        output.write('execute sql :[' + sql + ']' + '\n')
        # 执行sql语句
        cur.execute(sql)
        log.debug('sql execute done !')
        res = cur.fetchallDict()
        for resline in res:
            #resline就是一个字典
    	    #print json.dumps(resline, encoding="UTF-8", ensure_ascii=False)
            temp = json.dumps(resline,encoding='utf-8',ensure_ascii=False)
            output.write(temp + '\n')  
        log.debug(' ------------------data write into --%s-- success !' % output)
    except Exception as e:
        log.error('execute sql :[' + sql + '] error : %s' % (e.message))
    finally:
        # 关闭数据库连接
        conn.close()
