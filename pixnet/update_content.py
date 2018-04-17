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

#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}

headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; <64-bit tags>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev> Edge/<EdgeHTML Rev>.<Windows Build>'}


cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cursor = cnx.cursor()    
cnx2 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cursor2=cnx2.cursor()

cursor2.execute('SET NAMES utf8mb4')
cursor2.execute("SET CHARACTER SET utf8mb4")
cursor2.execute("SET character_set_connection=utf8mb4")
cnx2.commit()



def myparser(content):
    global url
    data={}
    soup = BeautifulSoup(content, "html.parser")  
    #content=soup.find("div",{"class":"post__article"})
    content=soup.find("div",{"class":"article-content-inner"})

    sql="update Serena.pix_list set content=%(content)s where url=%(url)s"
    try:
        #print(content.text)
        data={"content":content.text,"url":url}
        print('done:',url)
    except AttributeError:
        
     
        try:
            content=soup.find("div",{"class":"post__article"})
            data={"content":content.text,"url":url}
            print('Attribute handle:',url)
        except: 
            print('other exception',url)
            data={"content":"-1","url":url}   
            #traceback.print_exc()
        
    crawlerutil.save_elements(cnx2,sql,data)



sql = "select url from pix_list where content is null and ptime>=2015 order by rand() "
#sql = "select url from pixnet_post_makeupsharing_temp where title = '-1' or subcategory is null or username is null"
#sql = "select url from pixnet_post_makeupsharing where url ='http://styleme.pixnet.net/post/218390274'" #���疵嚙踐��

cursor.execute(sql)
url=None
for (id) in cursor:
    print(id[0])
    url=id[0]
#    crawlurl='https://styleme.pixnet.net/makeupsharing?page='+str(pagenum)
    do=0
    while do<10:
        try:
            crawlerutil.crawl(id[0],myparser)
            time.sleep(1)
            do=11
            
        except:
            print('except handle: no content:',url)
            do+=1
        
    
#    break

