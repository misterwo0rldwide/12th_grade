/*
 * 'slient net' project client tcp socket code.
 * Handles communication implementation.
 *
 * blah blah blah
 *
 */

#include "headers.h"
#include "tcp_socket.h"

/* Initialize a TCP struct socket */
struct socket* tcp_sock_create(void)
{
    	struct socket *sock;
    	int err;
    
    	/* Create tcp socket */
    	err = sock_create(AF_INET, SOCK_STREAM, IPPROTO_TCP, &sock);
    	if (err < 0) {
        	printk(KERN_ERR "Failed to create TCP socket\n");
        	return ERR_PTR(err);
    	}

    	/* Set 0.5 second timeout for recv/connect/send */
    	sock->sk->sk_sndtimeo = msecs_to_jiffies(500);
    	sock->sk->sk_rcvtimeo = msecs_to_jiffies(500);

	return sock;
}


/* Initialize a tcp connection */
int tcp_sock_connect(struct socket *sock, const char *dst_ip, uint16_t port)
{
	struct sockaddr_in addr = { 0 }; // Ensure all values inside struct are zeroed
	int err;

	/* Validate all arguments */
	if ( !sock || !sock->ops || !sock->ops->connect || !dst_ip)
		return -EINVAL; // Invalid argument passed

	/* Initialize address structure */
	addr.sin_family      = AF_INET;
	addr.sin_port        = htons(port);
	addr.sin_addr.s_addr = in_aton(dst_ip);

	// 0 - Means no specific use of the socket (Writing/Receving)
	err = sock->ops->connect(sock, (struct sockaddr *)&addr, sizeof(addr), 0);
	if ( err < 0  && err != -EINPROGRESS )
		return err;

	// Implement waiting till timeout connection

	return err;
}


/* Send message through a TCP socket */
int tcp_send_msg(struct socket *sock, const char *msg, size_t length)
{
	struct msghdr msg_met = { 0 };
	struct kvec vec;
	int err;

	/* Validate arguemnts */
	if ( !sock || !msg )
		return -EINVAL; // Invalid argument passed

	/* I/O Vector for message tranfering */
	vec.iov_base = (void *)msg;
	vec.iov_len  = length;

	err = kernel_sendmsg(sock, &msg_met, &vec, 1, length);
	if ( err < 0 )
		printk(KERN_ERR "Failed to send message %d\n", err);

	return err;
}


/* Close socket struct */
void tcp_sock_close(struct socket *sock)
{
	if ( sock )
		sock_release(sock);
}
