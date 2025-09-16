import re
import caesar_encrypt

def caesar_shift_text(text, shift):
    return "".join(caesar_encrypt.caesar_encrypt_char(ch, shift) for ch in text)

ciphertext = "YMJ VZNHP GWTBS KTC OZRUX TAJW YMJ QFED ITL"

common_words = ["THE", "AND", "TO", "OF", "IS", "THAT", "FOR",]

candidates = []

for s in range(26):

    text_decrypt = caesar_shift_text(ciphertext, -s)

    upper = " " + text_decrypt.upper() + " "

    score = sum(1 for w in common_words if w in upper)

    candidates.append((s,score,text_decrypt))

    print(f"Shift {s:02d} -> {text_decrypt} [score = {score}]")

candidates_sorted = sorted(candidates, key=lambda x: (-x[1], x[0]))

best = candidates_sorted[0]

print("\nGoi y tot nhat theo heuritic (nhieu tu pho bien xuat hien nhat) : ")

print(f"Shift = {best[0]:02d}, score = {best[1]}, plaintext candidate : \n {best[2]}")