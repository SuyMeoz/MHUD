## 1. Khởi tạo S và T
```python
S = list(range(256))
T = [0] * 256
key_len = len(key)

for i in range(256):
    T[i] = key[i % key_len]
```
`S`: mảng hoán vị ban đầu từ 0 → 255.

`T`: mảng lặp lại khóa để có độ dài 256.

## 2. Key Scheduling Algorithm (KSA)
```python
j = 0 
for i in range(256):
    j = (j + S[i] + T[i]) % 256
    S[i], S[j] = S[j], S[i]
```
Trộn mảng `S` dựa trên khóa.

Đây là bước KSA trong RC4.

## 3. Pseudo-Random Generation Algorithm (PRGA)
```python
i = 0
j = 0
result = bytearray()

for byte_in in data:
    i = (i + 1) % 256
    j = (j + S[i]) % 256

    S[i], S[j] = S[j], S[i]

    t = (S[i] + S[j]) % 256
    keystream_byte = S[t]

    result_byte = byte_in ^ keystream_byte
    result.append(result_byte)
```
Sinh từng byte keystream.

XOR với dữ liệu để mã hóa/giải mã.

Vì XOR đối xứng → cùng hàm dùng cho cả mã hóa và giải mã.

## 4. Chạy thử
```python
key = b'SecretKey'
plaintext = b'Hello, World! This is a test message.'

ciphertext = rc4_encrypt_decrypt(key, plaintext)

print(f"ban ro : {plaintext.decode('utf-8')}")
print(f"ban ma hoa (hex): {ciphertext.hex()}")

decrypted_text = rc4_encrypt_decrypt(key, ciphertext)
print(f"ban giai ma : {decrypted_text.decode('utf-8')}")
```