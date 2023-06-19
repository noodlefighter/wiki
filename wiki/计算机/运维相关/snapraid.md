## snapraid基本使用

备份：
```
# snapraid sync
```

恢复部分文件：

```
# snapraid fix -f FILENAME
```

整个磁盘恢复：

```
# snapraid -d d1 -l recovery.log fix
```

