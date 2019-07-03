



---

## i3wm



archlinux的Wiki：

https://wiki.archlinux.org/index.php/I3#Launching_programs_on_specific_workspaces

## i3命令

命令参考：https://i3wm.org/docs/userguide.html#list_of_commandsexec


### exec

```
# startup-id功能会确保GUI显示在工作区，执行无界面程序时最好禁用它
exec --no-startup-id xxx
```



## i3-cinnamon

cinnamon环境里的i3，可以使用cinnamon的设置、锁屏等

## dmenu-manjaro

manjaro的dmenu菜单，支持鼠标。

## i3status

状态栏

```
bar {
        status_command i3status
}
```

## i3exit

i3exit是个脚本集，需要在配置里做一个菜单来调用：

```
set $mode_system System (l) lock, (e) logout, (s) suspend, (h) hibernate, (r) reboot, (Shift>
mode "$mode_system" {
    bindsym l exec --no-startup-id i3exit lock, mode "default"
    bindsym e exec --no-startup-id i3exit logout, mode "default"
    bindsym s exec --no-startup-id i3exit suspend, mode "default"
    bindsym h exec --no-startup-id i3exit hibernate, mode "default"
    bindsym r exec --no-startup-id i3exit reboot, mode "default"
    bindsym Shift+s exec --no-startup-id $i3_path/i3exit shutdown, mode "default"
    # back to normal: Enter or Escape
    bindsym Return mode "default"
    bindsym Escape mode "default"
}
bindsym $mod+x mode "$mode_system"
```



## 锁屏

### i3lock

```
bindsym $mod+o exec i3lock -c 000000
```

-c指定背景颜色。

### i3exit的锁屏

背景不想纯色时，可以改用毛玻璃效果的`i3exit lock`。

### 使用cinnamon的锁屏

```
# 锁屏并黑屏
bindsym $mod+o exec "cinnamon-screensaver-command -l; xset dpms force off;"

# 单纯锁屏
bindsym $mod+o exec "cinnamon-screensaver-command -l"
```

## compton

淡入淡出、阴影，GUI配置界面`compton-conf`。

## 正在测试

suckless-tools

Rofi: A window switcher, application launcher and dmenu replacement

## 像其他环境中Alt+Tab循环切换焦点到下一个窗口

> via: https://gist.github.com/Nervengift/0ab9e6127ac17b8317ac

额外依赖：jq/awk

```bash
#!/bin/bash
# ================================================================================== #
# Focus the next window on the current workspace in i3, e.g. for binding to Alt+Tab  #
# Depends: jq, awk, i3wm (obviously)                                                 #
# Author: Nervengift <dev@nerven.gift>                                               #
# License: Don't think this deserves a license, Public Domain                        #
# Known bugs: doesn't work with non-window container focused                         #
# ================================================================================== #

ws=$(i3-msg -t get_workspaces|jq "map(select(.focused))[]|.name")
windows=$(i3-msg -t get_tree|jq ".nodes|map(.nodes[])|map(.nodes[])|map(select(.type==\"workspace\" and .name==$ws))[0].nodes|map(recurse(.nodes[]))|map(.window)|.[]|values")
current=$(i3-msg -t get_tree|jq "recurse(.nodes[])|select(.focused)|.window")
if [ "x$current" != "xnull" ]; then
	next=$(echo $windows | awk "BEGIN {RS=\" \";FS=\"   \"};NR == 1 {w=\$1};{if (f == 1){w=\$1;f=0}else if (\$1 == \"$current\") f=1};END {print w}")
	i3-msg [id=$next] focus > /dev/null
fi
```

i3加入配置：

```
bindsym $alt+Tab exec --no-startup-id ~/.config/i3/i3-focus-next
```

> 注意，虽然能实现功能，但是流畅度明显不行。。

## 特定工作区启动指定应用程序

```
exec --no-startup-id i3-msg 'workspace 1:Web; exec /usr/bin/firefox'
```

