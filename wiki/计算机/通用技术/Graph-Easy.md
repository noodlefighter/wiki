

# ASCII字符画流程图工具：Graph::Easy

想在代码里画流程图、状态机图，这是个合适的工具。



> ref: https://www.jianshu.com/p/1f0b295874eb



## 安装相关工具

* [graphviz](http://www.graphviz.org/)
* perl
* Graph::Easy: 用`cpan Graph::Easy`安装，[文档](http://bloodgate.com/perl/graph/manual/index.html)



>  **Graph::Easy** 就是今天要介绍的主角；它是 `perl`的一个软件包，可以使用`perl`代码直接描述图像；当然，我们肯定不会为了画个图专门去学习`perl`;
>  这个软件包的强大之处在于: 它定义了一套非常简单易用的专门用来描述图像的DSL（领域专用语言）,我们可以像写代码一样表达我们需要描述的图像（放心，这个语法非常简单）；不用关心图像里面如何布局；这种语言经过处理可以得到ASCII图像，直接放在代码注释中；如果需要还可以转换成png或者矢量图等格式。



## 命令

```
画简单图时
$ graph-easy <<< '[A]->[B]'
画复杂图时，先存成文件
$ graph-easy xxx.txt
```



## 语法

详细语法参考手册：http://bloodgate.com/perl/graph/manual/syntax.html

* 空格、换行会被忽略

* 注释用`#`，需要在井号后加空格
* 节点用`[]`框起来，连接节点的“边”可以是`->`或`=>`或`<->`等等以表示不同风格，参考原手册
* 多个节点表示：`[xxx|yyy]`



例：

```
[ "Monitor Size" ] --> { label: 21"; } [ Big ] { label: "Huge"; }
```

效果：

```
+----------------+  21"   +------+
| "Monitor Size" | -----> | Huge |
+----------------+        +------+
```

