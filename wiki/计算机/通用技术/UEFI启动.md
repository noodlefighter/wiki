

refers:

* https://wiki.archlinux.org/index.php/EFI_system_partition
* https://wiki.manjaro.org/index.php?title=UEFI_-_Install_Guide



旧的启动方式，放在现在被称为“Legacy Boot”，这种方式下BIOS会根据启动顺序，挨个读取硬盘分区表里的启动代码（所谓的“引导区”），然后启动这段代码；所以安装OS时会覆盖这段启动代码。

而UEFI启动方式依靠的是EFI分区，有启动需求的OS、程序会在这个分区里加入自己的EFI文件，UEFI BIOS会启动EFI分区里的程序，不同OS能和谐共存。



## Linux下用efibootmgr管理UEFI启动项



```
[r-lm3 efi]# efibootmgr
BootCurrent: 0006
Timeout: 0 seconds
BootOrder: 0006,0004,0005,0002,0001,0000,0003
Boot0000* MsTemp
Boot0001* Internal Storage
Boot0002* USB Storage
Boot0003* PXE Network
Boot0004* manjaro
Boot0005* Windows Boot Manager
Boot0006* rEFInd Boot Manager
Boot0007* MsTemp

改变顺序
# efibootmgr --bootorder 0004,0006,0005,0002,0001,0000,0003
```



## UEFI启动例：Windows+Linux启动

分区例子：

```
Device             Start        End   Sectors   Size Type
/dev/nvme0n1p1      2048     616447    614400   300M Microsoft basic data
/dev/nvme0n1p2    618496     876543    258048   126M Microsoft reserved
/dev/nvme0n1p3    880640  630034431 629153792   300G Microsoft basic data
/dev/nvme0n1p4 630034432 1000214527 370180096 176.5G Linux filesystem
```

EFI分区为`FAT32`，带`ESP`标签，按Arch Linux的wiki的说法，空间至少260M。

一个装Win+Linux双系统的思路：

* 先清了硬盘，装Windows，安装程序就帮建好了EFI分区；

* 然后装Linux，装的时候指定EFI分区（把EFI分区挂载到`/boot/efi`），这时聪明点的发行版会帮在EFI启动项中创建GRUB2的启动项，就不用做额外操作了；

* 如果发行版的安装程序比较笨，仅添加了启动项没帮Windows加启动项，那就只能手动修复，安装rEFInd到EFI分区，它能自动列出存在的UEFI可启动项，很傻瓜很方便。命令参考：

  ```
  # pacman -S refind
  # refind-install
  ```

  

装了rEFInd+Windows+Manjaro Linux的EFI分区文件结构：

```
[r-lm3 efi]# tree -L 3
.
├── bootmgr
├── EFI
│   ├── manjaro
│   │   └── grubx64.efi
│   ├── Microsoft
│   │   ├── Boot
│   │   └── Recovery
│   ├── refind
│   │   ├── BOOT.CSV
│   │   ├── drivers_x64
│   │   ├── icons
│   │   ├── keys
│   │   ├── refind.conf
│   │   └── refind_x64.efi
```

