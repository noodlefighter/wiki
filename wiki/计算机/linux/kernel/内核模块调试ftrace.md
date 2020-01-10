

---

https://lwn.net/Articles/365835/



printk常用，但效率差，ftrace机制是一个性能更高的追踪机制。

内核需要开启：

```
    CONFIG_FUNCTION_TRACER
    CONFIG_FUNCTION_GRAPH_TRACER
    CONFIG_STACK_TRACER
    CONFIG_DYNAMIC_FTRACE
```



## 基本用法，跟踪函数调用情况

```
    [~]# cd /sys/kernel/debug/tracing
    [tracing]#
    [tracing]# cat available_tracers 
    function_graph function sched_switch nop
    [tracing]# echo function > current_tracer
    [tracing]# cat current_tracer
    function

    [tracing]# cat trace | head -10
    # tracer: function
    #
    #           TASK-PID    CPU#    TIMESTAMP  FUNCTION
    #              | |       |          |         |
                bash-16939 [000]  6075.461561: mutex_unlock <-tracing_set_tracer
              <idle>-0     [001]  6075.461561: _spin_unlock_irqrestore <-hrtimer_get_next_event
              <idle>-0     [001]  6075.461562: rcu_needs_cpu <-tick_nohz_stop_sched_tick
                bash-16939 [000]  6075.461563: inotify_inode_queue_event <-vfs_write
              <idle>-0     [001]  6075.461563: mwait_idle <-cpu_idle
                bash-16939 [000]  6075.461563: __fsnotify_parent <-vfs_write
    [tracing]# echo function_graph > current_tracer 
    内核模块内：[tracing]# cat trace | head -20
    # tracer: function_graph
    #
    # CPU  DURATION                  FUNCTION CALLS
    # |     |   |                     |   |   |   |
     1)   1.015 us    |        _spin_lock_irqsave();
     1)   0.476 us    |        internal_add_timer();
     1)   0.423 us    |        wake_up_idle_cpu();
     1)   0.461 us    |        _spin_unlock_irqrestore();
     1)   4.770 us    |      }
     1)   5.725 us    |    }
     1)   0.450 us    |    mutex_unlock();
     1) + 24.243 us   |  }
     1)   0.483 us    |  _spin_lock_irq();
     1)   0.517 us    |  _spin_unlock_irq();
     1)               |  prepare_to_wait() {
     1)   0.468 us    |    _spin_lock_irqsave();
     1)   0.502 us    |    _spin_unlock_irqrestore();
     1)   2.411 us    |  }
     1)   0.449 us    |  kthread_should_stop();
     1)               |  schedule() {
```



## 使用 `trace_printk()`


For example you can add something like this to the kernel or module:

    trace_printk("read foo %d out of bar %p\n", bar->foo, bar);
Then by looking at the trace file, you can see your output.

    [tracing]# cat trace
    # tracer: nop
    #
    #           TASK-PID    CPU#    TIMESTAMP  FUNCTION
    #              | |       |          |         |
               <...>-10690 [003] 17279.332920: : read foo 10 out of bar ffff880013a5bef8