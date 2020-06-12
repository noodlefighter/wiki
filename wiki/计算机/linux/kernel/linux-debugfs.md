# Linux debugfs

为了方便内核开发者在用户态下对内核态下的程序debug而设计的机制。



文档：https://www.kernel.org/doc/Documentation/filesystems/debugfs.txt

Kconfig内核选项：`CONFIG_DEBUG_FS`

```
mount -t debugfs none /sys/kernel/debug
```