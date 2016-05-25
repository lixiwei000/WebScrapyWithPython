'''
Part I
这部分的六个章节是爬虫的基本功。
爬虫的基本工作流程：
    1.从网站获取HTML数据
    2.将数据转换成目标信息
    3.存储目标信息
    4.跳转到下一个页面继续处理

Chapter1 Your First Web Sracper
Internet交互:
    1.Client端发送0/1串代表高低电压，代表header、fromIP、destinationIP、destination Router's Mac 等
    2.Client将信息打包成数据包，发送到Internet
    3.数据包经过若干个中间服务器，最终定向到目标服务器
    4.目标服务器接收到数据包
    5.目标服务器的目标端口接收数据包
    6.目标服务应用程序解析数据包
    7.目标服务器定位html文件，并发送一个新的数据包给Client
'''

'''
Python2.x中得urllib2在Python3.x中被命名为urllib，并切分出了urlib.request,urllib.parse,urllib.error,urllib.response.
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

def urlopenTest():
    html = urlopen("http://pythonscraping.com/pages/page1.html")
    print(html.read())

'''
BeautifulSoup
'''
def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:#处理404 500等异常
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"lxml")
        title = bsObj.body.h1
    except AttributeError as e:# 如果没有bsObj没有目标属性则抛出异常
        return None
    if title == None:
        print("Title could not be found")
    else:
        print(title)

# getTitle("http://www.pythonscraping.com/pages/page1.html")
urlopenTest()
