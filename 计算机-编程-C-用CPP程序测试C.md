title: 用CPP程序测试C
date: 2019-06-12
categories:
- 计算机
- 编程
- C




---



这是一次尝试, 但是失败了, 本来想用CPP的匿名函数特性方便写mock测试:

```
extern "C" {
#include <cmocka.h>
} // extern "C" 

// 编写set_mock()以动态改变skproto_evtpool_updated_hook的接收者
std::function<void (skproto_evtpool_t*, int)> cur_hook;
extern "C" {
void skproto_evtpool_updated_hook(skproto_evtpool_t *obj, int evt_serial)
{
	cur_hook(obj, evt_serial);
}
} // extern "C"

void set_mock(std::function<void (skproto_evtpool_t*, int)> p_mock_func)
{
	cur_hook = p_mock_func;
}

void test_normal_usage(void **state)
{
	skproto_evtpool_t evtpool;
	int evt, arg;

	// init
	assert_true(skproto_evtpool_init(&evtpool) == 0);

	// case
	evt = 555; arg = 666;
	expect_value(xx);
	set_mock([=](skproto_evtpool_t *obj, int evt_serial) {
		check_expected_ptr(xxx);
	});
	assert_true(skproto_evtpool_raise(&evtpool, evt, arg) == 0);
}

```

但是发现cmocka的宏`_check_expected`用到了`__func__`, 这样就没法用匿名函数了.. 因为首先在`expect_xxx`宏中就要传入个函数名.

感觉可以试试gtest这种直接就是用来测试CPP的框架, 理由是:

* 线程安全, cmocka无法在多线程环境中的mock函数中做assert, 否则可能错误
* 支持C++11, 可以自然地使用匿名函数方便测试