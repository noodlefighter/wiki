---

## GNU Binutils 以及相关工具

http://www.gnu.org/software/binutils/

ld - the GNU linker. 链接器
as - the GNU assembler. 汇编编译器

addr2line - Converts addresses into filenames and line numbers. 将代码地址转换为对应的程序号
ar - A utility for creating, modifying and extracting from archives. 将目标文件打包成静态库的工具，还能查看、删除其中的模块（object文件）
nm - Lists symbols from object files. 列出目标文件中的符号
objcopy - Copies and translates object files. 翻译二进制文件，比如bin到hex
objdump - Displays information from object files. 查看二进制文件的程序段信息等
ranlib - Generates an index to the contents of an archive. 生成档案（静态库？）的索引
readelf - Displays information from any ELF format object file. 查看elf信息
size - Lists the section sizes of an object or archive file. 列出二进制文件中各段大小
strings - Lists printable strings from files.  查看文件中的字符串
strip - Discards symbols. 用于剔除多余的符号（调试信息）

c++filt - Filter to demangle encoded C++ symbols. 
dlltool - Creates files for building and using DLLs.
gold - A new, faster, ELF only linker, still in beta test.
gprof - Displays profiling information.
nlmconv - Converts object code into an NLM.

windmc - A Windows compatible message compiler.
windres - A compiler for Windows resource files.

ldd命令可以查看程序依赖的动态库：
```bash
$ ldd /bin/ls
/bin/ls: is setuid
        libc.so.0 => /lib//libc.so.0 (0xb6e7e000)
        ld-uClibc.so.1 => /lib/ld-uClibc.so.0 (0xb6f29000)

```

objdump工具：
```bash
$ objdump -p ./sample_venc |grep NEEDED
  NEEDED               libc.so.0
  NEEDED               ld-uClibc.so.1

```

查看正在运行中的程序的依赖库：
```bash
$ ps -ef|grep bash
dev      10280 10276  0 14:32 pts/0    00:00:00 -bash
dev      11711 10280  0 16:08 pts/0    00:00:00 grep --color=auto bash
dev@develop:~/workspaces/hi3516a/Hi3516A_SDK_V1.0.7.1/mpp/sample/venc$ pmap 10280 |head
10280:   -bash
0000000000400000    976K r-x-- bash
00000000006f3000      4K r---- bash
00000000006f4000     36K rw--- bash
00000000006fd000     24K rw---   [ anon ]
0000000000b84000   1816K rw---   [ anon ]
00007fee9e033000     44K r-x-- libnss_files-2.23.so
00007fee9e03e000   2044K ----- libnss_files-2.23.so
00007fee9e23d000      4K r---- libnss_files-2.23.so
00007fee9e23e000      4K rw--- libnss_files-2.23.so
```

`readelf`工具和objdump类似，但信息更好读，信息会更全因为objdump会省略部分辅助性的段。

## 把二进制文件用objcopy工具装入一个目标文件

就是把二进制资源变成符号：

```
# objcopy -I binary -O elf32-i386 -B i386 image.jpg image.o
# objdump -ht image.o
```