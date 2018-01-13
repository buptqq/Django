#-*- coding: UTF-8 -*-
################################################################################
#
#Copyright (c) 2016 Baidu.com, Inc. All Right Reserved
#
#
#Message Worker For QA Platfrom
#
#Author:qiuqian(qiuqian01@baidu.com)
#Date:      2016/12/19
#func:      各大行业详情覆盖率
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
outfile = curpath + '/fugailv_dp.txt'

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logpath + '/fugailv_dp.log',
        filemode='a')
#date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
def main(dic):
    countrys = dic['country']
    taskid = dic['taskid']
    global output
    output = open(outfile,'w')
    for country in countrys:
        sqls = [
            #"select city,category1,count(distinct basic.sid) from poi_basic_dp as basic inner join t_poi_dp as pic on basic.sid = pic.sid where city = '%s' group by city,category1" % country,
            "select city,category1,count(sid) from poi_basic_dp where city = '%s' group by category1" % country
            #"select city,category1,count(sid) form poi_basic_dp where city = '%s' and address is not NULL group by city,category1" % country,
            #"select city,category1,count(sid) form poi_basic_dp where city = '%s' and phone is not NULL group by city,category1" % country,
            #"select city,category1,count(sid) form poi_basic_dp where city = '%s' and overall_rating is not NULL group by city,category1" % (country),
            #"select city,category1,count(sid) form poi_basic_dp where city = '%s' and price is not NULL group by city,category1" % (country)    
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
        logging.debug('execute sql :[' + sql + ']')
        output.write('execute sql :[' + sql + ']' + '\n')
        # 执行sql语句
        cur.execute(sql)
        logging.debug('sql execute done !')
        res = cur.fetchallDict()
        for resline in res:
            #resline就是一个字典
    	    #print json.dumps(resline, encoding="UTF-8", ensure_ascii=False)
            temp = json.dumps(resline,encoding='utf-8',ensure_ascii=False)
            output.write(temp + '\n')  
        logging.debug(' ------------------data write into --%s-- success !' % output)
    except Exception as e:
        #logging.error('execute sql :[' + sql + ']')
        print e.message
    finally:
        # 关闭数据库连接
        conn.close()
if __name__ =='__main__':
    main({'country':['香港'],'taskid':1003})
