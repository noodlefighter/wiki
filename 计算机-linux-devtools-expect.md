title: expect
date: 2019-09-06
categories:
- 计算机
- linux
- devtools




---



Expect是Unix系统中用来进行自动化控制和测试的软件工具，相当于手动输入命令行。

替代品:python的pexpect.

参考：

https://www.ibm.com/developerworks/cn/education/linux/l-tcl/l-tcl-blt.html

## TCL语言

脚本语言，Tool Command Language，在仪表领域被用得很多。

## 主要命令

### expect/send

等待输出/输入

### spawn

创建进程

### interact



## autoexpect

用这调命令可以自动录制expect脚本

## expect操作串口



打开串口设备文件：

```
exec 5</dev/ttyS1
exec 6>/dev/ttyS1
read LINE <&5
echo "hello" >&6
```

