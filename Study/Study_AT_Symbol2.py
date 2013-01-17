#_*_ coding=utf-8 _*_
'''
minus因为本身已经是一个函数指针，
所以会直接以xxx作为参数传入，结果会输出‘minus’和‘ok’。
'''
def minus(f):
    print 'minus'
    f()
 
@minus
def xxx():
    print 'ok'