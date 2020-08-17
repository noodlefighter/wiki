

---



参考： http://zetcode.com/articles/cdatetime/

时间格式化：https://www.cnblogs.com/kaituorensheng/p/3922919.html



## C语言 打时间戳 tick-tock

```
#include <time.h>
#include <stdio.h>

start_t = clock();
lv_task_handler();
end_t = clock();
total_t = (end_t - start_t) * 1000 / CLOCKS_PER_SEC; // ms
if (total_t >= 1)
	printf("%dms\n", total_t);
```

