import struct, math

def left_rotate32(x, c):
    return ((x<<c) | (x>>(32-c))) & 0xFFFFFFFF

def md5(data_bytes):
    orig_len_bits = (len(data_bytes) * 8) & 0xFFFFFFFFFFFFFFFF
    data_bytes += b'\x80'
    while (len(data_bytes) % 64) != 56:
        data_bytes += b'\x00'
    data_bytes += struct.pack('<Q', orig_len_bits)

    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    K = [int(abs(math.sin(i + 1)) * (1<<32)) & 0xFFFFFFFF for i in range(64)]

    for i in range(0, len(data_bytes), 64):
        chunk = data_bytes[i:i+64]
        M = list(struct.unpack('<16I', chunk))

        a, b, c, d = A, B, C, D

        for i_round in range(64):
            if 0 <= i_round <= 15:
                F = (b & c) | (~b & d)
                g = i_round
            elif 16 <= i_round <= 31:
                F = (b & c) | (~d & c)
                g = (5 * i_round + 1) % 16
            elif 32 <= i_round <= 47:
                F = b ^ c ^ d  
                g = (3 * i_round + 5) % 16
            else:
                F = c ^ (b | ~d)
                g = (7 * i_round) % 16

            F = (F + a + K[i_round] + M[g]) & 0xFFFFFFFF
            a = d 
            d = c 
            c = b 
            b = (b + left_rotate32(F, s[i_round])) & 0xFFFFFFFF
           
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF
    return struct.pack('<4I', A, B, C, D)

m1 = b"Hello MD5"
m2 = b"Hello MD5?"

print("MD5 (m1):", md5(m1).hex())
print("MD5 (m2):", md5(m2).hex())