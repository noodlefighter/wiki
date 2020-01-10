---





## 复制资源文件夹到build目录



```
# copy "res" dir to build dir
copydata.commands = $(COPY_DIR) $$PWD/res $$OUT_PWD
first.depends = $(first) copydata
export(first.depends)
export(copydata.commands)
QMAKE_EXTRA_TARGETS += first copydata
```





## 安装



```
# 不指定files时，由qt自动推断需要安装的文件
target.path  += /opt/mytool
INSTALLS += target

# 指定files和安装的路径
res.files = res/*
res.path  = /opt/mytool/res
INSTALLS += res
```



用户使用时，指定prefix：

```
$ make install INSTALL_ROOT=my_rootfs/
```

