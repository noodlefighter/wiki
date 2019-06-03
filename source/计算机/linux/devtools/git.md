---



图形界面:
gitkraken   据说好用的git图形界面


```bash
# 检出分支到本地新分支、覆盖工作区
git checkout -f -B branchabc remotes/origin/branchabc --

# 添加gpg签名密钥
git config --global user.signingkey 0A46826A
```



## ff合并和合并细节

注意到有时执行`git merge`不会产生合并记录, 这是触发了git的fast-forward功能.

另外, 合并到master似乎默认使用`--no-ff`方式, 必然产生合并记录.

> 作者：Chuckiefan
>
> 链接：https://www.jianshu.com/p/58a166f24c81

### fast-forward合并

通常情况下分支合并都会产生一个合并节点，但是在某些特殊情况下例外。例如调用git pull命令更新远端代码时，如果本地的分支没有任何的提交，那么没有必要产生一个合并节点。这种情况下将不会产生一个合并节点，HEAD直接指向更新后的顶端代码，这种合并的策略就是fast-forward合并。

### 合并细节

除了上文所提到的fast-forward合并模式以外，被合并的分支将会通过一个合并节点和当前分支绑在一起，该合并节点同时拥有合并前的当前分支顶部节点和对方分支顶部节点，共同作为父节点。
 一个合并了的版本将会使所有相关分支的变化一致，包括提交节点，HEAD节点和index指针以及节点树都会被更新。只要这些节点中的文件没有重叠的地方，那么这些文件的变化都会在节点树中改动并更新保存。
 如果无法明显地合并这些变化，将会发生以下的情况：

1. HEAD指针所指向的节点保持不变
2.  `MERGE_HEAD`指针被置于其他分支的顶部
3. 已经合并干净的路径在index文件和节点树中同时更新
4. 对于冲突路径，index文件记录了三个版本：版本1记录了二者共同的祖先节点，版本2记录了当前分支的顶部，即HEAD，版本3记录了`MERGE_HEAD`。节点树中的文件包含了合并程序运行后的结果。例如三路合并算法会产生冲突。
5. 其他方面没有任何变化。特别地，你之前进行的本地修改将继续保持原样。
    如果你尝试了一个导致非常复杂冲突的合并，并想重新开始，那么可以使用`git merge --abort` 

> 关于三路合并算法：
>  三路合并算法是用于解决冲突的一种方式，当产生冲突时，三路合并算法会获取三个节点：本地冲突的B节点，对方分支的C节点，B，C节点的共同最近祖先节点A。三路合并算法会根据这三个节点进行合并。具体过程是，B，C节点和A节点进行比较，如果B，C节点的某个文件和A节点中的相同，那么不产生冲突；如果B或C只有一个和A节点相比发生变化，那么该文件将会采用该变化了的版本；如果B和C和A相比都发生了变化，且变化不相同，那么则需要手动去合并;如果B，C都发生了变化，且变化相同，那么并不产生冲突，会自动采用该变化的版本。最终合并后会产生D节点，D节点有两个父节点，分别为B和C。



## 无法显示中文问题

```
git config --global core.quotepath false
```

## tig

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

## icdiff

改善git diff体验, 双栏
https://github.com/jeffkaufman/icdiff

```
git config --global icdiff.options '--highlight --line-numbers'
git difftool --extcmd icdiff

```

## git flow

https://danielkummer.github.io/git-flow-cheatsheet/
gitflow插件及bash自动完成脚本

```
yay -S gitflow-avh gitflow-bashcompletion-avh
```

"next release"分支即开发分支

### 使用

```
# 建立特性分支
git flow feature start xxx [base]

# 完成特性

#     常用可选项: --rebase合并前变基  --squash合并提交
git flow finish

```






## crlf设置

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