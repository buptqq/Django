#-*- coding: UTF-8 -*- 
import MySQLdb
import sys
import json
import re
import logging
import os
import time

reload(sys)
sys.setdefaultencoding("utf-8")
#curpath = os.path.abspath('.')
#logpath = curpath + '/logs'
#if not os.path.exists(logpath):
#    os.mkdir(logpath)
#outfile = curpath + '/countpoi.txt'
#logging.basicConfig(level=logging.DEBUG,
#        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#        datefmt='%a, %d %b %Y %H:%M:%S',
#        filename=logpath + '/count_poi.log',
#        filemode='a')
date = time.localtime(time.time())
time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
def main(dic):
    countrys = dic['country']
    for country in countrys:
        sql = "select count(pid) from t_poi_res where city_id in (select cityid from area_qa where countryname = '%s')" % country
        execute(sql,country)

def execute():
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
        #logging.debug('execute sql :[' + sql + ']')
        # 执行sql语句
        sql = "select city_id,src_type,count(pid) from t_poi_basic where city_id in (select cityid from area_qa where countryname = '澳门特别行政区') group by src_type"
        cur.execute(sql)
        res = cur.fetchallDict()
        for i in res:
            print json.dumps(i,encoding='utf-8',ensure_ascii=False)
            for k in i:
                print k,i[k]       
            #print res[i]
            
        #logging.debug('sql execute done !')
        #res = cur.fetchall()
        #for resline in res:
    	#print json.dumps(resline, encoding="UTF-8", ensure_ascii=False)
        #print date
        #print time
        #sql = "insert into poicount (Countryname,PoiCount,Countryid,Time) values('%s',%d,%d,%s)" % ('澳门',50000,2911,time)
        #print json.dumps(sql,encoding="utf-8",ensure_ascii=False)
        #cur_out.execute(sql)
        #logging.debug('data write into --database-- success !' )
    #except:
        #logging.error('execute sql :[' + sql + ']')
    finally:
        conn_out.commit()
        conn_out.close()
        # 关闭数据库连接
        conn.close()
if __name__ == '__main__':
    execute()
