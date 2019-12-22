title: windows技巧集
date: 2019-07-26
categories:
- 计算机
- windows




---

## 屏蔽windows锁屏功能



```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System
```

建立DWORD项`DisableLockWorkstation`，值为1时禁止锁屏。

