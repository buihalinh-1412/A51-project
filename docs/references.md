# References — A5/1 Project (Giai đoạn 1)

Owner: Hoàng Yến Nhi · Nhánh: `docs/nhi-research`

Quy ước trích dẫn: trong các file docs/, ghi `[n, trang x]` hoặc `[n, mục x]` trỏ tới số thứ tự bên dưới. Slide môn học ghi `[Slide, trang x]`.
Ngày truy cập các nguồn trực tuyến: 02/10/2026.

## 1. Danh sách nguồn

[Slide] Bài giảng An toàn và bảo mật thông tin — Chương 2: Mã hoá khoá đối xứng (Mã hoá khoá bí mật), bản "Updated"
Author/Organization: ThS. Nguyễn Quốc Thái, Khoa Công nghệ thông tin, Đại học Kinh tế Quốc dân
Year: 2026
Link: Nguồn nội bộ (thư mục "2026.1 - ATBMTT - Slide bài giảng" trên Google Drive của môn học)
Used for: Phân loại mã dòng/mã khối (background.md mục 2, trang 15); mô hình mã hóa và giải mã mã dòng (mục 2, trang 42–44); giới thiệu A5/1 trong GSM (mục 1, trang 45); đặc tả TinyA5/1 (mục 4 và 6, trang 46–50); thông số A5/1 theo slide trong Ma trận nguồn (cột Slide, trang 51).
Ghi chú: đã đối chiếu trực tiếp trên file PDF các trang 15, 42–52 (ngày 02/10/2026). Số trang theo bản "Updated" (89 trang). Bản cũ (82 trang) lệch 7 trang ở phần mã dòng (ví dụ TinyA5/1 là trang 39 thay vì 46; trang 15 thành trang 14). Cả nhóm nên thống nhất dùng bản "Updated".

[1] ETSI TS 143 020 V7.0.0 (2007-06) — Digital cellular telecommunications system (Phase 2+); Security-related network functions (3GPP TS 43.020)
Author/Organization: ETSI / 3GPP
Year: 2007
Link: https://www.etsi.org/deliver/etsi_ts/143000_143099/143020/07.00.00_60/ts_143020v070000p.pdf
Used for: Bối cảnh GSM (background.md mục 1): khóa Kc 64 bit, COUNT 22 bit lấy từ số khung TDMA, BLOCK1/BLOCK2 mỗi khối 114 bit, thời gian 4,615 ms [Annex C, mục C.1.2–C.1.4]; Kc sinh bằng A8 từ Ki và RAND; A3/SRES; A5/1 bắt buộc, cấm A5/2 trên máy di động [mục 4.9]. Đây là nguồn chuẩn chính thức duy nhất trong danh sách, nhưng **không** mô tả cấu trúc bên trong A5 (mục C.1.4 nói đặc tả nội bộ do GSM/MoU quản lý).

[2] A pedagogical implementation of A5/1 (mã nguồn C)
Author/Organization: Marc Briceno, Ian Goldberg, David Wagner
Year: 1998–1999
Link: https://mtlin.org/article/a51.html (bản sao); bản A5/1 + A5/2 cùng nhóm tác giả: https://cryptome.org/gsm-a512.htm
Used for: Ma trận nguồn (Nguồn 1): độ dài R1/R2/R3, clocking bit, feedback taps, bit output (bit cao nhất), nạp key 64 chu kỳ + frame 22 chu kỳ, 100 chu kỳ trộn, 228 bit keystream, test vector. Background mục 5 (lịch sử dịch ngược). Header ghi bản cài đặt "has been verified against official A5/1 test vectors".

[3] Real Time Cryptanalysis of A5/1 on a PC
Author/Organization: Alex Biryukov, Adi Shamir, David Wagner
Year: 2000 (hội nghị FSE 2000; in trong LNCS 1978, Springer, 2001, trang 1–18)
Link: https://doi.org/10.1007/3-540-44706-7_1
Used for: Background mục 1 và 5: A5/1 bảo vệ khoảng 130 triệu thuê bao GSM ở châu Âu (thời điểm năm 2000); các tấn công trước đó cần 2^40–2^45 bước; tấn công time-memory tradeoff (tiền xử lý 2^48 bước, sau đó phá khóa thời gian thực trên một PC). Report outline: chương phân tích an toàn.
Ghi chú: mới đọc phần Abstract trên Springer, chưa đọc toàn văn.

[4] A New Guess-and-Determine Attack on the A5/1 Stream Cipher
Author/Organization: Jay Shah, Ayan Mahalanobis
Year: 2012
Link: https://arxiv.org/abs/1204.4535
Used for: Ma trận nguồn (Nguồn 2): R1/R2/R3 = 19/22/23, taps, clocking bit 8/10/10, công thức output R1[18]⊕R2[21]⊕R3[22] [mục 2, công thức (1)]; 86 chu kỳ (64 + 22) + 100 chu kỳ warm-up, 228 bit. Background mục 4: mỗi chu kỳ có 2 hoặc 3 register được clock, mỗi register di chuyển với xác suất 3/4 [mục 2]. Danh sách các tấn công trước (Anderson 1994, Golić 1997...).

[5] Handbook of Applied Cryptography, Chapter 6: Stream Ciphers
Author/Organization: Alfred J. Menezes, Paul C. van Oorschot, Scott A. Vanstone (CRC Press)
Year: 1996
Link: https://cacr.uwaterloo.ca/hac/about/chap6.pdf
Used for: Background mục 2 (định nghĩa stream cipher và so sánh với block cipher, trang 191; synchronous stream cipher, Định nghĩa 6.2, trang 192; binary additive stream cipher, Định nghĩa 6.4, trang 194; yêu cầu đồng bộ, không lan truyền lỗi, Ghi chú 6.3, trang 193). Mục 3 (LFSR, Định nghĩa 6.7, trang 195; connection polynomial, Định nghĩa 6.8, trang 196; LFSR dễ dự đoán, Berlekamp–Massey, trang 200 và 204). Mục 4 (clock-controlled generator, mục 6.3.3, trang 209).

[6] A5/1 — Wikipedia
Author/Organization: Wikipedia contributors
Year: truy cập 02/10/2026
Link: https://en.wikipedia.org/wiki/A5/1
Used for: Nguồn tổng hợp (không dùng làm nguồn duy nhất). Ma trận nguồn (Nguồn 3). Background mục 1 và 5: A5/1 phát triển năm 1987, A5/2 năm 1989 là bản làm yếu để xuất khẩu, thiết kế lộ năm 1994, dịch ngược hoàn toàn năm 1999; các tấn công Golić 1997, Barkan–Biham–Keller 2003, Ekdahl–Johansson 2003, dự án bảng cầu vồng của Karsten Nohl công bố năm 2009; 10 bit khóa bị cố định bằng 0 trong một số triển khai cũ (khóa hiệu dụng 54 bit). Quy ước "bit 0 là LSB".

[7] A5/1 stream cipher — asecuritysite.com
Author/Organization: Bill Buchanan (asecuritysite.com)
Year: truy cập 02/10/2026
Link: https://asecuritysite.com/symmetric/a5
Used for: Đối chiếu test vector (key 0x1223456789ABCDEF, frame 0x134) trong Ma trận nguồn. Trang ghi mã nguồn lấy từ scard.org, tức là cùng gốc với [2], nên **không tính là nguồn độc lập**.

[8] Hướng dẫn làm bài tập nhóm — An toàn và bảo mật thông tin (file "HD BTN TMDT CLC - C")
Author/Organization: Giảng viên môn học
Year: 2026
Link: https://docs.google.com/document/d/14vEU_3kHQfJmn0Tc6gY6WPPD9ZLRw0Fb62W0fCRP-mA
Used for: Bảng "Yêu cầu đề bài và chương đáp ứng" trong report_outline.md (mục 2 của đề bài: phần "Tìm hiểu hệ mã" và phần "Báo cáo").

## 2. Nguồn nên đọc thêm (chưa đọc trực tiếp, chưa được trích)

Các nguồn dưới đây chưa mở được toàn văn ngày 02/10/2026 (máy chủ giới hạn truy cập hoặc chặn bot). Chưa dùng cho bất kỳ câu nào trong background.md.

- E. Barkan, E. Biham, N. Keller, "Instant Ciphertext-Only Cryptanalysis of GSM Encrypted Communication", CRYPTO 2003, LNCS 2729. https://doi.org/10.1007/978-3-540-45146-4_35 → dùng cho chương phân tích an toàn.
- T. Gendrullis, M. Novotný, A. Rupp, "A Real-World Attack Breaking A5/1 within Hours", CHES 2008. https://eprint.iacr.org/2008/147.pdf → dùng cho chương phân tích an toàn (chi phí phần cứng).
- J. Golić, "Cryptanalysis of Alleged A5 Stream Cipher", EUROCRYPT 1997 → nguồn gốc của các con số tấn công năm 1997.

## 3. Ma trận nguồn

Nguồn 1 = [2] Briceno–Goldberg–Wagner · Nguồn 2 = [4] Shah–Mahalanobis · Nguồn 3 = [6] Wikipedia.
Cột Slide đã đối chiếu trực tiếp với slide gốc (bản "Updated").

| Thông số | Slide | Nguồn 1 [2] | Nguồn 2 [4] | Nguồn 3 [6] | Kết luận (khớp/khác) |
|---|---|---|---|---|---|
| Độ dài R1, R2, R3 | 19, 22, 23 bít ("thanh ghi X, Y, Z") [Slide, trang 51] | 19, 22, 23 bit (`R1MASK` đến `R3MASK`) | 19, 22, 23 bit [mục 2] | 19, 22, 23 bit | **Khớp**, VERIFIED |
| Feedback taps | X: 13, 16, 17, 18; Y: 20, 21; Z: 7, 20, 21, 22 [Slide, trang 51] | R1: 18, 17, 16, 13; R2: 21, 20; R3: 22, 21, 20, 7 | R1: 13, 16, 17, 18; R2: 20, 21; R3: 7, 20, 21, 22 [mục 2] | R1: 13, 16, 17, 18; R2: 20, 21; R3: 7, 20, 21, 22 | **Khớp**, VERIFIED |
| Clocking bit | m = maj(x8, y10, z10) [Slide, trang 51] | R1: bit 8; R2: bit 10; R3: bit 10 | R1: 8; R2: 10; R3: 10 [mục 2] | R1: 8; R2: 10; R3: 10 | **Khớp**, VERIFIED |
| Bit output | "Sau khi quay bít xong thì bít sinh ra: sᵢ = x8 ⊕ y10 ⊕ z10" [Slide, trang 51] | bit 18 ⊕ bit 21 ⊕ bit 22 ("the high bit"), lấy sau khi clock | R1[18] ⊕ R2[21] ⊕ R3[22] [mục 2, công thức (1)] | chưa có (phần đã đọc không nêu) | **Khác**, CONFLICT (xem CONFLICT-001). Ba nguồn ngoài thống nhất bit cao nhất; slide trùng với vị trí clocking bit |
| Số chu kỳ nạp key, frame, warm-up | Slide không có | 64 (key) + 22 (frame), không dùng majority; sau đó 100 chu kỳ majority, bỏ output | 64 + 22 = 86 chu kỳ, sau đó 100 chu kỳ warm-up [mục 2] | 64 + 22, sau đó 100 chu kỳ majority, bỏ output | **Khớp giữa các nguồn ngoài**, VERIFIED. Slide thiếu. Độ dài key 64 bit và frame 22 bit được [1] xác nhận [Annex C.1.2] |
| Test vector | Slide không có | Key `12 23 45 67 89 AB CD EF`, frame `0x134`; A→B `534EAA582FE8151AB6E1855A728C00`; B→A `24FD35A35D5FB6526D32F906DF1AC0` | Không có | chưa có (phần đã đọc không nêu) | **SINGLE-SOURCE**. [7] cho cùng giá trị nhưng lấy mã từ cùng gốc với [2]. Cần kiểm chứng bằng cài đặt ở GĐ3 |

Ghi chú thêm cho người chốt TD-003 (thứ tự bit), chỉ ghi nhận, không tự chốt:
- [6] ghi quy ước "bit 0 là LSB". [2] đánh số bit 0..18, bit 18 là "high bit".
- Trong mã của [2], bit key thứ i lấy bằng `(key[i/8] >> (i&7)) & 1`, tức là đọc từng byte từ bit thấp đến bit cao. Bit keystream được ghép vào byte đầu ra từ bit cao xuống (`<< (7-(i&7))`).
- [5] định nghĩa LFSR dịch về phía stage 0 và lấy output ở stage 0 [trang 195]. Hướng này ngược với cách slide và [2] mô tả A5/1 (bit mới vào vị trí 0). Đây là khác biệt **quy ước trình bày**, không phải mâu thuẫn thông số.

## 4. Ghi nhận chỗ lệch

```
CONFLICT-001
Issue:            Vị trí bit output của A5/1 đầy đủ (Ma trận nguồn, dòng "Bit output").
Lecture/Slide:    sᵢ = x8 ⊕ y10 ⊕ z10, tính sau khi quay [Slide, trang 51; trang 52 lặp lại y hệt]. Đã xác nhận trên trang gốc dạng hình.
External source:  bit 18 ⊕ bit 21 ⊕ bit 22, tức bit cao nhất của mỗi register [2]; R1[18] ⊕ R2[21] ⊕ R3[22] [4, mục 2, công thức (1)].
Possible reason:  Slide có thể chép nhầm vị trí clocking bit (8, 10, 10) sang công thức output. TinyA5/1 trên slide lấy output ở bit cuối (x5, y7, z8), cùng kiểu với nguồn ngoài.
Impact:           Có. Keystream khác thì ciphertext khác, và cài đặt sẽ không khớp test vector của [2].
Status:           OPEN
```
