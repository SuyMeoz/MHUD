# AES 

### 1. Bảng hằng số và ma trận (S_BOX, INV_S_BOX, MIX_COLUMNS_MATRIX, INV_MIX_COLUMNS_MATRIX, RCON, NUM_ROUNDS)

- **S_BOX = [ ... ]**
  - Đây là bảng thay thế không tuyến tính 256 phần tử, ánh xạ mỗi byte đầu vào sang byte đầu ra trong bước SubBytes của AES.
  - Mỗi giá trị là một số nguyên 0..255, viết dưới dạng hex để dễ đọc.

- **INV_S_BOX = [ ... ]**
  - Bảng thay thế đảo ngược, dùng trong giải mã ở bước InvSubBytes. Nếu S_BOX[x] = y thì INV_S_BOX[y] = x.

- **MIX_COLUMNS_MATRIX = [ [0x02,0x03,0x01,0x01], ... ]**
  - Ma trận 4×4 cho phép MixColumns; phép nhân ma trận này với mỗi cột trạng thái thực hiện hoán trộn tuyến tính từng cột trong trường hữu hạn GF(2^8).
  - Các hệ số 0x02, 0x03, 0x01 biểu diễn yếu tố của đa thức trong GF(2^8).

- **INV_MIX_COLUMNS_MATRIX = [ [0x0e,0x0b,0x0d,0x09], ... ]**
  - Ma trận đảo ngược dùng cho InvMixColumns trong quá trình giải mã.

- **RCON = [0x8d, 0x01, 0x02, 0x04, ...]**
  - Hằng số vòng (round constants) dùng trong KeyExpansion; RCON[i] được XOR vào byte đầu của từ khi thực hiện thao tác xoay + S-box trong việc mở rộng khóa.

- **NUM_ROUNDS = 10**
  - Số vòng cho AES-128 là 10. (AES-192 và AES-256 có nhiều vòng hơn.)

---

### 2. Lớp AES: __init__(self, key)
```python
class AES:
    def __init__(self,key):
        if len(key) not in [16, 24, 32]:
            raise ValueError("Do dai khoa khong hop le (16, 24, hoac 32 byte).")
        
        self.key = key
        self.round_keys = self._key_expansion()
```
- **def __init__(self, key):**
  - Khởi tạo đối tượng AES với khóa nhị phân `key`.
  - **if len(key) not in [16,24,32]: raise ValueError(...)**
    - Kiểm tra độ dài khóa hợp lệ; AES hỗ trợ 128, 192, 256 bit tương ứng 16, 24, 32 byte.
  - **self.key = key**
    - Lưu khóa gốc.
  - **self.round_keys = self._key_expansion()**
    - Sinh các round key bằng phương thức _key_expansion và gán cho thuộc tính.

---

### 3. Hàm hỗ trợ thay thế byte: _sub_bytes(self, state, sbox)
```python
def _sub_bytes(self, state, sbox):
    for row in range(4):
        for col in range(4):
            state[row][col] = sbox[state[row][col]]
```
- **def _sub_bytes(self, state, sbox):**
  - Duyệt từng ô trong ma trận trạng thái 4×4.
  - **state[row][col] = sbox[state[row][col]]**
    - Thay mỗi byte bằng giá trị tương ứng trong bảng S-BOX (hoặc INV_S_BOX khi giải mã).
  - Ý nghĩa: tạo phi tuyến cho AES, phá vỡ mối quan hệ tuyến tính.

---

### 4. Dịch hàng: _shift_rows(self, state) và _inv_shift_rows(self, state)
```python
def _shift_rows(self, state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]

def _inv_shift_rows(self, state):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]
```
- **def _shift_rows(self, state):**
  - Dịch hàng 1 sang trái 1 vị trí, hàng 2 sang trái 2 vị trí, hàng 3 sang trái 3 vị trí.
  - Cụ thể:
    - state[1] = state[1][1:] + state[1][:1]
    - state[2] = state[2][2:] + state[2][:2]
    - state[3] = state[3][3:] + state[3][:3]
  - Ý nghĩa: tạo phân tán ngang giữa các cột khác nhau.

- **def _inv_shift_rows(self, state):**
  - Là thao tác nghịch đảo: dịch phải tương ứng để phục hồi trạng thái trước đó.
  - Cụ thể:
    - state[1] = state[1][-1:] + state[1][:-1]
    - state[2] = state[2][-2:] + state[2][:-2]
    - state[3] = state[3][-3:] + state[3][:-3]

---

### 5. Trộn cột: _mix_columns(self, state, mtrix) và _inv_mix_columns(self, state, matrix)
```python
def _mix_columns(self, state, mtrix):
    new_state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for col in range(4):
        for row in range(4):
            val = 0
            for i in range(4):
                val ^= self._gf_mult(mtrix[row][i], state[i][col])
            new_state[row][col] = val
    state[:] = new_state

def _inv_mix_columns(self, state, matrix):
    new_state = [[0, 0, 0, 0] for _ in range(4)]
    for col in range(4):
        for row in range(4):
            val = 0
            for i in range(4):
                val ^= self._gf_mult(matrix[row][i], state[i][col])
            new_state[row][col] = val
    state[:] = new_state
```
- **def _mix_columns(self, state, mtrix):**
  - Tạo `new_state` (4×4) khởi tạo bằng 0.
  - Duyệt từng cột col (0..3) và từng hàng row (0..3).
  - Tính `val` bằng XOR của các tích giữa hệ số ma trận `mtrix[row][i]` và `state[i][col]` theo trường GF(2^8).
  - Gán `new_state[row][col] = val`.
  - Cuối cùng gán `state[:] = new_state` để thay thế toàn bộ trạng thái.
  - Ý nghĩa: áp dụng phép biến đổi tuyến tính lên mỗi cột nhằm tăng tính phân tán.

- **def _inv_mix_columns(self, state, matrix):**
  - Cùng cấu trúc như _mix_columns nhưng sử dụng ma trận đảo ngược để đảo quá trình trộn cột trong giải mã.

---

### 6. Nhân trong GF(2^8): _gf_mult(self, a, b)
```python
def _gf_mult(self, a, b):
    p = 0
    hi_bit_set = 0x80

    for _ in range(8):
        if (b & 1) == 1:
            p ^= a

        if (a & hi_bit_set) == hi_bit_set:
            a <<= 1
            a ^= 0x1b
        else:
            a <<= 1
        b >>= 1
    return p % 0x100
```
- **def _gf_mult(self, a, b):**
  - Thực hiện nhân hai byte `a` và `b` trong trường hữu hạn GF(2^8) với đa thức giảm mô 0x11b.
  - Thuật toán:
    - Khởi `p = 0`.
    - Lặp 8 lần (mỗi bit của b):
      - Nếu bit thấp nhất của `b` là 1: `p ^= a` (cộng trên GF là XOR).
      - Kiểm tra bit cao của `a` (0x80). Nếu set, trái `a` lên 1 bit rồi XOR với 0x1b để giảm mô.
      - Ngược lại chỉ trái `a`.
      - Dịch phải `b` sang phải 1 bit.
    - Trả `p % 0x100` để giữ giá trị 1 byte.
  - Ý nghĩa: phép nhân cần thiết để tính tích ma trận trong MixColumns theo GF(2^8).

---

### 7. Thêm khóa vòng: _add_round_key(self, state, round_key)
```python
def _add_round_key(self, state, round_key):
    for row in range(4):
        for col in range(4):
            state[row][col] ^= round_key[row][col]
```
- **def _add_round_key(self, state, round_key):**
  - Duyệt từng ô state và XOR với tương ứng `round_key[row][col]`.
  - Đây là bước duy nhất sử dụng trực tiếp khóa vòng, giúp liên kết khóa với dữ liệu.

---

### 8. Mở rộng khóa: _key_expansion(self)
```python
def _key_expansion(self):
    key_words = [word for word in self._to_words(self.key)]

    for i in range(4 ,4* (NUM_ROUNDS + 1)):
        temp = key_words[i - 1]

        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [S_BOX[b] for b in temp]
            temp[0] ^= RCON[i // 4]

        key_words.append([ (key_words[i - 4][j] ^ temp[j]) for j in range(4)])  

    round_keys = []
    for i in range(NUM_ROUNDS + 1):
        round_key = [[0, 0, 0, 0] for _ in range(4)]

        for col in range(4):
            for row in range(4):
                round_key[col][row] = key_words[i * 4 + col][row]
        
        round_keys.append(round_key)

    return round_keys
```
- **def _key_expansion(self):**
  - Chia khóa gốc thành các từ 4-byte bằng `_to_words(self.key)`: kết quả `key_words` là danh sách các từ.
  - Vòng for i từ 4 đến 4 * (NUM_ROUNDS + 1) - 1:
    - `temp = key_words[i - 1]`
    - Nếu `i % 4 == 0` (mỗi 4 từ):
      - **temp = temp[1:] + temp[:1]**: xoay từ (rotWord).
      - **temp = [S_BOX[b] for b in temp]**: áp S-Box cho từng byte (subWord).
      - **temp[0] ^= RCON[i // 4]**: XOR vào byte đầu với RCON.
    - Tạo từ mới bằng XOR từng byte của `key_words[i-4]` với `temp`.
    - Thêm vào `key_words`.
  - Tạo `round_keys`: nhóm mỗi 4 từ thành 1 round key (4×4 ma trận).
    - Lưu ý: khi gán vào `round_key[col][row] = key_words[i * 4 + col][row]` mã ánh xạ theo cột để phù hợp biểu diễn trạng thái theo cột.
  - Trả về danh sách `round_keys` có NUM_ROUNDS+1 phần tử.
  - Ý nghĩa: sinh đủ khóa cho mọi vòng mã/giải mã.

---

### 9. Chuyển đổi dữ liệu trạng thái: _to_words, _to_state, _from_state
```python
def _to_words(self, key):
    words = []
    for i in range(0, len(key), 4):
        words.append(list(key[i:i+4]))

    return words

def _to_state(self, block):
    state = [[0, 0, 0, 0] for _ in range(4)]
    for col in range(4):
        for row in range(4):
            state[row][col] = block[col * 4 + row]

    return state

def _from_state(self, state):
    block = bytearray(16)
    for col in range(4):
        for row in range(4):
            block[col * 4 + row] = state[row][col]
    
    return bytes(block)
```
- **def _to_words(self, key):**
  - Chia khóa thành các từ 4 byte: lặp từ 0 đến len(key) step 4, thêm list(key[i:i+4]).
  - Trả danh sách các từ.

- **def _to_state(self, block):**
  - Chuyển khối 16 byte (dạng mảng 1 chiều theo thứ tự bytes) thành ma trận trạng thái 4×4.
  - Cách ánh xạ: state[row][col] = block[col * 4 + row] (AES dùng cột là đơn vị liên tiếp trong bộ nhớ).
  - Trả `state`.

- **def _from_state(self, state):**
  - Chuyển ma trận trạng thái 4×4 trở về khối 16 byte cùng ánh xạ ngược.
  - Tạo `bytearray(16)` và gán block[col * 4 + row] = state[row][col].
  - Trả `bytes(block)`.

---

### 10. Mã hóa: encrypt(self, plaintext)
```python
def encrypt(self, plaintext):
    if len(plaintext) != 16:
        raise ValueError("Do dai ban ro phai la 16 byte.")
    
    state = self._to_state(plaintext)
    self._add_round_key(state, self.round_keys[0])
    for i in range(1, NUM_ROUNDS):
        self._sub_bytes(state, S_BOX)
        self._shift_rows(state)
        self._mix_columns(state, MIX_COLUMNS_MATRIX)
        self._add_round_key(state, self.round_keys[i])

    self._sub_bytes(state, S_BOX)
    self._shift_rows(state)
    self._add_round_key(state, self.round_keys[NUM_ROUNDS])

    return self._from_state(state)
```
- **def encrypt(self, plaintext):**
  - **if len(plaintext) != 16: raise ValueError(...)**
    - Hàm này hỗ trợ mã hóa khối 16 byte duy nhất (electronic codebook-style), không xử lý padding hay chế độ hoạt động.
  - **state = self._to_state(plaintext)**: đưa plaintext thành ma trận trạng thái.
  - **self._add_round_key(state, self.round_keys[0])**: thêm round key đầu tiên (AddRoundKey trước khi vào vòng).
  - Vòng for i từ 1 đến NUM_ROUNDS-1:
    - `_sub_bytes(state, S_BOX)` — SubBytes.
    - `_shift_rows(state)` — ShiftRows.
    - `_mix_columns(state, MIX_COLUMNS_MATRIX)` — MixColumns.
    - `_add_round_key(state, self.round_keys[i])` — AddRoundKey.
  - Sau vòng chính, thực hiện lần SubBytes, ShiftRows, rồi AddRoundKey cuối cùng (không MixColumns ở vòng cuối).
  - Trả `_from_state(state)` dưới dạng bytes: bản mã khối 16 byte.

---

### 11. Giải mã: decrypt(self, ciphertext)
```python
def decrypt(self, ciphertext):
    if len(ciphertext) != 16:
        raise ValueError("Do dai ban ro phai la 16 byte.")
    
    state = self._to_state(ciphertext)
    self._add_round_key(state, self.round_keys[NUM_ROUNDS])
    self._inv_shift_rows(state)
    self._sub_bytes(state, INV_S_BOX)

    for i in range(NUM_ROUNDS - 1, 0, -1):
        self._add_round_key(state, self.round_keys[i])
        self._inv_mix_columns(state, INV_MIX_COLUMNS_MATRIX)
        self._inv_shift_rows(state)
        self._sub_bytes(state, INV_S_BOX)

    self._add_round_key(state, self.round_keys[0])

    return self._from_state(state)
```
- **def decrypt(self, ciphertext):**
  - Kiểm tra độ dài ciphertext là 16 byte.
  - **state = self._to_state(ciphertext)**.
  - **self._add_round_key(state, self.round_keys[NUM_ROUNDS])**: thêm khóa của vòng cuối.
  - **self._inv_shift_rows(state)**: dịch phải các hàng (ngược ShiftRows).
  - **self._sub_bytes(state, INV_S_BOX)**: InvSubBytes (lưu ý trình tự có thể thay đổi ở các cài đặt; mã này áp trình tự InvShiftRows trước InvSubBytes).
  - Vòng for i từ NUM_ROUNDS-1 xuống 1:
    - `_add_round_key(state, self.round_keys[i])`
    - `_inv_mix_columns(state, INV_MIX_COLUMNS_MATRIX)`
    - `_inv_shift_rows(state)`
    - `_sub_bytes(state, INV_S_BOX)`
  - Cuối cùng `_add_round_key(state, self.round_keys[0])`.
  - Trả `_from_state(state)` là plaintext khôi phục.

---

### 12. Ví dụ sử dụng (phần cuối mã)

- **key = b'Sixteen byte key'**
  - Khóa 16 byte dùng cho AES-128. Đây là kiểu bytes trong Python.
- **plaintext = b'A test message!!'**
  - Khối 16 byte để mã hóa.
- **aes_cipher_encrypt = AES(key)**
  - Tạo đối tượng AES; gọi __init__ sẽ sinh round_keys.
- **encrypted_text = aes_cipher_encrypt.encrypt(plaintext)**
  - Thực hiện mã hóa 16 byte.
- **print(f\"Bản rõ: {plaintext.hex()}\")**
  - In bản rõ dưới dạng hex để dễ kiểm tra.
- **print(f\"Bản mã: {encrypted_text.hex()}\")**
  - In ciphertext hex.
- **aes_cipher_decrypt = AES(key)**
  - Tạo đối tượng AES khác (cũng có thể dùng cùng đối tượng).
- **decrypted_text = aes_cipher_decrypt.decrypt(encrypted_text)**
  - Giải mã lại.
- **print(f\"Bản giải mã: {decrypted_text.hex()}\")**
  - In plaintext khôi phục.
- **print(f\"Bản giải mã khớp với bản rõ: {decrypted_text == plaintext}\")**
  - Kiểm tra tính đúng đắn; giá trị True khi giải mã thành công.
