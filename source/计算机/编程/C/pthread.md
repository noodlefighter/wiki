<<<<<<< Updated upstream

---
> TODO: 

https://randu.org/tutorials/threads/

=======
---
> TODO: 

https://randu.org/tutorials/threads/

## 简单使用



```
pthread_t thread;
pthread_create(&thread, NULL, thr_func, NULL);
```



## 同步

### mutex 互斥锁

简单的锁, 常用.

### rwlock读写锁

仅在“并行读的次数远远大于写的次数”且“读占用时需要较多cpu时间”的场景使用.

因为rwlock的实现需要做更多的逻辑, 效率比简单的mutex差, 仅在满足上述条件的少数情况有使用的必要.
>>>>>>> Stashed changes
