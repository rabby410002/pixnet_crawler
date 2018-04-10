# -*- coding: utf-8 -*-
import codecs
import json
import traceback
from pprint import pprint
import jconfig2
import mysql.connector
from bs4 import BeautifulSoup
from io import StringIO
import crawlerutil
import re

cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
cnx2 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
cnx3 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 

def save_result(reviewid,brandid,score):
    global cnx3
    cursor3 = cnx3.cursor()
    sql = "insert into review_brandid(reviewid,brandid,score) values(%(reviewid)s,%(brandid)s,%(score)s)"
    data={'reviewid':reviewid,'score':score,'brandid':brandid}
    try:
        cursor3.execute(sql,data)
        cnx3.commit()
    except: 
        print('exception')
        traceback.print_exc()


def match_title(titlestr):
    global cnx2
    global reviewid
    cursor2 = cnx2.cursor()
    resultstr=""
#    sql = 'SELECT pixid,brand,MATCH (brand) AGAINST (%(title)s IN NATURAL LANGUAGE MODE)  FROM pixnet_brands WHERE MATCH (brand) AGAINST (%(title)s IN NATURAL LANGUAGE MODE) order by MATCH (brand) AGAINST (%(title)s IN NATURAL LANGUAGE MODE) desc limit 3'
    sql = 'SELECT pixid,brand,MATCH (brand) AGAINST (%(title)s IN BOOLEAN MODE)  FROM urcosme_brands WHERE MATCH (brand) AGAINST (%(title)s IN BOOLEAN MODE ) order by MATCH (brand) AGAINST (%(title)s IN BOOLEAN MODE) desc limit 3'

    data={'title':titlestr}
    try:
        cursor2.execute(sql,data)
        for (id) in cursor2:
            save_result(reviewid,id[0],id[2])
#            resultstr=titlestr+","+str(id[1])+","+str(id[2])
#            print(id[0])
#            print(id[1])
#            print(id[2])
#            print(resultstr)
    except: 
        print('exception')
        traceback.print_exc()
    cursor2.close()

#    try:

#    print('test')

#crawlerutil.crawl('https://styleme.pixnet.net/productschannel',myparser)
cursor=cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

cursor2=cnx2.cursor()
cursor2.execute('SET NAMES utf8mb4')
cursor2.execute("SET CHARACTER SET utf8mb4")
cursor2.execute("SET character_set_connection=utf8mb4")

reviewid=None
sql = "select title,reviewid from pixnet_post"
cursor.execute(sql)
for (id) in cursor:
#    print(id[0])
    reviewid=id[1]
    match_title(id[0])
#    break
#    return id[0]

#data_file=codecs.open('classes.json','r','utf-8')
#data = json.load(data_file)
#for elmt in data:
#    save_brand(elmt['id'],elmt['name'])

#view-source:https://styleme.pixnet.net/productschannel

#pprint(data)
