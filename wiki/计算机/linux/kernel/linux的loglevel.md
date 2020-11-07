---



## linux内核的loglevel日志等级

```
[r@r-pc ~]$ cat /proc/sys/kernel/printk
1	4	1	4
```

这4个值在`kernel/printk/printk.c` 中定义:

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



## Linux内核loglevel值的具体定义

定义在`./include/linux/kern_levels.h`中：

```
#define KERN_EMERG      KERN_SOH "0"    /* system is unusable */
#define KERN_ALERT      KERN_SOH "1"    /* action must be taken immediately */
#define KERN_CRIT       KERN_SOH "2"    /* critical conditions */
#define KERN_ERR        KERN_SOH "3"    /* error conditions */
#define KERN_WARNING    KERN_SOH "4"    /* warning conditions */
#define KERN_NOTICE     KERN_SOH "5"    /* normal but significant condition */
#define KERN_INFO       KERN_SOH "6"    /* informational */
#define KERN_DEBUG      KERN_SOH "7"    /* debug-level messages */
```

