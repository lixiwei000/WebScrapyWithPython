'''
存储数据
'''

# 使用urlretrieve根据url直接下载文件
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

# 入学年份-入学季节-学院-专业-班级-班级内个人编号
# 例如：07 1 02 01 0101
# 分别表示：07籍-秋季-经管学院-工商管理系-1班-1号。
# 11101010101
def downloadImg(start,stop):
    count = 0
    for sno in range(start,stop+1):
        stop1 = sno / 1000000 % 10  # 学院
        stop2 = sno / 10000 % 10    # 专业
        stop3 = sno / 100 % 100      # 班级
        stop4 = sno % 100           # 序号
        if stop1 >= 9 or stop2 >= 9 or stop3 >= 6 or stop4 > 60:
            continue
        print(sno)
        url = "http://jxxx.ncut.edu.cn/show_img.asp?xh=" + str(sno)
        path = "/Users/lixiwei-mac/Documents/student/"+str(sno)+".jpg"

        try:
            urlretrieve(url,path)
            if (os.path.getsize(path) < 10):
                os.remove(path)
            else:
                count = count + 1
                print("成功下载:" + str(sno),",第"+str(count)+"个用户")
        except:
            try:
                os.remove(path)
            except:
                pass
for year in range(11,19):
    # 11101010101
    downloadImg(year*1000000000+101010101,year*1000000000+109090660)