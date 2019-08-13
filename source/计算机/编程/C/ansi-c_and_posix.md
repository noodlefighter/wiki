

---

ANSI-C & POSIX

## memmove

与memcpy区别在于允许from和to区域重叠时的行为是可预期的, 不会出现错误.

size为0时行为未定义.



## dup2实现重定向



把标准输出重定向到fd：

```
int fd = open("output.txt", O_RDWR|O_CREAT, 0666);
int replaced = dup2(fd, STDOUT_FILENO);
```



## printf格式

| 型                     | フォーマット |
| :--------------------- | :----------- |
| ssize_t                | %zd          |
| size_t                 | %zu          |
| int_max_t              | %jd          |
| intmax_t               | %ju          |
| signed char            | %hhd         |
| unsigned char          | %hhu         |
| short int              | %hd          |
| unsigned short int     | %hu          |
| int                    | %d           |
| unsigned int           | %u           |
| long int               | %ld          |
| unsigned long int      | %lu          |
| long long int          | %lld         |
| unsigned long long int | %llu         |