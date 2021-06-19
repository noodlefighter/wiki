

向上转型upcasting（子类转父类）：直接隐式转换，安全

向下转型downcasting（父类转子类），明显是不安全的：

- static_cast：`static_cast<YourType*> foo`，静态转换

- dynamic_cast：`dynamic_cast<YourType*> foo`，动态转换，运行时检查类型，类型不符则返回null

