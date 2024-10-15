# Server side MD5 calculating - Fixed version

import socket, PROTOCOL, threading, sys

dict_clients = {}
lst_ranges_calcualte = [i for i in range(0, 10000000000, PROTOCOL.JUMPS)]
enc_hash = bytes.fromhex(sys.argv[1])

lock = threading.Lock()
stop_event = threading.Event()

def handle_client(client: socket) -> None:
    global dict_clients, lst_ranges_calcualte

    client.send(enc_hash)
    
    client.settimeout(5)
    lst_ranges = []

    try:
        tasks_amount = PROTOCOL.dismantle_message_start(client.recv(1024))
        tasks_amount *= 2

        with lock:
            if len(lst_ranges_calcualte) == 0:
                return

            lst_ranges = lst_ranges_calcualte[:tasks_amount]
            del lst_ranges_calcualte[:tasks_amount]
            dict_clients[client] = lst_ranges

        client.send(PROTOCOL.build_message_chunks(lst_ranges))

        while not stop_event.is_set():
            try:
                protocolMsg, chunk = PROTOCOL.dismantle_response_message(client.recv(1024))

                if protocolMsg == PROTOCOL.CHUNK_IS_HASH[0]:
                    print("Hashed chunk is:", chunk.decode())
                    stop_event.set()
                    break

                if len(lst_ranges_calcualte) == 0:
                    break

                with lock:
                    lst_ranges = lst_ranges_calcualte[:2]
                    del lst_ranges_calcualte[:2]

                dict_clients[client] = lst_ranges
                client.send(PROTOCOL.build_runner_chunk_message(lst_ranges[0], lst_ranges[1]))

            except (socket.timeout, ConnectionError):
                with lock:
                    if client in dict_clients:
                        lst_ranges_calcualte += dict_clients[client]
                        del dict_clients[client]
                break

    finally:
        client.close()

def main():
    clients_threads = []
    server_socket = socket.socket()

    max_clients = 3

    try:
        server_socket.bind((PROTOCOL.SOURCE_IP, PROTOCOL.DEST_PORT))
        server_socket.listen(PROTOCOL.MAX_CLIENT)

        for _ in range(max_clients):
            if len(lst_ranges_calcualte) != 0:
                client_socket, _ = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                clients_threads.append(thread)

        input("Press enter to start the cracking!")
        
        for thread in clients_threads:
            thread.start()


        # Wait for all threads to finish execution
        for thread in clients_threads:
            thread.join()

    except Exception as error_main:
        print(error_main)

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
