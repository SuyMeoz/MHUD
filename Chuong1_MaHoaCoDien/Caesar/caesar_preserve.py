def caesar_encrypt_preserve(text, shift):
    result = []

    for i, ch in enumerate(text):
        if ch.isalpha():

            base = ord('A') if ch.isupper() else ord('a')

            new_ch = chr((ord(ch) - base + shift) % 26 + base)

            print(f"pos {i:02d}:'{ch}'->'{new_ch}' (base {chr(base)})")
            result.append(new_ch)

        else :         
            print(f"pos {i:02d}:'{ch}' khong phai chu -> giu nguyen")
            result.append(ch)
        
    return "".join(result)
    
plaintext = "Attack at dawn! 123"
print("Ban ro : ", plaintext,"\n")
shift = -7

cipher = caesar_encrypt_preserve(plaintext,shift)

print("Ban ma : ", cipher)
print("\n----- Giai ma lai -----")
recovered = caesar_encrypt_preserve(cipher, -shift)
print("\nBan ro phuc hoi : ", recovered)