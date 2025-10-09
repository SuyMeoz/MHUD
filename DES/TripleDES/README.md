# TripleDES

## Bảng cấu hình DES

```python
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]
```
- **Bảng IP:** Hoán vị ban đầu 64 bit dữ liệu vào. Mỗi số là vị trí 1-based của bit nguồn cần đặt ở vị trí hiện tại.
- **Công dụng từng phần tử:** Ví dụ phần tử đầu 58 nghĩa là bit thứ 58 của đầu vào sẽ trở thành bit đầu của dữ liệu sau IP.

```python
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]
```
- **Bảng FP:** Hoán vị cuối 64 bit sau 16 vòng Feistel.
- **Công dụng:** Đưa dữ liệu R16||L16 về thứ tự chuẩn để xuất ra bản mã/bản rõ.

```python
E = [32, 1, 2, 3, 4, 5, 4, 5,
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1]
```
- **Bảng E (Expansion):** Ánh xạ 32 bit nửa phải thành 48 bit bằng cách lặp các bit rìa.
- **Công dụng từng phần:** Ví dụ 32 ở đầu nghĩa là bit 32 lặp lên vị trí mở rộng đầu tiên; 1,2,3,4,5 tiếp theo lấy bit liên tiếp; các cặp lặp như 4,5 xuất hiện để tạo 48 bit.

```python
S_BOXES = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        ...
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        ...
    ],
    ...
]
```
- **8 S-Box:** Mỗi S-Box là ma trận 4×16 (4 hàng, 16 cột), giá trị 0–15 (4 bit).
- **Công dụng:** Mỗi nhóm 6 bit vào S-Box: 2 bit biên chọn hàng, 4 bit giữa chọn cột; trả về 4 bit đầu ra phi tuyến.

```python
P = [16,7,20,21,29,12,28,17,
     1,15,23,26,5,18,31,10,
     2,8,24,14,32,27,3,9,
     19,13,30,6,22,11,4,25]
```
- **Bảng P:** Hoán vị 32 bit sau S-Box để khuếch tán ảnh hưởng bit trên toàn khối.
- **Công dụng:** Ví dụ vị trí đầu (16) nghĩa là bit 16 của đầu vào P trở thành bit đầu ra.

```python
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]
```
- **PC1:** Hoán vị/loại parity của khóa 64 bit để lấy 56 bit hiệu dụng.
- **Công dụng:** Chỉ số 1-based từ 1..64 trỏ vào bit khóa gốc; 8 bit parity bị loại bỏ.

```python
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]
```
- **PC2:** Chọn 48 bit từ (C+D) 56 bit để tạo subkey mỗi vòng.
- **Công dụng:** Tập hợp chỉ số 1-based trên chuỗi C||D sau dịch vòng.

```python
SHIFT_BITS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
```
- **Lịch dịch trái:** Cho 16 vòng. Số bit dịch vòng trái cho C và D tương ứng từng vòng.

---

## Lớp DES: khởi tạo và tiện ích

```python
class DES:
    def __init__(self, key):
        self.key = self._to_binary_list(key)
        self.subkeys = self._generate_subkeys() 
```
- **Định nghĩa lớp DES:** Bọc logic DES cho một khối 64 bit.
- **Gán khóa dạng bit:** `self.key` là list 64 bit từ `key` bytes.
- **Sinh subkeys:** `self.subkeys` chứa 16 subkey 48 bit; tính một lần dùng nhiều lần.

```python
def _to_binary_list(self, byte_data):
    bit_list = []
```
- **Khởi tạo danh sách bit:** Nơi chứa bit của dữ liệu đầu vào.

```python
for byte in byte_data:
```
- **Duyệt từng byte:** Mỗi giá trị 0–255 trong `bytes`.

```python
    for i in range(7, -1, -1):
        bit_list.append((byte >> i) & 1)
```
- **Duyệt bit từ MSB đến LSB:** i = 7..0.
- **Dịch phải:** `(byte >> i)` đưa bit thứ i về vị trí LSB.
- **Lọc LSB:** `& 1` lấy giá trị 0/1 của bit.
- **Append:** Thêm bit vào danh sách theo thứ tự big-endian trong byte.

```python
return bit_list
```
- **Trả danh sách bit:** Độ dài = số byte × 8.

```python
def _from_binary_list(self, bit_list):
    byte_data = bytearray()
```
- **Chuẩn bị xây bytes:** `bytearray` thuận tiện để append.

```python
for i in range(0, len(bit_list), 8):
    byte = 0
```
- **Duyệt nhóm 8 bit:** i tăng theo bước 8; `byte` sẽ ghép các bit thành một byte.

```python
    for j in range(8):
        byte = (byte << 1) | bit_list[i + j]
```
- **Dịch trái:** Mở chỗ cho bit mới; giữ thứ tự bit đúng (MSB→LSB).
- **OR bit:** Chèn bit hiện tại vào LSB của `byte`.

```python
    byte_data.append(byte)
```
- **Thêm vào mảng byte:** Lưu byte vừa ghép.

```python
return bytes(byte_data)
```
- **Trả `bytes`:** Dữ liệu bất biến, dùng để xuất/in.

```python
def _permute(self, data, p_table):
    return [data[bit -1 ] for bit in p_table]
```
- **Hoán vị tổng quát:** Dùng mọi bảng DES (1-based).
- **Chỉ số 1-based → 0-based:** `bit - 1` để truy cập đúng phần tử trong `data`.
- **Trả list mới:** Kích thước bằng độ dài `p_table`.

---

## Hàm Feistel (F-function)

```python
def _feistel(self, right, subkey):
    expanded_right = self._permute(right, E)
```
- **Đầu vào:** `right` là list 32 bit (nửa phải), `subkey` là list 48 bit.
- **Mở rộng:** Dùng `E` để từ 32 → 48 bit; tạo biên lặp cho S-Box.

```python
    xored_result = [a ^ b for a,b in zip(expanded_right, subkey)]
```
- **XOR với subkey:** Kết hợp khóa vòng với dữ liệu; `zip` ghép từng cặp bit; `^` là XOR.

```python
    sbox_result = []
```
- **Kết quả S-Box:** Nơi chứa 32 bit đầu ra sau 8 S-Box.

```python
    for i in range(8):
        sbox_input = xored_result[i*6:(i+1)*6]
```
- **Cắt nhóm 6 bit:** 48 bit thành 8 nhóm (0..7), mỗi nhóm cho một S-Box.

```python
        row = (sbox_input[0] << 1) + sbox_input[5]
```
- **Chọn hàng:** 2 bit biên: bit đầu làm MSB, bit cuối làm LSB → giá trị 0..3.

```python
        col = (sbox_input[1] << 3) + (sbox_input[2] << 2) + (sbox_input[3] << 1) + sbox_input[4]
```
- **Chọn cột:** 4 bit giữa tạo giá trị 0..15 theo trọng số 8,4,2,1.

```python
        val = S_BOXES[i][row][col]
```
- **Tra S-Box:** Lấy giá trị 4 bit (0..15) tại S-Box i, hàng `row`, cột `col`.

```python
        sbox_result.extend([(val >> 3) & 1,
                            (val >> 2) & 1,
                            (val >> 1) & 1,
                            val & 1])
```
- **Tách 4 bit:** Dịch phải 3,2,1,0 để lấy từng bit của `val`.
- **Append:** Thêm vào `sbox_result` theo thứ tự từ bit cao đến bit thấp (MSB→LSB).

```python
    return self._permute(sbox_result, P)
```
- **P-box:** Hoán vị 32 bit để khuếch tán; trả về 32 bit kết quả F-function.

---

## Sinh subkeys

```python
def _generate_subkeys(self):
    key_permuted = self._permute(self.key, PC1)
```
- **PC1:** Lọc và hoán vị khóa 64 → 56 bit (loại parity); tạo `key_permuted`.

```python
    C = key_permuted[:28]
    D = key_permuted[28:]
```
- **Chia đôi:** Tạo 2 nửa 28 bit: C (trái), D (phải) để dịch vòng.

```python
    subkeys = []
```
- **Danh sách subkey:** Nơi chứa 16 subkey 48 bit theo thứ tự vòng.

```python
    for shift in SHIFT_BITS:
```
- **Vòng 16 lần:** Mỗi lần tương ứng một vòng DES.

```python
        C = C[shift:] + C[:shift]
        D = D[shift:] + D[:shift]
```
- **Dịch vòng trái:** Dịch `shift` bit; phần dịch ra quay lại cuối danh sách.

```python
        combined = C + D
```
- **Ghép C||D:** Tạo chuỗi 56 bit sau dịch vòng.

```python
        subkey = self._permute(combined, PC2)
```
- **PC2:** Chọn 48 bit theo PC2; tạo subkey cho vòng hiện tại.

```python
        subkeys.append(subkey)
```
- **Lưu subkey:** Thêm vào danh sách `subkeys`.

```python
    return subkeys
```
- **Trả 16 subkey:** Dùng cho mã hóa theo thứ tự 0..15; giải mã sẽ dùng ngược lại.

---

## Mã hóa một khối

```python
def encrypt_block(self, plaintext_block):
    data = self._to_binary_list(plaintext_block)
```
- **Chuyển bytes → bit:** Tạo list 64 bit `data` từ `plaintext_block` 8 byte.

```python
    permuted_data = self._permute(data, IP)
```
- **IP:** Hoán vị ban đầu 64 bit; chuẩn hóa vị trí bit cho vòng Feistel.

```python
    left, right = permuted_data[:32], permuted_data[32:]
```
- **Tách L0/R0:** 32 bit đầu là L0, 32 bit sau là R0.

```python
    for i in range(16):
        temp_left = left
```
- **Bắt đầu vòng:** Lưu L(i-1) vào `temp_left`.

```python
        left = right
```
- **Hoán nửa:** L(i) = R(i-1) (định nghĩa mạng Feistel).

```python
        f_result = self._feistel(right, self.subkeys[i])
```
- **F(R, K):** Tính F-function với R(i-1) và subkey vòng i.

```python
        right = [a ^ b for a, b in zip(temp_left, f_result)]
```
- **Cập nhật R:** R(i) = L(i-1) XOR F(R(i-1), K(i)). `zip` ghép từng bit, `^` XOR.

```python
    combined = right + left
```
- **Ghép R16||L16:** Đảo vị trí nửa theo chuẩn DES trước FP.

```python
    ciphertext = self._permute(combined, FP)
```
- **FP:** Hoán vị cuối 64 bit; tạo dữ liệu bản mã.

```python
    return self._from_binary_list(ciphertext)
```
- **Bit → bytes:** Trả về 8 byte bản mã.

---

## Giải mã một khối

```python
def decrypt_block(self, ciphertext_block):
    data = self._to_binary_list(ciphertext_block)
```
- **Chuyển bytes → bit:** Tạo list 64 bit từ bản mã 8 byte.

```python
    permuted_data = self._permute(data, IP)
```
- **IP:** Áp dụng giống mã hóa (chuẩn DES yêu cầu).

```python
    left, right = permuted_data[:32], permuted_data[32:]
```
- **Tách L0/R0:** Như mã hóa.

```python
    for i in range(15, -1, -1):
        temp_left = left
```
- **Vòng ngược:** Duyệt i từ 15 đến 0; lưu L(i-1).

```python
        left = right
```
- **Hoán nửa:** L(i) = R(i-1).

```python
        f_result = self._feistel(right, self.subkeys[i])
```
- **F(R, K[i]):** Dùng subkey theo thứ tự ngược (nhờ cấu trúc Feistel).

```python
        right = [a ^ b for a, b in zip(temp_left, f_result)]
```
- **Cập nhật R:** R(i) = L(i-1) XOR F(...), hoàn tác đúng quy trình mã hóa.

```python
    combined = right + left
```
- **Ghép R16||L16:** Chuẩn bị cho FP.

```python
    decrypt_data = self._permute(combined, FP)
```
- **FP:** Hoán vị cuối; đưa dữ liệu về bản rõ.

```python
    return self._from_binary_list(decrypt_data)
```
- **Bit → bytes:** Trả về 8 byte bản rõ.

---

## Lớp TripleDES (EDE)

```python
class TripleDES:
    def __init__(self, key1, key2, key3):
        self.des1 = DES(key1)
        self.des2 = DES(key2)
        self.des3 = DES(key3)
```
- **Định nghĩa lớp:** Kết hợp 3 DES độc lập.
- **Khởi tạo 3 DES:** Mỗi DES sinh subkeys từ khóa riêng; tối ưu tính toán (sinh một lần).

```python
def encrypt(self, plaintext):
    sep1 = self.des1.encrypt_block(plaintext)
```
- **E bước 1:** Mã hóa khối với `key1` → `sep1`.

```python
    sep2 = self.des2.decrypt_block(sep1)
```
- **D bước 2:** Giải mã `sep1` với `key2` → `sep2`. Sử dụng giải mã để giữ tương thích DES khi khóa trùng.

```python
    ciphertext = self.des3.encrypt_block(sep2)
    return ciphertext
```
- **E bước 3:** Mã hóa `sep2` với `key3` → `ciphertext`. Trả về bản mã 8 byte.

```python
def decrypt(self, ciphertext):
    sep1 = self.des3.decrypt_block(ciphertext)
```
- **D bước 1:** Giải mã bản mã với `key3` → `sep1`.

```python
    sep2 = self.des2.encrypt_block(sep1)
```
- **E bước 2:** Mã hóa trung gian với `key2` → `sep2`.

```python
    plaintext = self.des1.decrypt_block(sep2)
    return plaintext
```
- **D bước 3:** Giải mã `sep2` với `key1` → bản rõ.

---

## Đoạn chạy thử

```python
key1 = b'12345678'
key2 = b'abcdefgh'
key3 = b'IJKLMNOP'
```
- **Ba khóa 8 byte:** Mỗi khóa 64 bit; DES dùng 56 bit hiệu dụng (8 bit parity bị loại bởi PC1).

```python
plaintext = b'12345678'
```
- **Bản rõ:** Một khối đúng 8 byte. Không có padding trong mã này.

```python
triple_des_cipher = TripleDES(key1, key2, key3)
```
- **Khởi tạo TripleDES:** Tạo ba đối tượng DES; subkeys được sinh ra.

```python
ciphertext = triple_des_cipher.encrypt(plaintext)
```
- **Mã hóa:** Thực hiện EDE trên `plaintext` → `ciphertext`.

```python
print(f"Bản rõ: {plaintext.hex()}")
```
- **In hex bản rõ:** Dễ quan sát giá trị theo hệ 16.

```python
print(f"Bản mã: {ciphertext.hex()}")
```
- **In hex bản mã:** Kiểm tra kết quả mã hóa.

```python
decrypted_text = triple_des_cipher.decrypt(ciphertext)
```
- **Giải mã:** Thực hiện EDE ngược trên `ciphertext` → `decrypted_text`.

```python
print(f"Giải mã: {decrypted_text.hex()}")
```
- **In hex giải mã:** Hiển thị giá trị sau giải mã.

```python
print(f"Khớp bản rõ: {decrypted_text == plaintext}")
```
- **Kiểm tra:** So sánh bytes trực tiếp; True nếu đúng.

---
