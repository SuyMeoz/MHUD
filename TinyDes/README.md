# 📝 TinyDES - Giải thích chi tiết từng dòng code


## 1. Các bảng hoán vị và S-box
```python
IP = [5, 2, 7, 4, 1, 8, 3, 6]      # Bảng hoán vị đầu (Initial Permutation): Xáo trộn thứ tự 8 bit đầu vào.
FP = [5, 2, 7, 4, 1, 8, 3, 6]      # Bảng hoán vị cuối (Final Permutation): Xáo trộn lại thứ tự bit cuối cùng.
E = [4, 1, 2, 3, 2, 3, 4, 1]       # Bảng mở rộng (Expansion): Biến 4 bit thành 8 bit bằng cách lặp lại và hoán vị.
S1, S2 = ...                       # 2 S-box 4x4: Bảng thay thế phi tuyến tính, nhận 4 bit đầu vào, trả về 2 bit.
P = [2, 4, 3, 1]                   # Bảng hoán vị P-box: Đổi chỗ 4 bit đầu ra S-box.
PC1, PC2 = ...                     # Bảng hoán vị cho sinh khóa con: Dùng để trộn key khi sinh subkey.
SHIFT_BITS = [1, 1, 2, 2]          # Số bit dịch vòng mỗi vòng sinh khóa: Quy định số bit dịch trái mỗi vòng.
```

## 2. Lớp TinyDes
### 2.1. Hàm khởi tạo
```python
def __init__(self, key):
    self.key = self._to_binary_list(key, 8)           # Chuyển key (số nguyên) thành list 8 bit (dạng [0,1,...])
    self.subkeys = self._generate_subkeys()           # Gọi hàm sinh 4 khóa con, lưu vào self.subkeys
```
**Kết quả:**
- self.key: list 8 bit của key
- self.subkeys: list 4 subkey, mỗi subkey là list 8 bit

### 2.2. Chuyển đổi giữa số và list bit
```python
def _to_binary_list(self, byte, num_bits):
    # Duyệt từ bit cao nhất (num_bits-1) đến thấp nhất (0)
    return [(byte >> i) & 1 for i in range(num_bits -1, -1, -1)]
# Ví dụ: byte=0b10101010, num_bits=8 -> [1,0,1,0,1,0,1,0]

def _from_binary_list(self, bits_list):
    result = 0
    for bit in bits_list:
        result = (result << 1) | bit   # Dịch trái 1 bit, thêm bit mới vào cuối
    return result
# Ví dụ: [1,0,1,0,1,0,1,0] -> 0b10101010
```

### 2.3. Hàm hoán vị
```python
def _permute(self, data, p_table):
    # Lấy từng chỉ số trong p_table (bắt đầu từ 1), lấy bit tương ứng trong data
    return [data[i - 1] for i in p_table]
# Ví dụ: data=[a,b,c,d], p_table=[2,1,4,3] -> [b,a,d,c]
```

### 2.4. Sinh khóa con
```python
def _generate_subkeys(self):
    key_permuted = self._permute(self.key, PC1)   # Hoán vị key theo PC1 (8 bit -> 8 bit)
    C = key_permuted[:4]                         # 4 bit đầu (C)
    D = key_permuted[4:]                         # 4 bit cuối (D)
    subkeys = []
    for shift in SHIFT_BITS:
        C = C[shift:] + C[:shift]                # Dịch vòng trái C (theo số bit shift)
        D = D[shift:] + D[:shift]                # Dịch vòng trái D
        combined = C + D                         # Ghép lại thành 8 bit
        subkey = self._permute(combined, PC2)    # Hoán vị tạo subkey theo PC2
        subkeys.append(subkey)                   # Lưu subkey
    return subkeys
# Kết quả: trả về list 4 subkey, mỗi subkey là list 8 bit
```

### 2.5. Vòng Feistel
```python
def _feistel_round(self, left, right, subkey, s_boxes):
    expanded_right = self._permute(right, E)         # Mở rộng 4 bit right thành 8 bit theo E
    xored_result = [a ^ b for a, b in zip(expanded_right, subkey)]
    # XOR từng bit với subkey (8 bit)
    sbox_result = []
    # S-box 1 xử lý 4 bit đầu
    sbox1_input = xored_result[:4]
    row1 = sbox1_input[0] * 2 + sbox1_input[3]       # Lấy bit 1 và 4 làm row
    col1 = sbox1_input[1] * 2 + sbox1_input[2]       # Lấy bit 2 và 3 làm col
    sbox1_value = s_boxes[0][row1][col1]             # Tra S1, ra số 0-3
    sbox_result.extend(self._to_binary_list(sbox1_value, 2)) # Đổi sang 2 bit
    # S-box 2 xử lý 4 bit sau
    sbox2_input = xored_result[4:]
    row2 = sbox2_input[0] * 2 + sbox2_input[3]
    col2 = sbox2_input[1] * 2 + sbox2_input[2]
    sbox2_value = s_boxes[1][row2][col2]
    sbox_result.extend(self._to_binary_list(sbox2_value, 2))
    # P-box: hoán vị 4 bit đầu ra S-box
    p_box_result = self._permute(sbox_result, P)
    # Tạo cặp mới: left mới là right cũ, right mới là left XOR p_box_result
    new_left = right
    new_right = [a ^ b for a, b in zip(left, p_box_result)]
    return new_left, new_right
# Kết quả: trả về cặp (left, right) mới cho vòng tiếp theo
```

### 2.6. Mã hóa
```python
def encrypt(self, plaintext):
    data = self._to_binary_list(plaintext, 8)         # Chuyển plaintext (số nguyên) thành list 8 bit
    permuted_data = self._permute(data, IP)           # Hoán vị đầu vào theo IP
    left = permuted_data[:4]                          # 4 bit trái
    right = permuted_data[4:]                         # 4 bit phải
    for i in range(4):                                # Lặp 4 vòng Feistel
        left, right = self._feistel_round(left, right, self.subkeys[i], [S1, S2])
        # Sau mỗi vòng: left, right cập nhật mới
    combined = right + left                           # Đảo vị trí: right trước, left sau
    ciphertext_bits = self._permute(combined, FP)     # Hoán vị cuối theo FP
    ciphertext = self._from_binary_list(ciphertext_bits) # Chuyển list bit thành số nguyên
    return ciphertext
# Kết quả: trả về ciphertext (số nguyên 8 bit)
```

### 2.7. Giải mã
```python
def decrypt(self, ciphertext):
    data = self._to_binary_list(ciphertext, 8)        # Chuyển ciphertext thành list 8 bit
    permuted_data = self._permute(data, IP)           # Hoán vị đầu vào theo IP
    left = permuted_data[:4]
    right = permuted_data[4:]
    for i in range(3, -1, -1):                        # Lặp 4 vòng Feistel ngược (subkey đảo ngược)
        left, right = self._feistel_round(left, right, self.subkeys[i], [S1, S2])
    combined = right + left                           # Đảo vị trí
    plaintext_bits = self._permute(combined, FP)      # Hoán vị cuối theo FP
    plaintext = self._from_binary_list(plaintext_bits) # Chuyển list bit thành số nguyên
    return plaintext
# Kết quả: trả về plaintext (số nguyên 8 bit)
```

### 2.8. Ví dụ sử dụng
```python
key = 0b10101010                  # Key 8 bit
plaintext = 0b11001100            # Plaintext 8 bit
des = TinyDes(key)                # Khởi tạo đối tượng TinyDes với key
encrypted_text = des.encrypt(plaintext)   # Mã hóa
decrypted_text = des.decrypt(encrypted_text) # Giải mã
print("Plaintext:", bin(plaintext)[2:].zfill(8))      # In ra dạng nhị phân 8 bit
print("Ciphertext:", bin(encrypted_text)[2:].zfill(8))
print("Decrypted:", bin(decrypted_text)[2:].zfill(8))
print("Match:", decrypted_text == plaintext)          # Kiểm tra giải mã đúng
```
**Kết quả:**
- In ra plaintext, ciphertext, decrypted (dạng nhị phân 8 bit)
- Match: True nếu giải mã đúng


