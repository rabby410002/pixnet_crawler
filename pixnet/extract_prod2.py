# -*- coding: utf-8 -*-
import mysql.connector
import pymysql, numpy as np
import jconfig2
import re
import datetime

#������load��O����


#cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 

cnx = pymysql.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database,charset='utf8mb4') 

cursor = cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")
cnx.commit()



##全部載入到記憶體
print(datetime.datetime.now())

sql="select id,url,title,content from Serena.pix_list "
cursor.execute(sql)
print(datetime.datetime.now())
pix_result=[]
cursor.execute(sql)
for u in cursor:
    pix_result.append(u)
print(len(pix_result))
print(datetime.datetime.now())

##產品list 對應到品牌
sql="select u.id,prodid,brandid,u.name,b.pixid,b.brand from Serena.urcosme_prods_select u ,gsearch.urcosme_prods p,gsearch.urcosme_brands b \
where u.id=p.id and brandid=b.pixid order by u.id"
cursor.execute(sql)
result2=[]

reChinese = re.compile('[\u4e00-\u9fa5]+') #只取中文
reEnglish = re.compile('[\s\w]+')  
for u in cursor:
    result2.append(u)

brand_dict={'12': ['CHANEL','香奈兒'], '76':['BOBBI BROWN','芭比波朗'],\
            '81':['M.A.C','M.A.C'],'50':['OLAY','歐蕾'],'195':['DR.WU','達爾膚'],\
            '68':['KIEHL','契爾氏'],'224':['GIORGIO ARMANI','亞曼尼'],\
            '113':['YSL','聖羅蘭'],'7':['Biotherm','碧兒泉'],'24':['Estee Lauder','雅詩蘭黛'],\
            '38' :['LANCOME','蘭蔻 '],'53':['shu uemura','植村秀'],'55':['SK-II','SK-II']}



def save_result(variablelist):
      sql="INSERT Serena.pix_extract(origin_id,url,reviewid,brandname0,brandname1,prodname,prodcate) VALUES (%s,%s,%s,%s,%s,%s,%s)"
      
          
      try:
          cursor.execute(sql,variablelist)
          cnx.commit()
      except:
          #except mysql.connector.DatabaseError: 
          print('error:')
          print(variablelist) 



#找對應
for i in result2[:100]: #result2 is the brand_product list
    
    
    ch_match=reChinese.findall(i[3]) #prodname(only chinese)
    
    b_name=brand_dict[str(i[2])]  #brandname
    print(b_name[0],b_name[1],ch_match[0],datetime.datetime.now())
    
    for j in pix_result: #j[2]:title #j[3]:content
        origin_id=j[0]
        url=j[1]
        #print(j)
        if j[3]!=None: # if content is not null
            if ( ( (b_name[0] in j[3]) or (b_name[1] in j[3]) )and (ch_match[0] in j[3]) ): #content include brand and prods
                #extract reviewid
                reviewid=j[1].split("/")[-1]
                if ('-' in reviewid):
                    reviewid=reviewid.split("-")[0]
                  
                #extract category
                sql="select category from gsearch.urcosme_prods where name like '%%%s%%'"%ch_match[0]
                res=cursor.execute(sql)
                cat_result=[]
                for u in cursor:
                    cat_result.append(u)
                res=cat_result[0]
                print('1')
                print(int(origin_id),str(url),reviewid,b_name[0],b_name[1],ch_match[0],res[0])
                vlist=(int(origin_id),str(url),reviewid,b_name[0],b_name[1],ch_match[0],res[0])
                save_result(vlist)
            elif (((b_name[0] in j[2]) or (b_name[1] in j[2]))and (ch_match[0] in j[3]) ):  #title include brand and content include prods
                #extract reviewid
                reviewid=j[1].split("/")[-1]
                if ('-' in reviewid):
                    reviewid=reviewid.split("-")[0]
                #extract category 
                sql="select category from gsearch.urcosme_prods where name like '%%%s%%'"%ch_match[0]
                res=cursor.execute(sql)
                cat_result=[]
                for u in cursor:
                    cat_result.append(u)
                res=cat_result[0]
                print('2')
                print(int(origin_id),str(url),reviewid,b_name[0],b_name[1],ch_match[0],res[0])
                vlist=(int(origin_id),str(url),reviewid,b_name[0],b_name[1],ch_match[0],res[0])
                save_result(vlist)
        elif (((b_name[0] in j[2]) or (b_name[1] in j[2]))and (ch_match[0] in j[2]) ): #title include brand and prods
            #extract reviewid
            reviewid=j[1].split("/")[-1]
            if ('-' in reviewid):
                reviewid=reviewid.split("-")[0]
              
            #extract category
            sql="select category from gsearch.urcosme_prods where name like '%%%s%%'"%ch_match[0]
            res=cursor.execute(sql)
            cat_result=[]
            for u in cursor:
                cat_result.append(u)
            res=cat_result[0]
            print('3')
            print(int(origin_id),str(url),reviewid,b_name[0],b_name[1],ch_match[0],res[0])
            vlist=(int(origin_id),str(url),reviewid,b_name[0],b_name[1],ch_match[0],res[0])
            save_result(vlist)


    
