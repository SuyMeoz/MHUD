# 🔐 Mã hóa dòng A5/1


## 1️⃣ Giới thiệu 

A5/1 là một stream cipher được thiết kế vào cuối thập niên 1980 để bảo mật cho hệ thống GSM (Global System for Mobile Communications).

Thuật toán dựa trên 3 thanh ghi dịch phản hồi tuyến tính (LFSR) có độ dài khác nhau:

- R1: 19 bit

- R2: 22 bit

- R3: 23 bit

Cơ chế đồng bộ: majority clocking – chỉ những LFSR có bit đồng bộ trùng với giá trị majority mới được dịch chuyển.

👉 Ưu điểm: tốc độ cao, dễ triển khai phần cứng. 

👉 Nhược điểm: đã bị phá vỡ (không còn an toàn cho bảo mật hiện đại).

## 2️⃣ Cấu trúc LFSR & taps

Mỗi LFSR có một tập hợp tap positions (các vị trí bit được XOR để sinh bit phản hồi).

- R1 (19 bit): taps tại [13, 16, 17, 18]

- R2 (22 bit): taps tại [20, 21]

- R3 (23 bit): taps tại [7, 20, 21, 22]

Bit đồng bộ (clocking bit):

- R1[8], R2[10], R3[10]

Nguyên tắc dịch chuyển:

- Tính majority của 3 clocking bits.

Chỉ dịch chuyển những LFSR có clocking bit = majority.

### 🔄 Cơ chế dịch trái trong LFSR (Linear Feedback Shift Register)
Mỗi lần dịch trái (shift left) trong LFSR diễn ra như sau:

1. ính toán bit phản hồi (feedback bit):
    - Lấy các bit ở vị trí tap (được định nghĩa trước cho từng LFSR).
    - Thực hiện phép XOR tất cả các bit này để tạo ra feedback bit.

2. Dịch chuyển:
    - Toàn bộ các bit trong thanh ghi dịch sang trái 1 vị trí.
    - Bit ngoài cùng bên trái (MSB) bị loại bỏ.
    - Bit mới (feedback bit) được đưa vào vị trí ngoài cùng bên phải (LSB).

3. Kết quả:
    - Thanh ghi có trạng thái mới, sẵn sàng cho vòng lặp tiếp the

## 3️⃣ Khởi tạo từ khóa bí mật
1. Chuyển key (bytes) → dãy bit.
2. Nếu chưa đủ 64 bit, lặp lại cho đủ.
3. Chia thành 3 phần:
    - R1: 19 bit
    - R2: 22 bit
    - R3: 23 bit
4. Gán giá trị ban đầu cho từng LFSR.

## 4️⃣ Sinh keystream
- Ở mỗi vòng lặp:  
  1. Tính majority từ 3 clocking bits.  
  2. Dịch chuyển các LFSR phù hợp.  
  3. Bit keystream = XOR(R1 cuối, R2 cuối, R3 cuối).  

## 5️⃣ Mã hóa & Giải mã
- **Mã hóa:**  
  - Plaintext ⊕ Keystream → Ciphertext  
- **Giải mã:**  
  - Ciphertext ⊕ Keystream → Plaintext  

👉 Vì là **stream cipher**, quá trình mã hóa và giải mã là **giống nhau**.

## **Quy trình:**
- Khởi tạo 3 LFSR từ khóa bí mật (key).
- Ở mỗi bước, xác định bit majority từ 3 LFSR.
- Chỉ các LFSR có bit đồng bộ trùng với majority mới được dịch chuyển.
- Bit keystream đầu ra là XOR của bit cuối mỗi LFSR.

## 🔑 Cách mã hóa (Encryption)
1. Chuyển plaintext thành dãy bit.
2. Sinh keystream (dòng khóa) từ key với độ dài bằng số bit của plaintext.
3. XOR từng bit của plaintext với keystream để tạo ciphertext.
4. Chuyển dãy bit kết quả thành bytes.

## 🔓 Cách giải mã (Decryption)
1. Chuyển ciphertext thành dãy bit.
2. Sinh lại keystream từ key (giống khi mã hóa).
3. XOR từng bit của ciphertext với keystream để thu lại plaintext.
4. Chuyển dãy bit kết quả thành bytes.

## 🛠️ Các hàm & công dụng

| Hàm | Công dụng |
|-----|-----------|
| `bytes_to_bits(b)` | Chuyển bytes thành danh sách bit |
| `bits_to_bytes(bits)` | Chuyển danh sách bit thành bytes |
| `init_registers_from_key(key_bytes)` | Khởi tạo 3 LFSR từ key |
| `majority(a, b, c)` | Tính bit majority từ 3 bit |
| `clock_reg(reg, taps)` | Dịch chuyển LFSR với các tap cho trước |
| `a5_1_keystream_from_key(key_bytes, n)` | Sinh keystream dài n bit từ key |
| `stream_xor_bytes_with_bitstream(data_bytes, keystream_bits)` | XOR dữ liệu bytes với keystream bit |

## Chi tiết các hàm
### 📑 bytes_to_bits(b)
```python
def bytes_to_bits(b):
    bits = []

    for byte in b:
        for i in range(8):
            bits.append((byte >> (7-i)) & 1)

    return bits
````
`for byte in b` : duyệt qua từng byte trong b

`for i in range(8)` : mỗi byte có 8 bit

`byte >> (7-i)` : dịch phải byte đi (7-i) vị trí. 
Khi `i = 0` → dịch phải 7 → lấy bit cao nhất (MSB).Khi `i = 7` → dịch phải 0 → lấy bit thấp nhất (LSB).

`& 1` : giữ lại bit cuối cùng (0 hoặc 1).

> ví dụ : 'A' trong ASCII có giá trị 65 = 01000001

```python
#--- khi i = 0 ---
(65 >> (7-0)) & 1 = (65 >> 7) & 1
                 = (0b01000001 >> 7) & 1
                 = 0b00000000 & 1
                 = 0
```

```python
#--- khi i = 1 ---
(65 >> (7-1)) & 1 = (65 >> 6) & 1
                 = (0b01000001 >> 6) & 1
                 = 0b00000001 & 1
                 = 1
```

```
ket qua : [0, 1, 0, 0, 0, 0, 0, 1]
```

### 📑 bits_to_bytes(bits)
```python
def bits_to_bytes(bits):
    out = []

    for i in range(0, len(bits), 8):
        byte = 0

        for j in range(8):
            byte = (byte << 1) | bits[i +j]

        out.append(byte)
    
    return bytes(out)
```
`for i in range(0, len(bits), 8)` : duyệt qua danh sách bits theo từng nhóm 8 bit

`for j in range(8)` : duyệt qua từng bit trong nhóm 8 bit

`byte << 1` : dịch trái byte 1 bit

`| bits[i +j]` : thêm bit mới nhất vào vị trí thấp nhất

### 📑 init_registers_from_key(key_bytes)
```python
def init_registers_from_key(key_bytes):
    key_bits = bytes_to_bits(key_bytes)

    while len(key_bits) < (19+22+23):
        key_bits += key_bits

    R1 = key_bits[0:19]
    R2 = key_bits[19:19+22]
    R3 = key_bits[19+22:19+22+23]

    return R1[:], R2[:], R3[:]
```
`while len(key_bits) < (19+22+23)` : Đảm bảo rằng số lượng bit đủ để khởi tạo ba thanh ghi

`R1 = key_bits[0:19]` : Lấy 19 bit đầu tiên để khởi tạo thanh ghi R1

`R2 = key_bits[19:19+22]` : Lấy 22 bit tiếp theo để khởi tạo thanh ghi R2

`R3 = key_bits[19+22:19+22+23]` : Lấy 23 bit tiếp theo để khởi tạo thanh ghi R3

### 📑 majority(a, b, c)
```python
def majority(a, b, c):
    return 1 if (a+b+c) >= 2 else 0
```
tính major dựa trên xác định giá trị chiếm đa số

### 📑 clock_reg(reg, taps)
```python
def clock_reg(reg, taps):
    feedback = 0

    for t in taps:
        feedback ^= reg[t]

    out = reg.pop()
    reg.insert(0, feedback)

    return out
```
`for t in taps` : duyệt qua từng vị trí t trong taps

`reg[t]` : lấy giá trị bit tại vị trí t

`feedback ^= reg[t]` : thực hiện phép XOR giữa feedback và bit đó

`out = reg.pop()` : Lấy và loại bỏ bit cuối cùng trong thanh ghi (bit bên phải)

`reg.insert(0, feedback)` : Chèn feedback vào đầu thanh ghi (bên trái)

### 📑 a5_1_keystream_from_key(key_bytes, n)
```python
def a5_1_keystream_from_key(key_bytes, n):
    R1, R2, R3 = init_registers_from_key(key_bytes)

    ks = []

    for _ in range(n):
        m = majority(R1[8], R2[10], R3[10])

        if R1[8] == m:
            clock_reg(R1, [13,16,17,18])

        if R2[10] == m:
            clock_reg(R2, [20,21])

        if R3[10] == m:
            clock_reg(R3, [7,20,21,22])
        
        ks_bit = R1[-1] ^ R2[-1] ^ R3[-1]
        ks.append(ks_bit)
    
    return ks
```
`R1, R2, R3 = init_registers_from_key(key_bytes)` : khởi tạo 3 thanh ghi từ khóa đầu vào

`for _ in range(n)` : Lặp n lần để sinh ra n bit trong chuỗi keystream

`m = majority(R1[8], R2[10], R3[10])` : gán giá trị của major cho m

`clock_reg(R1, [13,16,17,18])` : dịch thanh ghi phản nếu bằng major

`ks_bit = R1[-1] ^ R2[-1] ^ R3[-1]` : Tính bit keystream bằng XOR của bit cuối cùng (bit bên phải nhất) của mỗi thanh ghi
 
### 📑 stream_xor_bytes_with_bitstream(data_bytes, keystream_bits)
```python
def stream_xor_bytes_with_bitstream(data_bytes, keystream_bits):
    data_bits = bytes_to_bits(data_bytes)
    out_bits = [d ^ k for d, k in zip(data_bits, keystream_bits)]

    return bits_to_bytes(out_bits)
```
`data_bits = bytes_to_bits(data_bytes)` : chuyển dữ liệu từ dạng byte sang bit

`out_bits = [d ^ k for d, k in zip(data_bits, keystream_bits)]` : Thực hiện phép XOR từng cặp bit giữa data_bits và keystream_bits

> ví dụ
```python
data_bytes = b'\xAA'  # 10101010
keystream_bits = [1,0,1,0,1,0,1,0]  # 10101010

10101010 XOR 10101010 = 00000000 → b'\x00'
```

## 📄 Ví dụ sử dụng
```python
key = b"examplekey"
plaintext = b"Hello, A5/1"

# ... Mã hóa ...
ks = a5_1_keystream_from_key(key, len(bytes_to_bits(plaintext)))
ciphertext = stream_xor_bytes_with_bitstream(plaintext, ks)

# ... Giải mã ...
ks2 = a5_1_keystream_from_key(key, len(bytes_to_bits(ciphertext)))
decrypted = stream_xor_bytes_with_bitstream(ciphertext, ks2)
```

