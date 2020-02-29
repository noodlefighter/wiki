

---

linux内核中实现了环形buffer，它也能和内存屏障配合实现允许同时写、清空的buffer。

https://www.kernel.org/doc/html/latest/core-api/circular-buffers.html

```c
struct circ_buf {
	char *buf;
	int head;
	int tail;
};

/* 使用空间 */
#define CIRC_CNT(head,tail,size) (((head) - (tail)) & ((size)-1))

/* 剩余空间 */
#define CIRC_SPACE(head,tail,size) CIRC_CNT((tail),((head)+1),(size))

/* 立即可读的连续空间  */
#define CIRC_CNT_TO_END(head,tail,size) \
	({int end = (size) - (tail); \
	  int n = ((head) + end) & ((size)-1); \
	  n < end ? n : end;})

/* 立即可写的连续空间  */
#define CIRC_SPACE_TO_END(head,tail,size) \
	({int end = (size) - 1 - (head); \
	  int n = (end + (tail)) & ((size)-1); \
	  n <= end ? n : end+1;})
```





提供的设施还是比较原始的，用法参考了下，[acpi_dbg.c](https://github.com/torvalds/linux/blob/master/drivers/acpi/acpi_dbg.c)：

```c
#include <linux/circ_buf.h>

#define circ_count(circ) \
	(CIRC_CNT((circ)->head, (circ)->tail, ACPI_AML_BUF_SIZE))
#define circ_count_to_end(circ) \
	(CIRC_CNT_TO_END((circ)->head, (circ)->tail, ACPI_AML_BUF_SIZE))
#define circ_space(circ) \
	(CIRC_SPACE((circ)->head, (circ)->tail, ACPI_AML_BUF_SIZE))
#define circ_space_to_end(circ) \
	(CIRC_SPACE_TO_END((circ)->head, (circ)->tail, ACPI_AML_BUF_SIZE))

// 初始化
int __init acpi_aml_init(void) 
{
    acpi_aml_io.in_crc.buf = acpi_aml_io.in_buf;
}
static int acpi_aml_open(/* ... */) 
{
    /* ... */    
    acpi_aml_io.in_crc.head = acpi_aml_io.in_crc.tail = 0;
	/* ... */
}

// 生产者
static int acpi_aml_write_user(const char __user *buf, int len)
{
	int ret;
	struct circ_buf *crc = &acpi_aml_io.in_crc;        // <----实例
	int n;
	char *p;

	ret = acpi_aml_lock_write(crc, ACPI_AML_IN_USER);  // <----上锁
	if (ret < 0)
		return ret;
	/* sync tail before inserting cmds */
	smp_mb();
	p = &crc->buf[crc->head];                          // <----获取头部
	n = min(len, circ_space_to_end(crc));              // <----填充长度
	if (copy_from_user(p, buf, n)) {
		ret = -EFAULT;
		goto out;
	}
	/* sync head after inserting cmds */
	smp_wmb();
	crc->head = (crc->head + n) & (ACPI_AML_BUF_SIZE - 1); // <----计算新的head，与上mask（2^n-1就是掩码）
	ret = n;
out:
	acpi_aml_unlock_fifo(ACPI_AML_IN_USER, ret >= 0);
	return n;
}

// 消费者(每次只消耗1byte)
static int acpi_aml_readb_kern(void)
{
	int ret;
	struct circ_buf *crc = &acpi_aml_io.in_crc;        // <----实例
	char *p;

	ret = acpi_aml_lock_read(crc, ACPI_AML_IN_KERN);   // <----上锁
	if (ret < 0)
		return ret;
	/* sync head before removing cmds */
	smp_rmb();
	p = &crc->buf[crc->tail];                          // <----获取尾部
	ret = (int)*p;
	/* sync tail before inserting cmds */
	smp_mb();
	crc->tail = (crc->tail + 1) & (ACPI_AML_BUF_SIZE - 1); // <----计算新的tail，与上mask（2^n-1就是掩码）
	acpi_aml_unlock_fifo(ACPI_AML_IN_KERN, true);      // <----解锁
	return ret;
}
```

