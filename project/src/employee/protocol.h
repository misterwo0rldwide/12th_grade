#ifndef PROTOCOL_H
#define PROTOCOL_H

struct socket* tcp_sock_create();
int tcp_sock_connect(struct socket *sock, const char *dst_ip, uint16_t port);
int tcp_send_msg(struct socket *sock, const char *msg);
void tcp_sock_close(struct socket *sock);

/* PROTOCOL_H */
#endif
