title: linux的panic和oops
date: 2019-07-27
categories:
- 计算机
- linux
- kernel




---

panic和oops是linux的两种异常，前者是无法恢复的内核崩溃，后者是可恢复的（比如内核态的驱动模块崩溃）。

通常会希望内核在崩溃时自动重启，与两个内核配置相关：

```
CONFIG_PANIC_ON_OOPS:    
 
 Say Y here to enable the kernel to panic when it oopses. This    
 has the same effect as setting oops=panic on the kernel command  
 line.
 
 This feature is useful to ensure that the kernel does not do
 anything erroneous after an oops which could result in data 
 corruption or other issues.     
```

```
CONFIG_PANIC_TIMEOUT:    

 Set the timeout value (in seconds) until a reboot occurs when the  
 the kernel panics. If n = 0, then we wait forever. A timeout  
 value n > 0 will wait n seconds before rebooting, while a timeout  
 value n < 0 will reboot immediately.    
  
```

但工程里的做法一般是内核启动时动态传参：

```
        panic=          [KNL] Kernel behaviour on panic: delay <timeout>
                        timeout > 0: seconds before rebooting
                        timeout = 0: wait forever
                        timeout < 0: reboot immediately
                        Format: <timeout>
```

也可以通过动态修改这些文件来实现：

```
# ls /proc/sys/kernel/ |grep panic
panic
panic_on_oops
panic_on_warn
```

