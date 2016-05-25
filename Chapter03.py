'''
Chapter3
开始真正的爬虫，之前都是针对单个静态页面进行页面分析，但是爬虫一般都是对多个页面进行爬取。
爬取步骤：
    1.设置种子节点,加入到爬取队列。
    2.从队列中提取一个url，爬取当前页面，将页面内符合规则的url添加到爬取队列。
    3.判断url队列是否为空，不为空跳转到1
    ps:可以设置一个随机数，让每次取url都是随机的
Tip：随机数
    使用随机数之前，需要给随机数设置一个种子，不同的种子得到的随机数列不同，但是如果种子相同，那么随机数列也会相同。
    因此最好使用时间作为种子
    递归
    如果爬取内容时，为了继续爬取子url，肯呢会使用递归，python默认递归深度为1000，超过1000会报错。
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import datetime
import random
import re

def getLinks(articleUrl):
    try:
        html = urlopen("http://en.wikipedia.org"+articleUrl)
        bsObj = BeautifulSoup(html,"lxml")
        title = bsObj.h1.get_text()
        detail = bsObj.find(id="bodyContent").find(id="siteSub").get_text()
        print("Title:"+title+",Detail:"+detail+"\n")
    except AttributeError as e1:
        print("当前页面缺少响应的标题或副标题")
    except HTTPError as e2:
        print("HTTP连接错误")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",
                                                           href=re.compile("^(/wiki/)((?!:).)*$"))

def WikiSpider():
    links = set(getLinks("/wiki/Mao_Zedong"))
    crawled = list()
    while len(links) > 0:
        newArticle = links.pop().attrs["href"]
        crawled.append(newArticle)
        #     print(newArticle,"links_len:",len(links))
        for link in getLinks(newArticle):
            if link not in crawled:
                links.add(link)


'''
百度百科
'''

def getLinks(articleUrl):
    try:
        html = urlopen("http://baike.baidu.com"+articleUrl)
        bsObj = BeautifulSoup(html,"lxml")
        title = bsObj.h1.get_text()
        print("Title:"+title)
        detail = bsObj.h3.get_text()
        print("Detail:"+detail)
    except AttributeError as e1:
        print("当前页面缺少响应的标题或副标题")
    except HTTPError as e2:
        print("HTTP连接错误")
    print("--------------------------------")
    return bsObj.find("body").findAll("a",
                                      href=re.compile("^(/view/)"))
def baiduSpider():
    links = set(getLinks("/view/22806.htm"))
    crawled = list()
    while len(links) > 0:
        newArticle = links.pop().attrs["href"]
        crawled.append(newArticle)
        #     print(newArticle,"links_len:",len(links))
        for link in getLinks(newArticle):
            if link not in crawled:
                links.add(link)
'''
爬取整个网站内部链接、网站外部链接
更加通用的爬取方式，根据获取的域名来判断内部网址和外部网址
更加灵活，网址可以随意输入。
'''


pages = set()
random.seed(datetime.datetime.now())
# 获取所有的内部链接
def getInternelLinks(bsObj,includeUrl):
    internalLinks = []
    for link in bsObj.findAll("a",{"href":re.compile(r"^(/|.*" + includeUrl + ")")}):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# 获取所有外部链接
def getExternalLinks(bsObj,excludeUrl):
    externalLinks = []
    for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks
# 从链接中获取域名
def splitAddress(address):
    addressParts = address.replace("http://","").split("/")
    return addressParts
# 从外部链接中随机获取一条url
def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html,"lxml")
    externalLinks = getExternalLinks(bsObj,splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternelLinks(bsObj,startingPage)
        return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0,len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)

def followInternalOnly(startingSite):
    try:
        html = urlopen(startingSite)
    except ValueError as e:
        print("解析url失败")
    bsObj = BeautifulSoup(html,"lxml")
    internalLinks = getInternelLinks(bsObj,splitAddress(startingSite)[0])
    link = internalLinks[random.randint(0,len(internalLinks)-1)]
    print("Get internal link: " + link )
    internalLinks.pop()
    followInternalOnly(link)

# 获取全部内链接外链接
allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html,"lxml")
    internalLinks = getInternelLinks(bsObj,splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj,splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            print("Abount to get link:" + link)
            try:
                allIntLinks.add(link)
                getAllExternalLinks(link)
            except ValueError as e:
                print("地址信息异常:",e)

# followExternalOnly("http://oreilly.com")
getAllExternalLinks("http://oreilly.com")

'''
本书知识概述,没有详细讲解,具体参考官方文档
Scrapy
scrapy startproject wikiSpider
目录结构:
-wikiSpider
    - __init.py__
    - items.py
    - pipelines.py
    - settings.py
    - spiders
'''