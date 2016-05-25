'''
Chapter2 Advanced HTML Parsing
1.BeautifulSoup的其他用法
    1.使用标签找内容  （Chapter1）
    2.使用属性找标签  （CSS等）
        <span class="red"></span>
2.查询所有class为green的span标签
bsObj.tagName会获取第一个标签
h2 = bsObj.h2
print(h2)
'''
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def findSpan():
    url = "http://pythonscraping.com/pages/warandpeace.html"
    html = urlopen(url)
    bsObj = BeautifulSoup(html,"lxml")
    # nameList = bsObj.findAll("span",{"class":"green","class":"red"})
    nameList = bsObj.findAll("span",{"class":"green"},limit=10)
    print(len(nameList))
    for name in nameList:
        print(name.get_text())

'''
bs4.element.ResultSet，ResultSet里存放的是Tag
print(nameList.pop())
一般调用get_text()在最后做，因为他只会返回标签下的text，其他内涵的标签和全部都不会取。


find()和findAll()
    findAll(tag, attributes, recursive, text, limit, keywords)
    find(tag, attributes, recursive, text, keywords)
    tag参数可以是一组findAll({"h1","h2","h3"})
    attributes参数可以是dict  findAll("span",{"class":"red","class":"green"})
    text参数  findAll(text="abc") 查找所有text为abc的标签内容
    limit参数  返回前x个
    recursive  默认为true  搜索子标签
    keywords  findAll(id="text")查找具有特定属性的标签
    以下两行是等价的,比如id=class就不能使用keyword方法解析，需要使用attributes方法，因为class是python的关键字
    那么keyword存在的意义呢？
        attributes参数的属性之间的关系都是or，如果需要and操作，就需要keyword来处理
        bsObj.findAll(id="text")
        bsObj.findAll("", {"id":"text"})

'''
def findSpan2():
    url = "http://pythonscraping.com/pages/warandpeace.html"
    html = urlopen(url)
    bsObj2 = BeautifulSoup(html,"lxml")
    spanTags = bsObj2.findAll("span")
    names = bsObj2.findAll("span",{"class":"green"},limit=10)
    pros = bsObj2.findAll(text="the prince")
    id_text = bsObj2.findAll(id="text")
    bsObj2.div.span
    print(spanTags)
    # print(id_text[0].get_text())

'''
BeautifulSoup的四种对象类型
BeautifulSoup Object   上面的bsObj
Tag Object             解析得到的标签对象
NavigableString Object 标签里面的text，而不是标签本身
Comment Object         HTML中的注释<!-- like this one -->
'''

'''
处理children和descendants   --孩子节点和后代节点
children指父节点的直接子节点，而descentants代表父节点下全部的子节点。后者包含前者。
使用bsObj.find返回的是BeautifulSoup类对象，而findAll返回的是ResultSet

处理sibling(兄弟节点)
bsObj.next_siblings()
返回当前节点的下一个兄弟节点，遍历输出时不会将第一个节点输出，原因如下：
1.节点不能是自己的兄弟节点
2.这个方法只是返回下一个兄弟节点
bsObj.previous_sibling() 获取前一个节点

处理parent父节点
获取当前节点的父节点，一般当前节点比较容易获取，通过这个节点找到父节点。或者当前节点处理完毕，需要返回父节点继续处理其他节点。
'''
def childTest():
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html,"lxml")
    for child in bsObj.find("table",{"id":"giftList"}).children:
        print(child)
    print("===============================================")
    for child in bsObj.find("table",{"id":"giftList"}).descendants:
        print(child)
    for sibling in bsObj.find("table",{"id":"giftList"}).tr.next_siblings:
        print(sibling)
    print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"
                            }).parent.previous_sibling.get_text())

'''
正则表达式
aa*bbbbb(cc)*(d | )
aa*:a至少出现一次
bbbbb:固定5个b
(cc)*:c需要成对出现，当然也可以是0对
(d| ):d或空

常用正则表达式
a*b*  出现0次或更多
a+b+  出现1次或更多
[A-Z]  选择
(a*b)*  组合出现0次或更多
a{2,3}b{2,3}  出现次数为2~3
[^A-Z]*  不包含
b(a|i|e)d  或
b.d  任意字符
^a  以a开头
\.\|\\  特殊字符
[A-Z]*[a-z]*$  小写字母结尾
^((?![A-Z]).)*$ 不能以大写字母开头结尾
'''

from urllib.parse import re
def mailRegex():
    # 右键的正则表达式
    regex = r"[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)"
    # 为什么括号内的+，不被定义成正则表达式的+,而是普通的符号
    # 字符组内部的元字符与字符组外部的元字符不一样。
    # 在字符组内部写某个字符出现一次或多次是没有意义的。
    # 因为字符组只表示一个字符，这个字符是它内部的任意一个。
    pattern = re.compile(regex)
    mail = "511958060@qq.com"
    pattern.match(mail)
    # Test
    regex = r"b[aie]d" # 等价于 b(a|i|e)d
    pattern = re.compile(regex)
    pattern.match("bid")

'''
如果仅仅使用BS来找tag，那么有可能会找到多余的tag，比如img标签，在页面中会比较多。
使用REGEX配合BS寻找会更加精确的找到目标tag

正则表达式配合BeautifulSoup查找Tag
mytag.attrs会得到这个tag的所有属性,tag[attrname]或tag.attrs[attrname]得到对应的属性值
'''
def bsWithRe():
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html,"lxml")
    images = bsObj.findAll("img",{"src":re.compile(r"\.\.\/img\/gifts\/img.*\.jpg")}) # * 是否是多余的？
    for image in images:
        print(image.attrs['src'])

'''
Lambda 表达式的使用
'''
def lambdaTest():
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html,"lxml")
    images = bsObj.findAll(lambda tag : len(tag.attrs) == 2) # * 是否是多余的？
    for image in images:
        print(image.attrs)