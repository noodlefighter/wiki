

## QT程序Linux环境打包

[官方手册](https://doc.qt.io/qt-5/linux-deployment.html)中提到静态链接和动态链接两种。

另外使用[linuxdeployqt](https://github.com/probonopd/linuxdeployqt)可以快速完成打包：

```
$ mkdir build && cd build
$ qmake ..
$ make
$ mkdir pack
$ cp <编译好的程序> pack/
$ cd pack
$ ~/linuxdeployqt-7-x86_64.AppImage <编译好的程序> -appimage
```



## 判断QT框架版本号

```
#if (QT_VERSION <= QT_VERSION_CHECK(5,0,0))
#  warning "qt version <= 5.0.0"
#else 

#endif
```

## QT拖放

> via: <https://www.cnblogs.com/findumars/p/5599427.html>

子类中实现`dragEnterEvent`和`dropEvent`:

```cpp
//当用户拖动文件到窗口部件上时候，就会触发dragEnterEvent事件
void MainWindow::dragEnterEvent(QDragEnterEvent *event)
{
    //如果为文件，则支持拖放
    if (event->mimeData()->hasFormat("text/uri-list"))
        event->acceptProposedAction();
}
 
//当用户放下这个文件后，就会触发dropEvent事件
void MainWindow::dropEvent(QDropEvent *event)
{
    //注意：这里如果有多文件存在，意思是用户一下子拖动了多个文件，而不是拖动一个目录
    //如果想读取整个目录，则在不同的操作平台下，自己编写函数实现读取整个目录文件名
    QList<QUrl> urls = event->mimeData()->urls();
    if(urls.isEmpty())
        return;
 
    //往文本框中追加文件名
    foreach(QUrl url, urls) {
        QString file_name = url.toLocalFile();
        textEdit->append(file_name);
    }
}
```

## QT计算md5校验值

> via: <https://www.jianshu.com/p/fe774becf239>

```
QString fileMd5(const QString &sourceFilePath) {

    QFile sourceFile(sourceFilePath);
    qint64 fileSize = sourceFile.size();
    const qint64 bufferSize = 10240;

    if (sourceFile.open(QIODevice::ReadOnly)) {
        char buffer[bufferSize];
        int bytesRead;
        int readSize = qMin(fileSize, bufferSize);

        QCryptographicHash hash(QCryptographicHash::Md5);

        while (readSize > 0 && (bytesRead = sourceFile.read(buffer, readSize)) > 0) {
            fileSize -= bytesRead;
            hash.addData(buffer, bytesRead);
            readSize = qMin(fileSize, bufferSize);
        }

        sourceFile.close();
        return QString(hash.result().toHex());
    }
    return QString();
}
```



## QT的QTableWidgetItem设置编辑状态

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





## QString格式化

```
QString str = QString("%1:%2:%3").arg(0,2,10,QLatin1Char('0')).arg(1,2,10,QLatin1Char('0')) .arg(23,2,10,QLatin1Char('0'));
```

