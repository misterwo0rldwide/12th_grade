#ifndef PROTOCOL_H
#define PROTOCOL_H

/* IPV4 tcp connection */
#include <linux/net.h> // Kernel functions for network
#include <linux/socket.h> // Kernel socket structure
#include <net/sock.h> // Kernel socket structures
#include <linux/in.h> // IP structures
#include <linux/inet.h> // Internet addresses manipulatutions

struct socket* tcp_sock_create(void);
int tcp_sock_connect(struct socket *sock, const char *dst_ip, uint16_t port);
int tcp_send_msg(struct socket *sock, const char *msg);
void tcp_sock_close(struct socket *sock);

/* PROTOCOL_H */
#endif
