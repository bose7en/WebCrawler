# coding=utf-8
__author__ = 'zhangbojian'
import urllib2 as ul2
import zipfile
import MySQLdb
import datetime
import GetInertMessage
import GetInterfaceData


#取接口数据，下载到项目目录
GetInterfaceData.downloadInterfaceDate()

#解压数据，获取其中的url
zp=zipfile.ZipFile('data.zip')
fileall=zp.open(zp.namelist()[0],pwd='Gmcc_345')
link=fileall.readline()[:-2]
while link:
    #对URL进行爬虫操作
    try:
        targetPage=ul2.urlopen(link,timeout=120).read()
        #挖掘关键字
        keyword=GetInertMessage.getKeyword(targetPage)
        monneyStr=keyword['钱物相关']
        busiStr=keyword['业务相关']
        #获取域名信息
        whoisMes=GetInertMessage.getWhoisMes(link)
        domainReg=whoisMes['注册商']
        domainContact=whoisMes['联系人']
        domainUpTime=whoisMes['更新时间']
        domainCreTime=whoisMes['创建时间']
        domainDowTime=whoisMes['过期时间']
        #获取title
        titleTags=GetInertMessage.getTitle(targetPage)

        #插入数据库
        conn=MySQLdb.connect(host='10.245.254.55',user='stcluster',passwd='ST.cluster',db='clusterdb',port=8066,charset='utf8')
        cur=conn.cursor()
        today=datetime.date.today().strftime("%Y%m%d")
        insert_sql="insert into tb_storm_usr_url_info(STAT_DT,url,spider_title,spider_kw,spider_kw2,whois_reg,whois_create_time,whois_update_time,whois_down_time,whois_connect) " \
                   "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(today,link,titleTags,monneyStr,busiStr,domainReg,domainCreTime,domainUpTime,domainDowTime,domainContact)
        cur.execute(insert_sql)
        cur.close()
        conn.commit()
        conn.close()
    except Exception,e:
        print '3',link,e.message
    link=fileall.readline()[:-2]
fileall.close()




