import struct
import random

def left_rotate(x, n):
    return ((x<<n) | (x>>(32-n)) & 0xFFFFFFFF)

def sha1(data_bytes):
    orig_len_bits = len(data_bytes) * 8
    data_bytes += b'\x80'
    while (len(data_bytes)%64) != 56:
        data_bytes += b'\x00'

    data_bytes += struct.pack('>Q', orig_len_bits)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for i in range(0, len(data_bytes), 64):
        block = data_bytes[i:i+64]
        w = [0] * 80
        for t in range(16):
            w[t] = struct.unpack('>I', block[t*4:t*4+4])[0]
        for t in range(16, 80):
            w[t] = left_rotate(w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16], 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for t in range(80):
            if 0 <= t <= 19:
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elif 20 <= t <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= t <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[t]) & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
        
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
    return struct.pack('>5I', h0, h1, h2, h3, h4)

def hmac_sha1(key, message):
    block_size = 64
    if len(key) > block_size:
        key = sha1(key)
    key = key.ljust(block_size, b'\x00')
    o_key_pad = bytes((k ^ 0x5C) for k in key)
    i_key_pad = bytes((k ^ 0x36) for k in key)
    
    inner = sha1(i_key_pad + message)
    outer = sha1(o_key_pad + inner)
    return outer

key = bytes(random.randrange(0, 256) for _ in range(16))
message = b"Xin chao day la thong diep demo MAC0"
mac = hmac_sha1(key, message)
print("key (hex):", key.hex())
print("message (hex):", message.hex())
print("HMAC (hex):", mac.hex())


mac_verify = hmac_sha1(key, message)
print("Verification successful:", mac == mac_verify)