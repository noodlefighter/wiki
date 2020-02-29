

---



# linux 字符设备



字符设备的默认行为是，读、写时阻塞，即：

* read时，若当前没有数据，则阻塞直到有新数据到来
* write时，若当前缓冲区不足以写完数据，则阻塞直到数据完全写入缓冲区

配置了`O_NONBLOCK`后才是非阻塞读写。



这里是一个实现了

```
#define CHRDEV_CNT              1
#define CHRDEV_NAME             "spi_stream"
#define CHRDEV_CHILD_NAME       "spi_stream"   /* /dev/spi_stream */

/* 1. 确定主设备号 */
static int major;
static struct fasync_struct *chrdev_async;

// 队列，数据到达时，用wake_up(&wq)唤醒队列
static DECLARE_WAIT_QUEUE_HEAD(wq);

static int chrdev_open(struct inode *inode, struct file *file)
{
	int ret = 0;

	printk("chrdev_open\n");
	if (in_used) {
		ret = -EBUSY;
		goto err;
	}

err:
	return ret;
}

static int chrdev_release(struct inode *inode, struct file *file)
{
	printk("chrdev_release\n");
	return 0;
}

ssize_t chrdev_read(struct file *file, char __user *user_buffer, size_t size, loff_t *offset)
{
	int err;
	
	err = wait_event_interruptible(wq, (有可读数据的条件));
	if (0 != err) {
		return err;
	}
	return spidev_read(buf, len);
}

ssize_t chrdev_write(struct file *file, const char __user *user_buffer, size_t size, loff_t *offset)
{
	int err, n;
	int remain = len;

	while (remain) {
		err = wait_event_interruptible(wq, (缓冲区可写的条件));
		if (0 != err) {
			printk("blocking write err exit=%d\n", err);
			return err;
		}
		n = xxxxxx_write(buf, remain);
		remain -= n;
		buf    += n;
	}
	return len;
}

/* 2. 构造file_operations */
static struct file_operations chrdev_fops = {
	.owner          = THIS_MODULE,
	.open           = chrdev_open,
	.release        = chrdev_release,
	.read           = chrdev_read,
	.write          = chrdev_write,
};

static struct cdev chrdev_cdev;
static struct class *cls;

int chrdev_init(void)
{
	dev_t devid;
	// printk("chrdev char dev init\n");

	if (major) {
		devid = MKDEV(major, 0);
		 /* (major,0~1) 对应 chrdev_fops, (major, 2~255)都不对应chrdev_fops */
		register_chrdev_region(devid, CHRDEV_CNT, CHRDEV_NAME);
	} else {
		/* (major,0~1) 对应 chrdev_fops, (major, 2~255)都不对应chrdev_fops */
		alloc_chrdev_region(&devid, 0, CHRDEV_CNT, CHRDEV_NAME);
		major = MAJOR(devid);
	}

	cdev_init(&chrdev_cdev, &chrdev_fops);
	cdev_add(&chrdev_cdev, devid, CHRDEV_CNT);

	cls = class_create(THIS_MODULE, "chrdev");
	device_create(cls, NULL, MKDEV(major, 0), NULL, CHRDEV_CHILD_NAME);
	
	return 0;
}

void chrdev_exit(void)
{
	unregister_chrdev_region(MKDEV(major, 0), CHRDEV_CNT);

	device_destroy(cls, MKDEV(major, 0));
	device_destroy(cls, MKDEV(major, 1));
	class_destroy(cls);

	cdev_del(&chrdev_cdev);
}

```

