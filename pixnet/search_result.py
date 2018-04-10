# -*- coding: utf-8 -*-
import requests as r
from bs4 import BeautifulSoup
import requests
import re
import urllib
import codecs
import json
import sys
from pprint import pprint
import jconfig2
import mysql.connector
import crawlerutil
import traceback
import time
from dateutil.parser import parse
from datetime import datetime
from random import randint
#https://www.urcosme.com/find-brand/766/brand_product_list?type=category

cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cnx2 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cursor = cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")
cnx.commit()
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; <64-bit tags>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev> Edge/<EdgeHTML Rev>.<Windows Build>'}



def save_url(url,queryterm,pview,p,a,title):
    global cnx
    global userid
    cursor = cnx.cursor()
    sql = "insert into pix_list(url,title,pview,author,ptime,queryterm) values(%(url)s,%(title)s,%(pview)s,%(author)s,%(ptime)s,%(queryterm)s)" #,ptime,auther,title#,,%(a)s,%(t)s
    #print(url)
    try:
     
        cursor.execute(sql,{'url':url,'title':title,'pview':pview,'author':a,'ptime':p,'queryterm':queryterm})#,'ptime':p,'author':a,'title':t
        cnx.commit()
        print('ok:',url)
    except mysql.connector.DatabaseError: 
        #print('exception:DatabaseError: data重複or url過長')
        
        error_string=traceback.format_exc()
        #print(error_string)
        if ('Incorrect string value' and "for column 'title'" )in error_string:
            cursor.execute(sql,{'url':url,'title':'-1','pview':pview,'author':a,'ptime':p,'queryterm':queryterm})#,'ptime':p,'author':a,'title':t
            cnx.commit()
            print('Incorrect string handle done',url)
        elif 'Duplicate entry' in error_string:   
            print('url重複:',url) 
        else:
            print('other error:',url)
            print(error_string)    




def myparser(content,queryterm):
#    print(content)
    global logtype
    global userid
    global myurl
    data={}
    soup = BeautifulSoup(content, "html.parser")   
    posttime=soup.find_all("span",{"class":"search-postTime"})
   
    
        
    nexturl=soup.find_all("li",{"class":"search-list"})
    view=soup.find_all("span",{"class":"search-views"})

    
    author=soup.find_all("a",{"class":"search-author"})
    title=soup.find_all("li",{"class":"search-title"})    

    #title=soup.find("a",{"href":url})
    
    for n,v,p,a,t in zip(nexturl,view,posttime,author,title):
        if int(p.text[0:4])>= 2015:
            print('ptime:',p.text[0:4])
            newurl=n.a['href'].split("url=")[1]
            newurl=urllib.parse.unquote(newurl)
            v=v.text.lstrip('人氣( ')
            pview=v.rstrip(' )')
            
            p=p.text
            a=a.text
            title=t.text
            #update_at=datetime.strptime(datetime.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')
            save_url(newurl,queryterm,pview,p,a,title)
    #        print(newurl)
    #    sys.exit()

sql="SELECT name,flag FROM Serena.urcosme_prods_select where flag=-1 order by reviews desc"
cursor = cnx.cursor()
cursor.execute(sql)
dataGet=[]
for readline in cursor:
    list = []
    list.extend(readline)
    dataGet.append(list)
#%xdel list
#print(dataGet)


#print(randint(0, 9))

for j in dataGet[randint(0, len(dataGet)):]: ##############

    queryterm=j[0]
    print(queryterm)
    for i in range (1,301): #��憭�300���
        print('第',i,'頁')
        if i==1: #開始抓的時候
            sql="update Serena.urcosme_prods_select set flag=0 where name=%(name)s  "
            data={"name":queryterm}
            cursor = cnx.cursor()
            cursor.execute(sql,data)
            cnx.commit() 
        
        
        url="https://www.pixnet.net/searcharticle?q="+queryterm+"&type=related&period=all&page="+str(i+1)
        try:
            crawlerutil.crawl_and_savenext("test",url,myparser,queryterm)
            time.sleep(1)
        except:
            pass
            
    sql="update Serena.urcosme_prods_select set flag=1 where name=%(name)s  "
    data={"name":queryterm}
    cursor = cnx.cursor()
    cursor.execute(sql,data)
    cnx.commit()   
    print('product done:',queryterm) 
