# coding=utf-8
__author__ = 'zhangbojian'
import urllib2 as ul2
from urlparse import urlparse
import ftplib

#获取接口信息
#接口数据会下载到项目目录
def downloadInterfaceDate(url,values):
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


