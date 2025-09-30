# A5/1 Stream Cipher (Python Implementation)

- Khởi tạo 3 thanh ghi dịch phản hồi tuyến tính (LFSR) bằng khóa bí mật và frame number.

- Sinh keystream dựa trên cơ chế majority clocking.

- Thực hiện mã hóa/giải mã bằng cách XOR dữ liệu với keystream.

## 1. Định nghĩa tham số LFSR
```python
LFSR1 = 19
LFSR2 = 22
LFSR3 = 23

LFSR1_TAPS = [13, 16, 17, 18]
LFSR2_TAPS = [20, 21]
LFSR3_TAPS = [7, 20, 21, 22]

LFSR1_CLOCK_BIT = 8
LFSR2_CLOCK_BIT = 10
LFSR3_CLOCK_BIT = 10
```
`LFSR1, LFSR2, LFSR3`: độ dài (số bit) của 3 thanh ghi.

`*_TAPS`: các vị trí bit dùng để tính feedback (XOR).

`*_CLOCK_BIT`: vị trí bit dùng để tính majority.

## 2. Lớp A51Cipher
```python
class A51Cipher:
    def __init__(self):
        self.lfsr1 = 0
        self.lfsr2 = 0
        self.lfsr3 = 0
```
Mỗi LFSR được lưu dưới dạng **số nguyên**.

Bit thấp nhất (LSB) là output bit, bit cao nhất (MSB) là **feedback bit**.

## 3. Hàm majority
```python
def get_majority_bit(self):
    b1 = (self.lfsr1 >> (LFSR1 - 1 - LFSR1_CLOCK_BIT)) & 1
    b2 = (self.lfsr2 >> (LFSR2 - 1 - LFSR2_CLOCK_BIT)) & 1
    b3 = (self.lfsr3 >> (LFSR3 - 1 - LFSR3_CLOCK_BIT)) & 1
    return (b1 + b2 + b3) >= 2
```
Lấy bit clock từ mỗi LFSR.

Trả về giá trị đa số (ít nhất 2 trong 3 giống nhau).

## 4. Clock một LFSR
```python
def clock_lfsr(self, lfsr_val, lfsr_taps, lfsr_bits):
    output_bit = lfsr_val & 1
    feedback_bit = 0
    for tap in lfsr_taps:
        feedback_bit ^= (lfsr_val >> tap) & 1
    lfsr_val >>= 1
    lfsr_val |= (feedback_bit << (lfsr_bits - 1))
    return lfsr_val, output_bit
```
Lấy `output_bit` (bit cuối).

Tính `feedback_bit` bằng XOR các vị trí taps.

Dịch phải toàn bộ thanh ghi, chèn feedback vào MSB.

Trả về thanh ghi mới và output bit.

## 5. Clock theo majority
```python
def clock(self):
    majorrity = self.get_majority_bit()

    if ((self.lfsr1 >> LFSR1_CLOCK_BIT) & 1) == majorrity:
        self.lfsr1, _ = self.clock_lfsr(self.lfsr1, LFSR1_TAPS, LFSR1)
    if ((self.lfsr2 >> LFSR2_CLOCK_BIT) & 1) == majorrity:
        self.lfsr2, _ = self.clock_lfsr(self.lfsr2, LFSR2_TAPS, LFSR2)
    if ((self.lfsr3 >> LFSR3_CLOCK_BIT) & 1) == majorrity:
        self.lfsr3, _ = self.clock_lfsr(self.lfsr3, LFSR3_TAPS, LFSR3)
```
Chỉ dịch những thanh ghi có bit clock trùng với **majority**.

## 6. Sinh keystream bit
```python
def generate_keystream_bit(self):
    _, output_bit1 = self.clock_lfsr(self.lfsr1, LFSR1_TAPS, LFSR1)
    _, output_bit2 = self.clock_lfsr(self.lfsr2, LFSR2_TAPS, LFSR2)
    _, output_bit3 = self.clock_lfsr(self.lfsr3, LFSR3_TAPS, LFSR3)
    return output_bit1 ^ output_bit2 ^ output_bit3
```
Lấy output bit từ cả 3 LFSR.

XOR chúng để tạo 1 bit keystream.

## 7. Khởi tạo với key và frame number
```python
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
```
Chèn 64 bit khóa và frame number vào 3 LFSR.

Sau đó clock thêm 100 lần để “làm loãng” trạng thái ban đầu.

## 8. Mã hóa / Giải mã
```python
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
```
Sinh 1 byte keystream (8 bit).

XOR với byte dữ liệu.

Vì XOR là phép đối xứng → cùng hàm dùng cho cả mã hóa và giải mã.

## 9. Chạy thử
```python
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
```
Khởi tạo cipher với key và frame number.

Mã hóa plaintext → ciphertext.

Tạo lại cipher, giải mã ciphertext → plaintext.