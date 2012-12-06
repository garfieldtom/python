#-*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:删除网页上有些代码前面的序号
#
# Author:      Administrator
#
# Created:     04-09-2012
# Copyright:   (c) Administrator 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re,sys


#其实可以使用正则的批量替换，此处使用笨办法逐行判断
def refile():
    #命令行输入
    argvc=len(sys.argv)
    if argvc==1:
        sf=input('请输入要转换的原文件名：')
        df=input('请输入要转换的目标文件名：')
    if argvc==2:
        sf=sys.argv[1]
        df=input('请输入要转换的目标文件名：')
    if argvc==3:
        sf=sys.argv[1]
        df=sys.argv[2]

    fr=open(sf,'r')
    fw=open(df,'w')
    pat=re.compile('\A(\s\d)|(\d{1,3})')
    s=fr.readline()
    while s:
       m=pat.match(s)
       if m:
          ss=re.sub(pat, '', s)
       else:
          ss=s
       fw.write(ss)
       s=fr.readline()
       
    fr.close()
    fw.close()

if __name__ == '__main__':
    refile()

