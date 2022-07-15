---

## rsync同步工具

```
# 本地文件夹同步
rsync -av <源目录> <目标目录>
```


---

## rsync同步工具

```
# 本地文件夹同步
rsync -av <源目录> <目标目录>

# 复制符号链接
rsync -l
# 复制符号连接对应的文件
rsync -L
```



## 报错chgrp.....permission denied

去掉-a就不会执行这操作了



