/*
 *	'silent net' work queue handling
 *	
 *	Omer Kfir (C)
 */

#include "protocol.h"
#include "headers.h"
#include "workqueue.h"

/* Queue a new message to be sent */
void workqueue_message(struct workqueue_struct *workqueue, void (*queued_function)(struct work_struct *), const char *msg, size_t length)
{
        struct wq_msg *work;

        /* Because we are only able to send the pointer to workqueue
        * We will create a 'father' struct for it, which will contain it
        * And in the function we will perform container_of in order to get
        * The message itself and the length
        */
        work = kmalloc(sizeof(wq_msg), GFP_ATOMIC);
        if ( !work )
                return;

        /* Initialize work for it to point to the desired function*/
        INIT_WORK(&work->work, queued_function);

	/* Copy data to wq_msg metadata */
        memcpy(work->msg_buf, msg, min(length, BUFFER_SIZE - 1));
        work->length = min(length, BUFFER_SIZE - 1);

        /* Push work to workqueue - thread safe function (dont worry :) )*/
        queue_work(workqueue, &work->work);
}
