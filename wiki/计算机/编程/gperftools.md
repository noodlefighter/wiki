## gperftools

> 参考：https://luyuhuang.tech/2022/04/10/gperftools.html#%E5%86%85%E5%AD%98%E5%88%86%E6%9E%90



### 使用gperftools分析堆内存使用情况

不用重新编译程序，直接每10s采集一次：

```
$ LD_PRELOAD=/usr/lib/libtcmalloc.so HEAPPROFILE=heap HEAP_PROFILE_TIME_INTERVAL=10 ./ebsx_qt5
```

导出分析：

```
$ pprof --pdf ./ebsx_qt5 heap.0002.heap > heap.pdf
```

