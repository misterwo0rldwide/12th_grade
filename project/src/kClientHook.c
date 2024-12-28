/*
 * This is a source code of the client side
 * Of 'silent_net' project.
 *
 * blah blah blah
 *
 *
 */

#include "headers.h"

#define HOOK_PROCESS_EXIT "do_exit"
#define HOOK_PROCESS_FORK "kernel_clone" // Originally named 'do_fork'
				 // Linux newer versions use 'kernel clone'

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Omer Kfir");
MODULE_DESCRIPTION("Final project");

static struct kprobe kp_do_fork;
static struct kprobe kp_do_exit;
static struct kprobe kp_sys_open;

/* Fork hook */
static int handler_pre_do_fork(struct kprobe *kp, struct pt_regs *regs)
{
	printk(KERN_INFO "do fork was called: process name = %s\n", current->comm);
	return 0;
}

/* Process termination hook */
static int handler_pre_do_exit(struct kprobe *kp, struct pt_regs *regs)
{
	printk(KERN_INFO "do exit was called: process name = %s\n", current->comm);
	return 0;
}

static int __init hook_init(void)
{
	/* ret variable for returning value of init function */
	int ret;

	/* Set up creation of new processes function */
	kp_do_fork.pre_handler = handler_pre_do_fork;
	kp_do_fork.symbol_name = HOOK_PROCESS_FORK;

	/* Registering kprobe, which sets up an interrupt before calling function */
	ret = register_kprobe(&kp_do_fork);
	if (ret < 0) // Error
	{
		printk(KERN_INFO "Failed to register do_fork,goodbye\n");
		goto end;
	}

	/* Set up termination of process function */
	kp_do_exit.pre_handler = handler_pre_do_exit;
	kp_do_exit.symbol_name = HOOK_PROCESS_EXIT;

	ret = register_kprobe(&kp_do_exit);
	if (ret < 0)
	{
		printk(KERN_INFO "Fauled to register do_exit, bey bye\n");
		goto end;
	}

	printk(KERN_INFO "Finished hooking succusfully\n");
end:
	return ret;
}

static void __exit hook_exit(void)
{
	unregister_kprobe(&kp_do_fork);
	unregister_kprobe(&kp_do_exit);
	printk(KERN_INFO "Unregisterd kernel probes");
}

module_init(hook_init);
module_exit(hook_exit);
