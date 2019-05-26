---



图形界面:
gitkraken   据说好用的git图形界面


```bash
# 检出分支到本地新分支、覆盖工作区
git checkout -f -B branchabc remotes/origin/branchabc --

# 添加gpg签名密钥
git config --global user.signingkey 0A46826A
```

### 无法显示中文问题

```
git config --global core.quotepath false
```

### tig

tig是git的文字GUI，中文需要安装依赖。

```
sudo apt install libncursesw5 libncursesw5-dev
git clone https://github.com/jonas/tig.git
cd tig
git checkout -t origin/release
make configure
./configure --prefix=/usr
make
sudo make install install-release-doc
```

### icdiff

改善git diff体验, 双栏
https://github.com/jeffkaufman/icdiff

```
git config --global icdiff.options '--highlight --line-numbers'
git difftool --extcmd icdiff

```

### git flow

https://danielkummer.github.io/git-flow-cheatsheet/
gitflow插件及bash自动完成脚本
```
yay -S gitflow-avh gitflow-bashcompletion-avh
```

"next release"分支即开发分支


### crlf设置

```
AutoCRLF
#提交时转换为LF，检出时转换为CRLF <在win下编辑时好用>
git config --global core.autocrlf true

#提交时转换为LF，检出时不转换 <在linux下编辑时好用>
git config --global core.autocrlf input

#提交检出均不转换
git config --global core.autocrlf false

SafeCRLF
#拒绝提交包含混合换行符的文件
git config --global core.safecrlf true

#允许提交包含混合换行符的文件
git config --global core.safecrlf false

#提交包含混合换行符的文件时给出警告
git config --global core.safecrlf warn
```

## git中submodule子模块的添加、使用和删除

> via: <https://blog.csdn.net/guotianqing/article/details/82391665>
>
> 作者: [guotianqing](https://me.csdn.net/guotianqing)

### 子模块的添加
添加子模块非常简单，命令如下：

git submodule add <url> <path>

其中，url为子模块的路径，path为该子模块存储的目录路径。

执行成功后，git status会看到项目中修改了.gitmodules，并增加了一个新文件（为刚刚添加的路径）

git diff --cached查看修改内容可以看到增加了子模块，并且新文件下为子模块的提交hash摘要

git commit提交即完成子模块的添加

### 子模块的使用
克隆项目后，默认子模块目录下无任何内容。需要在项目根目录执行如下命令完成子模块的下载：

```
git submodule init
git submodule update
```

或：

```
git submodule update --init --recursive
```


执行后，子模块目录下就有了源码，再执行相应的makefile即可。

### 子模块的更新
子模块的维护者提交了更新后，使用子模块的项目必须手动更新才能包含最新的提交。

在项目中，进入到子模块目录下，执行 git pull更新，查看git log查看相应提交。

完成后返回到项目目录，可以看到子模块有待提交的更新，使用git add，提交即可。

### 删除子模块
有时子模块的项目维护地址发生了变化，或者需要替换子模块，就需要删除原有的子模块。

删除子模块较复杂，步骤如下：

- rm -rf 子模块目录 删除子模块目录及源码

- vi .gitmodules 删除项目目录下.gitmodules文件中子模块相关条目

- vi .git/config 删除配置项中子模块相关条目

- rm .git/module/* 删除模块下的子模块目录，每个子模块对应一个目录，注意只删除对应的子模块目录即可



执行完成后，再执行添加子模块命令即可，如果仍然报错，执行如下：

```
git rm --cached 子模块名称
```

完成删除后，提交到仓库即可。