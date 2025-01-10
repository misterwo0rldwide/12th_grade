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
#include <linux/input.h> // Structures of devices

/* HEADER_H */
#endif
