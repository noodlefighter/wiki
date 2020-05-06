---



## linux内核的loglevel日志等级

```
[r@r-pc ~]$ cat /proc/sys/kernel/printk
1	4	1	4
```

这4个值在`kernel/printk.c` 中定义:

* 控制台日志级别DEFAULT_CONSOLE_LOGLEVEL：打印至控制台的日志等级

* 默认的消息日志级别DEFAULT_MESSAGE_LOGLEVEL：将用该优先级来打印没有优先级的消息

* 最低的控制台日志级别MINIMUM_CONSOLE_LOGLEVEL：控制台日志级别可被设置的最小值(最高优先级)

* 默认的控制台日志级别DEFAULT_CONSOLE_LOGLEVEL：控制台日志级别的缺省值



动态修改：

```
echo "7 4 1 7" > /proc/sys/kernel/printk
```


调试驱动时常用的配置：

```
# cat /proc/sys/kernel/printk
7	4	1	7
```



## 修改DEFAULT_CONSOLE_LOGLEVEL

如果需要修改，可以在内核启动时通过传参的方式修改（如在grub、uboot中传参启动）：

```
loglevel=3
```

也可以动态修改：

```
echo 3 > /proc/sys/kernel/printk
```

## 修改DEFAULT_MESSAGE_LOGLEVEL

可在内核编译时修改`CONFIG_MESSAGE_LOGLEVEL_DEFAULT`，Kconfig中帮助：

```

Symbol: MESSAGE_LOGLEVEL_DEFAULT [=4]
   Type  : integer
   Range : [1 7]
   Prompt: Default message log level (1-7)
     Location:
       -> Kernel hacking
   (1)   -> printk and dmesg options
     Defined at lib/Kconfig.debug:18

```

