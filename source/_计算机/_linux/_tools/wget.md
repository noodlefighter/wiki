

---

## 用wget批量下载镜象站

像经常能见到类似`https://mirrors.edge.kernel.org/pub/`的站点，偶尔下几个文件的话，浏览器直接下载就好，但如果想整个下载下来就很费力，可以用wget批量下载：

```
wget -r -nd -np -l1 https://mirrors.xxxxx.org
```

-nd 不创建目录, wget默认会创建一个目录
-r 递归下载
-l1 (L one) 递归一层,只下载指定文件夹中的内容, 不下载下一级目录中的

