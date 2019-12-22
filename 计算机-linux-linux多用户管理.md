title: linux多用户管理
date: 2019-06-15
categories:
- 计算机
- linux




---

```
# 创建组
$ sudo groupadd group
# 将当前用户添加到指定组
$ sudo gpasswd -a $USER group
```

<https://wiki.archlinux.org/index.php/users_and_groups>