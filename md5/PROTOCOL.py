#  Protocol md5 calculating - Omer Kfir יב'3

SOURCE_IP = "0.0.0.0"
DEST_PORT = 6734

MAX_CLIENT = 20

JUMPS = 100000

CHUNK_NOT_HASH = b"\xff"
CHUNK_IS_HASH = b"\xfe"
 


def build_message_start(cpu_level : int, core_level : int) -> bytes:
    """
        Builds start message between client and server
        Data format is binary and order is little endian
    """
    
    msg = cpu_level.to_bytes(1, byteorder = 'little')
    msg += core_level.to_bytes(1, byteorder = 'little')
    
    return msg



def dismantle_message_start(msg : bytes) -> int:
    """
        Dismants start message between client and server
        Returns number of chunks to send to client
    """
    
    chunks = msg[1] / 100
    chunks *= msg[0]
    
    return int(chunks)


def build_message_chunks(ranges : list[int]) -> bytes:
    """
        Builds message which guides the client for chunks
        To calculate
    """

    msg = b"".join([r.to_bytes(6, byteorder='little') for r in ranges])

    return msg


def dismantle_message_chunks(msg : bytes) -> list[int]:
    """
        Dismants message which guides the client for chunks
        To calculate
    """

    ranges = [int.from_bytes(msg[i:i+6], byteorder='little') for i in range(0, len(msg), 6)]
    
    return ranges


def build_response_message(protcolMsg : bytes, chunk : bytes) -> bytes:
    """
        Builds message response from to server about chunk
    """

    msg = protcolMsg
    msg += chunk

    return msg


def dismantle_response_message(msg : bytes) -> tuple[bytes, int]:
    """
        Dismants message response from to server about chunk
    """

    protocolMsg = msg[0]
    chunk_number = msg[1:]

    return protocolMsg, chunk_number

def build_runner_chunk_message(chunk_first : int, chunk_second : int) -> bytes:
    """
        When one of client processes finished we send two chunks
        For it
    """

    msg = chunk_first.to_bytes(6, byteorder='little')
    msg += chunk_second.to_bytes(6, byteorder='little')

    return msg

def dismant_runner_chunk_message(msg : bytes) -> tuple[int, int]:
    """
        When one of client processes finished we send two chunks
        For it
    """

    return int.from_bytes(msg[0:6], byteorder='little'), int.from_bytes(msg[6:12], byteorder='little')