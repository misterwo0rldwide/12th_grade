obj-m += proj.o
proj-y := kClientHook.o tcp_socket.o protocol.o workqueue.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
