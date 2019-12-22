title: 缩小镜象文件
date: 2019-06-08
categories:
- 计算机
- linux
- tools




---

```
# 创建回环设备，但不挂载
losetup /dev/loop0 ./qt.img
# 置零空闲数据
zerofree -v /dev/loop0
# 断开回环设备
losetup -d /dev/loop0
# 文件系统检查
e2fsck -f qt.img
# 缩减空间
resize2fs -M qt.img
```

