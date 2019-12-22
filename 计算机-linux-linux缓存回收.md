title: linux缓存回收
date: 2019-09-06
categories:
- 计算机
- linux




---



```
# free
             total       used       free     shared    buffers     cached
Mem:         26892      13296      13596       2068        420       3320
-/+ buffers/cache:       9556      17336
Swap:            0          0          0
```

其中cached是内存中缓存，其中有一部分是可以用命令回收的。（比如`/dev/shm`里也占着空间，但无法被回收）

注意清Cache、swap并不是个必要的操作，可能会带来麻烦。

**江湖传言，保险起见sync要执行两次！因为这命令不可靠**

## Linux MemFree与MemAvailable的区别

> via: https://blog.51cto.com/xujpxm/1961072

2、MemFree：空闲内存数

  表示系统尚未使用的内存。MemUsed=MemTotal-MemFree就是已被用掉的内存。

3、MemAvailable：可用内存数

  应用程序可用内存数。系统中有些内存虽然已被使用但是可以回收的，比如cache/buffer、slab都有一部分可以回收，所以MemFree不能代表全部可用的内存，这部分可回收的内存加上MemFree才是系统可用的内存，即：**MemAvailable≈MemFree+Buffers+Cached**，它是内核使用特定的算法计算出来的，是一个估计值。**它与MemFree的关键区别点在于，MemFree是说的系统层面，MemAvailable是说的应用程序层面。**

## How to Clear RAM Memory Cache, Buffer and Swap Space on Linux

> via: <https://www.tecmint.com/clear-ram-memory-cache-buffer-and-swap-space-on-linux/>

### How to Clear Cache in Linux?

**1.** Clear PageCache only.

```
# sync; echo 1 > /proc/sys/vm/drop_caches
```

**2.** Clear dentries and inodes.

```
# sync; echo 2 > /proc/sys/vm/drop_caches
```

**3.** Clear PageCache, dentries and inodes.

```
# sync; echo 3 > /proc/sys/vm/drop_caches 
```

Explanation of above command.

**sync** will flush the file system buffer. Command Separated by `“;”` run sequentially. The shell wait for each command to terminate before executing the next command in the sequence. As mentioned in kernel documentation, writing to **drop_cache** will clean cache without killing any application/service, [command echo](https://www.tecmint.com/echo-command-in-linux/) is doing the job of writing to file.

If you have to clear the disk cache, the first command is safest in enterprise and production as `“...echo 1 > ….”` will clear the **PageCache** only. It is not recommended to use third option above `“...echo 3 >”` in production until you know what you are doing, as it will clear **PageCache**, **dentries** and **inodes**.

### How to Clear Swap Space in Linux?

you want to clear Swap space, you may like to run the below command.

```
# swapoff -a && swapon -a
```

Also you may add above command to a cron script above, after understanding all the associated risk.

Now we will be combining both above commands into one single command to make a proper script to clear RAM Cache and Swap Space.

```
# echo 3 > /proc/sys/vm/drop_caches && swapoff -a && swapon -a && printf '\n%s\n' 'Ram-cache and Swap Cleared'

OR

$ su -c "echo 3 >'/proc/sys/vm/drop_caches' && swapoff -a && swapon -a && printf '\n%s\n' 'Ram-cache and Swap Cleared'" root
```