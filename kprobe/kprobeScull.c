#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/kprobes.h>

#define SCULL_WRITE "scull_write"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Omer Kfir");
MODULE_DESCRIPTION("Simple hooking for scull driver write function");

static struct kprobe kp_write;

/*  Pre handler: Called before scull write  */
static int handler_pre_scull_write(struct kprobe *p, struct pt_regs *regs)
{
	printk(KERN_INFO "In kernel hook!!\n");
	return 0;
}

static int __init hook_init(void)
{
	/*  Define kprobe struct to hook on scull_write  */
	kp_write.pre_handler  = handler_pre_scull_write;
	kp_write.symbol_name  = SCULL_WRITE;

	if (register_kprobe(&kp_write) < 0)
	{
		printk(KERN_ERR "Could not register kprobe\n");
		return -1;
	}

	printk(KERN_INFO "Managed to register kprobe\n");
	return 0;

}

static void __exit hook_exit(void)
{
	/*  Unregistering the kprobe hook */
	unregister_kprobe(&kp_write);
	printk(KERN_INFO "Stopped hooking " SCULL_WRITE "\n");
}

module_init(hook_init);
module_exit(hook_exit);
