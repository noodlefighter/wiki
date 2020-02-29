

---



> 例如Debian在生成package的时候，编译完之后，不能立刻在当前环境执行make install，需要执行make install DESTDIR=$(pwd)/debian/tmp把生成的文件安装到build目录的里面$(pwd)/debian/tmp。然后使用那个目录里面的全部内容生成Debian包（实际上包里面还会包含control和maintainer script等）。 这个包里面的文件所有者必须是root，所以需要以root来执行打包命令。但是应该避免在制作Debian包的时候使用root权限。 为了解决这个矛盾，fakeroot被开发出来了。在fakeroot环境中，操作文件就像使用root操作文件一样。但是，实际上系统中文件的权限还是原来的权限。