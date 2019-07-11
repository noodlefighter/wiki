

---

有时候需要在内核态执行用户态应用，提供了一套`usermode-helper API`。

参考：

https://developer.ibm.com/articles/l-user-space-apps/



## 参考：linux里的UEVENT_HELPER机制

在linux kernel的Kconfig里有两个配置：`CONFIG_UEVENT_HELPER`和`CONFIG_UEVENT_HELPER_PATH`，前者确定是否开启功能，后者指定路径，功能是当hotplug发生时执行这个路径对应的用户空间的脚本（程序）。

这个路径也可以在运行期间通过写入`/proc/sys/kernel/hotplug`或者`/sys/kernel/uevent_helper`来动态修改。		

以下是Kconfig里的说明：

```
config UEVENT_HELPER
	bool "Support for uevent helper"
	help
	  The uevent helper program is forked by the kernel for
	  every uevent.
	  Before the switch to the netlink-based uevent source, this was
	  used to hook hotplug scripts into kernel device events. It
	  usually pointed to a shell script at /sbin/hotplug.
	  This should not be used today, because usual systems create
	  many events at bootup or device discovery in a very short time
	  frame. One forked process per event can create so many processes
	  that it creates a high system load, or on smaller systems
	  it is known to create out-of-memory situations during bootup.

config UEVENT_HELPER_PATH
	string "path to uevent helper"
	depends on UEVENT_HELPER
	default ""
	help
	  To disable user space helper program execution at by default
	  specify an empty string here. This setting can still be altered
	  via /proc/sys/kernel/hotplug or via /sys/kernel/uevent_helper

```

以下是相关实现，[github传送门](https://github.com/torvalds/linux/blob/f678d6da749983791850876e3421e7c48a0a7127/lib/kobject_uevent.c)：

```c
...
...
#ifdef CONFIG_UEVENT_HELPER
char uevent_helper[UEVENT_HELPER_PATH_LEN] = CONFIG_UEVENT_HELPER_PATH;
#endif
...
...
#ifdef CONFIG_UEVENT_HELPER
static int kobj_usermode_filter(struct kobject *kobj)
{
	const struct kobj_ns_type_operations *ops;

	ops = kobj_ns_ops(kobj);
	if (ops) {
		const void *init_ns, *ns;

		ns = kobj->ktype->namespace(kobj);
		init_ns = ops->initial_ns();
		return ns != init_ns;
	}

	return 0;
}

static int init_uevent_argv(struct kobj_uevent_env *env, const char *subsystem)
{
	int len;

	len = strlcpy(&env->buf[env->buflen], subsystem,
		      sizeof(env->buf) - env->buflen);
	if (len >= (sizeof(env->buf) - env->buflen)) {
		WARN(1, KERN_ERR "init_uevent_argv: buffer size too small\n");
		return -ENOMEM;
	}

	env->argv[0] = uevent_helper;
	env->argv[1] = &env->buf[env->buflen];
	env->argv[2] = NULL;

	env->buflen += len + 1;
	return 0;
}

static void cleanup_uevent_env(struct subprocess_info *info)
{
	kfree(info->data);
}
#endif
...
...
int kobject_uevent_env(struct kobject *kobj, enum kobject_action action,
		       char *envp_ext[])
{
...
...
#ifdef CONFIG_UEVENT_HELPER
	/* call uevent_helper, usually only enabled during early boot */
	if (uevent_helper[0] && !kobj_usermode_filter(kobj)) {
		struct subprocess_info *info;

		retval = add_uevent_var(env, "HOME=/");
		if (retval)
			goto exit;
		retval = add_uevent_var(env,
					"PATH=/sbin:/bin:/usr/sbin:/usr/bin");
		if (retval)
			goto exit;
		retval = init_uevent_argv(env, subsystem);
		if (retval)
			goto exit;

		retval = -ENOMEM;
		info = call_usermodehelper_setup(env->argv[0], env->argv,
						 env->envp, GFP_KERNEL,
						 NULL, cleanup_uevent_env, env);
		if (info) {
			retval = call_usermodehelper_exec(info, UMH_NO_WAIT);
			env = NULL;	/* freed by cleanup_uevent_env */
		}
	}
#endif
...
...
}


```



