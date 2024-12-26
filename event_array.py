import threading, sys
from random import randint

__author__ = "Manor"
arr_size = 100

rand_lst = [radint(1, 101) for _ in range(arr_size)]

count_event = threading.Event()
write_event = threading.Event()

counting_lock = threading.Lock()
threads_finished = 0

def shoot_the_opps(index):
    global threads_finished
    
    for _ in range(int(sys.argv[1])):
        
        

def main():

    print(rand_lst)
    lst_threads = [threading.Thread(target=calc, args=(i)) for i in range(arr_size)]
    
    for thread in lst_threads:
        thread.start()
    
    for thread in lst_threads:
        thread.join()
    

if __name__ = "__main__":
    main()