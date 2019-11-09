

---

> via: https://en.cppreference.com/w/c/variadic/va_arg

```
#include <stdarg.h>
...
double stddev(int count, ...) 
{
    double sum = 0;
    double sum_sq = 0;
    va_list args;
    va_start(args, count);
    for (int i = 0; i < count; ++i) {
        double num = va_arg(args, double);
        sum += num;
        sum_sq += num*num;
    }
    va_end(args);
    return sqrt(sum_sq/count - (sum/count)*(sum/count));
}
```

va_arg(args, type)宏等效于返回`(type)*p_arg`并把`p_arg`向后移`sizeof(type)`。

所以其实C的不定参数是无法知道真实传参的大小的。

