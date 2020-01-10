

---

## 文本编码转换

https://blog.csdn.net/u012724167/article/details/77248919

```
# 转换目录下所有文件到UTF8
enca -L zh_CN -x UTF-8 *
```

但是不成功啊：
```
r@r-work /mnt/hgfs/project/osukb/osu-keyboard-v3/app $ enca -V -L zh_CN -x utf-8 keymap.c
enca: converting `keymap.c': UCS-2/CRLF/21..UTF-8
enca: librecode warning: Conversion leads to ambiguous output in `keymap.c'
```