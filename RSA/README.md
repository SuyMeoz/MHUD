# RSA

### 1. Hàm chuyển byte => int
```python
def bytes_to_int(b):
    val = 0
    for byte in b:
        val = (val << 8) | byte
    return val
```
> ví dụ
```python
b = [0x12, 0x34, 0x56]
val = 0
for byte in b:
    val = (val << 8) | byte
print(hex(val))  # Output: 0x123456
```
### 2. Hàm chuyển int => byte
```python
def int_to_bytes(x):
    if x == 0:
        return b'\x00'
    out = []
    while x > 0:
        out.append(x & 0xFF)
        x >>= 8
    out.reverse()
    return bytes(out)
```
- `if x == 0` nếu số truyền vào bằng 0 trả về byte `b'\x00' = 0`
- `while x > 0` nếu số truyền vào lớn hơn 0 thì `x & 0xFF` lấy 8 bit thấp nhất của x bỏ vào mảng `out`
> ví dụ
```python
x = 0x1234  # = 0001001000110100
x & 0xFF    # = 0000000000110100 = 0x34
```
- sau đấy `x >>= 8` dịch phải x 8 bit nhằm loại bỏ 8 bit vừa lấy được
### 3. Hàm tính ước chung lớn nhất
```python
def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else: 
        g, y, x = gcd(b % a, a)
        return (g, x - (b//a) * y, y)
```
- nếu `a == 0` thì trả về `b,0,1` tức 0 * 𝑥 + 𝑏 * 1 = 𝑏
- ngược lại `g`,`y`,`x` sẽ bằng ước chung lớn nhất giữa b chia lấy dư a và a
- và trả về 𝑎 * 𝑥 + 𝑏 * 𝑦 = gcd(𝑎,𝑏)
> ví dụ
```python
g, x, y = gcd(30, 20)
print(f"GCD: {g}, x: {x}, y: {y}")
# ket qua : GCD: 10, x: 1, y: -1
```
- `g` ước số chung lớn nhất của 30 và 20
- `x` và `y` là nghiệm phương trình `30𝑥 + 20𝑦 = 10`
### 4. Hàm tính nghịch đảo modular
```python
def modinv(a, m):
    g, x, _ = gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
```
- nếu `g` ước chung lớn giữa `a` và `m` nhất khác 1 thì báo lỗi nghịch đảo modular không tồn tại.
- ngược lại trả về kết quả của phép chia lấy dư giữa `x` và `m`
### 5. Hàm lũy thừa theo modulo
```python
def pow_mod(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result
```
- khởi tạo `result` = 1
- `base` = kết quả chia lấy dư giữa `base` và `mod`
- trong khi `exp > 0`
    - nếu `exp & 1` bit cuối của exp là 1
    - thì `result` =  `(result * base) % mod`
- `exp >>= 1` dịch phải exp 1 bit
- `base` = `(base * base) % mod`
- trả về `result`
### 6. Hàm kiểm tra số nguyên tố xác suất
```python
def is_probable_prime(n, k=10):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    d = n - 1
    s = 0
    while d % 2 == 0:
        d//=2
        s += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True
```
>Viết lại n - 1 dưới dạng $2^s \cdot d$
- khi `d` chia lấy dư `2` bằng `0`
    - `d` chia lấy nguyên `2`
    - `s` tăng 1
- mục đích : Tìm số `s` và `d` sao cho n -1 = $2^s \cdot d$ vói `d` là số lẻ 

> Thực hiện k lần kiểm tra Miller–Rabin
- Chọn ngẫu nhiên `a` trong khoảng `[2, n-1]`
- Tính `𝑥` = `𝑎^(𝑑) mod 𝑛`
> Kiểm tra điều kiện nguyên tố
- `if x == 1 or x == n - 1` Nếu `x` là `1` hoặc `n - 1`, thì a không chứng minh được n là hợp số → tiếp tục vòng lặp.
>Lặp kiểm tra bình phương
- lặp tới `s-1` lần 
    - `x` = $x^2$ mod n
    - nếu `x` bằng `n-1` thì `n` có thể là nguyên tố → không kết luận được. 
> Nếu không thỏa điều kiện nào → hợp số
- `if composite` Nếu không có lần nào `x` == `n - 1`, thì `n` chắc chắn là hợp số.
### 7. Hàm tạo ra một số nguyên lẻ ngẫu nhiên có độ dài bits xác định
```python
def generate_prime_candidate(bits):
    candidate = random.getrandbits(bits)
    candidate |= (1 << (bits - 1))
    candidate |= 1
    return candidate
```
- `candidate = random.getrandbits(bits)` tạo ngẫy nhiên candidate với độ dài `bits`
- `candidate |= (1 << (bits - 1))` OR `candidate` với `1` dịch trái `bits - 1` lần
- `candidate |= 1` OR `candidate` với `1`
### 8. Hàm sinh số nguyên tố ngẫu nhiên có độ dài bits
```python
def generate_prime(bits):
    while True:
        cand = generate_prime_candidate(bits)
        if is_probable_prime(cand, k=10):
            return cand
```
- `cand = generate_prime_candidate(bits)` gán `cand` = một số nguyên lẻ ngẫu nhiên có độ dài bits xác định
- nếu `cand` có xác suất cao là số nguyên tố
    - thì trả về cand
### 9. Hàm cặp khóa RSA
```python
def generate_rsa_keypair(bits=512):
    half = bits // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while p == q:
        q = generate_prime(half)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    d = modinv(e, phi)
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modinv(q, p)

    public_key = (e, n)
    private_key = (d, n)
    crt_params = (p, q, dp, dq, qinv)
    return public_key, private_key, crt_params
```
- `half` = `512` chia lấy nguyên cho `2`
- gán `p` = nguyên tố ngẫu nhiên có độ dài half
- gán `q` = nguyên tố ngẫu nhiên có độ dài half
- khi mà `p` giống `q` 
    - thì gán `q` = nguyên tố ngẫu nhiên có độ dài half khác
- gán `n` = `p` * `q`
- gán phi `n` = `p-1` * `q-1`
- nếu `e` và `phi` không có ước chung lớn nhất với `phi` là `1` 
    - thì gán `e` = `3`
    - nếu `e` tiếp tục không có ước chung lớn nhất với `phi` là `1` 
        - `e` tăng lên `2`
- gán `d` = nghịch đảo modular giữa `e` và `phi`
- Các tham số CRT: `dp` `dq` `qinv`
