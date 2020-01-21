

---




```
# 创建用户 -m是创建home目录
useradd -m ebi

# 用户改密码
passwd ebi

# 创建组
$ sudo groupadd group
# 将当前用户添加到指定组
$ sudo gpasswd -a $USER group
```

<https://wiki.archlinux.org/index.php/users_and_groups>