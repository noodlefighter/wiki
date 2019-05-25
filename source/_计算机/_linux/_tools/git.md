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