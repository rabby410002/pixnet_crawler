# -*- coding: utf-8 -*-
import requests as r
from bs4 import BeautifulSoup
import requests
import shutil
import urllib
import codecs
import traceback
import mysql.connector
import json
import random
import time
import shutil
import sys
import io
import re
from pprint import pprint
import os
import jconfig2
import crawlerutil

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cursor = cnx.cursor()    
cnx2 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cursor2=cnx2.cursor()

cursor2.execute('SET NAMES utf8mb4')
cursor2.execute("SET CHARACTER SET utf8mb4")
cursor2.execute("SET character_set_connection=utf8mb4")
cnx2.commit()

'''
def log_behavior(param,logtype):
    global cursor
    global cnx

    sql = "insert into pixnet_log(param,logtype,logtime) values(%(param)s,%(logtype)s,NOW())"
    data={'param':param,'logtype':logtype}
    try:
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()



def save_user(username,avatar,uniqueid,follow,name):
    global cursor
    global cnx

    sql = "insert into pixnet_user(username,avatar,uniqueid,follow,name) values(%(username)s,%(avatar)s,%(uniqueid)s,%(follow)s,%(name)s)"
    data={'username':username,'avatar':avatar,'uniqueid':uniqueid,'follow':follow,'name':name}
    try:
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()


def save_post(url,title,hit,pdate,category,tags,uuid):
    global cursor
    global cnx
    tags=';'.join(tags)
    sql = "insert into pixnet_post(url,title,hit,pdate,category,tags,uniqueuid) values(%(url)s,%(title)s,%(hit)s,%(pdate)s,%(category)s,%(tags)s,%(uuid)s)"
    data={'url':url,'title':title,'pdate':pdate,'hit':hit,'category':category,'tags':tags,'uuid':uuid}

    try:
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()


def save_to_sql(jsondata):
        data=jsondata['categoriesArticles']['data']
        for dat in data:
            save_user(dat['user']['user_name'],dat['user']['avatar'],dat['user']['member_uniqid'],dat['user']['follow_count'],dat['user']['name'])
            save_post(dat['link'],dat['title'],dat['hit'],dat['published_date'],dat['category'],dat['tags'],dat['user']['member_uniqid'])
#            save_user()
    
def update_page(js):
    global cursor
    global cnx
    totalp=js['categoriesArticles']['totalPage']
    curp=js['categoriesArticles']['currentPage']
    if totalp!=curp:
        sql = "update job_toplist set curpage="+str(curp+1)
    try:
        cursor.execute(sql)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()
'''

def myparser(content):
    global url
    data={}
    soup = BeautifulSoup(content, "html.parser")  
    content=soup.find("div",{"class":"post__article"})
    
    
    sql="update pixnet_post_makeupsharing set content=%(content)s where url=%(url)s"
    try:
        print(content.text)
        data={"content":content.text,"url":url}
    except:
        data={"content":"-1","url":url}
        
    crawlerutil.save_elements(cnx2,sql,data)


'''

def proc_post(pagenum):
    crawlurl='https://styleme.pixnet.net/makeupsharing?page='+str(pagenum)
    crawlerutil.crawl(crawlurl,myparser)


def get_next_job():
    sql = "select curpage from job_toplist"
    cursor.execute(sql)
    for (id) in cursor:
        return id[0]
'''

sql = "select url from Serena.pix_content where content is null" #皜祈岫�

cursor.execute(sql)
url=None
for (id) in cursor:
    print(id[0])
    url=id[0]
#    crawlurl='https://styleme.pixnet.net/makeupsharing?page='+str(pagenum)
    ##crawlerutil.crawl(id[0],myparser)
#    time.sleep(1)
#    break

