
---

建立一个加密的git仓库
利用git-crypt可以做到给git仓库加密，这里用的win下的msys2兼容环境。

<!--more-->

参考：
https://www.jianshu.com/p/a40fc90df943


## 编译源码

https://github.com/AGWA/git-crypt

```bash

# 安装依赖
pacman -S openssl-devel

# 编译安装
git clone --branch 0.6.0 https://github.com/AGWA/git-crypt.git
cd git-crypt
make
make install

```

## 生成GPG密钥

```
gpg --gen-key
gpg --list-keys
```

## 加密仓库

```
git-crypt init
git-crypt add-gpg-user kelvv
```

## 配置需要加密的文件夹

`.gitattributes`文件

```
data/* filter=git-crypt diff=git-crypt
```

## 清除git缓存

```
git rm -r --cached config/
```

## 导出密钥

```
git-crypt export-key /path/to/git-crypt-key   
```

## 拿到仓库后解密

```
git-crypt unlock /path/to/git-crypt-key
```

或者先导入密钥到GPG，就不用输路径了

