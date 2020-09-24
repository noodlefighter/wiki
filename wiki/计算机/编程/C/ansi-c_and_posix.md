

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



## getopt()

```
	#include <unistd.h>
	
	const char *optstring = "ab:c"; // 参数有-a -b -c其中-b必须跟参数
	while ((opt = getopt(argc, argv, optstring)) != -1) {
        printf("opt = %c\n", opt);  // 命令参数，亦即 -a -b -c -d
        printf("optarg = %s\n", optarg); // 参数内容
        printf("optind = %d\n", optind); // 下一个被处理的下标值
        printf("argv[optind - 1] = %s\n\n",  argv[optind - 1]); // 参数内容	
    }
```

