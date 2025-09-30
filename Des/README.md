## 1. Các bảng hoán vị và S-Box
```python 
IP = [...]
FP = [...]
E = [...]
S_BOXES = [...]
P = [...]
PC1 = [...]
PC2 = [...]
SHIFT_BITS = [...]
```

**IP (Initial Permutation)**: Bảng hoán vị ban đầu, sắp xếp lại 64 bit của bản rõ trước khi vào vòng lặp Feistel.

**FP (Final Permutation)**: Bảng hoán vị cuối, đảo ngược IP để tạo ra bản mã.

**E (Expansion Table)**: Mở rộng 32 bit thành 48 bit để XOR với subkey.

**S_BOXES**: 8 bảng S-Box, mỗi bảng biến 6 bit thành 4 bit (giảm kích thước và tạo tính phi tuyến).

**P (Permutation)**: Hoán vị P-box, trộn các bit sau khi qua S-Box.

**PC1 (Permuted Choice 1)**: Chọn 56 bit từ khóa 64 bit ban đầu.

**PC2 (Permuted Choice 2)**: Chọn 48 bit từ 56 bit để tạo subkey.

**SHIFT_BITS**: Số bit dịch vòng cho mỗi vòng sinh subkey.

## 2. Lớp DES
```python
class DES:
    def __init__(self, key):
        self.key = self._to_binary_list(key)
        self.subkeys = self._generate_subkeys()
```
`__init__`: Nhận khóa 64 bit (8 byte).
- Chuyển khóa thành danh sách bit (_to_binary_list).
- Sinh ra 16 subkey cho 16 vòng (_generate_subkeys).

## 3. Chuyển đổi dữ liệu
```python
def _to_binary_list(self, byte_data):
    bit_list = []
    for byte in byte_data:
        for i in range(7, -1, -1):
            bit_list.append((byte >> i) & 1)
    return bit_list
```
Chuyển mỗi byte thành 8 bit.

> Ví dụ: 0x41 (A) → [0,1,0,0,0,0,0,1].

```python
def _from_binary_list(self, bit_list):
    byte_data = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bit_list[i + j]
        byte_data.append(byte)
    return bytes(byte_data)
```
Chuyển danh sách bit ngược lại thành bytes.

## 4. Hoán vị
```python
def _permute(self, data, p_table):
    return [data[bit - 1] for bit in p_table]
```
Lấy dữ liệu `data` và sắp xếp lại theo bảng `p_table`.

Ví dụ: nếu `p_table = [3,1,2]` và `data = [a,b,c]` → `[c,a,b]`.

## 5. Hàm Feistel
```python
def _feistel_function(self, right, subkey):
    expanded_right = self._permute(right, E)  # mở rộng 32 → 48
    xor_result = [a ^ b for a, b in zip(expanded_right, subkey)]  # XOR với subkey

    sbox_result = []
    for i in range(8):
        sbox_input = xor_result[i * 6 : (i + 1) * 6]
        row = sbox_input[0] << 1 | sbox_input[5]
        col = sbox_input[1] << 3 | sbox_input[2] << 2 | sbox_input[3] << 1 | sbox_input[4]
        val = S_BOXES[i][row][col]  # tra S-Box
        # chuyển giá trị 4 bit thành danh sách bit
        sbox_result.extend([(val >> 3) & 1, (val >> 2) & 1, (val >> 1) & 1, val & 1])

    return self._permute(sbox_result, P)  # hoán vị P-box
```
Mở rộng 32 bit → 48 bit.

XOR với subkey.

S-Box: chia thành 8 nhóm 6 bit, mỗi nhóm → 4 bit.

P-box: trộn bit để tăng tính khuếch tán.

## 6. Sinh subkey
```python
def _generate_subkeys(self):
    key_permuted = self._permute(self.key, PC1)  # chọn 56 bit
    C = key_permuted[:28]
    D = key_permuted[28:]
    subkeys = []
    for i in range(16):
        shift = SHIFT_BITS[i]
        C = C[shift:] + C[:shift]  # dịch vòng
        D = D[shift:] + D[:shift]
        combined = C + D
        subkey = self._permute(combined, PC2)  # chọn 48 bit
        subkeys.append(subkey)
    return subkeys
```
Tạo 16 subkey (mỗi cái 48 bit) cho 16 vòng.

## 7. Mã hóa
```python
def encrypt_block(self, plaintext_block):
    data = self._to_binary_list(plaintext_block)
    permuted_data = self._permute(data, IP)  # hoán vị ban đầu
    left = permuted_data[:32]
    right = permuted_data[32:]

    for i in range(16):
        temp_left = left
        left = right
        f_result = self._feistel_function(right, self.subkeys[i])
        right = [a ^ b for a, b in zip(temp_left, f_result)]

    combined = right + left  # đổi chỗ L và R
    ciphertext = self._permute(combined, FP)  # hoán vị cuối
    return self._from_binary_list(ciphertext)
```
16 vòng Feistel:
- `L_i = R_{i-1}`

- `R_i = L_{i-1} XOR f(R_{i-1}, K_i)`

Sau 16 vòng: ghép `R16 + L16`.

Áp dụng FP để ra bản mã.

## 8. Giải mã
```python
def decrypt_block(self, ciphertext_block):
    data = self._to_binary_list(ciphertext_block)
    permuted_data = self._permute(data, IP)
    left = permuted_data[:32]
    right = permuted_data[32:]

    for i in range(15, -1, -1):  # dùng subkey ngược
        temp_left = left
        left = right
        f_result = self._feistel_function(right, self.subkeys[i])
        right = [a ^ b for a, b in zip(temp_left, f_result)]

    combined = right + left
    plaintext = self._permute(combined, FP)
    return self._from_binary_list(plaintext)
```
Giống mã hóa nhưng dùng subkey theo thứ tự ngược lại.

Kết quả cuối cùng là bản rõ ban đầu.

## 9. Ví dụ chạy
```python
key = b'12345678'
plaintext = b'12345678'
des_cipher = DES(key)

encrypted_block = des_cipher.encrypt_block(plaintext)
print(f"Bản rõ: {plaintext.hex()}")
print(f"Bản mã: {encrypted_block.hex()}")

decrypted_block = des_cipher.decrypt_block(encrypted_block)
print(f"Bản giải mã: {decrypted_block.hex()}")
print(f"Bản giải mã khớp với bản rõ: {decrypted_block == plaintext}")
```
Bản rõ: dữ liệu gốc.

Bản mã: dữ liệu đã mã hóa.

Giải mã: khôi phục lại bản rõ.

Kiểm tra: `True` nếu khớp.