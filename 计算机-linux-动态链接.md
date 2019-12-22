title: 动态链接
date: 2019-06-08
categories:
- 计算机
- linux


---

配置动态链接库目录的地方`/etc/ld.so.conf`，提示找不到库的时候修改。

```none
# 刷新动态库高速缓存，安装新库之后找不到.so文件时执行
sudo ldconfig
# 打印缓存中的内容
ldconfig -p
```



动态库搜索路径`LD_LIBRARY_PATH`

```
export LD_LIBRARY_PATH=/xxx/lib/:$LD_LIBRARY_PATH
```

