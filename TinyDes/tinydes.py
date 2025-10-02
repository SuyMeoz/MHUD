IP = [5, 2, 7, 4, 1, 8, 3, 6]

FP = [5, 2, 7, 4, 1, 8, 3, 6]

E = [4, 1, 2, 3, 2, 3, 4, 1]

S1 = [
[1, 0, 3, 2],
[3, 2, 1, 0],
[0, 2, 1, 3],
[3, 1, 3, 2]
]

S2 = [
[0, 1, 2, 3],
[2, 0, 1, 3],
[3, 0, 1, 0],
[2, 1, 0, 3]
]

P = [2, 4, 3, 1]

PC1 = [3, 5, 2, 7, 4, 1, 8, 6]
PC2 = [6, 3, 7, 4, 8, 5, 1, 2]

SHIFT_BITS = [1, 1, 2, 2]

class TinyDes:
    def __init__(self, key):
        self.key = self._to_binary_list(key, 8)
        self.subkeys = self._generate_subkeys()

    def _to_binary_list(self, byte, num_bits):
        return [(byte >> i) & 1 for i in range(num_bits -1, -1, -1)]
    
    def _from_binary_list(self, bits_list):
        result = 0
        for bit in bits_list:
            result = (result << 1) | bit
        return result
    
    def _permute(self, data, p_table):
        return [data[i - 1] for i in p_table]
    
    def _generate_subkeys(self):
        key_permuted = self._permute(self.key, PC1)
        C = key_permuted[:4]
        D = key_permuted[4:]
        subkeys = []
        for shift in SHIFT_BITS:
            C = C[shift:] + C[:shift]
            D = D[shift:] + D[:shift]
            combined = C + D
            subkey = self._permute(combined, PC2)
            subkeys.append(subkey)
        return subkeys
    
    def _feistel_round(self, left, right, subkey, s_boxes):
        expanded_right = self._permute(right, E)

        xored_result = [a ^ b for a, b in zip(expanded_right, subkey)]
        
        sbox_result = []

        sbox1_input = xored_result[:4]
        sbox2_input = xored_result[4:]

        row1 = sbox1_input[0] * 2 + sbox1_input[3]
        col1 = sbox1_input[1] * 2 + sbox1_input[2]
        sbox1_value = s_boxes[0][row1][col1]
        sbox_result.extend(self._to_binary_list(sbox1_value, 2))

        row2 = sbox2_input[0] * 2 + sbox2_input[3]
        col2 = sbox2_input[1] * 2 + sbox2_input[2]
        sbox2_value = s_boxes[1][row2][col2]
        sbox_result.extend(self._to_binary_list(sbox2_value, 2))

        p_box_result = self._permute(sbox_result, P)

        new_left = right
        new_right = [a ^ b for a, b in zip(left, p_box_result)]

        return new_left, new_right
    
    def encrypt(self, plaintext):
        data = self._to_binary_list(plaintext, 8)
        permuted_data = self._permute(data, IP)
        left = permuted_data[:4]
        right = permuted_data[4:]

        for i in range(4):
            left, right = self._feistel_round(left, right, self.subkeys[i], [S1, S2])

        combined = right + left
        ciphertext_bits = self._permute(combined, FP)
        ciphertext = self._from_binary_list(ciphertext_bits)
        return ciphertext
    
    def decrypt(self, ciphertext):
        data = self._to_binary_list(ciphertext, 8)
        permuted_data = self._permute(data, IP)
        left = permuted_data[:4]
        right = permuted_data[4:]

        for i in range(3, -1, -1):
            left, right = self._feistel_round(left, right, self.subkeys[i], [S1, S2])

        combined = right + left
        plaintext_bits = self._permute(combined, FP)
        plaintext = self._from_binary_list(plaintext_bits)
        return plaintext
    
key = 0b10101010
plaintext = 0b11001100
des = TinyDes(key)
encrypted_text = des.encrypt(plaintext)
decrypted_text = des.decrypt(encrypted_text)
print("Plaintext:", bin(plaintext)[2:].zfill(8))
print("Ciphertext:", bin(encrypted_text)[2:].zfill(8))
print("Decrypted:", bin(decrypted_text)[2:].zfill(8))

print("Match:", decrypted_text == plaintext) 