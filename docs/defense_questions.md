# Câu hỏi bảo vệ – A5/1 và TinyA5/1

Người soạn: Trần Đại Lộc (GĐ4). Cập nhật 28/10/2026.

15 câu phủ đủ 7 chủ đề bảng phân công yêu cầu: TinyA5/1, A5/1, majority, feedback, Two-Time Pad, kiểm thử, benchmark. Mỗi đáp án nói trong khoảng 30 giây.

## A. TinyA5/1

**Câu 1. TinyA5/1 gồm những gì, khóa được nạp thế nào?**

Gồm 3 thanh ghi dịch LFSR: X dài 6 bit (x0–x5), Y dài 8 bit (y0–y7), Z dài 9 bit (z0–z8). Khóa K dài 6 + 8 + 9 = 23 bit, nạp thẳng theo thứ tự: 6 bit đầu vào X, 8 bit tiếp vào Y, 9 bit cuối vào Z. TinyA5/1 không nạp số khung và không có warm-up.

**Câu 2. Hàm majority hoạt động thế nào? Vì sao mỗi bước luôn có ít nhất 2 thanh ghi quay?**

m = maj(x1, y3, z3) là giá trị xuất hiện ít nhất 2 lần trong 3 bit điều khiển. Thanh ghi nào có bit điều khiển bằng m thì quay, còn lại đứng yên (stop-and-go). Vì m là đa số nên luôn có ít nhất 2 bit bằng m, tức ít nhất 2 thanh ghi quay. Mỗi thanh ghi quay với xác suất 3/4. Việc quay không đều này chính là thành phần phi tuyến của hệ mã.

**Câu 3. Bit phản hồi (feedback) tính thế nào, thanh ghi dịch ra sao, bit dòng khóa lấy ở đâu?**

- Phản hồi: tX = x2 ⊕ x4 ⊕ x5, tY = y6 ⊕ y7, tZ = z2 ⊕ z7 ⊕ z8.
- Khi quay, mọi bit dịch sang vị trí có chỉ số lớn hơn, bit cuối bị đẩy ra, bit t vừa tính được nạp vào vị trí 0.
- Bit dòng khóa si = x5 ⊕ y7 ⊕ z8, lấy **sau khi quay**.

**Câu 4. Trình bày lại ví dụ trên slide.**

K = 10010101001110100110000, P = 111, nên X = 100101, Y = 01001110, Z = 100110000.

| Bước | (x1, y3, z3) | m | Thanh ghi quay | Sau bước | (x5, y7, z8) | si |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0, 0, 1 | 0 | X, Y | X = 110010, Y = 10100111 | 0, 1, 0 | 1 |
| 1 | 1, 0, 1 | 1 | X, Z | X = 111001, Z = 010011000 | 1, 1, 0 | 0 |
| 2 | 1, 0, 0 | 0 | Y, Z | Y = 01010011, Z = 001001100 | 1, 1, 0 | 0 |

S = 100, C = 111 ⊕ 100 = 011, giải mã 011 ⊕ 100 = 111. Kết quả khớp slide.

**Câu 5. Slide có điểm lệch ở Z, nhóm xử lý thế nào?**

Slide in Z sau bước 2 là 101001100, nhưng tính theo quy tắc ra 001001100. Trước bước 2, Z = 010011000 nên tZ = z2 ⊕ z7 ⊕ z8 = 0 ⊕ 0 ⊕ 0 = 0, vì vậy bit mới ở z0 phải là 0. Hai giá trị chỉ khác ở z0, còn bit ra z8 đều bằng 0, nên s2, S và C không đổi. Nhóm giữ đúng giá trị toán học trong code, ghi chú điểm lệch trên GUI và trong báo cáo, không sửa slide.

## B. A5/1 đầy đủ

**Câu 6. A5/1 khác TinyA5/1 ở những điểm nào?**

| Thông số | TinyA5/1 | A5/1 |
| --- | --- | --- |
| Thanh ghi | X 6, Y 8, Z 9 bit | R1 19, R2 22, R3 23 bit |
| Khóa | 23 bit | 64 bit |
| Bit điều khiển | x1, y3, z3 | x8, y10, z10 |
| Taps | x2, x4, x5 / y6, y7 / z2, z7, z8 | x13, x16, x17, x18 / y20, y21 / z7, z20, z21, z22 |
| Bit ra | x5 ⊕ y7 ⊕ z8 | x18 ⊕ y21 ⊕ z22 |
| Khởi tạo | Nạp thẳng khóa | Nạp khóa, nạp khung, warm-up |
| Dòng khóa | Bằng độ dài bản rõ | 228 bit mỗi khung |

Cơ chế majority, cách quay và cách XOR tạo dòng khóa giống hệt nhau.

**Câu 7. A5/1 khởi tạo và sinh dòng khóa qua những giai đoạn nào?**

1. Xóa 3 thanh ghi về 0.
2. Nạp khóa 64 chu kỳ: cả 3 thanh ghi cùng quay (không dùng majority), bit khóa Ki được XOR vào bit mới ở vị trí 0.
3. Nạp số khung 22 chu kỳ, làm giống hệt bước 2 với bit khung Fj.
4. Warm-up 100 chu kỳ quay theo majority, bỏ toàn bộ bit ra.
5. Sinh 228 bit dòng khóa theo majority, chia 114 bit cho mỗi chiều truyền. Thứ tự nạp theo cài đặt tham chiếu của Briceno: khóa hex nạp từng byte, mỗi byte bit thấp trước; số khung cũng nạp bit thấp trước.

**Câu 8. Vì sao cần số khung và warm-up?**

Số khung giúp mỗi khung có dòng khóa khác nhau dù dùng chung khóa phiên. Thiếu nó thì mọi khung dùng lại cùng dòng khóa, chính là lỗi Two-Time Pad. Warm-up trộn trạng thái để bit ra đầu tiên không phụ thuộc trực tiếp, tuyến tính vào khóa và số khung.

## C. Mã hóa file và tấn công

**Câu 9. Chương trình mã hóa một file thật như thế nào?**

Mỗi khung cho 228 bit, hai khung cho 456 bit, đúng bằng 57 byte. File được chia thành đoạn 57 byte, đoạn thứ i dùng hai khung start\_frame + 2i và start\_frame + 2i + 1, rồi XOR với dữ liệu. File mã hóa có 4 byte đầu ghi start\_frame nên khi giải mã không phải nhập lại số khung. Mã hóa và giải mã dùng chung hàm crypt\_bytes vì (P ⊕ S) ⊕ S = P. Số khung dài 22 bit nên có tối đa 2^22 khung, đủ cho file khoảng 114 MiB nếu bắt đầu từ khung 0.

**Câu 10. Tấn công Two-Time Pad là gì, khai thác thế nào?**

Nếu P1, P2 mã bằng cùng dòng khóa S thì C1 ⊕ C2 = (P1 ⊕ S) ⊕ (P2 ⊕ S) = P1 ⊕ P2, dòng khóa bị triệt tiêu. Kẻ tấn công đoán một từ có trong P1 (crib), trượt nó qua từng vị trí của C1 ⊕ C2 và XOR. Vị trí nào ra chữ đọc được là lộ đoạn tương ứng của P2 (crib dragging). Biết cả P1 thì tính được S = C1 ⊕ P1 và đọc toàn bộ P2 = C2 ⊕ S.

**Câu 11. Trong demo, đổi khung thì kết quả ra rác. Vậy A5/1 an toàn không?**

Không. Đổi khung thì hai dòng khóa khác nhau, C1 ⊕ C2 = P1 ⊕ P2 ⊕ S1 ⊕ S2 không còn triệt tiêu, nên crib dragging thất bại. Demo chỉ chứng minh một điều: không được dùng lại cặp khóa và khung. A5/1 vẫn bị phá bằng các cách khác (câu 14).

## D. Kiểm thử và benchmark

**Câu 12. Làm sao biết chương trình chạy đúng?**

- TinyA5/1: test đối chiếu từng bước với ví dụ slide (s0, s1, s2 và X, Y, Z sau mỗi bước), test riêng cho điểm lệch Z, round-trip 111 → 011 → 111.
- A5/1: đối chiếu test vector chuẩn khóa 0x1223456789ABCDEF, khung 0x134 (cả hai chiều 114 bit); `python tests/run_verification.py` in bảng đối chiếu.
- Test tự viết: khóa ngắn, khung âm hoặc quá 2^22 báo lỗi; khóa toàn 0 và toàn 1; khóa lệch 1 bit làm trên 40% bit dòng khóa thay đổi; round-trip văn bản và file (0, 1, 56, 57, 58 byte, 10 KB); sai khóa; tấn công.
- Kết quả: ảnh pytest gần nhất trong repo (`Vu_final_D5`, ngày 23/10) ghi **50 passed**. Code trên main đã thêm 1 test sau đó, nên khi bảo vệ hãy nói đúng số trong ảnh B02 chụp trên bản nộp cuối.

**Câu 13. Benchmark đo thế nào, vì sao chậm?**

Đo crypt\_bytes trên dữ liệu ngẫu nhiên 1, 10, 50 và 100 KiB bằng time.perf\_counter, tốc độ = kích thước / 1024 / giây. Lần đo của nhóm (Windows, Python 3.15) cho tốc độ ổn định khoảng 63–64 KiB/s ở cả 4 mức; 100 KiB mất khoảng 1,58 giây. Chậm vì Python là ngôn ngữ thông dịch, mỗi chu kỳ quay là vài lời gọi hàm Python. Mỗi 57 byte cần 2 khung, mỗi khung 64 + 22 + 100 + 228 = 414 chu kỳ, tức 828 chu kỳ quay. Chương trình chỉ để học tập và minh họa; A5/1 thật chạy trên phần cứng.

## E. An toàn và phần mềm

**Câu 14. Vì sao A5/1 không còn an toàn? So với RC4 thì sao?**

Trạng thái chỉ 64 bit, và nhiều mạng đặt 10 bit khóa về 0 nên khóa hiệu dụng chỉ còn 54 bit. Các tấn công đánh đổi thời gian–bộ nhớ (Golic 1997; Biryukov, Shamir, Wagner 2000) và bảng cầu vồng (dự án Kraken, khoảng 2 TB) tìm lại được khóa trong vài giây. Mạng mới dùng A5/3 (KASUMI), rồi AES, SNOW 3G, ZUC ở 4G và 5G. RC4 cũng là mã dòng nhưng làm cho phần mềm (hoán vị 256 byte, khóa 40–2048 bit). RC4 yếu vì các byte đầu của dòng khóa bị thiên lệch (tấn công FMS vào WEP) và đã bị cấm trong TLS từ năm 2015.

**Câu 15. Phần mềm tổ chức thế nào, và phần em viết làm gì?**

- Lõi thuật toán trong `src/` viết bằng Python thuần, không dùng thư viện mật mã và không có `print()`, chỉ trả về dữ liệu. Giao diện (`gui/`, `demo_cli.py`) chỉ gọi lõi và hiển thị.
- `src/common.py`: đổi văn bản ↔ bit theo UTF-8 (mỗi byte 8 bit, bit cao trước), XOR hai chuỗi bit, kiểm tra chuỗi nhị phân hợp lệ.
- `tests/tests/test_tiny_a51.py` và `tests/tests/test_common.py`: test 3 bước ví dụ slide, điểm lệch Z, round-trip, khóa không hợp lệ và các hàm tiện ích.
- `gui/tab_file.py`: chọn file, nhập khóa hex 16 ký tự và số khung, mã hóa và giải mã, có thanh tiến trình và khung xem trước TXT/PNG. Việc mã hóa chạy trong luồng riêng (threading), kết quả gửi về qua hàng đợi (queue) và giao diện kiểm tra mỗi 100 ms bằng after(), nên cửa sổ không bị đơ.
- `gui/tab_attack.py`: nhập P1, P2 (có nút nạp file mẫu), ô “Dùng lại số khung”, hiện C1 ⊕ C2 dạng hex, báo hai dòng khóa TRÙNG hay KHÁC, và bảng dò crib (Vị trí, Đoạn chữ lộ ra, Điểm).
