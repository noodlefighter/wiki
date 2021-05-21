

---



参考：

一个15分钟演讲，让你改变对gdb的看法：

https://undo.io/resources/cppcon-2015-greg-law-give-me-15-minutes-ill-change/

GDB 自动化操作的技术

https://segmentfault.com/a/1190000005367875

## gdb基本使用

> - 作者：大CC
> - 博客：[http://blog.me115.com](http://blog.me115.com/)
> - Github地址：<https://github.com/me115/linuxtools_rst>

GDB是一个由GNU开源组织发布的、UNIX/LINUX操作系统下的、基于命令行的、功能强大的程序调试工具。 对于一名Linux下工作的c++程序员，gdb是必不可少的工具；

## 启动gdb

对C/C++程序的调试，需要在编译前就加上-g选项:

```
$g++ -g hello.cpp -o hello
```

调试可执行文件:

```
$gdb <program>
```

program也就是你的执行文件，一般在当前目录下。

调试core文件(core是程序非法执行后core dump后产生的文件):

```
$gdb <program> <core dump file>
$gdb program core.11127
```

调试服务程序:

```
$gdb <program> <PID>
$gdb hello 11127
```

如果你的程序是一个服务程序，那么你可以指定这个服务程序运行时的进程ID。gdb会自动attach上去，并调试他。program应该在PATH环境变量中搜索得到。

## gdb中忽略某些SIG

比如需要忽略SIGPIPE，输入：

```
(gdb) handle SIGPIPE nostop noprint pass
```



## gdbserver远程调试

gdbServer + gdb 调试
https://www.cnblogs.com/Dennis-mi/articles/5018745.html

```
target$ gdbserver --multi :5678
```

```
# 连接到目标机
gdb> target extended-remote 目标机器IP:5678

# 指定目标程序路径
gdb> set remote exec-file 目标机器运行程序路径

# 设置动态库搜索路径
gdb> set solib-search-path /home/mpc/workspaces/build/sk01/target/lib/

# 指定本地程序，载入符号表
gdb> file 本地程序路径

# 退出gdbserver
gdb> monitor exit 
```

## gdb交互命令

启动gdb后，进入到交互模式，通过以下命令完成对程序的调试；注意高频使用的命令一般都会有缩写，熟练使用这些缩写命令能提高调试的效率；

### 运行

- run：简记为 r ，其作用是运行程序，当遇到断点后，程序会在断点处停止运行，等待用户输入下一步的命令。
- continue （简写c ）：继续执行，到下一个断点处（或运行结束）
- next：（简写 n），单步跟踪程序，当遇到函数调用时，也不进入此函数体；此命令同 step 的主要区别是，step 遇到用户自定义的函数，将步进到函数中去运行，而 next 则直接调用函数，不会进入到函数体内。
- step （简写s）：单步调试如果有函数调用，则进入函数；与命令n不同，n是不进入调用的函数的
- until：当你厌倦了在一个循环体内单步跟踪时，这个命令可以运行程序直到退出循环体。
- until+行号： 运行至某行，不仅仅用来跳出循环
- finish： 运行程序，直到当前函数完成返回，并打印函数返回时的堆栈地址和返回值及参数值等信息。
- call 函数(参数)：调用程序中可见的函数，并传递“参数”，如：call gdb_test(55)
- quit：简记为 q ，退出gdb

### 设置断点

- break n （简写b n）:在第n行处设置断点

  （可以带上代码路径和代码名称： b OAGUPDATE.cpp:578）

- b fn1 if a＞b：条件断点设置

- break func（break缩写为b）：在函数func()的入口处设置断点，如：break cb_button

- delete 断点号n：删除第n个断点

- disable 断点号n：暂停第n个断点

- enable 断点号n：开启第n个断点

- clear 行号n：清除第n行的断点

- info b （info breakpoints） ：显示当前程序的断点设置情况

- delete breakpoints：清除所有断点：

- watch/rwatch [变量名]：设置内存断点，写时中断/读写时中断

### 查看源代码

- list ：简记为 l ，其作用就是列出程序的源代码，默认每次显示10行。
- list 行号：将显示当前文件以“行号”为中心的前后10行代码，如：list 12
- list 函数名：将显示“函数名”所在函数的源代码，如：list main
- list ：不带参数，将接着上一次 list 命令的，输出下边的内容。

### 打印表达式

- print 表达式：简记为 p ，其中“表达式”可以是任何当前正在被测试程序的有效表达式，比如当前正在调试C语言的程序，那么“表达式”可以是任何C语言的有效表达式，包括数字，变量甚至是函数调用。
- print a：将显示整数 a 的值
- print ++a：将把 a 中的值加1,并显示出来
- print name：将显示字符串 name 的值
- print gdb_test(22)：将以整数22作为参数调用 gdb_test() 函数
- print gdb_test(a)：将以变量 a 作为参数调用 gdb_test() 函数
- display 表达式：在单步运行时将非常有用，使用display命令设置一个表达式后，它将在每次单步进行指令后，紧接着输出被设置的表达式及值。如： display a
- watch 表达式：设置一个监视点，一旦被监视的“表达式”的值改变，gdb将强行终止正在被调试的程序。如： watch a
- whatis ：查询变量或函数
- info function： 查询函数
- 扩展info locals： 显示当前堆栈页的所有变量
- `display /20i $pc`：查看当前汇编命令
- 

### 查询运行信息

- where/bt ：当前运行的堆栈列表；
- bt backtrace 显示当前调用堆栈
- up/down 改变堆栈显示的深度
- set args 参数:指定运行时的参数
- show args：查看设置好的参数
- info program： 来查看程序的是否在运行，进程号，被暂停的原因。
- i registers：查看当前寄存器值（缩写`i r`？）

### 多线程

- info threads 查看线程列表
- thread <Id>  切换当前线程

### 分割窗口

- layout：用于分割窗口，可以一边查看代码，一边测试：
- layout src：显示源代码窗口
- layout asm：显示反汇编窗口
- layout regs：显示源代码/反汇编和CPU寄存器窗口
- layout split：显示源代码和反汇编窗口
- Ctrl + L：刷新窗口

>  交互模式下直接回车的作用是重复上一指令，对于单步调试非常方便；


### 忽略SIG

例如：

```
gdb) handle SIGPIPE nostop
```

## TUI文本模式UI

`Ctrl+X,A`开启TUI，`Ctrl+X,2`开启汇编代码

查看浮点寄存器`tui reg float`

Up、Down键被TUI用了，而CLI的上翻、下翻变成了`Ctrl+P`和`Ctrl+N`



## GDB 反向调试（Reverse Debugging）

比如在一个循环中某些情况下才触发的错误，得等到触发了程序才停下来。

```
watch 
reverse-continue
```


## GDB中使用python 

Or you can even set breakpoints in python:

```
python gdb.Breakpoint(‘7’)
```

## GDB脚本

* GDB启动时，会在当前目录下查找`.gdbinit`，存在则会自动执行脚本

* GDB运行期间可以使用 `source <file>` 来执行GDB脚本

