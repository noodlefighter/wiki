---

从JS学习Lua：
https://www.jianshu.com/p/2037aa6f8030



## luac

luac能将.lua源码转成二进制码，加速加载过程，并不能独立运行执行，因为不是ELF而是lua虚拟机字节码。



## Lua C混编

详细指导：http://lua-users.org/wiki/BindingCodeToLua



## lua的包 管理器luarocks

使用例：

```
$ luarocks --lua-version 5.2 install bit
```

