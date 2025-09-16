def caesar_encrypt_char(ch, shift):

    if 'A' <= ch <= 'Z':

        base = ord('A')

        return chr( (ord(ch) - base + shift ) % 26 + base )
    
    if 'a' <= ch <= 'z':
        
        base = ord('a')

        return chr( (ord(ch)  - base + shift) %  26 + base)
    
    return ch

def caesar_encrypt(plaintext, shift):
    print(f'Shift = {shift}')

    mapping_upper = { chr(ord('A') + i): chr( (ord('A') + i - ord('A') + shift) % 26 + ord('A')) for i in range(26) }
    mapping_lower = { chr(ord('a') + i): chr( (ord('a') + i - ord('a') + shift) % 26 + ord('a')) for i in range(26) }

    print("Anh xa (chi in A-Z) : ")

    print("" + "".join(mapping_upper.keys()))

    print("=>" + "".join(mapping_upper.values()))

    print()

    cipher_chars = []

    for idx, ch in enumerate(plaintext):

        enc = caesar_encrypt_char(ch, shift)

        print(f" pos {idx:02d} : '{ch}' -> '{enc}' ")

        cipher_chars.append(enc)
    
    cipher_text = "".join(cipher_chars)

    print("\nBan ma cuoi : ", cipher_text)

    return cipher_text

if __name__ == "__main__":
    plaintext = "HELLO WORLD"

    print("Ban ro : ",plaintext,"\n")

    cipher = caesar_encrypt(plaintext,3)