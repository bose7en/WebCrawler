# coding=utf-8
__author__ = 'zhangbojian'
import urllib2 as ul2
from urlparse import urlparse
from bs4 import BeautifulSoup

#获取关键字
def getKeyword(targetPage):
    keyword={'钱物相关':["银行","汇款","现金","领取","储蓄卡","信用卡","人民币","转账","身份证","款项","预存","缴费","充值","兑换","话费","余额"],
             '业务相关':["积分","号码卡","套卡","促销","中国移动","广东移动","汕头移动","沟通100","移动","电信","联通","全球通","动感地带","神州行","大众卡","网聊卡","流量王","免费打电话","免费通话","免费上网","畅听卡","畅聊卡","流量卡"]}
    monneyStrArray=[]
    lenMonArr=keyword['钱物相关'].__len__()
    busiStrArray=[]
    lenBusiArr=keyword['业务相关'].__len__()
    #挖掘钱物相关
    n=0
    while n<lenMonArr:
        if targetPage.find(keyword['钱物相关'][n])>=0:
            monneyStrArray.append(keyword['钱物相关'][n])
        n=n+1
    monneyStr='、'.join(monneyStrArray)
    #挖掘业务相关
    m=0
    while m<lenBusiArr:
        if targetPage.find(keyword['业务相关'][m])>=0:
            busiStrArray.append(keyword['业务相关'][m])
        m=m+1
    busiStr='、'.join(busiStrArray)
    return {'钱物相关':monneyStr,'业务相关':busiStr}

#获取域名信息
def getWhoisMes(link):
    whoispage=ul2.urlopen('http://whois.chinaz.com/'+urlparse(link).hostname).read()
    bswhoispage=BeautifulSoup(whoispage,'html.parser')
    try:
        domainmes=bswhoispage.div.find(id='whoisinfo').get_text('@#$',strip=True).split('@#$')
        mesLen=domainmes.__len__()
        #域名注册商
        domainReg=''
        i1=0
        while i1<mesLen:
            if domainmes[i1].encode('utf8').startswith('注册商'):
                domainReg=domainmes[i1][4:]
                break
            i1=i1+1
        #域名联系人
        domainContact=''
        i1=0
        while i1<mesLen:
            if domainmes[i1].encode('utf8').startswith('联系人'):
                domainContact=domainmes[i1][5:]
                break
            i1=i1+1
        #域名更新时间
        domainUpTime=''
        i1=0
        while i1<mesLen:
            if domainmes[i1].encode('utf8').startswith('更新时间'):
                domainUpTime=domainmes[i1][5:]
                break
            i1=i1+1
        #域名创建时间
        domainCreTime=''
        i1=0
        while i1<mesLen:
            if domainmes[i1].encode('utf8').startswith('创建时间'):
                domainCreTime=domainmes[i1][5:]
                break
            i1=i1+1
        #域名过期时间
        domainDowTime=''
        i1=0
        while i1<mesLen:
            if domainmes[i1].encode('utf8').startswith('过期时间'):
                domainDowTime=domainmes[i1][5:]
                break
            i1=i1+1
    except Exception,e:
        print '1',link,e.message
        domainReg=''
        domainContact=''
        domainUpTime=''
        domainCreTime=''
        domainDowTime=''
    return {'注册商':domainReg,'联系人':domainContact,'更新时间':domainUpTime,'创建时间':domainCreTime,'过期时间':domainDowTime}

#获取title
def getTitle(targetPage):
    try:
        bsPage=BeautifulSoup(targetPage,'html.parser')
        titleTags=bsPage.title.get_text()#.encode('gbk')
    except Exception,e:
        titleTags=''
    return  titleTags