title: pthread
date: 2019-07-09
categories:
- 计算机
- 编程
- C


---
> TODO: 

https://randu.org/tutorials/threads/

---
> TODO: 

https://randu.org/tutorials/threads/

## 简单使用



```
pthread_t thread;
pthread_create(&thread, NULL, thr_func, NULL);
```

thr_func返回时，pthread仍保留着线程资源和返回值，直到使用`pthread_join`取走返回值并释放资源。



## 同步

### mutex 互斥锁

简单的锁, 常用.

### rwlock读写锁

仅在“并行读的次数远远大于写的次数”且“读占用时需要较多cpu时间”的场景使用.


因为rwlock的实现需要做更多的逻辑, 效率比简单的mutex差, 仅在满足上述条件的少数情况有使用的必要.



## 错误

### 错误1

```
Assertion `mutex->__data.__owner == 0' failed
```

> <https://blog.csdn.net/luckyapple1028/article/details/51588946>

### 错误2

```
__pthread_mutex_lock_full: Assertion `INTERNAL_SYSCALL_ERRNO (e, __err) != ESRCH || !robust' failed
```
