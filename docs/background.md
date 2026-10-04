# Background — A5/1 và TinyA5/1

Owner: Hoàng Yến Nhi · Nhánh: `docs/nhi-research`
Mục đích: nền cho chương "Cơ sở lý thuyết" của báo cáo. Mọi số `[n]` trỏ tới `docs/references.md`.
Quy ước viết: TinyA5/1 dùng register X, Y, Z; A5/1 dùng R1, R2, R3 (theo `style_guide.md`). Khi trích công thức của slide, giữ nguyên ký hiệu slide (x, y, z).
Thuật ngữ (theo `terminology.md`): slide gọi thao tác dịch bit của thanh ghi là "quay"; thuật ngữ kỹ thuật là "dịch thanh ghi" (shift). File này dùng thống nhất từ **dịch**. "Register được clock" ở một chu kỳ nghĩa là register đó được dịch một bước ở chu kỳ đó.

## 1. GSM context

GSM là chuẩn điện thoại di động thế hệ 2 (2G). Trên đường truyền vô tuyến, GSM mã hóa dữ liệu bằng một họ thuật toán gọi là A5. Đặc tả bảo mật của ETSI/3GPP định nghĩa A5 như một "hộp đen" có hai đầu vào. Đầu vào thứ nhất là khóa mã Kc dài 64 bit. Đầu vào thứ hai là COUNT dài 22 bit, được tính từ số khung TDMA (frame number). Đầu ra gồm hai khối BLOCK1 và BLOCK2, mỗi khối 114 bit, và phải được sinh ra trong thời gian ngắn hơn một khung TDMA (4,615 ms) [1, Annex C.1.2–C.1.3]. Khóa Kc không truyền qua mạng mà được sinh từ khóa bí mật Ki trong SIM và số ngẫu nhiên RAND bằng thuật toán A8. Việc xác thực thuê bao dùng thuật toán A3 để tính SRES [1].

Slide giới thiệu A5/1 là hệ mã dùng trong mạng điện thoại GSM để bảo mật dữ liệu giữa máy điện thoại và trạm thu phát sóng vô tuyến, với đơn vị mã hoá là 1 bit [Slide, trang 45]. A5/1 là thành viên "mạnh" của họ A5, được phát triển năm 1987 [6]. Bản A5/2 ra đời năm 1989 và bị làm yếu có chủ đích để dùng ở các vùng xuất khẩu [6]. Đến năm 2000, A5/1 bảo vệ khoảng 130 triệu thuê bao GSM ở châu Âu [3]. Phiên bản đặc tả năm 2007 của ETSI quy định máy di động bắt buộc phải hỗ trợ A5/1 và A5/3, đồng thời cấm cài đặt A5/2 [1, mục 4.9]. Cấu trúc bên trong của A5 không được công bố trong chuẩn. ETSI ghi rằng đặc tả nội bộ do GSM/MoU quản lý và chỉ cung cấp khi có yêu cầu phù hợp [1, mục C.1.4]. Vì vậy, các mô tả A5/1 dùng trong đồ án đến từ nguồn dịch ngược công khai (mục 5), không phải từ tài liệu chuẩn.

## 2. Stream cipher

### 2.1. Các khái niệm cơ bản

- **Plaintext (bản rõ):** dữ liệu gốc cần mã hóa. Trong mã dòng, bản rõ P được chia thành các đơn vị mã hoá k bit: P = p₀p₁…pₙ₋₁ [Slide, trang 42].
- **Keystream (dòng khóa):** dãy bit do bộ sinh số tạo ra từ khóa K, có cùng kích thước với bản rõ. Slide gọi là "dãy số ngẫu nhiên" S = s₀s₁…sₙ₋₁ [Slide, trang 42]. Trong mã dòng đồng bộ, keystream được sinh độc lập với bản rõ và bản mã [5, Định nghĩa 6.2, trang 192][9].
- **Ciphertext (bản mã):** dữ liệu ở dạng đã mã hóa [13]. Trong mã dòng, mỗi đơn vị bản mã là cᵢ = pᵢ ⊕ sᵢ [Slide, trang 42].
- **XOR (⊕):** phép toán trên hai bit, cho kết quả `1` khi hai bit khác nhau và `0` khi hai bit giống nhau [12]:

| a | b | a ⊕ b |
|---|---|---|
| `0` | `0` | `0` |
| `0` | `1` | `1` |
| `1` | `0` | `1` |
| `1` | `1` | `0` |

XOR có tính tự nghịch đảo: XOR hai lần với cùng một giá trị thì trả lại giá trị ban đầu, tức (p ⊕ s) ⊕ s = p [12]. Nhờ tính chất này, bên nhận chỉ cần XOR bản mã với đúng keystream đã dùng là lấy lại được bản rõ.

### 2.2. Mô hình mã hóa và giải mã

```
                      Khóa K
                        │
                        ▼
              ┌───────────────────┐
              │ Bộ sinh keystream │
              └───────────────────┘
                        │  S = s₀ s₁ … sₙ₋₁
                        ▼
MÃ HÓA:   Bản rõ P ───▶ ⊕ ───▶ Bản mã C        cᵢ = pᵢ ⊕ sᵢ   [Slide, trang 42]

GIẢI MÃ:  Bản mã C ───▶ ⊕ ───▶ Bản rõ P        pᵢ = cᵢ ⊕ sᵢ   [Slide, trang 43]
                        ▲
                        │  cùng dãy S
```

Ví dụ trên slide (đơn vị mã hoá k = 4 bit) [Slide, trang 44]:

- Mã hóa: p₀ = `1111`, s₀ = `0101` → c₀ = `1111` ⊕ `0101` = `1010`
- Giải mã: c₀ = `1010`, s₀ = `0101` → p₀ = `1010` ⊕ `0101` = `1111` (khớp bản rõ ban đầu)

### 2.3. Vị trí của A5/1

- Slide xếp mã dòng (A5/1, RC4) và mã khối (DES, AES) vào nhóm mã hoá hiện đại, biểu diễn dữ liệu bằng giá trị nhị phân [Slide, trang 15].
- A5/1 là **synchronous stream cipher**: keystream sinh ra độc lập với bản rõ và bản mã [5, Định nghĩa 6.2, trang 192].
- A5/1 cũng là **binary additive stream cipher**: keystream, bản rõ và bản mã đều là bit, phép kết hợp là XOR [5, Định nghĩa 6.4, trang 194]. Đơn vị mã hoá của A5/1 là 1 bit [Slide, trang 45].

### 2.4. So sánh stream cipher và block cipher

| Tiêu chí | Stream cipher | Block cipher |
|---|---|---|
| Nguyên lý | Sinh keystream rồi XOR từng bit hoặc từng ký tự với bản rõ; phép biến đổi thay đổi theo thời gian [5, trang 191][9] | Chia dữ liệu thành các khối có độ dài cố định; mỗi khối được mã bằng cùng một phép biến đổi với cùng khóa [5, trang 191][10][13] |
| Ưu điểm | Thường nhanh hơn và mạch phần cứng đơn giản hơn [5, trang 191][9]; hợp khi không biết trước độ dài dữ liệu (ví dụ kết nối không dây) vì không cần đệm thêm dữ liệu [9]; lỗi truyền ở một bit không lan sang bit khác [5, Ghi chú 6.3, trang 193][9] | Đa dụng: ngoài mã hóa còn là "khối xây dựng" cho bộ sinh số giả ngẫu nhiên, mã dòng, MAC và hàm băm [11, trang 223][10] |
| Nhược điểm | Bên gửi và bên nhận phải đồng bộ (cùng khóa, cùng vị trí trạng thái) [5, Ghi chú 6.3, trang 193]; không được dùng lại cùng một keystream hai lần [9] | Dữ liệu dài hơn một khối phải dùng chế độ hoạt động (ECB, CBC, CTR…) và phải đệm (padding) khi không chia hết cho kích thước khối [10]; ở chế độ ECB, các khối bản rõ giống nhau cho ra khối bản mã giống nhau, làm lộ mẫu dữ liệu [11, trang 228]; ở chế độ CBC, lỗi 1 bit trong bản mã làm hỏng 2 khối khi giải mã [11, trang 230] |
| Ví dụ trong môn học | A5/1, RC4 [Slide, trang 15] | DES, AES [Slide, trang 15] |

Ưu điểm "lỗi không lan" và "xử lý từng bit, không cần đệm" phù hợp với kênh vô tuyến của GSM, nơi mỗi khung chỉ mang 114 bit dữ liệu [1, C.1.3].

## 3. LFSR

LFSR (linear feedback shift register) gồm L ô nhớ, mỗi ô chứa một bit. Ở mỗi nhịp clock, các bit dịch đi một vị trí. Bit mới (bit phản hồi, feedback bit) bằng tổng modulo 2 (XOR) của một tập vị trí cố định gọi là taps [5, Định nghĩa 6.7, trang 195]. Tập taps tương ứng với một đa thức kết nối (connection polynomial) [5, Định nghĩa 6.8, trang 196]. LFSR rất hợp với cài đặt phần cứng và cho dãy bit có tính chất thống kê tốt [5, trang 195]. Điểm yếu là đầu ra của một LFSR đơn lẻ dễ dự đoán. Thuật toán Berlekamp–Massey có thể tìm lại LFSR từ một đoạn đầu ra ngắn, chỉ cần dài ít nhất gấp đôi độ dài LFSR [5, trang 200 và 204]. Vì vậy, LFSR thường phải kết hợp với một thành phần phi tuyến.

A5/1 dùng ba LFSR làm ba register R1, R2, R3 có độ dài 19, 22 và 23 bit, tổng cộng 64 bit trạng thái [2][4][6][Slide, trang 51]. Slide cũng nhận xét A5/1 "được thực hiện dễ dàng bằng các thiết bị phần cứng, tốc độ nhanh" [Slide, trang 51], khớp với nhận định chung về LFSR của [5]. Lưu ý về quy ước: [5] mô tả LFSR dịch về phía ô 0 và lấy output ở ô 0. Slide và [2] mô tả theo chiều ngược lại: bit mới vào vị trí 0, output lấy ở bit chỉ số cao [Slide, trang 47–48][2]. Đây chỉ là khác biệt về cách trình bày. Đồ án theo quy ước của slide.

## 4. Majority clocking

Để phá tính tuyến tính của LFSR, A5/1 không cho cả ba register dịch đều mỗi nhịp. Thay vào đó nó dùng clock không đều, một dạng của clock-controlled generator. Ý tưởng chung của loại bộ sinh này là khi một register dịch không đều, các tấn công dựa trên chuyển động đều của LFSR sẽ khó thực hiện hơn [5, mục 6.3.3, trang 209]. Mỗi register có một clocking bit: bit 8 của R1, bit 10 của R2 và bit 10 của R3 [2][4]. Ở mỗi chu kỳ, ta tính giá trị đa số (majority) của ba clocking bit. Register nào có clocking bit bằng giá trị đa số thì được dịch, các register còn lại đứng yên [6].

Quy tắc này dẫn tới hai hệ quả. Mỗi chu kỳ luôn có 2 hoặc 3 register được dịch, và mỗi register được dịch với xác suất 3/4 [4, mục 2]. TinyA5/1 trên slide dùng đúng cơ chế này với clocking bit x₁, y₃, z₃. Hàm maj trả về 0 nếu có từ hai bit 0 trở lên, ngược lại trả về 1 [Slide, trang 47].

## 5. A5/1

Theo các nguồn dịch ngược, A5/1 gồm ba register:

| Register | Độ dài | Clocking bit | Feedback taps | Bit output |
|---|---|---|---|---|
| R1 | 19 bit | 8 | 13, 16, 17, 18 | 18 |
| R2 | 22 bit | 10 | 20, 21 | 21 |
| R3 | 23 bit | 10 | 7, 20, 21, 22 | 22 |

Nguồn: [2][4]; taps và clocking bit khớp với [6]. Mỗi bit keystream là R1[18] ⊕ R2[21] ⊕ R3[22] [4, mục 2, công thức (1)], tức XOR các bit cao nhất của ba register, lấy sau khi dịch [2]. Slide ghi "sau khi quay bít xong thì bít sinh ra: sᵢ = x8 ⊕ y10 ⊕ z10" [Slide, trang 51], khác với nguồn ngoài. Chỗ lệch này được ghi thành CONFLICT-001 trong `references.md` và chuyển cho người chốt TD-001.

Quá trình khởi tạo cho mỗi khung như sau. Đầu tiên nạp 64 bit khóa trong 64 chu kỳ, rồi nạp 22 bit số khung trong 22 chu kỳ. Ở hai giai đoạn này cả ba register đều được dịch, không dùng majority. Tiếp theo chạy 100 chu kỳ theo majority và bỏ đầu ra (warm-up). Cuối cùng sinh 228 bit keystream: 114 bit đầu cho chiều xuống (downlink), 114 bit sau cho chiều lên (uplink) [2][4][6]. Con số 2 × 114 bit khớp với BLOCK1 và BLOCK2 trong chuẩn ETSI [1, C.1.3]. Slide không mô tả giai đoạn nạp key, nạp frame và warm-up.

Về lịch sử, thiết kế chung của A5/1 bị lộ năm 1994 và được dịch ngược hoàn toàn năm 1999 [6]. Bản cài đặt C của Briceno, Goldberg và Wagner (1998–1999) được các tác giả xác nhận là khớp với test vector chính thức [2]. Về độ an toàn, A5/1 đã bị tấn công nhiều lần. Golić (1997) đưa ra tấn công có độ phức tạp thời gian 2^40.16 [6]. Biryukov, Shamir và Wagner (2000) dùng time-memory tradeoff: sau một giai đoạn tiền xử lý 2^48 bước, khóa có thể tìm được trong thời gian thực trên một PC [3]. Barkan, Biham và Keller (2003) công bố các tấn công chỉ cần bản mã trên GSM [6]. Năm 2009, dự án của Karsten Nohl công bố cách xây bảng cầu vồng (rainbow tables) để phá A5/1 [6]. Ngoài ra, một số triển khai cũ cố định 10 bit khóa bằng 0, khiến khóa hiệu dụng chỉ còn 54 bit [6]. Phần phân tích an toàn chi tiết sẽ được viết ở giai đoạn sau, và nên đọc trực tiếp các bài gốc (xem `references.md` mục 2).

## 6. TinyA5/1

TinyA5/1 là phiên bản thu nhỏ của A5/1 dùng trong bài giảng. Bộ sinh số có ba register X, Y, Z dài 6, 8 và 9 bit (x₀…x₅, y₀…y₇, z₀…z₈). Khóa K dài 23 bit được phân bổ vào các register theo K → XYZ [Slide, trang 46]. Thuật toán giữ nguyên ý tưởng của A5/1. Ở mỗi bước, ta tính m = maj(x₁, y₃, z₃). Register nào có clocking bit bằng m thì được dịch (slide gọi là "quay"). Sau đó tính sᵢ = x₅ ⊕ y₇ ⊕ z₈, và bản mã là C = P XOR S [Slide, trang 47]. Khi dịch, bit phản hồi t được tính bằng XOR các bit quy định (ví dụ t = x₂ ⊕ x₄ ⊕ x₅), các bit dịch từ chỉ số thấp sang cao và t vào vị trí 0 [Slide, trang 48]. Slide trang 45 nói rõ bài học chỉ "giới hạn xét mô hình thu nhỏ của A5/1, gọi tắt là TinyA5/1" [Slide, trang 45]. Khác với A5/1 đầy đủ, slide nạp khóa trực tiếp vào register và không có bước nạp frame hay warm-up [Slide, trang 46–47].

**Vì sao đồ án có TinyA5/1?**

TinyA5/1 chỉ có 23 bit trạng thái nên đủ nhỏ để tính tay. Nhờ vậy nhóm có thể:

- Kiểm tra logic từng bước: majority, bit phản hồi, keystream.
- Đối chiếu kết quả với ví dụ tính tay trên slide [Slide, trang 49–50].
- Đáp ứng căn cứ chấm đầu tiên của đề bài: phiên bản thu nhỏ phải tái hiện đúng ví dụ trên lớp [8, mục 2]. TinyA5/1 và A5/1 hoạt động theo cùng nguyên tắc [Slide, trang 51], nên nếu TinyA5/1 sai thì A5/1 cũng sẽ sai.
- Sau khi nắm chắc cơ chế, mở rộng sang A5/1 (64 bit trạng thái), phiên bản không thể tính tay được nữa.
