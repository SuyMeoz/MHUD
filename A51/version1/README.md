## 1. Chuyển đổi dữ liệu
```python
def bytes_to_bits(b):
    bits = []
    for byte in b:
        for i in range(8):
            bits.append((byte >> (7-i)) & 1)
    return bits
```
Hàm này chuyển mỗi byte thành 8 bit.

`(byte >> (7-i)) & 1` dịch bit và lấy giá trị tại vị trí tương ứng.

Kết quả: danh sách các bit (0/1).

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
> ket qua : [0, 1, 0, 0, 0, 0, 0, 1]

---

```python
def bits_to_bytes(bits):
    out = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        out.append(byte)
    return bytes(out)
```
Hàm này làm ngược lại: từ danh sách bit → bytes.

Gom 8 bit thành 1 byte bằng cách dịch trái và OR.

Trả về kiểu `bytes`.

## 2. Khởi tạo 3 thanh ghi LFSR từ khóa
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
Chuyển khóa từ bytes sang bit.

Đảm bảo đủ số bit để khởi tạo 3 thanh ghi:

- R1: 19 bit

- R2: 22 bit

- R3: 23 bit

Nếu khóa ngắn, lặp lại cho đủ.

Trả về 3 thanh ghi.

## 3. Hàm majority (đa số)
```python
def majority(a, b, c):
    return 1 if (a+b+c) >= 2 else 0
```
Trả về giá trị đa số trong 3 bit (ít nhất 2 giống nhau).

Đây là cơ chế đồng bộ trong A5/1.

## 4. Clocking (dịch thanh ghi)
```python
def clock_reg(reg, taps):
    feedback = 0
    for t in taps:
        feedback ^= reg[t]
    out = reg.pop()
    reg.insert(0, feedback)
    return out
```
`taps`: các vị trí bit dùng để tính feedback.

`feedback` = XOR của các bit tại vị trí taps.

Dịch thanh ghi sang phải, chèn feedback vào đầu.

Trả về bit bị đẩy ra.

> ví dụ 
```python
reg = [1, 0, 1, 1, 0]
taps = [0, 2, 4]

out = clock_reg(reg, taps)
print("Output bit:", out) # 0
print("Updated register:", reg) # [0,1,0,1,1]
```

## 5. Sinh keystream A5/1
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
Mỗi vòng lặp:

- Tính bit majority từ 3 thanh ghi.

- Chỉ dịch những thanh ghi có bit đồng bộ bằng majority.

- Bit keystream = XOR của bit cuối mỗi thanh ghi.

Lặp n lần để tạo ra n bit keystream.

## 6. XOR dữ liệu với keystream
```python
def stream_xor_bytes_with_bitstream(data_bytes, keystream_bits):
    data_bits = bytes_to_bits(data_bytes)
    out_bits = [d ^ k for d, k in zip(data_bits, keystream_bits)]
    return bits_to_bytes(out_bits)
```
Chuyển dữ liệu sang bit.

XOR từng bit với keystream.

Chuyển kết quả về bytes.

Dùng cho cả mã hóa và giải mã (vì XOR 2 lần sẽ ra dữ liệu gốc).

> ví dụ
```python
data_bytes = b'\xAA'  # 10101010
keystream_bits = [1,0,1,0,1,0,1,0]  # 10101010

10101010 XOR 10101010 = 00000000 → b'\x00'
```

## 7. Chạy thử chương trình
```python
key = b"examplekey"
plaintext = b"Hello, A5/1"

ks = a5_1_keystream_from_key(key, len(bytes_to_bits(plaintext)))
ciphertext = stream_xor_bytes_with_bitstream(plaintext, ks)

ks2 = a5_1_keystream_from_key(key, len(bytes_to_bits(ciphertext)))
decrypted = stream_xor_bytes_with_bitstream(ciphertext, ks2)

print("Plaintext : ", plaintext)
print("Ciphertext(hex) : ", ciphertext)
print("Decrypted : ", decrypted)
```
Khởi tạo khóa `"examplekey"`.

Sinh keystream có độ dài bằng số bit của plaintext.

Mã hóa: `plaintext XOR keystream → ciphertext`.

Giải mã: `ciphertext XOR keystream → plaintext`.

In kết quả.