#-*- coding: UTF-8 -*-
################################################################################
#
#Copyright (c) 2016 Baidu.com, Inc. All Right Reserved
#
#
#Message Worker For QA Platfrom
#
#Author:qiuqian(qiuqian01@baidu.com)
#Date:      2016/12/22
#func:      all 入口
##################################################################################
import MySQLdb
import sys
import json
import re
import logging
import os
import time
import chuli
from src_type import fugailv_ctrip
from src_type import fugailv_dp
from src_type import fugailv_ez
from src_type import fugailv_mfw
from src_type import fugailv_qy
from src_type import fugailv_ta

reload(sys)
sys.setdefaultencoding("utf-8")
'''
curpath = os.path.abspath('.')
logpath = curpath + '/../logs'
if not os.path.exists(logpath):
    os.mkdir(logpath)
outfile = curpath + '/../result/fugailv.txt'

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logpath + '/fugailv.log',
        filemode='a')
#date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
'''
def main(dic):
    #生成结果文件到result下的各个txt中
    fugailv_ctrip.main(dic)
    fugailv_dp.main(dic)
    fugailv_ez.main(dic)
    fugailv_mfw.main(dic)
    fugailv_qy.main(dic)
    fugailv_ta.main(dic)
    chuli.main(dic)

'''
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
        logging.error('execute sql :[' + sql + '] error : %s' % (e.message))
    finally:
        # 关闭数据库连接
        conn.close()
        '''
