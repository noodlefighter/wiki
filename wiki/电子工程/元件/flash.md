# Flash器件



## Nor Flash与Nand Flash的比较

> ref: https://www.eefocus.com/mcu-dsp/225968

基本上NOR比较适合存储程序代码，其容量一般较小(比如小于32 MB)，且价格较高；而NAND容量可达lGB以上，价格也相对便宜，适合存储数据。一般来说，128 MB以下容量NAND Flash芯片的一页大小为512字节，用来存放数据，每一页还有16字节的备用空间(SpareData)，充当OOB(Out Of Band)区域，用来存储ECC(Error Correction Codc)校验／坏块标志等信息；再由若干页组成一个块，通常一块为32页(16 KB)。与NOR相比，NAND不是完全可靠的。每块芯片出厂时允许有一定比例的坏块存在，对数据的存取不是使用线性地址映射，而是通过寄存器的操作串行存取数据。





## 常见缩写

Write-Enable (*WREN*) 

Enable-Write-Status-Register (*EWSR*)

Write-Enable-Latch (WEL)


