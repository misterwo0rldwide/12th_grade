#   'Silent net' project server
#   
#       Contains server side implementation 
#       Stores and handles DB
#
#   Omer Kfir (C)

import sys, threading

sys.path.append("..")
import protocol

# Project currently running
proj_run = True

# Clients globals
clients_connected = [] # List of (thread object, client object)
clients_recv_event = threading.Event()
clients_recv_lock = threading.Lock()

max_clients = 20 # Default number (Can be any other number)

def process_client_data(client : protocol.client, data_fields : list[bytes]) -> None:
    """
        Processes client's sent data
        
        INPUT: client, data
        OUTPUT: None
        
        @client -> Protocol client object
        @data -> List of fields of message sent by client
    """
    
    # For now we don't have any thing to process so just print
    print(client.get_address()[0], *data_fields)

def get_clients_hooked_data(client : protocol.client) -> None:
    """
        Gets connected client data from hooked functions
        
        INPUT: client
        OUTPUT: None
        
        @client -> Protocol client object
    """
    global clients_connected
    
    while proj_run:
        data = client.protocol_recv()
        
        # Ensure client is connected
        if data == b'':
            break
    
        process_client_data(client, data)
    
    # Search for client thread in list
    # Lock even when searching since list can change by the time finished
    # Searching and going to remove
    
    with clients_recv_lock:
        
        # Search for client in clients list
        for index in range(len(clients_connected)):
            _, client_object = clients_connected[index]
            
            if client_object == client:
                del clients_connected[index]
                break
    
    # If removed and now amount of clients is one below max
    # We can let the main thread which receives clients to get
    # Back to receiving clients
    if len(clients_connected) + 1 == max_clients:
        clients_recv_event.set()

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
        if len(clients_connected) < max_clients:
            client = server.recv_client()
            clients_thread = threading.Thread(target=get_clients_hooked_data, args=(client,))
            
            # Append client thread to list
            with clients_recv_lock:
                clients_connected.append((clients_thread, client))
            
            clients_thread.start()
            
            # If reached maximum amount of clients set the lock
            if len(clients_connected) >= max_clients:
                clients_recv_event.clear()
            
        else:
            
            # Efficienlty waiting for receiving clients again
            clients_recv_event.wait()

def main():
    global max_clients

    server = protocol.server(max_clients)
    get_clients(server, max_clients)
    

if __name__ == "__main__":
    main()