

---



## 救援模式

linux无法启动时，可以进LiveCD，mount整个rootfs，然后chroot，再进行修复操作，如：

```
$ su -
# mkdir rootfs
# mount /dev/sdb2 rootfs
# mount /dev/sdb1 rootfs/boot/efi
# mv /dev ./rootfs/
# mv /proc ./rootfs/
# cd rootfs
# chroot .
```

在archlinux下，使用arch-chroot替代chroot，无需移动设备文件，如：

```
$ sudo pacman-mirrors -c China
$ sudo pacman -Sy
$ sudo pacman -S arch-install-scripts
$ su -
# mkdir rootfs
# mount /dev/sdb2 rootfs
# mount /dev/sdb1 rootfs/boot/efi
# cd rootfs
# arch-chroot .
```



## 重建grub配置

```
# grub-mkconfig -o /boot/efi/grub/grub.cfg
```

## 管理内核

使用指定内核的最简单的方法，`/boot`中用不到的内核镜象全删了，重建grub配置即可。