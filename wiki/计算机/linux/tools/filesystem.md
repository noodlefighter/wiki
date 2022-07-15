

---

## /dev/shm

一个ramdisk，可以往内存里放需要高速缓存的问题。

## linux访问NTFS盘报错：no object for d-bus interface

```
mount | grep gvfs
sudo umount -fl /run/user/（用户ID数字） gvfs
sudo rm -rf /run/user/（用户ID数字） gvfs
reboot
```



## Linux下挂载samba

Linux下mount samba到目录：

```
mount.cifs '\\r-wm\share' '/home/r/abc' -o username=my_user,password=123456,dir_mode=0777,file_mode=0777,uid=本地用户名,vers=1.0
```

用fstab来挂载：

```
//192.168.3.200/ebsx /mnt/ebsx cifs username=用户,password=密码,uid=本地用户名,iocharset=utf8,file_mode=0777,dir_mode=0777,noperm,vers=1.0 0 0
```

