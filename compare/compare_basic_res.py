#-*- coding: UTF-8 -*-
################################################################################
#
#Copyright (c) 2016 Baidu.com, Inc. All Right Reserved
#
#
#Message Worker For QA Platfrom
#
#Author:qiuqian(qiuqian01@baidu.com)
#Date:      2016/12/21
#func:      竞品对比-来源分布（线上数据中分来源对比）
##################################################################################

import MySQLdb
import sys
import json
import re
import logging
import os
import time

reload(sys)
sys.setdefaultencoding("utf-8")
curpath = os.path.abspath('.')
logpath = curpath + '/logs'
if not os.path.exists(logpath):
    os.mkdir(logpath)
outfile = curpath + '/compare_basic_res.txt'
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logpath + '/compare_basic_res.log',
        filemode='a')
#date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
def main(dic):
    countrys = dic['country']
    taskid = dic['taskid']
    for country in countrys:
        sql = "select city_id,src_type,std_tag,count(pid) from t_poi_basic where uid in (select uid2bid.uid from t_poi_res as res left join uid2bid on (res.uid = uid2bid.bid) where city_id in (select cityid from area_qa where countryname = '%s')) and std_tag not like 'zt_%%' group by src_type,std_tag" % country
        execute(sql,country,taskid)
        sql = "select city_id,sub_src,std_tag,count(pid) from t_poi_basic where uid in (select uid2bid.uid from t_poi_res as res left join uid2bid on (res.uid = uid2bid.bid) where city_id in (select cityid from area_qa where countryname = '%s')) and sub_src = 'dianping' group by std_tag" % country
        execute_sub(sql,country,taskid)


def execute(sql,country,taskid):
    try:
        conn = MySQLdb.connect(
                host = "10.67.52.23",
                user = "root",
                passwd = "root",
                db = "ns_map_data_new",
                port = 3306)
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        conn_out = MySQLdb.connect(
                host = "10.99.199.16",
                user = "root",
                passwd = "root",
                db = "platform_test",
                port = 8778)
        cur_out = conn_out.cursor(cursorclass = MySQLdb.cursors.DictCursor)#返回值是一个字典
        logging.debug('execute sql :[' + sql + ']')
        # 执行sql语句
        cur.execute(sql)
        logging.debug('sql execute done !')
        res = cur.fetchallDict()
        for resline in res:
            #resline就是一个字典
    	    #print json.dumps(resline, encoding="UTF-8", ensure_ascii=False)
            push = "insert into platform_compare_basic_res (Countryname,PoiCount,Cityid,Time,taskid,src_type,std_tag) values('%s',%d,%d,%s,%d,'%s','%s')" % (country,resline['count(pid)'],resline['city_id'],time,taskid,resline['src_type'],resline['std_tag'])
            cur_out.execute(push)
            #logging.debug('----------------push into Mysql-%s-------------' % (push))
        logging.debug(' -------src_type-------    data write into --database-- success !' )
    except:
        logging.error('execute sql :[' + sql + ']')
    finally:
        conn_out.commit()
        conn_out.close()
        # 关闭数据库连接
        conn.close()

def execute_sub(sql,country,taskid):
    try:
        conn = MySQLdb.connect(
                host = "10.67.52.23",
                user = "root",
                passwd = "root",
                db = "ns_map_data_new",
                port = 3306)
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        conn_out = MySQLdb.connect(
                host = "10.99.199.16",
                user = "root",
                passwd = "root",
                db = "platform_test",
                port = 8778)
        cur_out = conn_out.cursor(cursorclass = MySQLdb.cursors.DictCursor)#返回值是一个字典
        logging.debug('execute sql :[' + sql + ']')
        # 执行sql语句
        cur.execute(sql)
        logging.debug('sql execute done !')
        res = cur.fetchallDict()
        for resline in res:
            #resline就是一个字典
    	    #print json.dumps(resline, encoding="UTF-8", ensure_ascii=False)
            push = "insert into platform_compare_basic_res (Countryname,PoiCount,Cityid,Time,taskid,src_type,std_tag) values('%s',%d,%d,%s,%d,'%s','%s')" % (country,resline['count(pid)'],resline['city_id'],time,taskid,resline['sub_src'],resline['std_tag'])
            cur_out.execute(push)
            #logging.debug('---------------push into Mysql-%s----------' % (push))
        logging.debug(' -----sub_src------    data write into --database-- success !' )
    except:
        logging.error('execute sql :[' + sql + ']')
    finally:
        conn_out.commit()
        conn_out.close()
        # 关闭数据库连接
        conn.close()

