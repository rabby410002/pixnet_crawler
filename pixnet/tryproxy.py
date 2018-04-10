#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import requests as r
from bs4 import BeautifulSoup
import re
import codecs
import json
import sys
from pprint import pprint
import traceback
import pickle
import datetime
import time
from bs4 import BeautifulSoup



#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}

headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; <64-bit tags>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev> Edge/<EdgeHTML Rev>.<Windows Build>'}

proxylist=[]
def get_content(myurl):
    global headers
    try:
        res = r.get(myurl,headers=headers)
        res.encoding='utf-8'
        content=res.text.encode('utf-8')
    except Exception:
        print("exception")
        return None
    return content
    

def myparser(content):
    proxy_lst=[]
    soup = BeautifulSoup(content, "html.parser")
    trs=soup.find_all("tr")
    for tr in trs:
        tds=tr.find_all("td")
        if tds:
            if re.match('[0-9\.]+',tds[0].text):
                #print(tds[0].text)
                proxy_lst.append((tds[0].text,tds[1].text))
    return proxy_lst

def proxy_speed(proxy_lst,target_url,timeout):
    global headers
    global proxylist
    rcode=0
    cnt=0
    for elmt in proxy_lst:
        try:
            begin=datetime.datetime.now()
            proxies = {'http': 'http://'+elmt[0]+':'+elmt[1],'https': elmt[0]+':'+elmt[1]}
            res = r.get(target_url,headers=headers,proxies=proxies,timeout=timeout)
            rcode=res.status_code
            #print(rcode)
        except Exception:
            True
#            print("exception")
#            traceback.print_exc()
        if rcode ==200:
            
            dtdiff=datetime.datetime.now()-begin
            soup = BeautifulSoup(res.text, "html.parser")    
            #entry=soup.find("img",{"at":"more"})
            #print(entry)
            #if '嚙踝蕭���謍望�蕭嚙踝蕭' in entry.text:
            print('http://'+elmt[0]+':'+elmt[1]+" "+str(dtdiff))
            proxylist.append( {'http':'http://'+elmt[0]+':'+elmt[1], 'https':'http://'+elmt[0]+':'+elmt[1]}  )
            cnt+=1
            if cnt >=50:
                pickle.dump(proxylist, open("proxy.pkl", "wb"))
                return

#            print(res.text)
        

#content=get_content('https://free-proxy-list.net/')
content=get_content('https://free-proxy-list.net/')
proxy_lst=myparser(content)
#print(proxy_lst[0])
proxy_speed(proxy_lst,'https://www.pixnet.net/blog',10)
#proxy_speed(proxy_lst,'https://www.pixnet.net/blog',20)

#proxylist
