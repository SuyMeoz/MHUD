import caesar_encrypt
from collections import Counter
import random


def caesar_encrypt_simple(text, shift):
    return "".join(caesar_encrypt.caesar_encrypt_char(ch, shift) for ch in text)

plaintext = "THIS IS A DEMONSTRATION OF THE CAESAR CIPHER. \
WE WILL ENCODE THIS LONGER MESSAGE OF FREQUENCY ANALYSIS \
HAS A CHANCE TO WORK. FREQUENCY OF LETTERS HELPS GUESS SHIFT."

print("Plaintext (original):")
print(plaintext,"\n")

hidden_shift = random.randint(1, 25)
ciphertext = caesar_encrypt_simple(plaintext, hidden_shift)

print(f"Tren thuc te code da dung shift bi mat = {hidden_shift} de sinh ban ma\n")
print("Ciphertext : ", ciphertext, "\n")

only_letter = "".join(ch for ch in ciphertext if ch.isalpha()).upper()

freq = Counter(only_letter)

print("Tan suat ky tu trong ban ma (giam dan) : ")
for ch, cnt in freq.most_common():
    print(f"{ch} : {cnt}")

most_common_cipher_letter, _ = freq.most_common(1)[0]

assumed_plain_most = 'E'

guessed_shift = (ord(most_common_cipher_letter) - ord(assumed_plain_most)) % 26

print(f"\nChu xuat hien nhieu nhat trong ban ma : '{most_common_cipher_letter}'")
print(f"Gia su chu tuong ung trong ban ro la '{assumed_plain_most}' => uoc luoc shift = {guessed_shift}")

guessed_plain_by_freq = caesar_encrypt_simple(ciphertext, -guessed_shift)
print("\nKet qua giai ma theo uoc luong tan suat : ")
print(guessed_plain_by_freq)


print("----- Brute Force (tat ca 26 shift) de doi chieu -----")

for s in range(26):
    candidate = caesar_encrypt_simple(ciphertext, -s)
    marker = "<-- guessed" if s == guessed_shift else ""
    print(f"shift {s:02d}: {candidate} {marker}")

print(f"\n(ghi chu : shift thuc te dung de sinh ban ma la {hidden_shift})")