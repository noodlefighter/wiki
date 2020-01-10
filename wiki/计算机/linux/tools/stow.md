

---

之前一直在debian

Gnu Stow主要用来管理以makefile方式安装的程序。

原理是安装时指定prefix到用户管理的文件夹，stow可以帮忙在真正的sysroot下建立符号链接，需要删除程序的时候就不会删错删漏了。

## 使用Gnu Stow管理安装

> 参考: http://fatmouse.xyz/2016/03/07/2016-03-07-manage-package-using-stow/

建立stow文件夹

```bash
mkdir /usr/local/stow
```

安装程序时：

```bash
./configure --prefix=/usr/local/stow/ruby
make
sudo make install
```

安装后执行映射，创建软链接：

```bash
cd /usr/local/stow
sudo stow ruby
```

需要卸载程序时：

```bash
cd /usr/local/stow
sudo stow --delete ruby
rm -rf ruby
```



## 使用Gnu Stow管理linux配置文件

> 参考：http://brandon.invergo.net/news/2012-05-26-using-gnu-stow-to-manage-your-dotfiles.html

例如，假设您要管理Bash，VIM和Uzbl的配置。Bash在顶级目录中有几个文件; VIM通常在顶级和.vim目录中有.vimrc文件; 和Uzbl在`${XDG_CONFIG_HOME}/uzbl`和中有文件 `${XDG_DATA_HOME}/uzbl`。因此，您的主目录如下所示：

```
home/
    brandon/
        .config/
            uzbl/
                [...some files]
        .local/
            share/
                uzbl/
                    [...some files]
        .vim/
            [...some files]
        .bashrc
        .bash_profile
        .bash_logout
        .vimrc
```

然后，您将创建一个`dotfiles`子目录并将所有文件移动到那里：

```
home/
    /brandon/
        .config/
        .local/
            .share/
        dotfiles/
            bash/
                .bashrc
                .bash_profile
                .bash_logout
            uzbl/
                .config/
                    uzbl/
                        [...some files]
                .local/
                    share/
                        uzbl/
                            [...some files]
            vim/
                .vim/
                    [...some files]
                .vimrc
```

然后，执行以下命令：

```bash
$ cd ~/dotfiles
$ stow bash
$ stow uzbl
$ stow vim
```



## stow文件冲突的问题

欲stow的文件目前已经存在于target中时，stow会失败，此时：

* 使用`--override=.*`可以将强制覆盖其他stow包创建的符号链接
* 提示"existing target is neither a link nor a directory"，因为冲突的目标文件不是符号链接，只能手动删除，或者如果希望自动备份到stow包中（就是源）可以使用`--adopt`选项