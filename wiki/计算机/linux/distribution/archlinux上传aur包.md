

> 参考：
>
> - [AUR 纯萌新向入门教学(3)-提交软件包到AUR](https://blog.yoitsu.moe/arch-linux/aur_sumbiting_guidebook.html)
> - [Arch Build System (简体中文)](https://wiki.archlinux.org/index.php/Arch_Build_System_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E6%9E%84%E5%BB%BA%E8%BD%AF%E4%BB%B6%E5%8C%85)
> - [PKGBUILD](https://wiki.archlinux.org/index.php/PKGBUILD)
> - [Official repositories (简体中文)](https://wiki.archlinux.org/index.php/Official_repositories_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
> - [Arch package guidelines (简体中文)](https://wiki.archlinux.org/index.php/Arch_package_guidelines_(%E7%AE%80%E4%D%93%E4%B8%AD%E6%96%87))
> - AUR： https://aur.archlinux.org/

## 上传 AUR包 简单流程

1. 去AUR注册账号，上传 SSH 公钥

2. git clone 一个不存在的仓库，仓库就会自动创建：

   ```
   git clone ssh://aur@aur.archlinux.org/<我的仓库>.git
   ```

3. 编写`.SRCINFO` (供 AUR Web 界面解析的元数据), 可以通过 [pkgbuild-introspection](https://www.archlinux.org/packages/?name=pkgbuild-introspection) 包内的 `mksrcinfo` 工具生成；**每次更新时要记得更新元数据**

4. git push 上去就好了



## AUR包 开发相关工具

[pbget](https://xyne.archlinux.ca/projects/pbget/) - 从web接口直接获取某个包的PKGBUILD，支持AUR.

[makepkg](https://wiki.archlinux.org/title/Makepkg): 将 PKGBUILD 描述的包打包为二进制包

[mksrcinfo](https://www.archlinux.org/packages/?name=pkgbuild-introspection): 根据 PKGBUILD 生成 SRCINFO 元数据

.pkg.tar.zst 格式：默认打包的二进制包为这个格式，速度很快，用zstd工具打包、解压

