import threading, sys
from random import randint

__author__ = "Manor"
arr_size = int(sys.argv[1])

rand_lst = [randint(1, 100) for _ in range(arr_size)]

count_event = threading.Event()
write_event = threading.Event()
print_event = threading.Event()

counting_lock = threading.Lock()
threads_finished = 0

def calculate_operation(index):
    
    #  Take value inside the index
    val_index = rand_lst[index]
    
    #  Take value before and after the index in cyclic order
    val_before = rand_lst[(index - 1) % arr_size]
    val_after = rand_lst[(index + 1) % arr_size]
    
    if val_index < val_before and val_index < val_after:
        val_index += 1
    
    elif val_index > val_before and val_index > val_after:
        val_index -= 1
    
    return val_index


def operate(index):
    global threads_finished
    
    for _ in range(int(sys.argv[2])):
        
        #  Set event of reading
        count_event.clear()
        number = calculate_operation(index)
        
        #  To count the number of threads that have read we need to lock since it is a shared variable
        with counting_lock:
            threads_finished += 1
            
            if threads_finished == arr_size:
                threads_finished = 0
                print_event.set()
                write_event.clear()
                write_event.wait()
                write_event.clear()
                count_event.set()
                
        #  All threads wait to continue
        count_event.wait()
        
        #  Now all threads write "at the same time"
        
        #  Set the index to the right value
        rand_lst[index] = number
        
        #  To count the number of threads that have written their value we need a lock
        with counting_lock:
            threads_finished += 1
            
            if threads_finished == arr_size:
                threads_finished = 0
                write_event.set()
        
        #  All threads wait to continue
        write_event.wait()
        
def main():

    lst_threads = [threading.Thread(target=operate, args=(i,)) for i in range(arr_size)]
    
    #  Start all threads
    for thread in lst_threads:
        thread.start()
    
    #  The main thread will be the one who prints the values
    for _ in range(int(sys.argv[2])):
        print_event.wait()
        print(rand_lst)
        print_event.clear()
        write_event.set()
    
    for thread in lst_threads:
        thread.join()
    

if __name__ == "__main__":
    main()
