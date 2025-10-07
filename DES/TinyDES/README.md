# TinyDes - Triển khai đơn giản của thuật toán DES

## Giải thích code chi tiết
Dưới đây là phân tích toàn bộ code. Tôi sẽ trích dẫn từng phần code gốc (hoặc nhóm dòng liên quan) và giải thích công dụng từng dòng một cách chi tiết. Code được chia thành các phần logic để dễ theo dõi.

### 1. Định nghĩa các bảng permutation và S-boxes
Các bảng này là các hằng số cố định trong DES, dùng để hoán vị bit và thay thế dữ liệu. Chúng được rút gọn cho phiên bản 8-bit.

```python
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
```

- `IP = [5, 2, 7, 4, 1, 8, 3, 6]`: Bảng **Initial Permutation (IP)**. Dùng để hoán vị ban đầu dữ liệu đầu vào (plaintext hoặc ciphertext). Mỗi số chỉ vị trí bit mới (1-based index), ví dụ bit đầu tiên sau IP lấy từ vị trí 5 của dữ liệu gốc.
- `FP = [5, 2, 7, 4, 1, 8, 3, 6]`: Bảng **Final Permutation (FP)**. Tương tự IP nhưng dùng ở cuối quá trình mã hóa/giải mã để hoán vị ngược lại. Ở đây giống IP để đơn giản hóa.
- `E = [4, 1, 2, 3, 2, 3, 4, 1]`: Bảng **Expansion (E)**. Mở rộng nửa phải (right, 4 bit) thành 8 bit để XOR với subkey. Nó lặp lại một số bit (ví dụ bit 2 và 3 lặp).
- `S1` và `S2`: Hai **S-boxes** (Substitution boxes). Mỗi là ma trận 4x4, dùng để thay thế 4 bit đầu vào thành 2 bit đầu ra dựa trên row và column. Row = bit1 + bit4 (nhị phân), Column = bit2 + bit3.
- `P = [2, 4, 3, 1]`: Bảng **Permutation (P)** sau S-box. Hoán vị 4 bit kết quả từ S-boxes.
- `PC1 = [3, 5, 2, 7, 4, 1, 8, 6]`: Bảng **Permuted Choice 1 (PC1)**. Hoán vị key 8-bit thành 8-bit để chia thành C (4 bit đầu) và D (4 bit sau) cho việc tạo subkeys.
- `PC2 = [6, 3, 7, 4, 8, 5, 1, 2]`: Bảng **Permuted Choice 2 (PC2)**. Hoán vị kết hợp C+D sau dịch chuyển để tạo subkey 8-bit cho mỗi round.
- `SHIFT_BITS = [1, 1, 2, 2]`: Danh sách số bit dịch chuyển trái cho C và D ở mỗi round (4 round). Round 1 và 2 dịch 1 bit, round 3 và 4 dịch 2 bit.

### 2. Class TinyDes
Class chính triển khai thuật toán. Nó nhận key 8-bit và tạo subkeys.

```python
class TinyDes:
    def __init__(self, key):
        self.key = self._to_binary_list(key, 8)
        self.subkeys = self._generate_subkeys()
```

- `class TinyDes:`: Định nghĩa class TinyDes để đóng gói logic mã hóa/giải mã.
- `def __init__(self, key):`: Constructor. Nhận key (số nguyên 8-bit).
  - `self.key = self._to_binary_list(key, 8)`: Chuyển key thành list 8 bit nhị phân (MSB first, từ bit cao đến thấp).
  - `self.subkeys = self._generate_subkeys()`: Tạo danh sách 4 subkeys cho 4 round.

```python
    def _to_binary_list(self, byte, num_bits):
        return [(byte >> i) & 1 for i in range(num_bits -1, -1, -1)]
```

- `def _to_binary_list(self, byte, num_bits):`: Phương thức private chuyển số nguyên `byte` thành list `num_bits` bit nhị phân.
  - `return [(byte >> i) & 1 for i in range(num_bits -1, -1, -1)]`: List comprehension: Dịch phải `byte` từng bit từ cao (i = num_bits-1) đến thấp (i=0), lấy bit cuối cùng bằng `& 1`. Kết quả là list bit từ MSB đến LSB.

```python
    def _from_binary_list(self, bits_list):
        result = 0
        for bit in bits_list:
            result = (result << 1) | bit
        return result
```

- `def _from_binary_list(self, bits_list):`: Phương thức private chuyển list bit về số nguyên.
  - `result = 0`: Khởi tạo kết quả = 0.
  - `for bit in bits_list:`: Duyệt từng bit trong list (từ MSB đến LSB).
  - `result = (result << 1) | bit`: Dịch trái result 1 bit và OR với bit hiện tại để xây dựng số.

```python
    def _permute(self, data, p_table):
        return [data[i - 1] for i in p_table]
```

- `def _permute(self, data, p_table):`: Phương thức private thực hiện hoán vị dữ liệu theo bảng `p_table`.
  - `return [data[i - 1] for i in p_table]`: List comprehension: Lấy bit tại vị trí `i-1` (vì p_table dùng index 1-based) từ `data` (list bit), sắp xếp theo thứ tự trong p_table.

```python
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
```

- `def _generate_subkeys(self):`: Phương thức private tạo 4 subkeys từ key.
  - `key_permuted = self._permute(self.key, PC1)`: Hoán vị key theo PC1 để chia thành C và D.
  - `C = key_permuted[:4]`: Lấy 4 bit đầu làm nửa trái (C).
  - `D = key_permuted[4:]`: Lấy 4 bit sau làm nửa phải (D).
  - `subkeys = []`: Khởi tạo list rỗng để lưu subkeys.
  - `for shift in SHIFT_BITS:`: Duyệt qua 4 giá trị shift (1,1,2,2) cho 4 round.
    - `C = C[shift:] + C[:shift]`: Dịch trái C `shift` bit (cắt đuôi + đầu).
    - `D = D[shift:] + D[:shift]`: Tương tự cho D.
    - `combined = C + D`: Ghép C và D thành 8 bit.
    - `subkey = self._permute(combined, PC2)`: Hoán vị combined theo PC2 để tạo subkey.
    - `subkeys.append(subkey)`: Thêm subkey vào list.
  - `return subkeys`: Trả về list 4 subkeys.

```python
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
```

- `def _feistel_round(self, left, right, subkey, s_boxes):`: Phương thức private thực hiện một round Feistel (hàm f).
  - `expanded_right = self._permute(right, E)`: Mở rộng right (4 bit) thành 8 bit theo bảng E.
  - `xored_result = [a ^ b for a, b in zip(expanded_right, subkey)]`: XOR từng bit của expanded_right với subkey (8 bit).
  - `sbox_result = []`: Khởi tạo list cho kết quả S-box.
  - `sbox1_input = xored_result[:4]`: Lấy 4 bit đầu cho S1.
  - `sbox2_input = xored_result[4:]`: Lấy 4 bit sau cho S2.
  - `row1 = sbox1_input[0] * 2 + sbox1_input[3]`: Tính row cho S1 (bit 0 và 3 làm số nhị phân 2 bit).
  - `col1 = sbox1_input[1] * 2 + sbox1_input[2]`: Tính column cho S1.
  - `sbox1_value = s_boxes[0][row1][col1]`: Tra cứu giá trị từ S1 (2 bit).
  - `sbox_result.extend(self._to_binary_list(sbox1_value, 2))`: Chuyển 2 bit của S1 vào list.
  - Tương tự cho S2: `row2`, `col2`, `sbox2_value`, và extend vào `sbox_result` (tổng 4 bit).
  - `p_box_result = self._permute(sbox_result, P)`: Hoán vị 4 bit theo P.
  - `new_left = right`: Nửa trái mới = right cũ (theo Feistel).
  - `new_right = [a ^ b for a, b in zip(left, p_box_result)]`: Nửa phải mới = left cũ XOR f(right).
  - `return new_left, new_right`: Trả về left và right mới.

```python
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
```

- `def encrypt(self, plaintext):`: Phương thức mã hóa plaintext (8-bit) thành ciphertext.
  - `data = self._to_binary_list(plaintext, 8)`: Chuyển plaintext thành 8 bit.
  - `permuted_data = self._permute(data, IP)`: Hoán vị ban đầu theo IP.
  - `left = permuted_data[:4]`: Chia thành left (4 bit đầu).
  - `right = permuted_data[4:]`: Right (4 bit sau).
  - `for i in range(4):`: Thực hiện 4 round Feistel.
    - `left, right = self._feistel_round(left, right, self.subkeys[i], [S1, S2])`: Gọi round với subkey thứ i, truyền S1 và S2.
  - `combined = right + left`: Sau 4 round, ghép right + left (ngược lại left + right ban đầu).
  - `ciphertext_bits = self._permute(combined, FP)`: Hoán vị cuối theo FP.
  - `ciphertext = self._from_binary_list(ciphertext_bits)`: Chuyển bit về số nguyên.
  - `return ciphertext`: Trả về ciphertext.

```python
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
```

- `def decrypt(self, ciphertext):`: Phương thức giải mã, tương tự encrypt nhưng đảo ngược subkeys.
  - Các bước đầu giống encrypt: Chuyển bit, IP, chia left/right.
  - `for i in range(3, -1, -1):`: Duyệt subkeys ngược (từ subkey 3 về 0) để giải mã.
    - `left, right = self._feistel_round(left, right, self.subkeys[i], [S1, S2])`: Gọi round với subkey đảo.
  - Các bước cuối giống: Ghép right + left, FP, chuyển về số.
  - `return plaintext`: Trả về plaintext.

### 3. Phần test code
```python
key = 0b10101010
plaintext = 0b11001100
des = TinyDes(key)
encrypted_text = des.encrypt(plaintext)
decrypted_text = des.decrypt(encrypted_text)
print("Plaintext:", bin(plaintext)[2:].zfill(8))
print("Ciphertext:", bin(encrypted_text)[2:].zfill(8))
print("Decrypted:", bin(decrypted_text)[2:].zfill(8))
print("Match:", decrypted_text == plaintext)
```

- `key = 0b10101010`: Định nghĩa key 8-bit (binary: 10101010).
- `plaintext = 0b11001100`: Định nghĩa plaintext 8-bit (binary: 11001100).
- `des = TinyDes(key)`: Tạo instance của TinyDes với key.
