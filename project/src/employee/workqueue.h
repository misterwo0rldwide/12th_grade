/*
 *	'silent net' workqueue header file.
 *	Defines specific work message structures
 *
 * 	Omer Kfir (C)
 */

#include "headers.h"

void workqueue_message(struct workqueue_struct*, void (*)(struct work_struct *), const char*, size_t);

/* Workqueue message */
typedef struct wq_msg
{
        /* Current mission */
        struct work_struct work;

        /* Message dara for sending data */
        char msg_buf[BUFFER_SIZE];
        size_t length;
}wq_msg;

