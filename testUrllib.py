# coding=utf-8
__author__ = 'zhangbojian'
import urllib2 as ul2
from bs4 import BeautifulSoup
import chardet
link='http://www.595555.com'
targetPage=ul2.urlopen(link,timeout=120).read()
bsPage=BeautifulSoup(targetPage,'html.parser')
titleTags=bsPage.title.get_text().encode('gbk')
fileout=open('out.txt',mode='a')
fileout.write(link+':'+titleTags+'\r')
fileout.write(link+':'+titleTags+'\r')
fileout.close()
