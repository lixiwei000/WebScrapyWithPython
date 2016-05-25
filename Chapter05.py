'''
Chapter05-存储数据
'''

# 使用urlretrieve通过url直接存储文件
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

'''
5.1 下载媒体文件
'''

# 下载迅播影院首页所有图片
def downloadImgFromXunBo():
    html = urlopen("http://www.xiamp4.com/")
    bsObj = BeautifulSoup(html,"lxml")
    imageLocation = bsObj.findAll("img")
    # imageAlt = bsObj.findAll("img")["alt"]
    print(len(imageLocation))
    for image in imageLocation:
        urlretrieve(image["src"],"/Users/lixiwei-mac/Documents/IdeaProjects/PythonWebScrapy/download/xunbo/"+image["alt"].split("/")[-1]+".jpg")
        print("成功下载",image["alt"])

# 整理IMG下载路径
def getAbsoluteURL(baseUrl,source):
    if source.startswith("http://www"):
        url = "http://" + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source.replace("www.","http://")
    else:
        url = baseUrl + "/" + source
    if baseUrl not in url:
        return None
    print(url)
    return url
# 获取本地图片存储路径
def getDownloadPath(baseUrl,absoluteUrl,downloadDirectory):
    path = absoluteUrl.replace("www.","")
    path = path.replace(baseUrl,"")
    path = downloadDirectory + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)
    return path

# Main:开始下载
def downloadImgFromPS():
    downloadDir = "/Users/lixiwei-mac/Documents/IdeaProjects/PythonWebScrapy/download/pythonscraping"
    baseUrl = "http://pythonscraping.com"

    html = urlopen("http://www.pythonscraping.com")
    bsObj = BeautifulSoup(html)
    downloadList = bsObj.findAll(src=True)

    for download in downloadList:
        fileUrl = getAbsoluteURL(baseUrl,download["src"])
        if fileUrl is not None:
            print(fileUrl)
            urlretrieve(fileUrl,getDownloadPath(baseUrl,fileUrl,downloadDir))

# downloadImgFromPS()

'''
5.2 把数据存储到CSV
'''
import csv

def csvTest():
    path = "/Users/lixiwei-mac/Documents/IdeaProjects/PythonWebScrapy/download/csv/1.csv"
    csvFile = open(path,"w")
    try:
        writer = csv.writer(csvFile)
        writer.writerow(("n ","n+2","n*n"))
        for i in range(10):
            writer.writerow((i,i+2,i*i))
    finally:
        csvFile.close()

# csvTest()
# 从wiki下载一个table存储到csv
def downTableFromPS():
    html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
    bsObj = BeautifulSoup(html,"lxml")

    table = bsObj.findAll("table",{"class":"wikitable"})[0]     # 获取第一个Table
    rows = table.findAll("tr")                                  # 获取Table中所有<tr>

    csvFile = open("/Users/lixiwei-mac/Documents/IdeaProjects/PythonWebScrapy/download/csv/wiki_table.csv","wt",newline='',encoding="utf-8")
    writer = csv.writer(csvFile)

    try:
        for row in rows:    # 遍历table的每一行
            csvRow = []
            for cell in row.findAll(['td','th']):
                csvRow.append(cell.get_text())              # 将tb和th都存入数组,逗号分隔
            writer.writerow(csvRow)                         # 以行为单位存储
    finally:
        csvFile.close()

# downTableFromPS()

'''
5.3 使用Mysql
获取迅播影院龙珠下载链接
'''

import pymysql
import datetime
import random
import re
def mysqlTest():
    conn = pymysql.connect(host = '127.0.0.1',user="root",passwd="lxw1993822",db="test")
    cur = conn.cursor()
    cur.execute("select * from user")
    print(cur.fetchall())
    cur.close()
    conn.close()

conn = pymysql.connect(host = '127.0.0.1',user="root",passwd="lxw1993822",db="test")
cur = conn.cursor()
random.seed(datetime.datetime.now())
# 插入数据
def store(title,content):
    cur.execute("insert into wiki(title,content) values(\"%s\",\"%s\")",(title,content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html,"lxml")
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div",{"id":"mw-content-text"}).find("p").get_text()
    store(title,content)
    return bsObj.find("div",{"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

def mysqlTest2():
    links = getLinks("/wiki/Kevin_Bacon")
    try:
        while len(links) > 0:
            newArticle = links[random.randint(0,len(links) - 1)].attrs["href"]
            print(newArticle)
            try:
                links = getLinks(newArticle)
            except:
                print("重复title")
    finally:
        cur.close()
        conn.close()

mysqlTest2()
