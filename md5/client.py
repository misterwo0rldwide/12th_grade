# Client side MD5 calculating - Fixed version

import socket, subprocess, threading, PROTOCOL, sys, os

hash = -1
cracked_hash = b""

thread_lock = threading.Lock()
stop_event = threading.Event()

jumps = PROTOCOL.JUMPS
main_socket = None

def bruteforce_hash(start_first, start_second, client_socket):
    global cracked_hash

    try:
        while True:
            if stop_event.is_set():
                return

            # First range calculation
            output = subprocess.check_output(args=f"md5.exe {hash} {start_first} {start_first + jumps}", text=True)

            if output:
                cracked_hash = output[:10].encode()
                stop_event.set()

            # Check the second range if available and if hash not found yet
            if start_second != -1 and not stop_event.is_set():
                output = subprocess.check_output(args=f"md5.exe {hash} {start_second} {start_second + jumps}", text=True)

                if output:
                    cracked_hash = output[:10].encode()
                    stop_event.set()

            if cracked_hash:
                client_socket.send(PROTOCOL.build_response_message(PROTOCOL.CHUNK_IS_HASH, cracked_hash))
                break
            else:
                client_socket.send(PROTOCOL.build_response_message(PROTOCOL.CHUNK_NOT_HASH, cracked_hash))
                start_first, start_second = PROTOCOL.dismant_runner_chunk_message(client_socket.recv(1024))

    except Exception as e:
        print(f"Error in bruteforce_hash: {e}")


def main():
    global hash, main_socket

    threads = []
    dest_ip, cpu, load = sys.argv[1], os.cpu_count(), int(sys.argv[2])

    try:
        main_socket = socket.socket()
        main_socket.connect((dest_ip, PROTOCOL.DEST_PORT))

        hash = main_socket.recv(1024).hex()
        main_socket.send(PROTOCOL.build_message_start(cpu, load))

        lst_ranges = PROTOCOL.dismantle_message_chunks(main_socket.recv(1024))

        for rang in range(0, len(lst_ranges), 2):
            client_socket = main_socket  # Create a local client socket reference for each thread
            thread = threading.Thread(target=bruteforce_hash, args=(lst_ranges[rang], lst_ranges[rang + 1] if rang + 1 < len(lst_ranges) else -1, client_socket))
            thread.start()
            threads.append(thread)

        main_socket.settimeout(2)

        for thread in threads:
            thread.join()

    except (socket.timeout, ConnectionError) as e:
        print(f"Connection lost or timed out: {e}")
    finally:
        if main_socket:
            main_socket.close()


if __name__ == "__main__":
    main()
