import sys


LFSR1 = 19
LFSR2 = 22
LFSR3 = 23

LFSR1_TAPS = [13, 16, 17, 18]
LFSR2_TAPS = [20, 21]
LFSR3_TAPS = [7, 20, 21, 22]

LFSR1_CLOCK_BIT = 8
LFSR2_CLOCK_BIT = 10
LFSR3_CLOCK_BIT = 10

class A51Cipher:
    def __init__(self):
        self.lfsr1 = 0
        self.lfsr2 = 0
        self.lfsr3 = 0

    def get_majority_bit(self):
        b1 = (self.lfsr1 >> (LFSR1 - 1 - LFSR1_CLOCK_BIT)) & 1
        b2 = (self.lfsr2 >> (LFSR2 - 1 - LFSR2_CLOCK_BIT)) & 1
        b3 = (self.lfsr3 >> (LFSR3 - 1 - LFSR3_CLOCK_BIT)) & 1
        return (b1 + b2 + b3) >= 2
    
    def clock_lfsr(self, lfsr_val, lfsr_taps, lfsr_bits):
        output_bit = lfsr_val & 1

        feedback_bit = 0

        for tap in lfsr_taps:
            feedback_bit ^= (lfsr_val >> tap ) & 1

        lfsr_val >>= 1
        lfsr_val |= (feedback_bit << (lfsr_bits - 1))

        return lfsr_val, output_bit
    
    def clock(self):
        majorrity = self.get_majority_bit()

        if ((self.lfsr1 >> LFSR1_CLOCK_BIT) & 1) == majorrity:
            self.lfsr1, _ = self.clock_lfsr(self.lfsr1, LFSR1_TAPS, LFSR1)
        if ((self.lfsr2 >> LFSR2_CLOCK_BIT) & 1) == majorrity:
            self.lfsr2, _ = self.clock_lfsr(self.lfsr2, LFSR2_TAPS, LFSR2)
        if ((self.lfsr3 >> LFSR3_CLOCK_BIT) & 1) == majorrity:
            self.lfsr3, _ = self.clock_lfsr(self.lfsr3, LFSR3_TAPS, LFSR3)

    def generate_keystream_bit(self):
        _, output_bit1 = self.clock_lfsr(self.lfsr1, LFSR1_TAPS, LFSR1)
        _, output_bit2 = self.clock_lfsr(self.lfsr2, LFSR2_TAPS, LFSR2)
        _, output_bit3 = self.clock_lfsr(self.lfsr3, LFSR3_TAPS, LFSR3)

        return output_bit1 ^ output_bit2 ^ output_bit3
    
    def initialize(self, key, frame_number):
        key_val = int.from_bytes(key, sys.byteorder)
        frame_val = int.from_bytes(frame_number, sys.byteorder)

        for i in range(64):
            key_bit = (key_val >> i) & 1
            frame_bit = (frame_val >> i) & 1

            self.lfsr1, _ = self.clock_lfsr(self.lfsr1, LFSR1_TAPS, LFSR1)
            self.lfsr1 ^= key_bit
            self.lfsr1 ^= frame_bit

            self.lfsr2, _ = self.clock_lfsr(self.lfsr2, LFSR2_TAPS, LFSR2)
            self.lfsr2 ^= key_bit
            self.lfsr2 ^= frame_bit

            self.lfsr3, _ = self.clock_lfsr(self.lfsr3, LFSR3_TAPS, LFSR3)
            self.lfsr3 ^= key_bit
            self.lfsr3 ^= frame_bit

        for i in range(100):
            self.clock()

    def encrypt_decrypt(self, data):
        result = bytearray()

        for byte in data:
            keystream_byte = 0

            for i in range(8):
                keystream_bit = self.generate_keystream_bit()
                keystream_byte |= (keystream_bit << (7 - i))

            result_byte = byte ^ keystream_byte
            result.append(result_byte)
        
        return bytes(result)
    
cipher = A51Cipher()

secret_key = b'\x12\x34\x56\x78\x9a\xbc\xde\xf0'
frame_number = b'\x00\x00\x01'

cipher.initialize(secret_key, frame_number)

plaintext = b'Hello, thi is a test message.'

ciphertext = cipher.encrypt_decrypt(plaintext)
print("ban ro :", plaintext.decode('utf-8'))
print("ban ma hoa (hex): ", ciphertext.hex())

cipher_decrypt = A51Cipher()
cipher_decrypt.initialize(secret_key, frame_number)
decrypted_text = cipher_decrypt.encrypt_decrypt(ciphertext)
print("ban giai ma :", decrypted_text.decode('utf-8'))
        
