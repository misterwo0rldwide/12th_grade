import threading, sys
from random import randint

__author__ = "Manor"
arr_size = 100

rand_lst = [radint(1, 101) for _ in range(arr_size)]

count_event = threading.Event()
write_event = threading.Event()

counting_lock = threading.Lock()
threads_finished = 0

def calculate_operation(index):
    
    #  Take value inside the index
    val_index = rand_lst[index]
    
    #  Take value before and after the index in cyclic order
    val_before = rand_lst[(index - 1) % arr_size]
    val_after = rand_lst[(index + 1) % arr_size]
    
    
    
    

def operate(index):
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