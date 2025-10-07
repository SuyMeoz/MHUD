# RC4 - Triển khai thuật toán mã hóa Stream Cipher RC4

### 1. Hàm chính: `rc4_encrypt_decrypt`
Hàm này thực hiện cả mã hóa và giải mã (vì RC4 dùng cùng keystream). Nó nhận `key` (bytes) và `data` (bytes), trả về ciphertext/decrypted bytes.

```python
def rc4_encrypt_decrypt(key, data):
    S = list(range(256))
    T = [0] * 256
    key_len = len(key)
```

- `def rc4_encrypt_decrypt(key, data):`: Định nghĩa hàm nhận `key` (chuỗi bytes làm key) và `data` (dữ liệu bytes cần mã hóa/giải mã).
- `S = list(range(256))`: Khởi tạo mảng trạng thái S (State array) là một list từ 0 đến 255 (256 phần tử). S đại diện cho một permutation của các giá trị 0-255, dùng để tạo keystream.
- `T = [0] * 256`: Khởi tạo mảng tạm T (Temporary array) với 256 phần tử bằng 0. T dùng để trộn key vào S trong bước KSA (Key Scheduling Algorithm).
- `key_len = len(key)`: Lưu độ dài của key (số bytes) để dễ sử dụng sau.

```python
    for i in range(256):
        T[i] = key[i % key_len]
```

- `for i in range(256):`: Duyệt qua 256 phần tử của T.
- `T[i] = key[i % key_len]`: Sao chép key vào T, lặp lại key nếu key ngắn hơn 256 bytes (sử dụng modulo `%` để lấy byte từ key theo vòng lặp). Ví dụ: nếu key dài 9 bytes, T[0] = key[0], T[9] = key[0], v.v. Điều này giúp mở rộng key ngắn.

```python
    j = 0 

    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
```

- `j = 0`: Khởi tạo chỉ số j = 0. j là biến tích lũy dùng trong thuật toán hoán đổi.
- `for i in range(256):`: Duyệt qua 256 phần tử để thực hiện KSA (Key Scheduling Algorithm) - bước khởi tạo permutation S dựa trên key.
  - `j = (j + S[i] + T[i]) % 256`: Cập nhật j bằng tổng (j cũ + S[i] + T[i]) modulo 256. Điều này tạo ra sự "ngẫu nhiên" dựa trên key.
  - `S[i], S[j] = S[j], S[i]`: Hoán đổi (swap) giá trị tại vị trí i và j trong mảng S. Đây là bước cốt lõi của RC4 để làm rối S theo key.

Sau bước này, S đã là một permutation "ngẫu nhiên hóa" bởi key, sẵn sàng cho PRGA (Pseudo-Random Generation Algorithm) để tạo keystream.

```python
    i = 0
    j = 0

    result = bytearray()
```

- `i = 0`: Reset i = 0 cho PRGA (bắt đầu tạo keystream).
- `j = 0`: Reset j = 0 cho PRGA.
- `result = bytearray()`: Khởi tạo bytearray rỗng để lưu kết quả (ciphertext hoặc decrypted data). Bytearray cho phép append từng byte.

```python
    for byte_in in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) % 256

        keystream_byte = S[t]

        result_byte = byte_in ^ keystream_byte
        result.append(result_byte)
```

- `for byte_in in data:`: Duyệt qua từng byte trong dữ liệu đầu vào (plaintext cho mã hóa, ciphertext cho giải mã).
  - `i = (i + 1) % 256`: Tăng i lên 1 (modulo 256 để giữ trong phạm vi 0-255).
  - `j = (j + S[i]) % 256`: Cập nhật j bằng (j cũ + S[i]) modulo 256. Đây là bước tích lũy cho hoán đổi tiếp theo.
  - `S[i], S[j] = S[j], S[i]`: Hoán đổi S[i] và S[j] để tiếp tục làm rối trạng thái S (PRGA).
  - `t = (S[i] + S[j]) % 256`: Tính chỉ số t = (S[i] + S[j]) modulo 256. t dùng để lấy byte từ keystream.
  - `keystream_byte = S[t]`: Lấy giá trị S[t] làm byte keystream (giá trị ngẫu nhiên từ 0-255).
  - `result_byte = byte_in ^ keystream_byte`: XOR byte đầu vào với keystream_byte để tạo byte kết quả (mã hóa: plaintext ^ keystream; giải mã: ciphertext ^ keystream = plaintext gốc).
  - `result.append(result_byte)`: Thêm byte kết quả vào mảng result.

```python
    return bytes(result)
```

- `return bytes(result)`: Chuyển bytearray thành bytes và trả về kết quả cuối cùng (ciphertext hoặc decrypted data).

### 2. Phần test code
```python
key = b'SecretKey'

plaintext = b'Hello, World! This is a test message.'

ciphertext = rc4_encrypt_decrypt(key, plaintext)

print(f"ban ro : {plaintext.decode('utf-8')}")
print(f"ban ma hoa (hex): {ciphertext.hex()}")

decrypted_text = rc4_encrypt_decrypt(key, ciphertext)
print(f"ban giai ma : {decrypted_text.decode('utf-8')}")
```

- `key = b'SecretKey'`: Định nghĩa key dưới dạng bytes (chuỗi UTF-8 'SecretKey' chuyển thành bytes). Key có thể là bất kỳ bytes nào, nhưng nên có độ dài hợp lý (thường 5-256 bytes).
- `plaintext = b'Hello, World! This is a test message.'`: Định nghĩa plaintext dưới dạng bytes (chuỗi UTF-8 chuyển thành bytes). Đây là dữ liệu gốc cần mã hóa.
- `ciphertext = rc4_encrypt_decrypt(key, plaintext)`: Gọi hàm để mã hóa plaintext, lưu kết quả vào ciphertext (bytes).
- `print(f"ban ro : {plaintext.decode('utf-8')}")`: In plaintext gốc, decode từ bytes về UTF-8 để hiển thị chuỗi dễ đọc. "ban ro" có lẽ là lỗi đánh máy của "bản rõ" (plaintext).
- `print(f"ban ma hoa (hex): {ciphertext.hex()}")`: In ciphertext dưới dạng hex (chuỗi hex của bytes) để dễ quan sát. "ban ma hoa" là "bản mã hóa".
- `decrypted_text = rc4_encrypt_decrypt(key, ciphertext)`: Gọi hàm lần nữa với ciphertext để giải mã, sử dụng cùng key (vì RC4 symmetric).
- `print(f"ban giai ma : {decrypted_text.decode('utf-8')}")`: In kết quả giải mã, decode về UTF-8. "ban giai ma" là "bản giải mã". Kết quả nên khớp với plaintext gốc.

## Tài liệu tham khảo
- [RC4 Algorithm Explanation](https://en.wikipedia.org/wiki/RC4)
- DES/RC4 so sánh: RC4 là stream cipher (dữ liệu bất kỳ độ dài), khác với block cipher như TinyDes trước đó.

