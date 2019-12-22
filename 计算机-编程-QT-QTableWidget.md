title: QTableWidget
date: 2019-06-08
categories:
- 计算机
- 编程
- QT






---

## QTableWidgetItem设置编辑状态

> via: https://blog.csdn.net/sinat_27593959/article/details/53048614

通过QTableWidget中的item( )方法可以获得相应行数和列数的QTableWidgetItem，若要设置该Item的编辑状态（即可编辑状态和不可编辑状态），可以通过QTableWidgetItem下的setflags函数来设置。setflags函数需要传入的参数为枚举型的Qt::ItemFlags，该枚举类型描述如下： 

```c

enumItemFlag{
 NoItemFlags=0,
 ItemIsSelectable=1,
 ItemIsEditable=2,
 ItemIsDragEnabled=4,
 ItemIsDropEnabled=8,
 ItemIsUserCheckable=16,
 ItemIsEnabled=32,
 ItemIsTristate=64,
 ItemNeverHasChildren=128,
 ItemIsUserTristate=256
}; 
```

通过需要表格框状态可分为如下三种：灰色不可编辑状态、浅色不可编辑状态和浅色可双击编辑状态，而setflags的参数传入可以通过强制类型转换的方式。即对应于如下：

灰色不可编辑状态：Item.setflags((ItemFlags) 0); 
浅色不可编辑状态：Item.setflags((ItemFlags) 32); 
浅色可双击编辑状态：Item.setflags((ItemFlags) 63);

（注意：此处为63，不是64。虽然枚举类型中没有对应于63的值，但是63是QTableWidget实体创建的时候给每个Item的初始化flags值。设置成它就是可编辑状态！）
