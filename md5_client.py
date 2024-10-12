#  MD5 Cracker - Omer Kfir יב'3

import ctypes

MD5_HASH_SIZE = 16

#  Loading the dll and defining function
MD5_DLL = ctypes.CDLL("./md5.dll")
MD5_DLL.md5String.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8)]


def calculate_md5(enc_str : bytes) -> int:
    """
        Gets encoded string and returns its md5 hashed result
        As an int type value
    """

    md5_result = (ctypes.c_uint8 * MD5_HASH_SIZE)()
    MD5_DLL.md5String(enc_str, md5_result)  #  Returns the hash in md5_result
    
    length_result = len(md5_result)
    return sum(md5_result[i] * (256 ** (length_result - i - 1)) for i in range(length_result))




def main():
    pass


if __name__ == "__main__":
    main()