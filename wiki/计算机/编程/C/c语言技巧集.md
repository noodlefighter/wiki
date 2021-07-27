

## C语言结构体赋值技巧

```
#include <stdio.h>

struct test {
        int a;
        int b;
};
int main (void)
{
        struct test my_test;
        int c = 114514;

        my_test = (struct test) { 
        	.a = c, 
        	.b = c + 1
        };                               // <=== 这样赋值也是可以的
        printf("my_test {a=%d, b=%d}\n", my_test.a, my_test.b);
        return 0;
}
```



## strnlen 与 memchr

`strnlen()`是 POSIX 函数，检查字符串长度是否合法，又需要纯 ANSI C 时，可以被`memchr()`代替：

```
if (NULL == memchr(str, '\0', max_len)) {
	// over max_len
}
```

