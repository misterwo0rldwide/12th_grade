# Shared buffer for school assigment - Omer Kfir יב'3

from multiprocessing import shared_memory
from sys import argv
from time import sleep

__author__ = "MANOR"

W_DONE = 1
R_DONE = 2
W_FINI = 3
R_EXIT = 4

SHARED_MEMORY_NICKNAME = "ITZIK"
SHARED_MEMORY_MAX_SIZE = 100

FILE_NAME = "itzik.txt"

def get_shared():
    # Both open shared memory, if fails opens it
    
    existing_shm = 0
    try:
        existing_shm = shared_memory.SharedMemory(name=SHARED_MEMORY_NICKNAME)

    except Exception:
        # If Failed then open it
        existing_shm = shared_memory.SharedMemory(name=SHARED_MEMORY_NICKNAME, create=True, size=SHARED_MEMORY_MAX_SIZE)
    
    return existing_shm


def reader():
    shm = get_shared()
    buffer = shm.buf

    buffer[SHARED_MEMORY_MAX_SIZE - 1] = R_DONE # Sign reader has buffer

    while buffer[SHARED_MEMORY_MAX_SIZE - 1] != W_FINI:
    
        # Wait for writer to finish
        while buffer[SHARED_MEMORY_MAX_SIZE - 1] != W_DONE and buffer[SHARED_MEMORY_MAX_SIZE - 1] != W_FINI:
            pass

        if buffer[SHARED_MEMORY_MAX_SIZE - 1] == W_FINI:
            break
            
        line = buffer.tobytes().split(b'\n', 1)[0]
        print(line.decode())
        
        # Indicate that reading is final
        buffer[SHARED_MEMORY_MAX_SIZE - 1] = R_DONE
    
    buffer[SHARED_MEMORY_MAX_SIZE - 1] = R_EXIT
    shm.unlink()


def writer():
    shm = get_shared()
    buffer = shm.buf
    
    file_lines = open(FILE_NAME, "rb").readlines()
    for line in file_lines:
        
        # Wait for reader to finish
        while buffer[SHARED_MEMORY_MAX_SIZE - 1] != R_DONE:
            pass
        
        line_size = len(line)
        buffer[:line_size] = line # Write line
        
        # Indicate finished writing
        buffer[SHARED_MEMORY_MAX_SIZE - 1] = W_DONE
    
    while buffer[SHARED_MEMORY_MAX_SIZE - 1] != R_DONE:
        pass

    buffer[SHARED_MEMORY_MAX_SIZE - 1] = W_FINI
    while buffer[SHARED_MEMORY_MAX_SIZE - 1] != R_EXIT:
        pass
    
    # Wait for reader to unlink
    sleep(1)
    
    shm.close()
    shm.unlink()


# Functions dictionary
func = {'r' : reader, 'w' : writer}

def main():

    # Get if reader or writer from sys argv
    if len(argv) != 2:
        print("Wrong Usage: python shm.py r/w")
        
    state = argv[1]
    if state not in func:
        print("State has to be r - read or w - write")
        
    # Call function
    func[state]()
    
    
if __name__ == "__main__":
    main()