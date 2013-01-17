#_*_ coding=utf8 _*_
'''
解释器首先会解释@符号后面的代码，
如果如上面的代码类似，那么test(5)将被执行，
因为test参数5大于3，所以会返回一个函数指针plus（可以用C的这个名字来理解），
plus将下一行的函数指针xxx当作参数传入，直到执行完成。
最后结果将输出‘plus’和‘ok’。
'''
def minus(f):
    print 'minus'
    f()
 
def plus(f):
    print 'plus'
    f()
 
def test(a):
    if a > 3 : return plus
    else : return minus
 
@test(5)
def xxx():
    print 'ok'