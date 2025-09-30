# RC4 Stream Cipher in Python

## 1. Giới thiệu

RC4 là một thuật toán mã hóa dòng (stream cipher) nổi tiếng, được thiết kế bởi Ron Rivest năm 1987. RC4 hoạt động bằng cách sinh ra một dòng khóa (keystream) giả ngẫu nhiên, sau đó XOR với dữ liệu gốc để tạo ra bản mã. 

Vì phép XOR là đối xứng, cùng một hàm có thể dùng cho cả mã hóa và giải mã.

## 2. Nguyên lý hoạt động
RC4 có hai giai đoạn chính:

1. Key Scheduling Algorithm (KSA)
    - Khởi tạo một mảng S gồm 256 phần tử (0 → 255).
    - Dùng khóa bí mật để hoán vị mảng S.
    - Kết quả: một trạng thái ban đầu phụ thuộc vào khóa.

2. Pseudo-Random Generation Algorithm (PRGA)
    - Từ mảng S, sinh ra một dãy byte giả ngẫu nhiên gọi là keystream.
    - Mỗi byte dữ liệu được XOR với một byte keystream để tạo ra bản mã.

## 3. Đặc điểm
Loại: mã hóa dòng (stream cipher).

Độ dài khóa: từ 40 bit đến 2048 bit (thường dùng 128 bit).

Tốc độ: rất nhanh, phù hợp cho cả phần mềm và phần cứng.

Đơn giản: dễ cài đặt, chỉ vài chục dòng code.

## 4. Ứng dụng lịch sử
WEP (Wired Equivalent Privacy): chuẩn bảo mật Wi-Fi đầu tiên (1997).

WPA (Wi-Fi Protected Access): giai đoạn đầu vẫn dùng RC4.

SSL/TLS: từng là lựa chọn mặc định trong nhiều phiên bản cũ.

VPN, RDP, phần mềm thương mại: nhờ tốc độ cao.

## 5. Các lỗ hổng bảo mật
Mặc dù RC4 từng rất phổ biến, nhưng nhiều nghiên cứu đã chỉ ra lỗ hổng nghiêm trọng:

Bias trong keystream: các byte đầu tiên của RC4 không ngẫu nhiên hoàn toàn, có thể bị khai thác để suy ra khóa.

FMS attack (Fluhrer, Mantin, Shamir): tấn công nổi tiếng vào WEP, cho phép khôi phục khóa Wi-Fi chỉ sau vài triệu gói tin.

TLS attacks: nhiều công trình (2013–2015) chỉ ra RC4 trong SSL/TLS có thể bị phá bằng cách khai thác bias thống kê.

RFC 7465 (2015): IETF chính thức cấm RC4 trong TLS.

## 6. Tình trạng hiện nay
Không còn an toàn: NIST, IETF, Microsoft, Mozilla đều khuyến nghị không dùng RC4 trong bất kỳ ứng dụng mới nào.

Thay thế: các thuật toán hiện đại như AES (CTR, GCM) được khuyến nghị thay thế RC4.

Vẫn có giá trị học thuật: RC4 thường được dùng trong giảng dạy để minh họa về stream cipher.