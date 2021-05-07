

## C语言中的无符号数减法

```
#include <stdio.h>
#include <stdint.h>

int main (void)
{
        uint32_t a = UINT32_MAX, b = 1;
        int diff1 = a - b;
        int diff2 = b - a;

        printf("a-b=%d, b-a=%d\n", diff1, diff2);
        return 0;
}
```

输出：

```
a-b=-2, b-a=2
```

