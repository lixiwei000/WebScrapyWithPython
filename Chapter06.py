'''
读取文档

'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
'''
纯文本文件
'''
# textPage = urlopen('http://www.pythonscraping.com/pages/warandpeace/chapter1.txt')
# for line in textPage.readlines():
#     print(line)

'''
编码类型
UTF-8   全球通用,8位是最小位数,一般是4字节-32位
ASCII   7位,可以表示128个字符,英文的文档够了
ISO标准  为每种语言都创建一种编码  ISO-8859-1 拉丁文字母
'''
# 显示俄文
# textPage = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
# print(str(textPage.read(),"utf-8"))

# 使用BS对文本进行U8转码
# html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
# bsObj = BeautifulSoup(html,"lxml")
# content = bsObj.find("div",{"id":"mw-content-text"}).get_text()
# content = bytes(content,"UTF-8")
# content = content.decode("UTF-8")
# print(content)

'''
CSV格式
'''
from io import StringIO
import csv
# data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode("ascii","ignore")
# dataFile = StringIO(data)
# csvReader = csv.reader(dataFile)
# for row in csvReader:               # csvReader是可迭代的
#     print("The album " + row[0] + " was released in " + str(row[1]))

# 不想要第一行没用的数据?
# data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode("ascii","ignore")
# dataFile = StringIO(data)
# dictReader = csv.DictReader(dataFile)
# print(dictReader.fieldnames)
# for row in dictReader:
#     print(row)

'''
PDF格式
'''
# from pdfminer.pdfinterp import PDFResourceManager,process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from io import StringIO
# from io import open
#
# def readPDF(pdfFile):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr,retstr,laparams=laparams)
#
#     process_pdf(rsrcmgr,device,pdfFile)
#     device.close()
#
#     content = retstr.getvalue()
#     retstr.close()
#     return content
#
# pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
# outputString = readPDF(pdfFile)
# print(outputString)
# pdfFile.close()

'''
Microsoft Word
'''
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

wordFile = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
wordFile = BytesIO(wordFile)
document = ZipFile(wordFile)
xml_content = document.read("word/document.xml")
# print(xml_content.decode("utf-8"))
# 使用BeautifulSoup解析word
wordObj = BeautifulSoup(xml_content.decode("utf-8"),"lxml")
textStrings = wordObj.findAll("w:t")
for textElem in textStrings:
    # 找到标题等其他样式文字
    # print(textElem.text)
    closeTag = ""
    try:
        style = textElem.parent.previousSibling.find("w:pstyle")
        if style is not None and style["w:val"] == "Title":
            print("<h1>")
            closeTag = "</h1>"
    except:
        # 不打印标签
        pass
    print(textElem.text)
    print(closeTag)



