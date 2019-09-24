

---

xdelta是个用于制作二进制patch的工具，生成出来的补丁很小。

新文件（targetfile）和旧文件（sourcefile）做差分（differencing），又有对产生的patch包进行压缩（compression），产生patch包的过程统称为编码（encoding），而将合成新文件的过程统称为解码（decoding）。

Xdelta3和经典的压缩算法LZ’77一样，也是将source file划分成一个个不相交而又连续的window，然后进行encoding和decoding。

