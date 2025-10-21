import random
import time
import math
import matplotlib.pyplot as plt

def bytes_to_int(b):
    val = 0
    for byte in b:
        val = (val << 8) | byte
    return val

def int_to_bytes(x):
    if x == 0:
        return b'\x00'
    out = []
    while x > 0:
        out.append(x & 0xFF)
        x >>= 8
    out.reverse()
    return bytes(out)

def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else: 
        g, y, x = gcd(b % a, a)
        return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, _ = gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    
def pow_mod(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

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

def generate_prime_candidate(bits):
    candidate = random.getrandbits(bits)
    candidate |= (1 << (bits - 1))
    candidate |= 1
    return candidate

def generate_prime(bits):
    while True:
        cand = generate_prime_candidate(bits)
        if is_probable_prime(cand, k=10):
            return cand
        
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

def pkcs1_v1_5_pad_for_encryption(message_bytes, k):
    m_len = len(message_bytes)
    if m_len > k - 11:
        raise ValueError("Message too long for RSA encryption")
    ps_len = k - 3 - m_len
    ps = b''
    while len(ps) < ps_len:
        new = random.randrange(1, 256)
        ps += bytes([new])
    return b'\x00\x02' + ps + b'\x00' + message_bytes

def pkcs1_v1_5_unpad_for_encryption(padded):
    if len(padded) < 11:
        raise ValueError("decryption error, padded too short")
    if padded[0:1] != b'\x00' or padded[1:2] != b'\x02':
        raise ValueError("decryption error, incorrect padding")
    sep_index = padded.find(b'\x00', 2)
    if sep_index < 0 or sep_index < 10: # PS phải có ít nhất 8 byte
        raise ValueError("decryption error, invalid padding")
    return padded[sep_index + 1:]

def rsa_encrypt_with_padding(message_bytes, public_key):
    e, n = public_key
    k = (n.bit_length() + 7) // 8
    padded = pkcs1_v1_5_pad_for_encryption(message_bytes, k)
    m = bytes_to_int(padded)
    c = pow_mod(m, e, n)
    return c

def rsa_decrypt_with_privatekey(ciphertext_int, private_key):
    d, n = private_key
    m = pow_mod(ciphertext_int, d, n)
    return int_to_bytes(m)

def rsa_decrypt_with_crt(ciphertext_int, crt_params):
    p, q, dp, dq, qinv = crt_params
    m1 = pow_mod(ciphertext_int % p, dp, p)
    m2 = pow_mod(ciphertext_int % q, dq, q)
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q
    return int_to_bytes(m)

def rsa_decrypt_with_padding_crt(cipher_int, private_key, crt_params):
    m_bytes = rsa_decrypt_with_crt(cipher_int, crt_params)
    try:
        message = pkcs1_v1_5_unpad_for_encryption(m_bytes)
    except Exception as ex:
        m_bytes_stripped = m_bytes.lstrip(b'\x00')
        message = pkcs1_v1_5_unpad_for_encryption(m_bytes_stripped)
    return message

def benchmark_rsa(bits_list=[512, 1024, 2048], trials=3, message=b"Test RSA message"):
    results = {}
    for bits in bits_list:
        print("\n=== Benchmark for %d-bit modulus ===" % bits)
        t0 = time.time()
        pubkey, privkey, crt_params = generate_rsa_keypair(bits)
        t1 = time.time()
        keygen_time = t1 - t0
        print("Đã sinh cặp khóa (%d-bit). Thời gian: %.3f s" % (bits, keygen_time))

        enc_times = []
        cipher_int = None
        for _ in range(trials):
            t0 = time.time()
            cipher_int = rsa_encrypt_with_padding(message, pubkey)
            t1 = time.time()
            enc_times.append(t1 - t0)
        enc_avg = sum(enc_times) / len(enc_times)
        print("Thời gian mã hóa trung bình (trials=%d): %.6f s" % (trials, enc_avg))

        dec_times_trad = []
        for _ in range(trials):
            t0 = time.time()
            m_bytes = rsa_decrypt_with_privatekey(cipher_int, privkey) 
            
            try:
                _ = pkcs1_v1_5_unpad_for_encryption(m_bytes.lstrip(b'\x00'))
            except:
                pass
            t1 = time.time()
            dec_times_trad.append(t1 - t0)
        dec_trad_avg = sum(dec_times_trad) / len(dec_times_trad)
        print("Thời gian giải mã (truyền thống) trung bình: %.6f s" % dec_trad_avg)

        dec_times_crt = []
        for _ in range(trials):
            t0 = time.time()
            m_bytes_crt = rsa_decrypt_with_crt(cipher_int, crt_params)
            # unpad thử
            try:
                _ = pkcs1_v1_5_unpad_for_encryption(m_bytes_crt.lstrip(b'\x00'))
            except:
                pass
            t1 = time.time()
            dec_times_crt.append(t1 - t0)
        dec_crt_avg = sum(dec_times_crt) / len(dec_times_crt)
        print("Thời gian giải mã (CRT) trung bình: %.6f s" % dec_crt_avg)

        results[bits] = {
            'keygen_time': keygen_time,
            'enc_avg': enc_avg,
            'dec_trad_avg': dec_trad_avg,
            'dec_crt_avg': dec_crt_avg,
            'pubkey': pubkey,
            'privkey': privkey,
            'crt_params': crt_params
        }

    bits_labels = [str(b) for b in bits_list]
    keygen_vals = [results[b]['keygen_time'] for b in bits_list]
    enc_vals = [results[b]['enc_avg'] for b in bits_list]
    dec_trad_vals = [results[b]['dec_trad_avg'] for b in bits_list]
    dec_crt_vals = [results[b]['dec_crt_avg'] for b in bits_list]

    x = range(len(bits_list))
    plt.figure(figsize=(12,5))
    # Biểu đồ 1: thời gian sinh khóa
    plt.subplot(1,2,1)
    plt.bar(x, keygen_vals, tick_label=bits_labels)
    plt.title("Key generation time (seconds)")
    plt.xlabel("Modulus bits")
    plt.ylabel("Seconds")
    for i, v in enumerate(keygen_vals):
        plt.text(i, v * 1.01, "%.3f" % v, ha='center', va='bottom')
    
    # Biểu đồ 2: encode/decode
    plt.subplot(1,2,2)
    width = 0.2
    plt.bar([i - 1.5*width for i in x], enc_vals, width=width, label='Encrypt avg')
    plt.bar([i - 0.5*width for i in x], dec_trad_vals, width=width, label='Decrypt (trad) avg')
    plt.bar([i + 0.5*width for i in x], dec_crt_vals, width=width, label='Decrypt (CRT) avg')
    plt.xticks(x, bits_labels)
    plt.title("Encrypt/Decrypt times (seconds)")
    plt.xlabel("Modulus bits")
    plt.ylabel("Seconds")
    plt.legend()
    for i, v in enumerate(enc_vals):
        plt.text(i - 1.5*width, v * 1.01, "%.4f" % v, ha='center', va='bottom',fontsize=8)
    for i, v in enumerate(dec_trad_vals):
        plt.text(i - 0.5*width, v * 1.01, "%.4f" % v, ha='center', va='bottom',fontsize=8)
    for i, v in enumerate(dec_crt_vals):
        plt.text(i + 0.5*width, v * 1.01, "%.4f" % v, ha='center', va='bottom',fontsize=8)
    plt.tight_layout()
    plt.show()
    return results

bits_list = [512, 1024] 
trials = 3 
message = b"RSA benchmark test message"
results = benchmark_rsa(bits_list=bits_list, trials=trials, message=message)

for bits in bits_list:
    r = results[bits]
    print("\nSummary %d-bit:" % bits)
    print(" keygen: %.3f s; encrypt avg: %.6f s; decrypt(trad) avg: %.6f s;decrypt(CRT) avg: %.6f s" % (r['keygen_time'], r['enc_avg'], r['dec_trad_avg'], r['dec_crt_avg']))