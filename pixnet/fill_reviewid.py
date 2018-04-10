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
cnx3 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 

def save_result(reviewid,id):
    global cnx3
    cursor3 = cnx3.cursor()
    sql = "update pixnet_post set reviewid=%(reviewid)s where id=%(id)s"
    data={'reviewid':reviewid,'id':id}
    try:
        cursor3.execute(sql,data)
        cnx3.commit()
    except: 
        print('exception')
        traceback.print_exc()

#crawlerutil.crawl('https://styleme.pixnet.net/productschannel',myparser)
cursor=cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

cursor3=cnx3.cursor()
cursor3.execute('SET NAMES utf8mb4')
cursor3.execute("SET CHARACTER SET utf8mb4")
cursor3.execute("SET character_set_connection=utf8mb4")

gurl=None
sql = "select url,id from pixnet_post where reviewid is null"
cursor.execute(sql)
for (id) in cursor:
    print(id[0])
    reviewid=id[0].split("/")[-1]
    print(reviewid)
    print(id[1])
    save_result(reviewid,id[1])

#    gurl=id[1]
#    match_title(id[0])
#    break
#    return id[0]

#data_file=codecs.open('classes.json','r','utf-8')
#data = json.load(data_file)
#for elmt in data:
#    save_brand(elmt['id'],elmt['name'])

#view-source:https://styleme.pixnet.net/productschannel

#pprint(data)
