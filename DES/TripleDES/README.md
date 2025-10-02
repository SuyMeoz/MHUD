
# Giải thích chi tiết cho `tripledes.py`

## 1) Bảng và hằng số DES

- `IP` — Initial Permutation (64 số, 1-based): hoán vị đầu vào 64-bit.
- `FP` — Final Permutation (64 số): hoán vị cuối cùng (nghịch đảo của IP).
- `E` — Expansion (48 chỉ số): mở rộng 32-bit -> 48-bit (dùng trước khi XOR với subkey).
- `S_BOXES` — 8 S-box, mỗi S-box là ma trận 4 x 16: ánh xạ 6-bit -> 4-bit.
- `P` — P-box (32 chỉ số): hoán vị cho kết quả S-box.
- `PC1` — Permuted Choice 1 (56 chỉ số): hoán vị khóa 64-bit -> 56-bit (bỏ parity bits).
- `PC2` — Permuted Choice 2 (48 chỉ số): hoán vị 56-bit (C||D) -> 48-bit subkey.
- `SHIFT_BITS` — danh sách 16 số (1 hoặc 2): số bit shift cho mỗi vòng key schedule.

> Ghi chú: các bảng trên là danh sách Python (list of ints). Khi áp dụng hoán vị, vì bảng dùng chỉ số 1-based nên code lấy `data[index - 1]`.

## 2) Lớp `DES`

Lớp `DES` cài đặt toàn bộ chức năng DES cơ bản. Các phương thức chính:

```python
class DES:
    def __init__(self, key):
        self.key = self._to_binary_list(key)
        self.subkeys = self._generate_subkeys() 
```

`key` là `bytes` (8 byte = 64 bit). Trong constructor, `key` được chuyển thành danh sách bit và `subkeys` (16 subkeys) được sinh bằng `_generate_subkeys()`.

```python
def _to_binary_list(self, byte_data):
    bit_list = []

    for byte in byte_data:
        for i in range(7, -1, -1):
            bit_list.append((byte >> i) & 1)

    return bit_list
```
Chuyển `bytes` hoặc `bytearray` thành `list` các bit (0/1), duyệt từng byte từ bit 7 xuống 0 (big-endian). Kết quả là một danh sách có độ dài `8 * len(byte_data)`.

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
Chuyển danh sách bit về `bytes`. Gom từng 8 bit thành 1 byte bằng dịch trái và OR.

```python
def _permute(self, data, p_table):
    return [data[bit -1 ] for bit in p_table]
```
Áp một bảng hoán vị `p_table` lên danh sách `data`. Triển khai bằng list comprehension: `[data[bit - 1] for bit in p_table]`.

```python
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
```
Hàm F của Feistel: mở rộng `right` (32->48) bằng `E`, XOR với `subkey`, chia thành 8 nhóm 6-bit, chạy qua 8 S-box để được 8 nhóm 4-bit (tổng 32 bit), sau đó áp P-box. Trả về danh sách 32 bit.

```python
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
```
 Sinh 16 subkeys: áp PC-1 để có 56 bit, chia thành C/D (28 bit), dịch vòng trái theo `SHIFT_BITS`, sau đó áp PC-2 để lấy subkey 48-bit cho mỗi vòng.

```python
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
```
Mã hoá một block 8 byte:
1. Chuyển block thành danh sách 64 bit, áp IP.
2. Chia thành `left`/`right` 32-bit.
3. Lặp 16 vòng: new_left = old_right; new_right = old_left XOR F(old_right, subkey_i).
4. Sau vòng, nối `right + left` (chú ý hoán đổi cuối), áp FP, chuyển về `bytes`.

```python
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
```
Quy trình giống `encrypt_block` nhưng dùng subkeys theo thứ tự ngược (vòng 15 -> 0), do đó giải mã được bản rõ.

### Ghi chú về cú pháp/ý nghĩa Python

- `for i in range(7, -1, -1):` — lặp đếm giảm (7..0) để lấy bit từ MSB.
- `zip(expanded_right, subkey)` kết hợp hai danh sách để XOR từng cặp bit.
- `list_a[shift:] + list_a[:shift]` là cách thực hiện rotate trái đơn giản cho danh sách.

## 3) Lớp `TripleDES`

Lớp `TripleDES` đơn giản dùng ba instance của `DES`:

```python
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
```

`__init__(self, key1, key2, key3)` — khởi tạo `DES(key1)`, `DES(key2)`, `DES(key3)`.

`encrypt(self, plaintext)` — thực hiện EDE: `C = E_K3(D_K2(E_K1(P)))` bằng cách gọi lần lượt `encrypt_block` / `decrypt_block` của các đối tượng DES.

`decrypt(self, ciphertext)` — thực hiện nghịch lại: `P = D_K1(E_K2(D_K3(C)))`.

## 4) Phần demo trong file
```
Bản rõ: 3132333435363738
Bản mã: 36bae9990a54169e
Giải mã: 3132333435363738
Khớp bản rõ: True
```

