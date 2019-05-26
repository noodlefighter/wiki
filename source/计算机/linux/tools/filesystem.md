

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