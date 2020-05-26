#!/usr/bin/env python
# coding: utf-8

# In[18]:


# -*- coding:utf-8 -*-
import requests
import re
import random
import time
import json
# import pymysql
# from sqlalchemy import create_engine
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import urllib
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  ###禁止提醒SSL警告

 
class jd(object):
    def __init__(self):
 
        self.s = requests.session()   ## 创建一个session对象
        self.headers = { 
            'cookie': 'language=zh_CN; __jdv=95931165|direct|-|none|-|1590429040494; 3AB9D23F7A4B3C9B=XVKMQNOWK2ECB27HE7YUYVNTCXOIOWVWLVVY44T3UVAJILYV62QYIUYBATHFOLMSYO3MZKPGELM23IVSHJFRFDKHUQ; __jdu=15904290404941086576685; pinId=gqiaZTYYOyziJlDulDYsZQ; pin=jrt19950829; unick=jrt19950829; _tp=ZzSD6JwF16oddjUeHZCXHA%3D%3D; _pst=jrt19950829; shshshfpa=5915fe8a-80e8-211f-09ad-406cfcb15c39-1590431566; shshshfpb=wRkLsRZa5c8W3DZDvOL6PSg%3D%3D; user-key=0b9f5840-b115-4104-b024-3422225022d2; cn=0; wxa_level=1; retina=0; webp=1; jxsid=15904386877651048623; sc_width=1920; visitkey=50020397727715436; areaId=5; ipLoc-djd=5-239-243-48622; wq_logid=1590444913.1080998799; cid=9; mba_muid=15904290404941086576685; __wga=1590444914880.1590444914880.1590438688001.1590438688001.1.2; PPRD_P=UUID.15904290404941086576685-LOGID.1590444914890.1230274150; __jd_ref_cls=MDownLoadFloat_AppArouseA1; sk_history=208399%2C; shshshfp=eb90c0aecb73620eb49a794afca3b318; __jda=122270672.15904290404941086576685.1590429040.1590435660.1590447537.4; __jdc=122270672; wlfstk_smdl=ha2yeqnk9d6f5oss2yad2d0hymd0bynt; TrackID=1EJgxhvOsbIkASDnIFwmz6wPqDckhJfH7s7L8dh8-2v3ExurT7j9xzZAl3cNJuW9gGr93Gh5Dy03el8jZKHuwweJg4K7ATlzrIqyAdZBzIqDWh0c31WGlNnhIhRFTxVfx; thor=7BB3945161F1186F84841A299AC44C8109B6576BAE7862CA973B294B0B927A74CD665A703D566E43C63A9CB411B03A9A9310D32F35BD8CEFA44A9E17004D7D024F8D16F6E31EFC0AAB5779EDFE0BBEFDD5566CA9C6A3960B700FD6ADAFAAD6E3509CD82CAD893D7D5FA4E46C74DF57D8B9984A1D3401DC752189CAA9D9314D9DC977C806F117A338C740E11287E760BC; ceshi3.com=000; shshshsID=6e2c1a84e7555b67c3c1cd781ba23c35_4_1590448080338; __jdb=122270672.7.15904290404941086576685|4.1590447537; JSESSIONID=D5FDA613A5878CF07853EFF5D952A42A.s1',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection' : 'keep-alive',
                   }
        self.s.headers.update(self.headers)   ### 设置请求头
        #self.engine = create_engine('mysql+pymysql://root:123456@192.168.0.1:3306/jd')   ##存储到SQL
 
 
    def getdata(self,url,name):
 
        getdate=time.strftime("%Y-%m-%d",time.localtime())
        self.shopid=re.search('index-(.*?).html',url).group(1)    ###获取店铺ID号
        self.s.get('https://shop.m.jd.com/search/search?shopId='+str(self.shopid))
        
        wareId_list = []
        wname_list = []
        detail_list = []
        size_list = []
        number_list = []
        jdPrice_list = []
        hPrice_list = []
        coupons_list = []
        quans_list = []
        promotions_list = []
 
        for i in range(1,1000):   ###爬取页数范围   没有找到商品后会自动退出循环
            time.sleep(random.random())  ##随机延时0-1秒
            t = int(time.time() * 1000)
            ##           https://wqsou.jd.com/search/searchjson?datatype=1&page=2&pagesize=40&merge_sku=yes&qp_disable=yes&key=ids%2C%2C121614&_=1537524375713&sceneval=2&g_login_type=1&callback=jsonpCBKQ&g_ty=ls
            searchurl = 'https://wqsou.jd.com/search/searchjson?datatype=1&page={}&pagesize=40&merge_sku=yes&qp_disable=yes&key=ids%2C%2C{}&_={}&sceneval=2&g_login_type=1&callback=jsonpCBKA&g_ty=ls'.format(i,self.shopid,t)  ##请求数据网址
            print(searchurl)
            req=self.s.get(url=searchurl,verify=False).text   ###获取数据
            #print(req)
            print(name,i)
            wareId=re.findall('"wareid": "(.*?)",',req)   ##获取商品ID
            wname=re.findall('"warename": "(.*?)",',req)    ###获取商品名称
            jdPrice=re.findall('"dredisprice": "(.*?)",',req)    ###获取商品价格
            hPrice=re.findall('"hprice": "(.*?)",',req)    ###获取商品价格
            print(hPrice)
            
            ###优惠券 促销
            vender_id = re.findall('"vender_id": "(.*?)",',req)
            sku_id = re.findall('"wareid": "(.*?)",',req) 
            cat_id = re.findall('"catid": "(.*?)",',req) 
            cid1 = re.findall('"cid1": "(.*?)",',req) 
            cid2 = re.findall('"cid2": "(.*?)",',req) 
            area = '5_239_243_48622'
            
            
            if wareId==[]:    ###如果没有找到ID退出循环
                break
                
                
            
            coupons = []
            promotions = []
            quans = []
            for i in range(len(vender_id)):
                cur_cat = cid1[i] + '%2C' + cid2[i] + '%2C' + cat_id[i]
                coupon_url = 'https://item.jd.com/coupons?skuId=' + sku_id[i] + '&cat=' + cur_cat + '&venderId=' + vender_id[i] + '&session=61D56A4B951B4A9963EE93C046E341F5.s1'
                #req=self.s.get(url=coupon_url,verify=False).text
                #print (req)

                sauce = self.s.get(url=coupon_url)
                soup = BeautifulSoup(sauce.content,'html.parser')
                cur_rmb = []
                cur_name = []
                cur_time = []
                for line in soup.findAll('span', attrs={'class': 'coupon-val'}):
                    cur_rmb.append(line.text)
                for line in soup.findAll('span', attrs={'class': 'condition'}):
                    cur_name.append(line.text)
                for line in soup.findAll('p', attrs={'class': 'coupon-time'}):
                    cur_time.append(line.text)
                cur_coupon = ['¥' + a + '东券 ' + b + ' (' + c + ')' for a, b, c in zip(cur_rmb, cur_name, cur_time)]
                
                #print (coupon_url)
                #print (cur_coupon)
                
                promotion_url = 'https://cd.jd.com/promotion/v2?skuId=' + sku_id[i] + '&area=2_2813_51976_0&venderId=' + vender_id[i] + '&cat=' + cur_cat
                #print (req)

                sauce = self.s.get(url=promotion_url)
                soup = json.loads(BeautifulSoup(sauce.content).text)
                #promotions= [soup['quan']['title'],soup['prom']['pickOneTag']['content'],soup['prom']['tags']['content']]
                #print (soup)
                cur_promotions = [[i['content'] for i in soup['prom']['pickOneTag']],[i['content'] for i in soup['prom']['tags']]]
                cur_quans = soup['quan']['title'] if soup['quan'] else []
                coupons.append(cur_coupon) 
                promotions.append(cur_promotions)
                quans.append(cur_quans)
                                  

                
                
            ##https://item.jd.com/coupons?skuId=208399&cat=1319%2C1525%2C7057&venderId=1000001933
            #https://cd.jd.com/promotion/v2?callback=jQuery8797075&skuId=208399&area=5_239_243_48622&venderId=1000001933&cat=1319%2C1525%2C7057
 
 
            #####处理数据
            ## 名字处理
            sname = []
            detail = []
            size = []
            number= []

            for s in wname:
                if '裤' in s and '片' in s:
                    sub = s.split('裤')
                    ssub = sub[1].split('片')
                    if len(ssub) == 1:
                        ssub.append('')
                    cursize = ''
                    curnumber = ''
                    for i in ssub[0]:
                        if i.isalpha():
                            cursize += i 
                        else:
                            curnumber += i
                    sname.append(sub[0]+'裤')
                    detail.append(ssub[1])
                    size.append(cursize)
                    number.append(curnumber)
                elif '裤' in s:
                    sub = s.split('裤')
                    ssub = sub[1].split('(')
                    if len(ssub) == 1:
                        ssub.append('')
                    cursize = ''
                    curnumber = ''
                    for i in ssub[0]:
                        if i.isalpha():
                            cursize += i 
                        else:
                            curnumber += i
                    sname.append(sub[0]+'裤')
                    detail.append(ssub[1])
                    size.append(cursize)
                    number.append(curnumber)
                else:
                    sname.append(s)
                    size.append('null')
                    number.append('null')
                    detail.append('null')

            wareId_list.extend(wareId)
            wname_list.extend(sname)
            jdPrice_list.extend(jdPrice)
            hPrice_list.extend(hPrice)
            coupons_list.extend(coupons)
            promotions_list.extend(promotions)
            quans_list.extend(quans)
            detail_list.extend(detail)
            size_list.extend(size)
            number_list.extend(number)
            wareId_l=len(wareId_list)
            name_list=[]
            name_list.append(name)
            name_list.extend(name_list*(wareId_l-1))
            getdate_list = []
            getdate_list.append(getdate)
            getdate_list.extend(getdate_list * (wareId_l - 1))

 
        jddata={
            'name':name_list,
            'wareId':wareId_list,
            'wname':wname_list,
            'detail':detail_list,
            'size':size_list,
            'number(片)':number_list,
            '最终jdPrice':jdPrice_list,
            'coupon':coupons_list,
            'promotion':promotions_list,
            'quan':quans_list,
            'update': getdate_list
        }

        return jddata


    ###保存csv文件
        #df.to_sql('店铺前端', con=self.engine, if_exists='append', index=False)  ##上传到数据库
 
 
if __name__ == '__main__':
 ##haoqi:1000001934  pamper:1000001933  
    j=jd()
    url='https://mall.jd.com/index-1000001933.html'
    nm='pamper'
    jddata = j.getdata(url,nm)
    df = pd.DataFrame(data=jddata)
    getdate=time.strftime("%Y-%m-%d",time.localtime())
    df.to_csv('Downloads/result-dawn-' + nm + '-' + getdate + '.csv',  index=False, encoding="utf-8") 


# In[157]:


jddata


# In[141]:


s = '帮宝适超薄干爽绿帮纸尿裤L84片(9-14kg)大码纸尿裤尿不湿瞬吸干爽'
sub = s.split('裤')
ssub = sub[1].split('片')
size = ''
number = ''
for i in ssub[0]:
    if i.isalpha():
        size += i 
    else:
        number += i
print ([sub[0],size,number,ssub[1]])


# In[ ]:




