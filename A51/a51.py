# chuyen bytes --> danh sach bit
def bytes_to_bits(b):
    bits = []

    for byte in b:
        for i in range(8):
            bits.append((byte >> (7-i)) & 1)

    return bits

# chuyen danh sach bit --> bytes
def bits_to_bytes(bits):
    out = []

    for i in range(0, len(bits), 8):
        byte = 0

        for j in range(8):
            byte = (byte << 1) | bits[i +j]

        out.append(byte)
    
    return bytes(out)

# khoi tao 3 LFSR tu khoa
def init_registers_from_key(key_bytes):
    key_bits = bytes_to_bits(key_bytes)

    while len(key_bits) < (19+22+23):
        key_bits += key_bits

    R1 = key_bits[0:19]
    R2 = key_bits[19:19+22]
    R3 = key_bits[19+22:19+22+23]

    return R1[:], R2[:], R3[:]

def majority(a, b, c):
    return 1 if (a+b+c) >= 2 else 0

def clock_reg(reg, taps):
    feedback = 0

    for t in taps:
        feedback ^= reg[t]

    out = reg.pop()
    reg.insert(0, feedback)

    return out

def a5_1_keystream_from_key(key_bytes, n):
    R1, R2, R3 = init_registers_from_key(key_bytes)

    ks = []

    for _ in range(n):
        m = majority(R1[8], R2[10], R3[10])

        if R1[8] == m:
            clock_reg(R1, [13,16,17,18])

        if R2[10] == m:
            clock_reg(R2, [20,21])

        if R3[10] == m:
            clock_reg(R3, [7,20,21,22])
        
        ks_bit = R1[-1] ^ R2[-1] ^ R3[-1]
        ks.append(ks_bit)
    
    return ks

def stream_xor_bytes_with_bitstream(data_bytes, keystream_bits):
    data_bits = bytes_to_bits(data_bytes)
    out_bits = [d ^ k for d, k in zip(data_bits, keystream_bits)]

    return bits_to_bytes(out_bits)

key = b"examplekey"
plaintext = b"Hello, A5/1"
ks = a5_1_keystream_from_key(key, len(bytes_to_bits(plaintext)))
ciphertext = stream_xor_bytes_with_bitstream(plaintext, ks)
ks2 = a5_1_keystream_from_key(key, len(bytes_to_bits(ciphertext)))
decrypted = stream_xor_bytes_with_bitstream(ciphertext, ks2)

print("Plaintext : ", plaintext)
print("Ciphertext(hex) : ", ciphertext)
print("Decrypted : ", decrypted)