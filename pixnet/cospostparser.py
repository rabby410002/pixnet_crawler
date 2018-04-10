#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import requests as r
from bs4 import BeautifulSoup
import requests

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

cursor=cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")
cnx.commit()


#瘝�
def log_behavior(param,logtype):
    global cursor
    global cnx

    sql = "insert into pixnet_log(param,logtype,logtime) values(%(param)s,%(logtype)s,NOW())"
    data={'param':param,'logtype':logtype}
    try:
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception:log behavior')
        traceback.print_exc()



def save_user(username,avatar,uniqueid,follow,name):
    #print('oooooooooooooooooooooooooooooooooooooooooooooooo')
    global cursor
    global cnx

    sql = "insert into pixnet_user(username,avatar,uniqueid,follow,name) values(%(username)s,%(avatar)s,%(uniqueid)s,%(follow)s,%(name)s)"
    data={'username':username,'avatar':avatar,'uniqueid':uniqueid,'follow':follow,'name':name}
    try:
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception:dup user')
        print(username)
        print(uniqueid)
        #traceback.print_exc()


def save_post(url,title,hit,pdate,category,subcategory,tags,uuid):
    #print('ppppppppppppppppppppppppppppppppppppppppppppppp')
    global cursor
    global cnx

    tags=';'.join(tags)
    sql = "insert into pixnet_post_makeupsharing(url,title,hit,pdate,category,subcategory,tags,uniqueuid) values(%(url)s,%(title)s,%(hit)s,%(pdate)s,%(category)s,%(subcategory)s,%(tags)s,%(uuid)s)"
    data={'url':url,'title':title,'pdate':pdate,'hit':hit,'category':category,'subcategory':subcategory,'tags':tags,'uuid':uuid}

    try:
        cursor.execute(sql,data)
        cnx.commit()
 
    except mysql.connector.IntegrityError: 
        print('exception:save_post duplicate')
        print(url)
        print(uuid)
        
        #traceback.print_exc()
    except  mysql.connector.DatabaseError: 
        print('exception:save_post title error')
        print(title)
        print(url)
        try:
            data={'url':url,'title':'-1','pdate':pdate,'hit':hit,'category':category,'subcategory':subcategory,'tags':tags,'uuid':uuid}
            cursor.execute(sql,data)
            cnx.commit()
        except:
            pass    

    except  mysql.connector.DataError: 
        print('exception:save_post tag too long')
        #print(url)
        data={'url':url,'title':title,'pdate':pdate,'hit':hit,'category':category,'subcategory':subcategory,'tags':'-1','uuid':uuid}
        cursor.execute(sql,data)
        cnx.commit()  
    except:
        print(url)   
   

def save_to_sql(jsondata):
        data=jsondata['categoriesArticles']['data']
        for dat in data:
            save_user(dat['user']['user_name'],dat['user']['avatar'],dat['user']['member_uniqid'],dat['user']['follow_count'],dat['user']['name'])
            save_post(dat['link'],dat['title'],dat['hit'],dat['published_date'],dat['category'],dat['subcategory'],dat['tags'],dat['user']['member_uniqid'])
#            save_user()
    
def update_page(js): #瘥摰���
    #print('upupupupupupupupupupupupupupupupupupupupupupupupup')
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
        print('exception:update_page')
        traceback.print_exc()


def reset_progress():
    #print('reset_progressreset_progressreset_progressreset_progressreset_progressreset_progressreset_progress')
    global cursor
    global cnx
    sql = "update job_toplist set curpage=1"
    try:
        cursor.execute(sql)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()

def myparser(content):
    #print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    data={}
    soup = BeautifulSoup(content, "html.parser")
    span=soup.find("span",{"class":"sprite-img pagination__page--next"})
    if span ==None:
        reset_progress()

    scripts=soup.find_all("script")
    for script in scripts:
        if 'REDUX_STATE' in script.text:
            elmts=script.text.split('REDUX_STATE =')
            jsstr=elmts[1]
            jsstr=re.sub(r'([; ])$','',jsstr)
    #        print(elmts[1])
            js=json.loads(jsstr)
#            print(js)
            save_to_sql(js)
            update_page(js)


def proc_post(pagenum):
    print('pagenum:',pagenum)
    crawlurl='https://styleme.pixnet.net/skincare?page='+str(pagenum)  #cosmetic #makeupsharing
    crawlerutil.crawl(crawlurl,myparser)



def get_next_job():
    sql = "select curpage from job_toplist"
    cursor.execute(sql)
    for (id) in cursor:
        print(id[0])
        return id[0]

#class="sprite-img pagination__page--next"

#print(content)
#content=content.text.
for i in range(300):
    pgnum=get_next_job()
#    pgnum=348
    proc_post(pgnum)
    time.sleep(1)
