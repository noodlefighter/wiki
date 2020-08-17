

---

## 生成patch && 打patch

a为修改前，b为修改后。

单文件生成patch：
```
diff -up a/1.txt b/1.txt > patch
```

多文件生成patch：
```
diff -uprN a/ b/ > patch
```

打patch，需要切换到该目录中，用p1参数忽略第一级目录，因为目录名可能不同：
```
patch -p1 < patch1.diff
```



## 使用git生成UNIX Patch

直接用patch工具生成标准patch还是略麻烦，可以先生成git仓库，再用git生成patch：

```
临时做个git仓库
$ git init
$ git commit -am "init"

拷贝进来，打commit
$ cp ../b/* ./
$ git add file1 file2 file3
$ git commit -m "a little bit of work"

生成patch
$ git format-patch -1
```
