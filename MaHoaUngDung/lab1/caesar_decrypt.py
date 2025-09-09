import caesar_encrypt 

def caesar_decrypt_char(ch, shift):
    return caesar_encrypt.caesar_encrypt_char(ch, -shift)

def caesar_decrypt(ciphertext, shift):

    print(f"Shift de giai ma = {shift} (tuc dich nguoc bang {-shift})")

    plain_chars = []

    for idx, ch in enumerate(ciphertext):

        dec = caesar_decrypt_char(ch, shift)

        print(f"pos {idx:02d} : '{ch}' -> '{dec}'")

        plain_chars.append(dec)

    plaintext = "".join(plain_chars)

    print("\nBan ro phuc hoi : ", plaintext)

    return plaintext

ciphertext = "MJQQT BTWQI"
print("Ban ma : ", ciphertext, "\n")
plain = caesar_decrypt(ciphertext, 5)
