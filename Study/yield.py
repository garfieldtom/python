#_*_ coding=utf-8 _*_
'''
执行下面的代码，可以知道：获取函数迭代器时候，并不会执行函数的代码；第一次必须调用next，函数将执行到yield返回，
但yield表达式左边的ret并不会被赋值；send被调用的时候，yield左边的ret被赋值，代码运行到再次调用yield返回。
故包含yield的函数执行逻辑流程的周期可以总结为，从yield表达式左边的变量被赋值开始，执行完yield表达式的地方结束。
yield不同于return，可以理解为一个断点，return后所有状态都没有了，而yield还可以从断点继续。
'''

def show(i):
    while(1):
        i+=1
        ret = yield i
        print 'ret',ret
 
import time
f=show(0)
k=f.next()
print 'k',k
j=99
while(j):
    j+=1
    time.sleep(1)
    k=f.send(j)
    print 'k',k