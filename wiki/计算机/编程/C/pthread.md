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





## 从 pthread_t 获得 PID 和 TID

一个思路是找到偏移量，然后打印出来，问题是不同实现的偏移量不同，做法不能通用

```
int get_tid_from_pthread(pthread_t t)
{
	struct pthread_fake {
		void *nothing[90];
		pid_t tid;
	};

	struct pthread_fake* f = (struct pthread_fake*)t;
	return f->tid;
}

int get_pid_from_pthread(pthread_t t)
{
	struct pthread_fake {
		void *nothing[90];
		pid_t tid;
		pid_t pid;
	};

	struct pthread_fake* f = (struct pthread_fake*)t;
	return f->pid;
}

```

还是在线程里使用gettid()来得快（版本过早的glibc没有gettid()，改用syscall）：

```
#include <sys/types.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>

printf("thread %s: %d\n", This->name.c_str(), syscall(SYS_gettid));;
```







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
