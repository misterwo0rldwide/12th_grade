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
#define HOOK_FILE_OPEN "__x64_sys_open"

#define MAX_FILE_NAME_LENGTH 256

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Omer Kfir");
MODULE_DESCRIPTION("Final project");

static struct kprobe kp_do_fork;
static struct kprobe kp_do_exit;
static struct kprobe kp_sys_open;

/* Fork hook */
static int handler_pre_do_fork(struct kprobe *kp, struct pt_regs *regs)
{
	//printk(KERN_INFO "do fork was called: process name = %s\n", current->comm);
	return 0;
}

/* Process termination hook */
static int handler_pre_do_exit(struct kprobe *kp, struct pt_regs *regs)
{
	//printk(KERN_INFO "do exit was called: process name = %s\n", current->comm);
	return 0;
}

/* Process opens a file hook */
static int handler_pre_sys_open(struct kprobe *kp, struct pt_regs *regs)
{
	/* Buffer to store file name */
	char fname[MAX_FILE_NAME_LENGTH];
	int ret;

	ret = strncpy_from_user(fname, (char __user *)regs->di, MAX_FILE_NAME_LENGTH - 1);
	if (ret < 0)
	{
		printk(KERN_INFO "Failed to copy file name from user\n");
		return -EFAULT;
	}
	
	fname[MAX_FILE_NAME_LENGTH - 1] = '\0'; // NULL byte at end of string
	
	printk(KERN_INFO "Filed opened: name = %s\n", fname);
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
		unregister_kprobe(&kp_do_fork);
		printk(KERN_INFO "Failed to register do_exit, bey bye\n");
		goto end;
	}

	/* Set up opening of a file function */
	kp_sys_open.pre_handler = handler_pre_sys_open;
	kp_sys_open.symbol_name = HOOK_FILE_OPEN;

	ret = register_kprobe(&kp_sys_open);
	if (ret < 0)
	{
		unregister_kprobe(&kp_do_fork);
		unregister_kprobe(&kp_do_exit);
		printk(KERN_INFO "Failed to register sys_open, byeee\n");
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
	unregister_kprobe(&kp_sys_open);
	printk(KERN_INFO "Unregisterd kernel probes");
}

module_init(hook_init);
module_exit(hook_exit);
