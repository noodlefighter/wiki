# libc替代

## Libc

### msul libc

https://www.musl-libc.org/

为linux嵌入式设备设计的轻量C库，强调静态编译时的体积。


## 工具库

### tbox

https://github.com/tboox/tbox
A glib-like multi-platform c library 



### libite

libc缺失的函数，似乎在这个库里可以找到



## 格式化输出

### tinyprintf [BSD/LGPL]

https://github.com/cjlano/tinyprintf

The formats supported by this implementation are:

%% %c %d %i %o %p %u %s %x %X

功能比较全 支持利用宏剪裁 支持像"%4.4x" "%3d" "%lld"的格式

### mini-printf [BSD]

https://github.com/mludvig/mini-printf

Minimal printf() implementation for embedded projects.

%% %c %s %d %u %x %X

功能比较简单 只支持类似"%03d"这样的格式 无法支持像"%ld"这样的格式

### xprintfc [LGPL]

https://github.com/MarioViara/xprintfc

支持浮点数的libc sprintf替代 功能齐全 可用宏剪裁

