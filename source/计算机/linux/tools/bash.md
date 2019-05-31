---

CLI下方便的操作、相关工具。

## 基本操作

### 应用挂起、恢复

ctrl+z挂起
命令fg恢复

## 快捷操作

```
ctrl+u   ctrl+k   光标处往前删除/光标处往后删除
```

### pushd,popd命令

pushd：当前目录入目录栈，并进入到指定的目录
popd：跳转到目录栈顶部弹出的目录

### bd工具

https://linux.cn/article-8491-1.html

https://github.com/vigneshwaranr/bd

```
bd <需要导航到的目录的前几个字母>

# 比如当前目录是/d/tools/android-sdk-tools/tools/lib/x86
# 想要导航到tools目录，输入：
bd too

# 还可以这样获取路径，比如
ls `bd too`
```

### autojump工具

https://linux.cn/article-5983-1.html

工具会记录下cd过的路径，不用输入完整路径即可快速导航。
```
cd /etc/local/
cd /home
j local
```

## 给less加高亮显示

1. 装source-highlight
2. 修改`~/.bashrc`:
```
PAGER='less -X -M'
export LESSOPEN="| /usr/share/source-highlight/src-hilite-lesspipe.sh %s"
export LESS=' -R
```
3. 测试 `less -N abc.c`

## 让less颜色不消失的方法

https://qiita.com/mkasahara/items/60049ee20956e835738b

经常要用到例如`ls |less`，但会发现怎颜色消失了

```
ls -al --color=always | less -R
```

文中提到了用expect工具包中的unbuffer能解决，但实际使用发现无效。

## set命令

可以控制bash的行为，比如`set -e`使脚本在错误时退出bash。

查看帮助用`help set`命令：

```
-a allexport
   Flag variables for export when assignments are made to them.

-b notify
   Enable asynchronous notification of background job completion.
        (UNIMPLEMENTED)

-C noclobber
        Do not overwrite existing files with ``>''.

-E emacs
        Enable the built-in emacs(1) command line editor (disables the -V
        option if it has been set).

-e errexit 脚本遇错时退出

-f noglob
        Disable pathname expansion.

-I ignoreeof
        Ignore EOF's from input when in interactive mode.

-i interactive 强制shell表现为交互式的

-m monitor
        Turn on job control (set automatically when interactive).

-n noexec
        If not interactive, read commands but do not execute them.  This
        is useful for checking the syntax of shell scripts.

-P physical
        Change the default for the cd and pwd commands from -L (logical
        directory layout) to -P (physical directory layout).

-p privileged
        Turn on privileged mode.  This mode is enabled on startup if
        either the effective user or group id is not equal to the real
        user or group id.  Turning this mode off sets the effective user
        and group ids to therealuserand=groupids.  When this mode is
        enabled for interactive shells, the file /etc/suid_profile is
        sourced instead of ~/.profile after /etc/profile is sourced, and
        the contents of the ENV variable are ignored.

-s stdin
        Read commands from standard input (set automatically if no file
        arguments are present).  This option has no effect when set after
        the shell has already started running (i.e., when set with the
        set command).

-T trapsasync
        When waiting for a child, execute traps immediately.  If this
        option is not set, traps are executed after the child exits, as
        specified in IEEE Std 1003.2 (``POSIX.2'').  This nonstandard
        option is useful for putting guarding shells around children that
        block signals.  The surrounding shell may kill the child or it
        may just return control to the tty and leave the child alone,
        like this:
              sh -T -c "trap 'exit 1' 2 ; some-blocking-program"

-u nounset 展开未定义的变量时，报错退出

-V Vi 启用内置vi

-v verbose 输出详细信息，用于debug

-x 在执行每个命令前，将它打印输出
```

## win下给cmd.exe赋予unix系sh补全特性的工具

http://mridgers.github.io/clink/

好像不怎么用得到。。毕竟win下也能用bash