

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

