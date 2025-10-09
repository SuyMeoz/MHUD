# TripleDES

### Các bảng DES: vai trò và cách sử dụng

```python
IP = [58, 50, 42, 34, 26, 18, 10, 2, ...]
```
- **Danh sách chỉ số 1-based:** Mỗi số biểu diễn vị trí bit (1 đến 64) trong khối 64 bit đầu vào.
- **Ý nghĩa:** Bảng hoán vị ban đầu. Sau khi đưa dữ liệu vào, DES đổi thứ tự các bit theo IP để chuẩn hóa trước vòng Feistel.
- **Tác động:** Tạo ra phân bố bit thuận lợi cho khuếch tán trong 16 vòng tiếp theo.

```python
FP = [40, 8, 48, 16, 56, 24, 64, 32, ...]
```
- **Danh sách chỉ số 1-based:** Hoán vị 64 bit sau 16 vòng.
- **Ý nghĩa:** Bảng hoán vị cuối. Đưa dữ liệu sau khi hoàn tất vòng về thứ tự chuẩn để xuất ra bản mã hoặc bản rõ.

```python
E = [32, 1, 2, 3, 4, 5, 4, 5, ...]
```
- **Danh sách 48 phần tử:** Mỗi phần tử là vị trí bit (1–32) từ nửa phải.
- **Ý nghĩa:** Mở rộng 32 → 48 bit bằng cách lặp lại một số bit rìa (vì 48 = 8×6 để vào 8 S-Box).
- **Tác động:** Cho phép XOR với subkey 48 bit.

```python
S_BOXES = [ ... 8 bảng ... ]
```
- **Cấu trúc:** 8 hộp; mỗi hộp là ma trận 4 hàng × 16 cột; tổng 64 giá trị (0–15).
- **Ý nghĩa:** Ánh xạ 6 bit → 4 bit (phi tuyến). Hàng chọn bởi 2 bit biên, cột chọn bởi 4 bit giữa.
- **Tác động:** Giảm 48 bit sau XOR về 32 bit, thêm phi tuyến để chống tấn công tuyến tính/vi sai.

```python
P = [16,7,20,21,29,12,28,17, ...]
```
- **Danh sách 32 chỉ số:** Hoán vị 32 bit sau S-Box.
- **Ý nghĩa:** Khuếch tán: lan tỏa ảnh hưởng của mỗi bit vào nhiều vị trí.

```python
PC1 = [57, 49, 41, 33, 25, 17, 9, ...]
```
- **Danh sách 56 chỉ số:** Chọn 56 bit từ 64 bit khóa (loại parity).
- **Ý nghĩa:** Chuẩn bị khóa cho dịch vòng và PC2.

```python
PC2 = [14, 17, 11, 24, 1, 5, ..., 32]
```
- **Danh sách 48 chỉ số:** Chọn 48 bit từ (C+D) để tạo subkey.
- **Ý nghĩa:** Tạo subkey dùng trong mỗi vòng Feistel.

```python
SHIFT_BITS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
```
- **Lịch dịch:** Số bit dịch trái cho C và D ở mỗi vòng (dịch vòng – circular).

---

### Lớp DES: khởi tạo và chuyển đổi bit/byte

```python
class DES:
    def __init__(self, key):
        self.key = self._to_binary_list(key)
        self.subkeys = self._generate_subkeys() 
```
- **Định nghĩa lớp:** Khai báo lớp DES.
- **Nhận khóa:** `key` là bytes 8 byte (64 bit).
- **Chuyển khóa sang bit:** `self._to_binary_list(key)` tạo list 64 phần tử (0/1), thuận tiện cho hoán vị.
- **Sinh subkey:** `self._generate_subkeys()` tạo và lưu 16 subkeys 48 bit vào `self.subkeys` để dùng lại (tránh tính lại).

```python
def _to_binary_list(self, byte_data):
    bit_list = []
```
- **Khởi tạo danh sách bit:** `bit_list` rỗng, sẽ chứa toàn bộ bit của `byte_data`.

```python
for byte in byte_data:
```
- **Duyệt từng byte:** Lấy giá trị 0–255 ứng với mỗi ký tự trong `bytes`.

```python
    for i in range(7, -1, -1):
        bit_list.append((byte >> i) & 1)
```
- **Duyệt bit trong byte:** Từ bit 7 (MSB) đến bit 0 (LSB), theo thứ tự big-endian.
- **Dịch phải:** `(byte >> i)` đưa bit thứ i về LSB.
- **Lấy bit:** `& 1` giữ lại LSB (0 hoặc 1).
- **Thêm vào danh sách:** Append bit vào `bit_list`.

```python
return bit_list
```
- **Kết quả:** Trả list bit, độ dài = số byte × 8.

```python
def _from_binary_list(self, bit_list):
    byte_data = bytearray()
```
- **Chuẩn bị ghép lại bytes:** `bytearray` cho phép append từng byte.

```python
for i in range(0, len(bit_list), 8):
    byte = 0
```
- **Duyệt khối 8 bit:** Mỗi vòng tạo ra một byte từ 8 bit liên tiếp.
- **Khởi tạo byte:** Bắt đầu từ 0.

```python
    for j in range(8):
        byte = (byte << 1) | bit_list[i + j]
```
- **Dịch trái:** Nhân đôi byte hiện tại để mở chỗ cho bit mới (dịch 1 vị trí).
- **OR bit:** Thêm bit kế tiếp vào LSB. Kết quả là ghép bit theo thứ tự từ MSB đến LSB.

```python
    byte_data.append(byte)
```
- **Lưu byte:** Thêm vào `bytearray`.

```python
return bytes(byte_data)
```
- **Chuyển kiểu:** Trả về `bytes` bất biến để sử dụng/bản in.

```python
def _permute(self, data, p_table):
    return [data[bit -1 ] for bit in p_table]
```
- **Hoán vị chung:** Áp dụng mọi bảng hoán vị DES.
- **Chỉ số 1-based → 0-based:** `bit - 1` chuyển sang chỉ số Python.
- **Kết quả:** Tạo list bit mới theo thứ tự yêu cầu của bảng (không thay đổi độ dài).

---

### Hàm Feistel (F-function) của DES

```python
def _feistel(self, right, subkey):
    expanded_right = self._permute(right, E)
```
- **Đầu vào:** `right` là list 32 bit; `subkey` là list 48 bit cho vòng hiện tại.
- **Mở rộng:** Hoán vị `right` bằng bảng E để tạo `expanded_right` 48 bit.

```python
    xored_result = [a ^ b for a,b in zip(expanded_right, subkey)]
```
- **XOR subkey:** Kết hợp `expanded_right` và `subkey` bit–bit.
- **`zip`:** Ghép từng cặp bit tương ứng; XOR tạo 48 bit đầu vào cho S-Box.

```python
    sbox_result = []
```
- **Chuẩn bị kết quả S-Box:** Danh sách rỗng sẽ chứa 32 bit sau S-Box.

```python
    for i in range(8):
        sbox_input = xored_result[i*6:(i+1)*6]
```
- **Chia nhóm:** Mỗi vòng lấy 6 bit liên tiếp (tổng 8 nhóm: i = 0..7).
- **Phân nhóm:** `i*6` đến `(i+1)*6` cắt lát 6 bit phù hợp với S-Box i.

```python
        row = (sbox_input[0] << 1) + sbox_input[5]
```
- **Tính hàng:** Lấy bit đầu và bit cuối (biên) của 6 bit. Kết hợp thành số 2 bit: `row ∈ {0..3}`.
- **Dịch trái:** `(bit0 << 1)` để bit đầu trở thành MSB của row.

```python
        col = (sbox_input[1] << 3) + (sbox_input[2] << 2) + (sbox_input[3] << 1) + sbox_input[4]
```
- **Tính cột:** Lấy 4 bit giữa, đặt vị trí theo trọng số 8–4–2–1. `col ∈ {0..15}`.

```python
        val = S_BOXES[i][row][col]
```
- **Tra S-Box:** Lấy giá trị 4 bit (0–15) từ bảng S-Box thứ i với chỉ số hàng/cột.

```python
        sbox_result.extend([(val >> 3) & 1,
                            (val >> 2) & 1,
                            (val >> 1) & 1,
                            val & 1])
```
- **Tách thành 4 bit:** Dịch phải 3, 2, 1, 0 để lấy từng bit của `val` từ MSB đến LSB.
- **Append:** Nối 4 bit vào `sbox_result`. Sau 8 nhóm, tổng cộng 32 bit.

```python
    return self._permute(sbox_result, P)
```
- **P-Box:** Hoán vị 32 bit đầu ra S-Box theo bảng P để khuếch tán.
- **Kết quả F-function:** Trả list 32 bit.

---

### Sinh subkeys: PC1, dịch vòng, PC2

```python
def _generate_subkeys(self):
    key_permuted = self._permute(self.key, PC1)
```
- **PC1:** Hoán vị khóa 64 bit (list 64 bit) thành 56 bit (loại parity), đúng chuẩn DES.

```python
    C = key_permuted[:28]
    D = key_permuted[28:]
```
- **Chia đôi:** Tạo hai nửa 28 bit: C (trái) và D (phải) để tiến hành dịch vòng.

```python
    subkeys = []
```
- **Danh sách subkey:** Sẽ chứa 16 subkey 48 bit.

```python
    for shift in SHIFT_BITS:
```
- **Duyệt 16 vòng:** Mỗi vòng có số dịch trái tương ứng.

```python
        C = C[shift:] + C[:shift]
        D = D[shift:] + D[:shift]
```
- **Dịch vòng trái:** C và D đều dịch trái `shift` bit. Phần bị đẩy ra đầu quay về cuối (circular).

```python
        combined = C + D
```
- **Ghép lại:** Tạo khóa tạm 56 bit từ C và D sau khi dịch vòng.

```python
        subkey = self._permute(combined, PC2)
```
- **PC2:** Chọn 48 bit từ `combined` để tạo `subkey` cho vòng hiện tại.

```python
        subkeys.append(subkey)
```
- **Lưu subkey:** Thêm subkey vào danh sách.

```python
    return subkeys
```
- **Trả về:** 16 subkey 48 bit, thứ tự đúng cho mã hóa (0..15).

---

### Mã hóa một khối 64 bit

```python
def encrypt_block(self, plaintext_block):
    data = self._to_binary_list(plaintext_block)
```
- **Đổi bytes → bit:** `plaintext_block` (8 byte) chuyển thành list 64 bit.

```python
    permuted_data = self._permute(data, IP)
```
- **IP:** Hoán vị ban đầu 64 bit để chuẩn hóa vị trí bit.

```python
    left, right = permuted_data[:32], permuted_data[32:]
```
- **Chia nửa:** L0 = 32 bit đầu; R0 = 32 bit sau.

```python
    for i in range(16):
        temp_left = left
```
- **Bắt đầu vòng:** Lưu L(i-1) trong `temp_left`.

```python
        left = right
```
- **Hoán vị nửa:** L(i) = R(i-1) (quy tắc Feistel).

```python
        f_result = self._feistel(right, self.subkeys[i])
```
- **F-function:** Tính F(R(i-1), K(i)) bằng `_feistel`.

```python
        right = [a ^ b for a, b in zip(temp_left, f_result)]
```
- **XOR cập nhật:** R(i) = L(i-1) XOR F(R(i-1), K(i)).
- **`zip`:** Ghép từng cặp bit tương ứng; XOR tạo list 32 bit mới.

```python
    combined = right + left
```
- **Ghép cuối:** Tạo chuỗi R16 || L16 (đảo nửa cuối theo chuẩn DES).

```python
    ciphertext = self._permute(combined, FP)
```
- **FP:** Hoán vị cuối 64 bit để ra bản mã.

```python
    return self._from_binary_list(ciphertext)
```
- **Đổi bit → bytes:** Trả về 8 byte bản mã.

---

### Giải mã một khối 64 bit

```python
def decrypt_block(self, ciphertext_block):
    data = self._to_binary_list(ciphertext_block)
```
- **Đổi bytes → bit:** `ciphertext_block` (8 byte) thành list 64 bit.

```python
    permuted_data = self._permute(data, IP)
```
- **IP:** Hoán vị ban đầu (giải mã cũng áp dụng IP theo chuẩn DES).

```python
    left, right = permuted_data[:32], permuted_data[32:]
```
- **Chia nửa:** L0, R0 giống mã hóa.

```python
    for i in range(15, -1, -1):
        temp_left = left
```
- **Vòng ngược:** Duyệt subkeys theo thứ tự đảo (15 xuống 0); lưu L(i-1).

```python
        left = right
```
- **Hoán vị nửa:** L(i) = R(i-1), giống mã hóa.

```python
        f_result = self._feistel(right, self.subkeys[i])
```
- **F-function:** Dùng subkey ngược cho cùng phép F.

```python
        right = [a ^ b for a, b in zip(temp_left, f_result)]
```
- **XOR cập nhật:** R(i) = L(i-1) XOR F(R(i-1), K(i)), cấu trúc Feistel đảm bảo hoàn tác.

```python
    combined = right + left
```
- **Ghép cuối:** R16 || L16.

```python
    decrypt_data = self._permute(combined, FP)
```
- **FP:** Hoán vị cuối, đưa dữ liệu về bản rõ đúng thứ tự.

```python
    return self._from_binary_list(decrypt_data)
```
- **Đổi bit → bytes:** Trả về 8 byte bản rõ.

---

### TripleDES (EDE): kết hợp ba DES

```python
class TripleDES:
    def __init__(self, key1, key2, key3):
        self.des1 = DES(key1)
        self.des2 = DES(key2)
        self.des3 = DES(key3)
```
- **Định nghĩa lớp:** Bọc ba instance DES riêng.
- **Khởi tạo DES:** Mỗi DES sinh subkeys từ khóa riêng (tối ưu: subkeys chỉ sinh một lần).

```python
def encrypt(self, plaintext):
    sep1 = self.des1.encrypt_block(plaintext)
```
- **Bước 1 (E):** Mã hóa khối bằng `key1` (DES#1) → `sep1` trung gian.

```python
    sep2 = self.des2.decrypt_block(sep1)
```
- **Bước 2 (D):** Giải mã `sep1` bằng `key2` (DES#2) → `sep2`.
- **Ý nghĩa:** EDE giữ tương thích khi `key1 == key2 == key3` (hành vi như DES), nhưng tăng bảo mật khi khác nhau.

```python
    ciphertext = self.des3.encrypt_block(sep2)
    return ciphertext
```
- **Bước 3 (E):** Mã hóa `sep2` bằng `key3` (DES#3) → `ciphertext`.
- **Trả về:** Bản mã 8 byte của TripleDES.

```python
def decrypt(self, ciphertext):
    sep1 = self.des3.decrypt_block(ciphertext)
```
- **Bước 1 (D):** Giải mã bằng `key3` (DES#3) → `sep1`.

```python
    sep2 = self.des2.encrypt_block(sep1)
```
- **Bước 2 (E):** Mã hóa bằng `key2` (DES#2) → `sep2`.

```python
    plaintext = self.des1.decrypt_block(sep2)
    return plaintext
```
- **Bước 3 (D):** Giải mã bằng `key1` (DES#1) → bản rõ cuối cùng.

---

```python
key1 = b'12345678'
key2 = b'abcdefgh'
key3 = b'IJKLMNOP'
```
- **Tạo ba khóa:** Mỗi khóa là 8 byte. DES sẽ dùng 56 bit hiệu dụng (8 bit parity bị PC1 loại).

```python
plaintext = b'12345678'
```
- **Bản rõ:** Một khối đúng 8 byte. Mã này không xử lý padding; chỉ dành cho dữ liệu tròn khối 8 byte.

```python
triple_des_cipher = TripleDES(key1, key2, key3)
```
- **Khởi tạo 3DES:** Tạo ba DES bên trong với khóa tương ứng, sinh subkeys.

```python
ciphertext = triple_des_cipher.encrypt(plaintext)
```
- **Mã hóa:** Thực hiện EDE (DES1 encrypt → DES2 decrypt → DES3 encrypt) trên `plaintext`. Trả 8 byte bản mã.

```python
print(f"Bản rõ: {plaintext.hex()}")
```
- **In hex bản rõ:** Chuyển `plaintext` sang chuỗi hex để quan sát dễ hơn.

```python
print(f"Bản mã: {ciphertext.hex()}")
```
- **In hex bản mã:** Hiển thị kết quả mã hóa dạng hex.

```python
decrypted_text = triple_des_cipher.decrypt(ciphertext)
```
- **Giải mã:** Thực hiện EDE ngược (DES3 decrypt → DES2 encrypt → DES1 decrypt) trên `ciphertext`. Trả 8 byte bản rõ.

```python
print(f"Giải mã: {decrypted_text.hex()}")
```
- **In hex giải mã:** Cho thấy dữ liệu sau giải mã.

```python
print(f"Khớp bản rõ: {decrypted_text == plaintext}")
```
- **Kiểm tra tính đúng:** So sánh bytes trực tiếp, in True nếu giải mã khớp bản rõ ban đầu.
