#ifndef TCP_SOCK_H
#define TCP_SOCK_H

/* IPV4 tcp connection */
#include <linux/net.h> // Kernel functions for network
#include <linux/socket.h> // Kernel socket structure
#include <net/sock.h> // Kernel socket structures
#include <linux/in.h> // IP structures
#include <linux/inet.h> // Internet addresses manipulatutions

struct socket* tcp_sock_create(void);
int tcp_sock_connect(struct socket*, const char*, uint16_t);
int tcp_send_msg(struct socket*, const char*, size_t);
void tcp_sock_close(struct socket *);

/* TCP_SOCK_H */
#endif
