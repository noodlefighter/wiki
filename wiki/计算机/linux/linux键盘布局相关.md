

---

archlinuxu的wiki上的说明：

https://wiki.archlinux.org/index.php/Linux_console/Keyboard_configuration

loadkeys:

https://jlk.fjfi.cvut.cz/arch/manpages/man/loadkeys.1

问答：

https://superuser.com/questions/729585/remap-keys-without-xmodmap-or-any-x-tools#comment1565295_729585

https://stackoverflow.com/questions/34582279/linux-c-keymapping-keycodes

## 总结

在linux中，输入设备在input子系统中被抽象，如`/dev/input/event*`，我们能拿到的keycode在这里被归一。测试按键，获得keycode：

```
# showkeys
```

只有keycode是不足以在console上输入字符的，因为不同的键盘布局上的同一个键打出来的字符是不一样的，比如Shift+2在US布局里是“@”而欧洲布局里是欧元符号，所以linux还有一套从keycode转换到字符的机制。

从linux的map文件生成c语言数组的map表：

```
# loadkeys --mktable defkeymap.map
```

查看当前映射表：

```
# dumpkeys
```

