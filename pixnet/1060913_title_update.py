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
cnx3 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4',buffered=True) 
cursor3 = cnx3.cursor(buffered=True)    

cursor3.execute('SET NAMES utf8mb4')
cursor3.execute("SET CHARACTER SET utf8mb4")
cursor3.execute("SET character_set_connection=utf8mb4")
cnx3.commit()

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
'''

def save_post(url,title,hit,pdate,category,subcategory,username,tags,uuid):
    global cursor3
    global cnx3
    
    #tags=';'.join(tags)
    #sql = "insert into pixnet_post(url,title,hit,pdate,category,tags,uniqueuid) values(%(url)s,%(title)s,%(hit)s,%(pdate)s,%(category)s,%(tags)s,%(uuid)s)"
    #data={'url':url,'title':title,'pdate':pdate,'hit':hit,'category':category,'tags':tags,'uuid':uuid}
    sql="update pixnet_post_makeupsharing set title=%(title)s,username=%(username)s,subcategory=%(subcategory)s where url=%(url)s"
    print("title:",title,"user:",username,"sub:",subcategory,"url:",url)
    data={'title':title,"username":username,"subcategory":subcategory,"url":url}
    print('data:',data)
    try:
        cursor3.execute(sql,data)
        cnx3.commit()
    except: 
        print('exception')
        traceback.print_exc()


def save_to_sql(jsondata):
        #print('hi')
        #print(jsondata)
        #data=jsondata['categoriesArticles']['data']
        data=jsondata['postArticles']
        #print(data)
        for dat in data:
            print('herrrrrrrrrr')
            #save_user(dat['user']['user_name'],dat['user']['avatar'],dat['user']['member_uniqid'],dat['user']['follow_count'],dat['user']['name'])
            save_post(dat['link'],dat['title'],dat['hit'],dat['published_date'],dat['category'],dat['subcategory'],dat['user']['user_name'],dat['tags'],dat['user']['member_uniqid'])
#            save_user()
'''
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
#            save_user()
'''
def myparser(content):
    #print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    #data={}
    soup = BeautifulSoup(content, "html.parser")
    #span=soup.find("span",{"class":"sprite-img pagination__page--next"})
    #if span ==None:
    #    reset_progress()

    scripts=soup.find_all("script")
    for script in scripts:
        
        if 'REDUX_STATE' in script.text:
            
            elmts=script.text.split('REDUX_STATE =')
            jsstr=elmts[1]
            jsstr=re.sub(r'([; ])$','',jsstr)
    #        print(elmts[1])
            js=json.loads(jsstr)
            #print(js)
            save_to_sql(js)
            #update_page(js)
'''
def reset_progress():
    #print('reset_progressreset_progressreset_progressreset_progressreset_progressreset_progressreset_progress')
    global cursor3
    global cnx3
    sql = "update job_toplist set curpage=1"
    try:
        cursor3.execute(sql)
        cnx3.commit()
    except: 
        print('exception')
        traceback.print_exc()        
        
        
def myparser(content):
    #print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    data={}
    soup = BeautifulSoup(content, "html.parser")
    span=soup.find("span",{"class":"sprite-img go-top"})
    
    #if span ==None:
    #    reset_progress()
    
    scripts=soup.find_all("script")
    for script in scripts:
        if 'REDUX_STATE' in script.text:
            elmts=script.text.split('REDUX_STATE =')
            jsstr=elmts[1]
            jsstr=re.sub(r'([; ])$','',jsstr)
    #       print(elmts[1])
            js=json.loads(jsstr)
            #print(js)
            save_to_sql(js)
            #update_page(js)

'''
def save_elements(cnx2,sql,data):
    cursor2 = cnx2.cursor()
    
    
    
    try:
        cursor2.execute(sql,data)
        cnx2.commit()
    
    except mysql.connector.DatabaseError: 
        print('exception:DatabaseError')
        #print(contentparser.content.text)
        traceback.print_exc()
        #sql="update pixnet_post_makeupsharing set content='-1' where url=%(url)s"

        #data={"content":content.text,"url":url}
        #data={"content":'-1111',"url":'-1'}
        #print(sql)
        #print(data)
        cursor2.execute(sql,data)
        cnx2.commit()
'''

'''
def myparser(content):
    global url
    data={}
    soup = BeautifulSoup(content, "html.parser")  
    content=soup.find("div",{"class":"post__article"})
    print(content.text)
    sql="update pixnet_post set title=%(title)s,username=%(username)s,reviewid where url=%(url)s"

    data={"content":content.text,"url":url}
    crawlerutil.save_elements(cnx2,sql,data)
'''


'''
def proc_post(pagenum):
    print('pagenum:',pagenum)
    crawlurl='https://styleme.pixnet.net/makeupsharing?page='+str(pagenum)  #cosmetic
    crawlerutil.crawl(crawlurl,myparser)
'''

'''
def get_next_job():
    sql = "select curpage from job_toplist"
    cursor.execute(sql)
    for (id) in cursor:
        return id[0]
'''
cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 

cursor=cnx.cursor()   
    
sql = "select url from pixnet_post_makeupsharing where title = '-1' or subcategory is null or username is null"
#sql = "select url from pixnet_post_makeupsharing where url ='http://styleme.pixnet.net/post/216994535'" #皜祈岫�

cursor.execute(sql)
url=None
for (id) in cursor:
    print(id[0])
    url=id[0]

    crawlerutil.crawl(id[0],myparser)


