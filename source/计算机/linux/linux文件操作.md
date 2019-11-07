

---

## 打开文件fopen

```c
#include <stdio.h>
FILE *fopen(char *filename,char *type); 
```

type为`<A>[B][C]`组合字符串.

A:

```
* r: 读, 指针设0, 不改变文件长度;
* w: 写, 文件不存在时文件被创建, 文件存在时文件长度设为0, 指针设为0;
* a: 追加写, 指针设为文件尾
```

B:
```
* b: 二进制方式打开 
* t: 文本方式打开
```

C:
```
* +: 可以同时input/output, 使用时必须注意用fflush或者fseek来防止内置buffer没消耗干净
```

## 读文件fread/写文件fwrite

```c
#include <stdio.h>
size_t fread(void *ptr, size_t size, size_t nmembFILE *stream );
size_t fwrite(const void *ptr, size_t size, size_t nmemb,
FILE *stream);
```

`fwrite()`的语义是写入`nmemb`个`size`大小的对象, 返回值为写入对象的数量(而不是总共的字节数).

## 空间预分配posix_fallocate

```c
#include <fcntl.h>
int posix_fallocate(int __fd, off_t __offset, off_t __len);
```

据说还有个linux版本的 <http://man7.org/linux/man-pages/man2/fallocate.2.html>: 
```c
#define _GNU_SOURCE      /* See feature_test_macros(7) */
#include <fcntl.h>
int fallocate(int fd, int mode, off_t offset, off_t len);
```

## 改变文件大小ftruncate

将文件大小改变为参数length指定的大小，如果原来的文件大小比参数length大，则超过的部分会被删除，如果原来的文件大小比参数length小，则文件将被扩展.

```c
#include <unistd.h>
int ftruncate (int __fd, __off_t __length);
```

注意这个操作不会改变当前指针, 比如缩小文件为0时, 并不会将指针置0.

## 将通过posix接口打开的文件改为非阻塞方式读

`fopen`和`popen`打开的文件，直接操作会是阻塞方式读，这里有个技巧：

```
fp = popen(path, "r");
if (NULL == fp) {
    LOG_ERR("%s:fail to open %s\n", __func__, path);
    return -1;
}
fcntl(fileno(fp), F_SETFL, O_NONBLOCK);

n = read(fileno(fp), buff, sizeof(buff));
if (n == -1 && errno == EAGAIN) {
	// no data yet, do nothing
}
else if (n > 0) {
	print_hex(buff, n);
}
else {
	// pipe closed
	LOG("n=%d, err=%d\n", n, errno);
}

```

