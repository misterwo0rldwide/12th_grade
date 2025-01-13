import sys, threading

sys.path.append("..")
import protocol

# Project currently running
proj_run = True

# Clients globals
clients_threads_connected = []
clients_recv_event = threading.Event()
clients_recv_lock = threading.Lock()

def get_clients_hooked_data(client : protocol.client) -> None:
    pass

def get_clients(server : protocol.server, max_clients : int) -> None:
    """
        Connect clients to server
        
        INPUT: server, max_clients
        OUTPUT: None
        
        @server -> Protocol server object
        @max_clients -> Maximum amount of clients chosen by the manager
    """
    global clients_connected
    
    # Main loop for receiving clients
    while proj_run:
    
        # If did not receive maximum amount of clients
        if len(clients_threads_connected) < max_clients:
            client = server.recv_client()
            clients_thread = threading.Thread(target=get_clients_hooked_data, args=(client))
            
            # Append client thread to list
            with clients_recv_lock:
                clients_threads_connected.append(clients_thread)
            
            clients_thread.start()
            
            # If reached maximum amount of clients set the lock
            if len(clients_threads_connected) == max_clients:
                clients_recv_event.clear()
            
        else:
            
            # Efficienlty waiting for receiving clients again
            clients_recv_event.wait()

def main():
    
    server = protocol.server()
    

if __name__ == "__main__":
    main=()