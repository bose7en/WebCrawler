# coding=utf-8
__author__ = 'zhangbojian'
import urllib2 as ul2
from urlparse import urlparse
import ftplib

#获取接口信息
#接口数据会下载到项目目录
def downloadInterfaceDate():
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


