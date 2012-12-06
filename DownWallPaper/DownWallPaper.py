#-*- encoding:utf-8  -*-
'''
自动下载壁纸，太平洋电脑网壁纸，http://wallpaper.pconline.com.cn
By garfieldtom,2012
python ver:python 3

感谢   枫叶饭团  提供解答，软件取回内容有压缩
'''

import re,urllib.request
import gzip

#获得页面内容
def downwallpapers(url):
    urlcontent=geturlcontent(url)
    imglist=getimglist(urlcontent)
    for img in imglist:
        downimg(img)
    

def geturlcontent(url):
    #返回页面内容
    doc = urllib.request.urlopen(url).read()
    #解码,有些是压缩的，或者说有时是压缩的，随机？？没搞懂
    try:
        html=gzip.decompress(doc).decode("gbk")
    except:
        html=doc.decode("gbk")
    return html

#下载图片
def downimg(url):
    imgdir ='/home/xxh/图片/wallpapers/'
    filename = imgdir + url.split("/")[-1]
    print("准备下载................")
    print("url:"+url)
    print("filename:"+filename)
    urllib.request.urlretrieve(url, filename)
    
#取图片链接
def getimglist(doc):
    #取照图图片地址
    regImg =  '<td class="show_mainbox"><img src=\'(.*?)\''
    imglist = re.findall(regImg,doc)
    #print(imglist)
    return imglist
    

if __name__=="__main__":
    for i in range(1,11):
        print('开始下载第%d个....' % i)
        #打开http://wallpaper.pconline.com.cn，选择一个系列，然后打开一个图片，打开原图，地址就是类似下面的样子
        #然后是系列的序号，总个数参考网页，其实可以从网页上抓取，偷懒了  :-)
        url="http://wallpaper.pconline.com.cn/picsource/12721_"+str(i)+".html"
        downwallpapers(url)