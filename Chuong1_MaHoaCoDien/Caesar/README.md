# Mã hóa Caesar

## 1. Mã hóa Caesar là gì?

Mã hóa Caesar (Caesar cipher) là một phương pháp mã hóa thay thế đơn giản, trong đó mỗi ký tự trong bản rõ được thay thế bằng một ký tự khác cách nó một số vị trí nhất định trong bảng chữ cái. Số vị trí này gọi là "shift" (độ dịch chuyển). Ví dụ, với shift = 3, 'A' sẽ thành 'D', 'B' thành 'E', ...

## 2. Cách mã hóa

Để mã hóa một ký tự:
- Nếu là chữ cái, dịch chuyển nó theo số lượng shift trong bảng chữ cái (vòng quanh nếu vượt quá 'Z' hoặc 'z').
- Nếu không phải chữ cái, giữ nguyên.

Giải mã thực hiện ngược lại: dịch chuyển lùi lại số lượng shift.

## 3. Các hàm và module Python chuẩn được sử dụng

| Hàm/Module | Công dụng |
|------------|-----------|
| ord()      | Chuyển ký tự thành mã số nguyên Unicode |
| chr()      | Chuyển mã số nguyên thành ký tự |
| enumerate()| Lặp qua đối tượng, lấy cả chỉ số và giá trị |
| random     | Sinh số ngẫu nhiên (dùng cho shift ngẫu nhiên) |
| collections.Counter | Đếm tần suất xuất hiện ký tự |
| re         | Xử lý chuỗi bằng regex |

Ví dụ:
```python
print(ord('A'))   # 65
print(chr(65))    # 'A'
for i, ch in enumerate('ABC'):
    print(i, ch)
```

## 4. Các hàm tự viết trong các file .py

### caesar_encrypt.py
- `caesar_encrypt_char(ch, shift)`: Mã hóa một ký tự với shift cho trước (giữ nguyên nếu không phải chữ cái).
- `caesar_encrypt(plaintext, shift)`: Mã hóa toàn bộ chuỗi, in ra quá trình mã hóa từng ký tự và ánh xạ bảng chữ cái.

### caesar_decrypt.py
- `caesar_decrypt_char(ch, shift)`: Giải mã một ký tự (gọi lại hàm mã hóa với shift âm).
- `caesar_decrypt(ciphertext, shift)`: Giải mã toàn bộ chuỗi, in ra quá trình giải mã từng ký tự.

### caesar_preserve.py
- `caesar_encrypt_preserve(text, shift)`: Mã hóa/giải mã, giữ nguyên ký tự không phải chữ cái, in chi tiết từng bước.

### caesar_simple.py
- `caesar_encrypt_simple(text, shift)`: Mã hóa toàn bộ chuỗi, chỉ dùng hàm mã hóa ký tự, không in chi tiết.

### brute_force.py
- `caesar_shift_text(text, shift)`: Mã hóa/giải mã toàn bộ chuỗi với shift cho trước.
- Script thử tất cả các shift, dùng heuristic dựa trên từ phổ biến tiếng Anh để đoán shift đúng.

## 5. Mô tả các file

- `caesar_encrypt.py`: Hàm mã hóa ký tự và chuỗi, có in chi tiết.
- `caesar_decrypt.py`: Hàm giải mã ký tự và chuỗi, có in chi tiết.
- `caesar_preserve.py`: Mã hóa/giải mã, giữ nguyên ký tự đặc biệt, in chi tiết.
- `caesar_simple.py`: Mã hóa nhanh, dùng cho ví dụ tần suất và brute force.
- `brute_force.py`: Thử tất cả shift, đoán shift dựa trên từ phổ biến.

---
Tài liệu này giúp bạn hiểu rõ về mã hóa Caesar, cách cài đặt và các hàm đã được xây dựng trong các file Python kèm theo.