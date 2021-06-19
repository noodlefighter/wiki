

## QObject 中的父对象

> refer: https://doc.qt.io/qt-5/qobject.html

QObjects 中在对象树中组织自己，当您使用另一个对象作为父对象创建 QObject 时，该对象将自动将自己添加到父对象的 children() 列表中。父对象拥有对象的所有权； 即，它将在其析构函数中自动删除其子项。

QObject 的构造函数`QObject(QObject *parent = nullptr)`，创建时可传入父对象指针，也可以用`setParent()`设置父对象。

父对象和子对象会在同一个线程中接收信号。

比较反直觉的是，**继承了 QObject 的类的成员，不会自动成为子对象**，毕竟类的构造最终还是 C++ 帮做的，它可不会自动帮你传个参或者调用函数。



