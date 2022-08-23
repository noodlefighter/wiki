

## scons交叉编译

参考：
Scons 简单入门
https://www.jianshu.com/p/e4bd3ab9e5d6

http://leng521.top/posts/79065537/
http://leng521.top/posts/66615451/

https://blog.csdn.net/arag2009/article/details/17392653


https://stackoverflow.com/questions/23898584/how-can-i-use-a-cross-compiler-with-scons

https://stackoverflow.com/questions/13161690/how-to-tell-scons-to-use-mingw-instead-of-msvc



## scons继承运行环境



```
env = Environment(ENV=os.environ.copy())
```





## scons中使用pkg-config

> refer: https://scons.org/doc/2.0.1/HTML/scons-user/c1882.html



```

    env = Environment()
    env.ParseConfig("pkg-config x11 --cflags --libs")
    env.ParseConfig("pkg-config x11 --cflags --libs")
    print env['CPPPATH']
 

    % scons -Q
    ['/usr/X11/include']
    scons: `.' is up to date.
```

