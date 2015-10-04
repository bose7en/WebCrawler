# coding=utf-8
__author__ = 'chinamobile'
import urllib2 as ul2
from urlparse import urlparse
import ftplib
import zipfile
from bs4 import BeautifulSoup
import MySQLdb
import datetime
'''
#获取接口信息
url="http://10.245.254.110:8080/etl_platform/rest/service.shtml"
values="{\"identify\": \"87da5cdc-6b4a-48f6-8014-470441b66383\", \"userName\":\"ST_BIGDATA\",\"password\":\"Gmcc_345\",\"systemName\":\"STORM\",\"parameter\":{\"rn1\":\"1\",\"rn2\":\"600000\"}}"
send_headers={"Content-Type":"application/json"}
req=ul2.Request(url,values,headers=send_headers)
response=ul2.urlopen(req)
rp_content=response.read()
ftp_mes=eval(rp_content)
#获取接口返回的FTP的数据
ftpurl=urlparse(ftp_mes['ftpPath'])
ftp = ftplib.FTP(ftpurl.hostname)
ftp.login(ftp_mes['ftpUserName'],ftp_mes['ftpPassword'])
ftp.retrbinary('RETR '+ftpurl.path, open('data.zip', 'wb').write)
'''
#解压数据，获取其中的url
zp=zipfile.ZipFile('data.zip')
fileall=zp.open(zp.namelist()[0],pwd='Gmcc_345')
link=fileall.readline()[:-2]
keyword={'钱物相关':["银行","汇款","现金","领取","储蓄卡","信用卡","人民币","转账","身份证","款项","预存","缴费","充值","兑换","话费","余额"],
         '业务相关':["积分","号码卡","套卡","促销","中国移动","广东移动","汕头移动","沟通100","移动","电信","联通","全球通","动感地带","神州行","大众卡","网聊卡","流量王","免费打电话","免费通话","免费上网","畅听卡","畅聊卡","流量卡"]}

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
    return [domainReg,domainContact,domainUpTime,domainCreTime,domainDowTime]

i=0
while link and i<10:
    i=i+1
    #对URL进行爬虫操作
    try:
        targetPage=ul2.urlopen(link,timeout=120).read()
        #挖掘关键字
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
        #获取域名信息
        whoisMes=getWhoisMes(link)
        #获取title
        try:
            bsPage=BeautifulSoup(targetPage,'html.parser')
            titleTags=bsPage.title.get_text()#.encode('gbk')
        except Exception,e:
            print '2',link,e.message
            titleTags=''
        #插入数据库
        conn=MySQLdb.connect(host='10.245.254.55',user='stcluster',passwd='ST.cluster',db='clusterdb',port=8066,charset='utf8')
        cur=conn.cursor()
        today=datetime.date.today().strftime("%Y%m%d")
        insert_sql="insert into tb_storm_usr_url_info(STAT_DT,url,spider_title,spider_kw,spider_kw2,whois_reg,whois_create_time,whois_update_time,whois_down_time,whois_connect) " \
                   "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(today,link,titleTags,monneyStr,busiStr,whoisMes[0],whoisMes[3],whoisMes[1],whoisMes[4],whoisMes[2])
        cur.execute(insert_sql)
        cur.close()
        conn.commit()
        conn.close()
    except Exception,e:
        print '3',link,e.message
    link=fileall.readline()[:-2]
fileall.close()


'''
import httplib

h3=httplib.HTTPConnection('10.245.254.110:8080')
h3.request('POST','/etl_platform/rest/service.shtml',values)
reponse2=h3.getresponse()
rp_content2=reponse2.read()
ftp_mes=eval(rp_content2)
'''
'''
import ftplib
ftp = ftplib.FTP("10.245.254.18")
ftp.login("sjsn","ST.sJsN.12#")
ftp.cwd('/WEB/02c3ccf8-c90a-4605-9ae7-9d58fe0c38d0')
#ftp.retrlines('LIST /WEB/ca3e5a15-7a41-42c1-bb7f-3dd7ece6d469')
ftp.retrbinary('RETR /WEB/ca3e5a15-7a41-42c1-bb7f-3dd7ece6d469/data.zip', open('test.zip', 'wb').write)

import zipfile
openfile=open('data.zip')


zipFile=zipfile.ZipFile('data.zip')
fileall=zipFile.open(zipFile.namelist()[0],pwd='Gmcc_345')
filechunk=fileall.readlines(100)
cnt=0
while filechunk:
    cnt=cnt+len(filechunk)
    filechunk=fileall.readlines(100)

zipFile.extract(zipFile.namelist()[0],pwd='Gmcc_345')
'''