#ifndef HEADER_H
#define HEADER_H

/* Common header files */
#include <linux/module.h> // Kernel module macros
#include <linux/kernel.h> // Kernel base functions
#include <linux/init.h> // Module __init __exit
#include <linux/kprobes.h> // Kprobe lib (King)
#include <linux/fs.h> // Kernel file system
#include <linux/sched.h> // Scheduler lib, Mainly for current structure (PCB)
#include <asm/uaccess.h> // Copy and write to user buffers
#include <linux/types.h> // Fixed width integer sizes

/* IPV4 tcp connection */
#include <linux/net.h> // Kernel functions for network
#include <linux/socket.h> // Kernel socket structure
#include <net/sock.h> // Kernel socket structures
#include <linux/in.h> // IP structures
#include <linux/inet.h> // Internet addresses manipulatutions

/* HEADER_H */
#endif
