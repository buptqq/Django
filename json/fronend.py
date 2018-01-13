#-*- coding: UTF-8 -*-
import json,MySQLdb
import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")
curpath = os.path.abspath('.')
outfile = curpath + '/jsonData.txt'
if not os.path.exists(outfile):
    os.system('touch %s' % outfile)

def tableToJson(sql):
    try:
        conn = MySQLdb.connect(
                host = "10.99.199.16",
                user = "root",
                passwd = "root",
                db = "platform_test",
                port = 8778)
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    except Exception as e:
        print "Mysql connect fail ,Exception is %s" % (e.message)
    finally:
        cur.execute(sql)
        data = cur.fetchallDict()
        jsonData = []
        for dic in data:
            jsonData.append(dic)
        return json.dumps(jsonData)

if __name__ == '__main__':
    sql = "select Countryname,PoiCount,Countryid,taskid from poicount where taskid = 1000"
    jsonData = tableToJson(sql)
    f = open(outfile,'w+')
    f.write(jsonData)
    f.close()
	
