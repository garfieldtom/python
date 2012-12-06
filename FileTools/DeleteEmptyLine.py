#-*- coding:utf-8 -*-
'''
删除文件中的空行
'''

import re,sys

#TODO:使用正则表达式批量替换
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
    s=fr.read()
    print(s)
    result, number = re.subn('(^\r)', '', s) 
    
    fw.write(s)
       
    fr.close()
    fw.close()
    
#最笨的办法，逐行判断  :-(
def refilelinebyline():
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
        
    print("开始处理文件....")    
    fr=open(sf,'r')
    fw=open(df,'w')
    s=fr.readline()
    print("s:"+s)
    while s:
       ss=s.strip()
       print("ss:"+ss+"#")
       if ss!="":
          print("写入新文件:"+ss)
          fw.write(s)
       s=fr.readline()
       
    fr.close()
    fw.close()

if __name__ == '__main__':
    #refilelinebyline()
    refile()

