# Bảng thuật ngữ kỹ thuật (Terminology)

Owner: Nguyễn Thị Nhật Linh · Nhánh: `docs/nhatlinh-standard`

## 1. Quy tắc dùng từ

- Trong văn bản kỹ thuật dùng **register** (hoặc "thanh ghi"); **LFSR** chỉ dùng khi nói về khái niệm tổng quát.
- Thao tác làm các bit chuyển sang vị trí kế bên gọi là **dịch** (shift). Slide gọi thao tác này là "quay" [Slide, trang 46–48]. Khi trích nguyên văn slide thì giữ chữ "quay"; mọi chỗ khác trong `docs/` viết "dịch".
- Không dùng "rotate" / "xoay vòng" cho TinyA5/1 và A5/1 (xem mục 3).
- Cột "Tài liệu tham khảo" dùng mã nguồn ở mục 4.

## 2. Bảng thuật ngữ

| Thuật ngữ (tiếng Anh) | Từ trong slide | Thuật ngữ kỹ thuật | Định nghĩa ngắn gọn | Vị trí trong slide Chương 2 | Tài liệu tham khảo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Register** | Thanh ghi | Thanh ghi (register, shift register) | Dãy ô nhớ, mỗi ô chứa 1 bit. TinyA5/1 có 3 register X, Y, Z dài 6, 8, 9 bit; A5/1 có R1, R2, R3 dài 19, 22, 23 bit. | Trang 46, 51 | [T1, Định nghĩa 6.7, trang 195]; [Slide] |
| **Shift** | Quay thanh ghi / Quy tắc quay | Dịch thanh ghi (shift) | Mỗi bit chuyển sang vị trí kế bên; bit ở đầu cuối bị đẩy ra và bỏ đi; vị trí trống nhận bit mới. Theo slide: xⱼ = xⱼ₋₁ (j từ chỉ số cao nhất xuống 1), rồi x₀ = t. | Trang 46, 47, 48, 51 | [T1, Định nghĩa 6.7, trang 195]; [T8]; [Slide] |
| **Rotate** | Không có | Dịch vòng (rotate, circular shift) | Bit bị đẩy ra ở một đầu được đưa lại vào đầu kia. **TinyA5/1 và A5/1 không dùng thao tác này.** | không áp dụng | [T7] |
| **Majority** | Hàm chiếm đa số | Hàm đa số (majority function) | maj(a, b, c) trả về giá trị xuất hiện ít nhất 2 lần trong 3 bit. Slide: có từ hai bit 0 trở lên thì trả về 0, ngược lại trả về 1. Ví dụ maj(0, 0, 1) = 0. | Trang 47, 51 | [Slide]; [T3] |
| **Clocking bit** | Slide không đặt tên riêng; slide viết "Nếu x₁ = m thì thực hiện Quay X" | Bit điều khiển nhịp (clocking bit) | Bit ở vị trí cố định của mỗi register, dùng để tính majority: x₁, y₃, z₃ (TinyA5/1); x8, y10, z10 (A5/1). Register nào có clocking bit bằng giá trị majority thì được dịch. | Trang 47, 51 | [Slide]; [T4, mục 2]; [T3] |
| **Feedback bit** | Bít t | Bit phản hồi (feedback bit) | Bit mới, bằng XOR các bit ở vị trí tap, được đưa vào vị trí 0 khi register dịch. Ví dụ X: t = x₂ ⊕ x₄ ⊕ x₅. | Trang 48, 51 | [T1, Định nghĩa 6.7, trang 195]; [Slide] |
| **Taps / Tapping positions** | Slide không đặt tên riêng (chỉ ghi công thức t) | Vị trí tap (taps) | Các vị trí bit được XOR để tạo feedback bit. TinyA5/1: X: x₂, x₄, x₅; Y: y₆, y₇; Z: z₂, z₇, z₈. A5/1: R1: 13, 16, 17, 18; R2: 20, 21; R3: 7, 20, 21, 22. | Trang 48, 51 | [Slide]; [T4, mục 2] |
| **Keystream** | Dãy số ngẫu nhiên S; "bít sinh ra" | Dòng khóa (keystream) | Dãy bit do bộ sinh số tạo ra từ khóa, đem XOR với bản rõ. Mỗi bước sinh 1 bit sᵢ. | Trang 42, 47, 51 | [T1, Định nghĩa 6.2, trang 192]; [Slide] |
| **State** | Không có tên riêng (slide ghi nội dung X, Y, Z sau mỗi bước) | Trạng thái (state) | Toàn bộ nội dung các register tại một thời điểm. Trạng thái thay đổi sau mỗi bước. | Trang 49, 50 | [T1, Định nghĩa 6.2, trang 192] |
| **Step / Clock cycle** | Bước; "bước sinh số thứ i" | Bước / chu kỳ nhịp (step, clock cycle) | Một lần: tính majority, dịch các register có clocking bit bằng majority (2 hoặc 3 register), rồi sinh 1 bit keystream. | Trang 47, 49, 50 | [Slide]; [T4, mục 2] |
| **Plaintext** | Văn bản rõ; Bản rõ | Bản rõ (plaintext) | Dữ liệu đọc hiểu được, chưa mã hóa; là đầu vào của quá trình mã hóa. | Trang 6, 7, 42 | [T6]; [Slide] |
| **Ciphertext** | Văn bản mã hoá; Bản mã | Bản mã (ciphertext) | Dữ liệu ở dạng đã mã hóa. Với mã dòng: cᵢ = pᵢ ⊕ sᵢ. | Trang 6, 7, 42, 47 | [T6]; [Slide] |
| **Encryption / Decryption** | Mã hoá / Giải mã | Mã hóa / Giải mã | Biến bản rõ thành bản mã và ngược lại. Với mã dòng, cả hai chiều đều XOR với cùng keystream. | Trang 8, 42, 43, 50 | [Slide] |
| **Stream cipher** | Mã dòng; Mã hoá dòng | Mã dòng (stream cipher) | Hệ mã mã hóa từng bit hoặc từng đơn vị nhỏ, bằng cách XOR với keystream; phép biến đổi thay đổi theo thời gian. | Trang 15, 39, 42 | [T1, trang 191]; [Slide] |
| **LFSR** | Slide không dùng từ này | Thanh ghi dịch phản hồi tuyến tính (linear feedback shift register) | Register mà bit phản hồi là XOR của một số vị trí cố định. Ba register của A5/1 là ba LFSR. | không áp dụng | [T1, Định nghĩa 6.7, trang 195]; [T3] |
| **Frame number** | Slide không đề cập | Số khung (frame number, COUNT) | Số thứ tự khung TDMA trong GSM, công khai, dài 22 bit; nạp vào A5/1 cùng khóa để mỗi khung có keystream riêng. | không áp dụng (slide thiếu bước này) | [T5, Annex C.1.2]; [T3] |
| **Initialization vector (IV)** | Slide không đề cập | Véc-tơ khởi tạo (IV) | Giá trị công khai đưa vào cùng khóa khi khởi tạo. Trong A5/1, vai trò này do frame number 22 bit đảm nhận. | không áp dụng | [T4, mục 2] |
| **Warm-up** | Slide không đề cập | Giai đoạn khởi động (warm-up, mixing) | Sau khi nạp key (64 chu kỳ) và frame (22 chu kỳ), chạy 100 chu kỳ dịch theo majority và bỏ đầu ra; sau đó mới sinh keystream thật. | không áp dụng (slide thiếu bước này) | [T3]; [T4, mục 2]; [T2] |
| **Test vector** | Slide không đề cập | Dữ liệu kiểm thử chuẩn (test vector) | Bộ dữ liệu mẫu gồm khóa, frame và keystream mong đợi, dùng để kiểm tra cài đặt có đúng không. | không áp dụng | [T2] |

## 3. Chỗ slide dùng thuật ngữ chưa chuẩn (ghi cho Hà Linh)

1. **"Quay" thực chất là dịch (shift), không phải xoay vòng (rotate).** Slide ghi xⱼ = xⱼ₋₁ rồi x₀ = t [Slide, trang 48]: bit cuối x₅ bị đẩy ra và bỏ đi, bit mới t là feedback chứ không phải bit vừa bị đẩy ra. Rotate thì bit bị đẩy ra được đưa lại vào đầu kia [T7]. Vì vậy nhóm dùng "dịch".
2. **"Dãy số ngẫu nhiên S" thực chất là dãy giả ngẫu nhiên.** Keystream được sinh hoàn toàn xác định từ khóa (cùng khóa cho cùng keystream) [T1, Định nghĩa 6.2, trang 192], nên thuật ngữ chính xác là "giả ngẫu nhiên" (pseudorandom) [T9].
3. **Slide trang 51 vẫn gọi ba register của A5/1 là X, Y, Z**, còn `style_guide.md` quy định R1, R2, R3. Đây không phải lỗi; chỉ cần khi trích slide thì giữ X, Y, Z và ghi rõ X ↔ R1, Y ↔ R2, Z ↔ R3.

## 4. Nguồn tham khảo

| Mã | Tài liệu | Link |
| :--- | :--- | :--- |
| Slide | ThS. Nguyễn Quốc Thái, Bài giảng An toàn và bảo mật thông tin, Chương 2 (bản "Updated") | Nguồn nội bộ |
| T1 | Menezes, van Oorschot, Vanstone, *Handbook of Applied Cryptography*, Chương 6 (1996) | https://cacr.uwaterloo.ca/hac/about/chap6.pdf |
| T2 | Briceno, Goldberg, Wagner, *A pedagogical implementation of A5/1* (1998–1999), có test vector | https://mtlin.org/article/a51.html |
| T3 | Wikipedia, "A5/1" | https://en.wikipedia.org/wiki/A5/1 |
| T4 | Shah, Mahalanobis, *A New Guess-and-Determine Attack on the A5/1 Stream Cipher* (2012) | https://arxiv.org/abs/1204.4535 |
| T5 | ETSI TS 143 020 V7.0.0 (2007), *Security-related network functions* | https://www.etsi.org/deliver/etsi_ts/143000_143099/143020/07.00.00_60/ts_143020v070000p.pdf |
| T6 | NIST CSRC Glossary, "plaintext" và "ciphertext" | https://csrc.nist.gov/glossary/term/plaintext ; https://csrc.nist.gov/glossary/term/ciphertext |
| T7 | Wikipedia, "Circular shift" | https://en.wikipedia.org/wiki/Circular_shift |
| T8 | Wikipedia, "Logical shift" | https://en.wikipedia.org/wiki/Logical_shift |
| T9 | Wikipedia, "Stream cipher" | https://en.wikipedia.org/wiki/Stream_cipher |

Các nguồn có trong bảng nháp nhưng đã **bỏ** vì không khớp nội dung hoặc chưa đọc được: IEEE 1364 (chuẩn ngôn ngữ Verilog, không phải mật mã), IEEE 1363 (chuẩn mật mã khóa công khai, không liên quan A5/1), Wikipedia "Barrel shifter" (mạch phần cứng), Schneier *Applied Cryptography* và Golić (1997) (chưa đọc được bản gốc để dẫn trang).
