# ================== Bảng DES ==================
IP = [58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17, 9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5, 4, 5,
6, 7, 8, 9, 8, 9, 10, 11,
12, 13, 12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21, 20, 21,
22, 23, 24, 25, 24, 25, 26, 27,
28, 29, 28, 29, 30, 31, 32, 1]

S_BOXES = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    # S3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    # S4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Bảng hoán vị P-box
P = [16,7,20,21,29,12,28,17,
1,15,23,26,5,18,31,10,
2,8,24,14,32,27,3,9,
19,13,30,6,22,11,4,25]

# Bảng hoán vị PC1 (Khóa chính 64 bit -> 56 bit)
PC1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Bảng hoán vị PC2 (56 bit -> 48 bit)
PC2 = [14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]

SHIFT_BITS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

class DES:
    def __init__(self, key):
        self.key = self._to_binary_list(key)
        self.subkeys = self._generate_subkeys() 

    def _to_binary_list(self, byte_data):
        bit_list = []

        for byte in byte_data:
            for i in range(7, -1, -1):
                bit_list.append((byte >> i) & 1)

        return bit_list
    
    def _from_binary_list(self, bit_list):
        byte_data = bytearray()

        for i in range(0, len(bit_list), 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bit_list[i + j]
            byte_data.append(byte)

        return bytes(byte_data)
    
    def _permute(self, data, p_table):
        return [data[bit -1 ] for bit in p_table]
    
    def _feistel(self, right, subkey):
        expanded_right = self._permute(right, E)
        xored_result = [a ^ b for a,b in zip(expanded_right, subkey)]

        sbox_result = []

        for i in range(8):
            sbox_input = xored_result[i*6:(i+1)*6]
            row = (sbox_input[0] << 1) + sbox_input[5]
            col = (sbox_input[1] << 3) + (sbox_input[2] << 2) + (sbox_input[3] << 1) + sbox_input[4]
            val = S_BOXES[i][row][col]

            sbox_result.extend([(val >> 3) & 1,
                                (val >> 2) & 1,
                                (val >> 1) & 1,
                                val & 1])
            
        return self._permute(sbox_result, P)
        
    def _generate_subkeys(self):
        key_permuted = self._permute(self.key, PC1)

        C = key_permuted[:28]
        D = key_permuted[28:]
        subkeys = []

        for shift in SHIFT_BITS:
            C = C[shift:] + C[:shift]
            D = D[shift:] + D[:shift]
            combined = C + D
            subkey = self._permute(combined, PC2)
            subkeys.append(subkey)

        return subkeys
    
    def encrypt_block(self, plaintext_block):
        data = self._to_binary_list(plaintext_block)
        permuted_data = self._permute(data, IP)
        left, right = permuted_data[:32], permuted_data[32:]
        for i in range(16):
            temp_left = left

            left = right
            f_result = self._feistel(right, self.subkeys[i])
            right = [a ^ b for a, b in zip(temp_left, f_result)]

        combined = right + left
        ciphertext = self._permute(combined, FP)
        return self._from_binary_list(ciphertext)
    
    def decrypt_block(self, ciphertext_block):
        data = self._to_binary_list(ciphertext_block)
        permuted_data = self._permute(data, IP)
        left, right = permuted_data[:32], permuted_data[32:]

        for i in range(15, -1, -1):
            temp_left = left
            left = right
            f_result = self._feistel(right, self.subkeys[i])
            right = [a ^ b for a, b in zip(temp_left, f_result)]

        combined = right + left
        decrypt_data = self._permute(combined, FP)
        return self._from_binary_list(decrypt_data)
        

class TripleDES:
    def __init__(self, key1, key2, key3):
        self.des1 = DES(key1)
        self.des2 = DES(key2)
        self.des3 = DES(key3)

    def encrypt(self, plaintext):
        sep1 = self.des1.encrypt_block(plaintext)
        sep2 = self.des2.decrypt_block(sep1)
        ciphertext = self.des3.encrypt_block(sep2)
        return ciphertext
    
    def decrypt(self, ciphertext):
        sep1 = self.des3.decrypt_block(ciphertext)
        sep2 = self.des2.encrypt_block(sep1)
        plaintext = self.des1.decrypt_block(sep2)
        return plaintext
    

key1 = b'12345678'
key2 = b'abcdefgh'
key3 = b'IJKLMNOP'

plaintext = b'12345678'

triple_des_cipher = TripleDES(key1, key2, key3)

ciphertext = triple_des_cipher.encrypt(plaintext)
print(f"Bản rõ: {plaintext.hex()}")
print(f"Bản mã: {ciphertext.hex()}")
decrypted_text = triple_des_cipher.decrypt(ciphertext)
print(f"Giải mã: {decrypted_text.hex()}")
print(f"Khớp bản rõ: {decrypted_text == plaintext}")