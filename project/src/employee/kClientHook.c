/*
 * This is a source code of the client side
 * Of 'silent_net' project.
 *
 * blah blah blah
 *
 *
 */

#include "headers.h"
/*#include "protocol.h"*/

#define HOOK_MSG_SEND "sock_sendmsg"
#define HOOK_PROCESS_EXIT "do_exit"
#define HOOK_PROCESS_FORK "kernel_clone" // Originally named 'do_fork'
					 // Linux newer versions use 'kernel clone'
/* #define HOOK_FILE_OPEN "do_sys_openat" - Not used, OS opens files frequently
 * 				 	    Hooking such function will crash the computer
 */


MODULE_LICENSE("GPL");
MODULE_AUTHOR("Omer Kfir");
MODULE_DESCRIPTION("Final project");

static int handler_pre_do_fork(struct kprobe*, struct pt_regs*);
static int handler_pre_do_exit(struct kprobe*, struct pt_regs*);
static int handler_pre_msg_send(struct kprobe*, struct pt_regs*);
static int register_probes(void);
static void unregister_probes(int);

/* Enum of all kprobes, each kprobe value is the index inside the array */
typedef enum {kp_do_fork, kp_do_exit, kp_msg_send, PROBES_SIZE} kernel_probes;

/* Kprobes structures */
static struct kprobe kps[PROBES_SIZE] = {0};

/* Fork hook */
static int handler_pre_do_fork(struct kprobe *kp, struct pt_regs *regs)
{
	if ( !current )
		return 0;
	
	printk(KERN_INFO "do fork was called: process name = %s\n", current->comm);
	return 0;
}

/* Process termination hook */
static int handler_pre_do_exit(struct kprobe *kp, struct pt_regs *regs)
{
	if ( !current )
		return 0;
	
	printk(KERN_INFO "do exit was called: process name = %s\n", current->comm);
	return 0;
}

/* Socket creation */
static int handler_pre_msg_send(struct kprobe *kp, struct pt_regs *regs)
{
	struct socket *sock = (struct socket *)regs->di; // First parameter passed 
							 // Through di register
	printk(KERN_INFO "Got to msg_send\n"); // Remove later
	if ( !sock || !sock->sk || !sock->sk->sk_daddr || !current )
		return 0;

	printk(KERN_INFO "Message was sent to %d from %s\n", sock->sk->sk_daddr, current->comm);
	return 0;
}

/* Register all hooks */
static int register_probes(void)
{
	/* ret variable for returning value of init function */
        int ret;

        /* Set up creation of new processes function */
        kps[kp_do_fork].pre_handler = handler_pre_do_fork;
        kps[kp_do_fork].symbol_name = HOOK_PROCESS_FORK;

        /* Registering kprobe, which sets up an interrupt before calling function */
        ret = register_kprobe(&kps[kp_do_fork]);
        if (ret < 0) // Error
        {
                printk(KERN_INFO "Failed to register %s,goodbye\n", kps[kp_do_fork].symbol_name);
                goto end;
        }

        /* Set up termination of process function */
        kps[kp_do_exit].pre_handler = handler_pre_do_exit;
        kps[kp_do_exit].symbol_name = HOOK_PROCESS_EXIT;

        ret = register_kprobe(&kps[kp_do_exit]);
        if (ret < 0)
        {
                unregister_probes(kp_do_exit);
                printk(KERN_INFO "Failed to register %s, bye bye\n", kps[kp_do_exit].symbol_name);
                goto end;
        }

	/* Set up sending message using socket */
	kps[kp_msg_send].pre_handler = handler_pre_msg_send;
	kps[kp_msg_send].symbol_name = HOOK_MSG_SEND;

	ret = register_kprobe(&kps[kp_msg_send]);
	printk(KERN_INFO "Registered msg send\n");
	if (ret < 0)
	{
		unregister_probes(kp_msg_send);
		printk(KERN_INFO "Failed to register %s, banana\n", kps[kp_msg_send].symbol_name);
		goto end;
	}
        printk(KERN_INFO "Finished hooking succusfully\n");
end:
        return ret;

}

/* Unregister all kprobes */
static void unregister_probes(int max_probes)
{
	/* Static char to indicate if already unregistered */
	static atomic_t unreg_kprobes = ATOMIC_INIT(0); // Use atomic to avoid race condition

	/* Check if it has been set to 1, if not set it to one */
	if (atomic_cmpxchg(&unreg_kprobes, 0, 1) == 0)
	{	
		/* Create i variable
		 * While it's not a good practice to 
		 * put it inside of a branch
		 * we want to not create it if already
		 * unregistered devices
		*/
		int i;
		for (i=0;i<max_probes;i++)
		{
			unregister_kprobe(&kps[i]);
		}
	}
}

static int __init hook_init(void)
{
	int ret;

	/* More logic */

	ret = register_probes();
	if (ret < 0)
		goto end;
end:
	return ret;
}

static void __exit hook_exit(void)
{
	unregister_probes(PROBES_SIZE);
	printk(KERN_INFO "Unregisterd kernel probes");
}

module_init(hook_init);
module_exit(hook_exit);
