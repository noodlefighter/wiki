

---

## 屏蔽windows锁屏功能



```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System
```

建立DWORD值`DisableLockWorkstation`，值为1时禁止锁屏，`disale-win+l.reg`：

```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System]
"DisableLockWorkstation"=dword:00000001
```

