#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/net.h>
#include <linux/socket.h>
#include <linux/in.h>
#include <linux/kthread.h>
#include <linux/inet.h>

#define TARGET_IP "10.100.102.103"  // Change this to your target IP
#define TARGET_PORT 6734      // Change this to your target port
#define MESSAGE "Hello from kernel module!"

static struct socket *sock = NULL;
static struct task_struct *connection_thread;

static int connection_handler(void *data)
{
    struct sockaddr_in addr;
    struct msghdr msg;
    struct kvec iov;
    int ret;

    // Create socket
    ret = sock_create(AF_INET, SOCK_STREAM, IPPROTO_TCP, &sock);
    if (ret < 0) {
        printk(KERN_ERR "Failed to create socket: %d\n", ret);
        return ret;
    }

    printk(KERN_INFO "After creation\n");

    // Setup address structure
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(TARGET_PORT);
    addr.sin_addr.s_addr = in_aton(TARGET_IP);

    // Connect to server
    ret = sock->ops->connect(sock, (struct sockaddr *)&addr, sizeof(addr), O_RDWR);
    if (ret < 0) {
        printk(KERN_ERR "Failed to connect: %d\n", ret);
        sock_release(sock);
        return ret;
    }

    printk(KERN_INFO "After connection\n");

    // Prepare message
    memset(&msg, 0, sizeof(msg));
    iov.iov_base = MESSAGE;
    iov.iov_len = strlen(MESSAGE);

    // Send message
    ret = kernel_sendmsg(sock, &msg, &iov, 1, strlen(MESSAGE));
    if (ret < 0) {
        printk(KERN_ERR "Failed to send message: %d\n", ret);
    } else {
        printk(KERN_INFO "Message sent successfully\n");
    }

    printk(KERN_INFO "After sending message\n");

    // Cleanup
    sock_release(sock);
    return 0;
}

static int __init network_module_init(void)
{
    printk(KERN_INFO "Network module loading\n");
    
    // Create kernel thread to handle connection
    connection_thread = kthread_run(connection_handler, NULL, "network_connection");
    if (IS_ERR(connection_thread)) {
        printk(KERN_ERR "Failed to create kernel thread\n");
        return PTR_ERR(connection_thread);
    }

    return 0;
}

static void __exit network_module_exit(void)
{
    printk(KERN_INFO "Network module unloading\n");
}

module_init(network_module_init);
module_exit(network_module_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Itzko the king");
MODULE_DESCRIPTION("Simple network connection module");
