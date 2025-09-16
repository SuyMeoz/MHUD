## 1

Tạo các chương trình :
- mã hóa văn bản theo mã hóa caeser
- giải mã bản mã đã được mã hóa 
- tấn công mã hóa caeser bằng phương pháp Brute Force ( tấn công vét cạn )
- mã hóa caeser nhưng bảo toàn các chữ cái hoa, thường và các ký tự không phải chữ

## 2

### Mã hóa từng ký tự 
```
def caesar_encrypt_char(ch, shift):

    if 'A' <= ch <= 'Z':

        base = ord('A')

        return chr( (ord(ch) - base + shift ) % 26 + base )
    
    if 'a' <= ch <= 'z':
        
        base = ord('a')

        return chr( (ord(ch)  - base + shift) %  26 + base)
    
    return ch
```

### mã hóa chuỗi ký tự :

```
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
```

`chr(ord('A') + i)` : tạo từng chữ cái từ 'A' tới 'Z'

`chr( (ord('A') + i - ord('A')` : tính vị trí của chữ cái trong bảng chữ cái từ (0-25)

`+ shift` dịch chuyển vị trí

`print("" + "".join(mapping_upper.keys()))` : in ra bảng chữ cái gốc 
> nguồn từ câu lệnh : { `chr(ord('a') + i)`: chr( (ord('a') + i - ord('a') + shift) % 26 + ord('a')) for i in range(26) }

`print("=>" + "".join(mapping_upper.values()))` : in ra bảng chữ cái đã mã hóa theo shift 
> nguồn từ câu lệnh : { chr(ord('a') + i): `chr( (ord('a') + i - ord('a') + shift) % 26 + ord('a')) for i in range(26)` }


`enc = caesar_encrypt_char(ch, shift)` : mã hóa từng ký tự trong chuỗi

`cipher_chars.append(enc)` : thêm ký tự mã hóa vào danh sách

### giải mã chuỗi ký tự đã mã hóa :

```
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
```

`dec = caesar_decrypt_char(ch, shift)` : giải mã từng ký tự trong chuỗi

`plain_chars.append(dec)` thêm ký tự đã giải mã vào danh sách

### tấn công brute force
```
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
```

`return "".join(caesar_encrypt.caesar_encrypt_char(ch, shift) for ch in text)` : dịch chuyển toàn bộ chuỗi theo shift

`upper = " " + text_decrypt.upper() + " "` : chuyển toàn bộ sang chữ hoa để so sánh với danh sách từ phổ biến

`score = sum(1 for w in common_words if w in upper)` : tính điểm bằng cách duyệt qua từng từ trong danh sách và kiểm tra có xuất hiện trong chuỗi upper hay không

`candidates_sorted = sorted(candidates, key=lambda x: (-x[1], x[0]))
best = candidates_sorted[0]
` : Sắp xếp theo điểm số giảm dần (-x[1]) và nếu bằng nhau thì chọn shift nhỏ hơn (x[0]). Best là bản giải mã có nhiều từ phổ biến nhất → khả năng cao là bản rõ đúng

### tấn công dựa trên tần suất

```
def caesar_encrypt_simple(text, shift):
    return "".join(caesar_encrypt.caesar_encrypt_char(ch, shift) for ch in text)
```
 hàm mã hóa toàn bộ chuỗi

`hidden_shift = random.randint(1, 25)` : chọn shift ngẫu nhiên từ (1 - 25)

`only_letter = "".join(ch for ch in ciphertext if ch.isalpha()).upper()` chỉ chuyển mỗi ký tự thành chữ hoa

`freq = Counter(only_letter)` : đếm tần suất xuất hiện của từng chữ cái

`most_common_cipher_letter, _ = freq.most_common(1)[0]` : trả về danh sách chứa 1 phần tử có tần suất cao nhất

`assumed_plain_most = 'E'` : suy đoán E là ký tự suất hiện nhiều nhất

`guessed_shift = (ord(most_common_cipher_letter) - ord(assumed_plain_most)) % 26` : ước lượng khóa dịch chuyển bằng cách so sánh vị trí của chữ cái phổ biến nhất trong bản mã với chữ cái phổ biến nhất trong ngôn ngữ gốc

`guessed_plain_by_freq = caesar_encrypt_simple(ciphertext, -guessed_shift)` : giải mã bằng khóa đã ước lượng


```
for s in range(26):
    candidate = caesar_encrypt_simple(ciphertext, -s)
    marker = "<-- guessed" if s == guessed_shift else ""
    print(f"shift {s:02d}: {candidate} {marker}")
```

dùng brute force thử tất cả các khóa dịch chuyển


## 3

### Ưu điểm 
- đơn giản, dễ hiểu 
- mã hóa nhanh chóng

### Nhược điểm 
- bảo mật kém
- chỉ dùng cho bảng chữ cái cố định

## 4 

Các phương pháp tấn công :
 - tấn công vét cạn 
 - tấn công phân tích tần suất
 - tấn công dựa vào ngữ cảnh hoặc từ khóa
 - tấn công thống kê

Các phương pháp tấn công sử dụng trong bài lab:
 - tấn công vét cạn Brute Force : Vì Caesar Cipher chỉ có 25 khóa khả thi (dịch từ 1 đến 25), kẻ tấn công có thể thử tất cả các khả năng để giải mã văn bản.
 - tấn công phân tích tần suất : Trong tiếng Anh một số chữ cái xuất hiện thường xuyên hơn (ví dụ: E, T, A), Bằng cách đếm tần suất xuất hiện của các ký tự trong bản mã, ta có thể đoán được ký tự nào đã bị mã hóa từ ký tự phổ biến nhất.
