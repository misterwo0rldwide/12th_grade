/*
 * protocol.h - A header file for all protocol important data.
 * 		This file only provides msg type.
 *		
 *		Omer Kfir (C)
 */

#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <linux/stdarg.h> // Handling unkown amount of arguments

/* Message types */
#define MSG_PROCESS_CLOSE "MPC"
#define MSG_PROCESS_OPEN "MPO"
#define MSG_INPUT_EVENT "MIE"

#define PROTOCOL_SEPERATOR "\x1f"

/* Destination information */
#define DEST_IP "10.100.102.103"
#define DEST_PORT 6734

/* Protocol buffer handling */
#define BUFFER_SIZE 512
#define SIZE_OF_SIZE 4 // Characters amount of size of a message

int protocol_format(char *dst, const char* format, ...);

/* PROTOCOL_H */
#endif
