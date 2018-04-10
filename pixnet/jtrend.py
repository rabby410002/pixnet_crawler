#!/usr/bin/python3
import json
from py import jconfig2
import mysql.connector
from datetime import datetime

#import imp
#import sys
#imp.reload(sys)
#sys.setdefaultencoding('utf-8')

def get_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]
    
    sql = "SELECT distinct t.kw,b.brand,b.pixid FROM urcosme_trend t,urcosme_brands b,urcosme_brand_segment s where t.kw=s.segment and b.pixid=s.brandid"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'keyword':u[0],'brand':u[1],'bid':u[2]})
    
    myobj=result
    return myobj


def trend_brand_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
    cursor = cnx.cursor()
    result=[]
    
    sql = "SELECT distinct t.kw,b.brand,b.pixid FROM urcosme_trend t,urcosme_brands b,urcosme_brand_segment s where t.kw=s.segment and b.pixid=s.brandid limit 50"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'keyword':u[0],'brand':u[1],'bid':u[2]})
    
    myobj=result
    return myobj

def trend_pix_list():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database='gsearch') 
    cursor = cnx.cursor()
    result=[]
    
    #sql = "SELECT brand_name,prod FROM oneil.pixnet_raw_ts where brand_name='SK-II' group by prod"
    #sql = "SELECT distinct t.kw,b.brand,b.pixid FROM urcosme_trend t,urcosme_brands b,urcosme_brand_segment s where t.kw=s.segment and b.pixid=s.brandid limit 50"
    #sql="SELECT o.brand_name,o.prod,g.id FROM oneil.pixnet_raw_ts o,gsearch.prod_category g where o.prod=g.name group by o.brand_name,o.prod,g.id ;"
    sql="select brand_name,prod,sn from Serena.prodid_match;"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'category':u[1],'brand':u[0],'bid':u[2]})
    
    myobj=result
    return myobj



def trend_brand_list2():
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]
    
    sql = "SELECT distinct SOM_clusterID,Brand,Brand FROM HMM_pred_16gp order by SOM_clusterID asc"
    cursor.execute(sql)
    for (u) in cursor:
        result.append({'keyword':u[0],'brand':u[1],'bid':u[2]})
    
    myobj=result
    return myobj




def gtrend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT t.kw,date_format(t.gdate,'%Y-%m-%d'),t.val FROM urcosme_trend t,urcosme_brand_segment s where t.kw=s.segment and s.brandid="+ str(bid)+" order by t.gdate desc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    #print(lst)    
    return lst

def ctrend(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database='gsearch') 
    cursor = cnx.cursor()
    result={}
    
    #query = "SELECT t.kw,date_format(t.gdate,'%Y-%m-%d'),t.val FROM urcosme_trend t,urcosme_brand_segment s where t.kw=s.segment and s.brandid="+ str(bid)+" order by t.gdate desc"
    #query="SELECT o.brand_name,o.prod,o.pdate,o.raw_ts FROM oneil.pixnet_raw_ts o,gsearch.prod_category g where g.id="+bid+" and o.prod=g.name order by pdate desc;"
    
    query="SELECT o.brand_name,o.prod,o.pdate,o.raw_ts FROM oneil.pixnet_raw_ts o,Serena.prodid_match s where s.sn="+bid+" and s.prod=o.prod and s.brand_name=o.brand_name order by pdate desc;"
    #print(query)
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':datetime.strftime(u[2], '%Y-%m-%d'),'value':u[3]})
    #print(lst)
    return lst

def ctrend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result=[]

    sql = "SELECT brand_name, prod FROM Serena.prodid_match WHERE sn = " + str(bid) 
    cursor.execute(sql)
    for (u) in cursor:
        brand = u[0]
        prod = u[1]

    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT date_format(pdate,'%Y-%m-%d'),raw_ts FROM oneil.pixnet_raw_ts where brand_name = \'"+ brand + "\' and prod = \'" + prod + "\' order by pdate asc"
    cursor.execute(query)
    lst=[]
    data = {}

    data['key'] = brand + ' X ' + prod
    data['values'] = []
    for (u) in cursor:
        data['values'].append({'date': u[0], 'value': u[1]})

    lst.append(data)

    return lst
def pixnet_season(pid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port) 
    cursor = cnx.cursor()

    sql = "select brand, category from gsearch.urcosme_brand_category where id = "+ str(pid)
    cursor.execute(sql)
    for (u) in cursor:
        Brand = u[0]
        Category = u[1]
    
    result={}
    #query = "SELECT r.prodname, date_format(r.pdate,'%Y-%m-%d'), r.likes FROM urcosme_prods p, urcosme_reviews r where r.prodid = '"+ str(pid)+"' limit 100 "
    query = "select m_date, percent_all, percent_5, percent_6, percent_7 from oneil.pixnet_raw_ts_season_mean where brand_name = '"+ str(Brand)+"' and prod = '"+ str(Category)+"' "    
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[0],'mean':u[1],'five':u[2],'six':u[3],'seven':u[4] })
    return lst

def gtrend2(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT Brand,date_format(Date,'%Y-%m-%d'),gtrend FROM HMM_pred_16gp where Brand='"+ str(bid)+"' order by Date asc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst



def gtrend3(bid):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    result={}
    query = "SELECT Brand,date_format(Date,'%Y-%m-%d'),MarkovInd FROM HMM_pred_16gp where Brand='"+ str(bid)+"' order by Date asc"
    cursor.execute(query)
    lst=[]
    
    for (u) in cursor:
        lst.append({'dt':u[1],'value':u[2]})
    return lst


#myobj=[{'id':1, 'name':"Oli Bob \n steve",'age':"55"},
#    {'id':2, 'name':"Mary May", 'age':"1" },
#    {'id':3, 'name':"Christine Lobowski", 'age':"42" },
#    {'id':4, 'name':"Brendon Philips", 'age':"125" },
#    {'id':5, 'name':"Margret Marmajuke", 'age':"16"}]


#print(json.dumps(myobj))

