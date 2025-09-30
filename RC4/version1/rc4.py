def rc4_encrypt_decrypt(key, data):
    S = list(range(256))
    T = [0] * 256
    key_len = len(key)

    for i in range(256):
        T[i] = key[i % key_len]

    j = 0 

    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    
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
    
    return bytes(result)

key = b'SecretKey'

plaintext = b'Hello, World! This is a test message.'

ciphertext = rc4_encrypt_decrypt(key, plaintext)

print(f"ban ro : {plaintext.decode('utf-8')}")
print(f"ban ma hoa (hex): {ciphertext.hex()}")

decrypted_text = rc4_encrypt_decrypt(key, ciphertext)
print(f"ban giai ma : {decrypted_text.decode('utf-8')}")
