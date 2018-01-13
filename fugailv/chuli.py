#-*- coding:UTF-8 -*-
################################################################################
#
#Copyright (c) 2016 Baidu.com, Inc. All Right Reserved
#
#
#Message Worker For QA Platfrom
#
#Author:qiuqian(qiuqian01@baidu.com)
#Date:      2016/12/19
#func:      数据整合
##################################################################################

from collections import Counter
import sys
import os
import json
import MySQLdb
import logging
import time




curpath = os.path.abspath('.')
logpath = curpath + '/logs'
if not os.path.exists(logpath):
    os.mkdir(logpath)

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logpath + '/fugailv.log',
        filemode='a')
#date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

#guojia = {}
hangye = {}
xiangqing = {}
global type
def main(dic):
    countrys = dic['country']
    taskid = dic['taskid']
    for country in countrys:
    #yFile = curpath + "/need_6_other_mafengwo_4city.txt"
        logging.debug('---------------begin tongji ctrip-----------------')
        yFile = curpath +'/fugailv/result/fugailv_ctrip.txt'
        tongji(yFile,country,'ctrip',taskid)
        logging.debug('-------------------ctrip done---------------------')

        logging.debug('-------------------begin tongji dp----------------')
        yFile = curpath +'/fugailv/result/fugailv_dp.txt'
        tongji(yFile,country,'dp',taskid)
        logging.debug('------------------dp done-------------------------')

        logging.debug('-------------------begin tongji ez----------------')
        yFile = curpath +'/fugailv/result/fugailv_ez.txt'
        tongji(yFile,country,'eztable',taskid)
        logging.debug('-------------------ez done----------------')

        logging.debug('-------------------begin tongji mfw----------------')
        yFile = curpath +'/fugailv/result/fugailv_mfw.txt'
        tongji(yFile,country,'mfw',taskid)
        logging.debug('-------------------mfw done----------------')

        logging.debug('-------------------begin tongji qy----------------')
        yFile = curpath +'/fugailv/result/fugailv_qy.txt'
        tongji(yFile,country,'qy',taskid)
        logging.debug('-------------------qy done----------------')

        logging.debug('-------------------begin tongji ta----------------')
        yFile = curpath +'/fugailv/result/fugailv_ta.txt'
        tongji(yFile,country,'ta',taskid)
        logging.debug('-------------------ta done----------------')

def tongji(yFile,country,src_type,taskid):
    try:
        fp = open(yFile,'r')
        for line in fp:
            if ('inner join' in line ) and ('execute' in line):
                type = '头图'
                continue
            elif ('execute' and 'address') in line:
                type = '地址'
                continue
            elif ('execute' and 'phone') in line:
                type = '电话'
                continue
            elif ('execute' and 'overall_rating') in line:
                type = '评分'
                continue
            elif ('execute' and 'price') in line:
                type = '价格'
                continue
            elif 'execute' in line:
                type = '全部'
                continue
            dic = eval(line)
            xiangqing.clear()
            if type == '头图':
                if dic['category1'] not in hangye.keys():
                    hangye[dic['category1']] = {}
                xiangqing[type] = dic['count(distinct basic.sid)']
                hangye[dic['category1']].update(xiangqing)
            else:
                if dic['category1'] not in hangye.keys():
                    hangye[dic['category1']] = {}
                xiangqing[type] = dic['count(sid)']
                hangye[dic['category1']].update(xiangqing)
            #全都保存在了行业这个字典里，{‘酒店’：{‘头图’：**，‘电话’：**}}这样
        execute(country,hangye,src_type,taskid)
        fp.close()
    except Exception as e:
        logging.error('-----------------tongji ERROR : %s--------------------' % e.message)

def execute(country,hangye,src_type,taskid):
    try:
        conn = MySQLdb.connect(
                host = "10.99.199.16",
                user = "root",
                passwd = "root",
                db = "platform_test",
                port = 8778)
        cur = conn.cursor()
        for key in hangye.keys():
            for key1 in hangye[key].keys():
                sql = "insert into platform_fugailv(Countryname,PoiCount,Time,taskid,src_type,type,category,rate) values('%s',%d,%s,%d,'%s','%s','%s','%s')" % (country,hangye[key][key1],time,taskid,src_type,key1,key,(str(round((float)(hangye[key][key1])/hangye[key]['全部'],4) * 100 ) + '%'))
                cur.execute(sql)
        logging.debug('--------------------------data write into platform_fugailv success!------------------------')
    except Exception as e:
        logging.error('execute sql + [' + sql + '] -----------------%s--------------' % (e.message))
    finally:
        conn.commit()
        conn.close()







'''
        if type == '头图':
            if dic['city'] not in guojia.keys():
                guojia[dic['city']] = {}
            if dic['category1'] not in guojia[dic['city']].keys():#行业没在
                guojia[dic['city']][dic['category1']] = {}
            xiangqing[type] = dic['count(distinct basic.sid)']#头图：5
            guojia[dic['city']][dic['category1']].update(xiangqing)
        else:
            if dic['city'] not in guojia.keys():
                guojia[dic['city']] = {}
            if dic['category1'] not in guojia[dic['city']].keys():#添加新行业，之前的详情就要清零
                guojia[dic['city']][dic['category1']] = {}
            xiangqing[type] = dic['count(sid)']#详情数量
            guojia[dic['city']][dic['category1']].update(xiangqing)
    i=1
    j=1
    for key in guojia.keys():
        table.write(i,j,key)
        for key1 in guojia[key].keys():
            k = j
            i += 1
            table.write(i,j,key1)
            j += 1
            for key2,value in guojia[key][key1].items():
                table.write(i,j,key2)
                table.write(i,j+1,value)
                table.write(i,j+2,str(round(((float)(guojia[key][key1][key2])/guojia[key][key1]['全部']),4) * 100) + '%')
                i += 1
            j = k
    fp.close()
'''
