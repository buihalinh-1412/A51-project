# Cơ sở lý thuyết (Background) — A5/1 và TinyA5/1

Owner: Hoàng Yến Nhi · Nhánh: `docs/nhi-research`
Mục đích: nền cho chương "Cơ sở lý thuyết" của báo cáo. Mọi số `[n]` trỏ tới `docs/references.md`.

Quy ước viết:

- Tên thanh ghi: X, Y, Z cho TinyA5/1; R1, R2, R3 cho A5/1 (theo `style_guide.md`). Khi trích công thức của slide, giữ nguyên ký hiệu slide (x, y, z).
- Thuật ngữ bám theo slide, viết tiếng Việt trước, tiếng Anh trong ngoặc ở lần dùng đầu:

| Từ dùng trong file này | Tiếng Anh | Chỗ slide dùng |
|---|---|---|
| thanh ghi | register | trang 46, 51 |
| quay (thanh ghi) | clock / shift | trang 46–48, 51 |
| hàm chiếm đa số | majority function | trang 47, 51 |
| bit điều khiển quay | clocking bit | trang 47, 51 (slide không đặt tên riêng) |
| bit t | feedback bit | trang 48, 51 |
| dãy số ngẫu nhiên S | keystream | trang 42 |
| bản rõ / bản mã | plaintext / ciphertext | trang 6, 7, 42 |
| mã dòng / mã khối | stream cipher / block cipher | trang 15, 42 |
| khoá | key | trang 42, 46 |

- Chữ "quay" của slide thực chất là thao tác dịch bit (bit cuối bị đẩy ra và bỏ đi, bit t vào vị trí 0), không phải xoay vòng [Slide, trang 48]. File này vẫn dùng "quay" cho khớp slide.

## 1. Bối cảnh GSM (GSM context)

GSM là chuẩn điện thoại di động thế hệ 2 (2G). Trên đường truyền vô tuyến, GSM mã hóa dữ liệu bằng một họ thuật toán gọi là A5. Đặc tả bảo mật của ETSI/3GPP định nghĩa A5 như một "hộp đen" có hai đầu vào. Đầu vào thứ nhất là khoá mã Kc dài 64 bit. Đầu vào thứ hai là COUNT dài 22 bit, được tính từ số khung TDMA (frame number). Đầu ra gồm hai khối BLOCK1 và BLOCK2, mỗi khối 114 bit, và phải được sinh ra trong thời gian ngắn hơn một khung TDMA (4,615 ms) [1, Annex C.1.2–C.1.3]. Khoá Kc không truyền qua mạng mà được sinh từ khoá bí mật Ki trong SIM và số ngẫu nhiên RAND bằng thuật toán A8. Việc xác thực thuê bao dùng thuật toán A3 để tính SRES [1].

Slide giới thiệu A5/1 là hệ mã dùng trong mạng điện thoại GSM để bảo mật dữ liệu giữa máy điện thoại và trạm thu phát sóng vô tuyến, với đơn vị mã hoá là 1 bit [Slide, trang 45]. A5/1 là thành viên "mạnh" của họ A5, được phát triển năm 1987 [6]. Bản A5/2 ra đời năm 1989 và bị làm yếu có chủ đích để dùng ở các vùng xuất khẩu [6]. Đến năm 2000, A5/1 bảo vệ khoảng 130 triệu thuê bao GSM ở châu Âu [3]. Phiên bản đặc tả năm 2007 của ETSI quy định máy di động bắt buộc phải hỗ trợ A5/1 và A5/3, đồng thời cấm cài đặt A5/2 [1, mục 4.9]. Cấu trúc bên trong của A5 không được công bố trong chuẩn. ETSI ghi rằng đặc tả nội bộ do GSM/MoU quản lý và chỉ cung cấp khi có yêu cầu phù hợp [1, mục C.1.4]. Vì vậy, các mô tả A5/1 dùng trong đồ án đến từ nguồn dịch ngược công khai (mục 5), không phải từ tài liệu chuẩn.

## 2. Mã dòng (stream cipher)

### 2.1. Các khái niệm cơ bản

- **Bản rõ (plaintext):** dữ liệu gốc cần mã hoá. Trong mã dòng, bản rõ P được chia thành các đơn vị mã hoá k bit: P = p₀p₁…pₙ₋₁ [Slide, trang 42].
- **Dãy số ngẫu nhiên S (keystream):** dãy bit do bộ sinh dãy số ngẫu nhiên tạo ra từ khoá K, mỗi phần tử có kích thước bằng một đơn vị mã hoá: S = s₀s₁…sₙ₋₁ [Slide, trang 42]. Trong mã dòng đồng bộ, dãy S được sinh độc lập với bản rõ và bản mã [5, Định nghĩa 6.2, trang 192][9]. Lưu ý: dãy S hoàn toàn được quyết định bởi khoá (cùng khoá cho cùng dãy S), nên về kỹ thuật đây là dãy giả ngẫu nhiên (pseudorandom) [9].
- **Bản mã (ciphertext):** dữ liệu ở dạng đã mã hoá [13]. Trong mã dòng, mỗi đơn vị bản mã là cᵢ = pᵢ ⊕ sᵢ [Slide, trang 42].
- **Phép XOR (⊕):** phép toán trên hai bit, cho kết quả `1` khi hai bit khác nhau và `0` khi hai bit giống nhau [12]:

| a | b | a ⊕ b |
|---|---|---|
| `0` | `0` | `0` |
| `0` | `1` | `1` |
| `1` | `0` | `1` |
| `1` | `1` | `0` |

XOR có tính tự nghịch đảo: XOR hai lần với cùng một giá trị thì trả lại giá trị ban đầu, tức (p ⊕ s) ⊕ s = p [12]. Nhờ tính chất này, bên nhận chỉ cần XOR bản mã với đúng dãy S đã dùng là lấy lại được bản rõ.

### 2.2. Mô hình mã hoá và giải mã

```
                        Khoá K
                          │
                          ▼
            ┌─────────────────────────────┐
            │ Bộ sinh dãy số ngẫu nhiên   │
            └─────────────────────────────┘
                          │  S = s₀ s₁ … sₙ₋₁
                          ▼
MÃ HOÁ:   Bản rõ P ─────▶ ⊕ ─────▶ Bản mã C      cᵢ = pᵢ ⊕ sᵢ   [Slide, trang 42]

GIẢI MÃ:  Bản mã C ─────▶ ⊕ ─────▶ Bản rõ P      pᵢ = cᵢ ⊕ sᵢ   [Slide, trang 43]
                          ▲
                          │  cùng dãy S
```

Ví dụ trên slide (đơn vị mã hoá k = 4 bit) [Slide, trang 44]:

- Mã hoá: p₀ = `1111`, s₀ = `0101` → c₀ = `1111` ⊕ `0101` = `1010`
- Giải mã: c₀ = `1010`, s₀ = `0101` → p₀ = `1010` ⊕ `0101` = `1111` (khớp bản rõ ban đầu)

### 2.3. Vị trí của A5/1

- Slide xếp mã dòng (A5/1, RC4) và mã khối (DES, AES) vào nhóm mã hoá hiện đại, biểu diễn dữ liệu bằng giá trị nhị phân [Slide, trang 15].
- A5/1 là **mã dòng đồng bộ (synchronous stream cipher)**: dãy S sinh ra độc lập với bản rõ và bản mã [5, Định nghĩa 6.2, trang 192].
- A5/1 cũng là **mã dòng cộng nhị phân (binary additive stream cipher)**: dãy S, bản rõ và bản mã đều là bit, phép kết hợp là XOR [5, Định nghĩa 6.4, trang 194]. Đơn vị mã hoá của A5/1 là 1 bit [Slide, trang 45].

### 2.4. So sánh mã dòng và mã khối

| Tiêu chí | Mã dòng (stream cipher) | Mã khối (block cipher) |
|---|---|---|
| Nguyên lý | Sinh dãy S rồi XOR từng bit hoặc từng ký tự với bản rõ; phép biến đổi thay đổi theo thời gian [5, trang 191][9] | Chia dữ liệu thành các khối có độ dài cố định; mỗi khối được mã bằng cùng một phép biến đổi với cùng khoá [5, trang 191][10][13] |
| Ưu điểm | Thường nhanh hơn và mạch phần cứng đơn giản hơn [5, trang 191][9]; hợp khi không biết trước độ dài dữ liệu (ví dụ kết nối không dây) vì không cần đệm thêm dữ liệu [9]; lỗi truyền ở một bit không lan sang bit khác [5, Ghi chú 6.3, trang 193][9] | Đa dụng: ngoài mã hoá còn là "khối xây dựng" cho bộ sinh số giả ngẫu nhiên, mã dòng, mã xác thực thông điệp (MAC) và hàm băm [11, trang 223][10] |
| Nhược điểm | Bên gửi và bên nhận phải đồng bộ (cùng khoá, cùng vị trí trạng thái) [5, Ghi chú 6.3, trang 193]; không được dùng lại cùng một dãy S hai lần [9] | Dữ liệu dài hơn một khối phải dùng chế độ hoạt động (ECB, CBC, CTR…) và phải đệm (padding) khi không chia hết cho kích thước khối [10]; ở chế độ ECB, các khối bản rõ giống nhau cho ra khối bản mã giống nhau, làm lộ mẫu dữ liệu [11, trang 228]; ở chế độ CBC, lỗi 1 bit trong bản mã làm hỏng 2 khối khi giải mã [11, trang 230] |
| Ví dụ trong môn học | A5/1, RC4 [Slide, trang 15] | DES, AES [Slide, trang 15] |

Ưu điểm "lỗi không lan" và "xử lý từng bit, không cần đệm" phù hợp với kênh vô tuyến của GSM, nơi mỗi khung chỉ mang 114 bit dữ liệu [1, C.1.3].

## 3. Thanh ghi dịch phản hồi tuyến tính (LFSR)

Slide không dùng từ "LFSR", mà gọi chung là các thanh ghi X, Y, Z [Slide, trang 46]. Theo định nghĩa chuẩn, một LFSR gồm L ô nhớ, mỗi ô chứa một bit. Mỗi nhịp, các bit chuyển đi một vị trí, và bit mới (bit phản hồi, feedback bit) bằng XOR của một số vị trí cố định (các vị trí này gọi là taps) [5, Định nghĩa 6.7, trang 195]. Tập vị trí tap tương ứng với một đa thức kết nối (connection polynomial) [5, Định nghĩa 6.8, trang 196]. Trong slide, bit phản hồi chính là bit t, ví dụ với thanh ghi X: t = x₂ ⊕ x₄ ⊕ x₅ [Slide, trang 48].

LFSR rất hợp với cài đặt phần cứng và cho dãy bit có tính chất thống kê tốt [5, trang 195]. Điểm yếu là đầu ra của một LFSR đơn lẻ dễ dự đoán: thuật toán Berlekamp–Massey có thể tìm lại LFSR từ một đoạn đầu ra ngắn, chỉ cần dài ít nhất gấp đôi độ dài LFSR [5, trang 200 và 204]. Vì vậy, LFSR thường phải kết hợp với một thành phần phi tuyến.

A5/1 dùng ba LFSR làm ba thanh ghi R1, R2, R3 có độ dài 19, 22 và 23 bit, tổng cộng 64 bit trạng thái [2][4][6][Slide, trang 51]. Slide cũng nhận xét A5/1 "được thực hiện dễ dàng bằng các thiết bị phần cứng, tốc độ nhanh" [Slide, trang 51], khớp với nhận định chung về LFSR của [5]. Lưu ý về quy ước: [5] mô tả LFSR chuyển bit về phía ô 0 và lấy đầu ra ở ô 0. Slide và [2] mô tả theo chiều ngược lại: khi quay, bit t vào vị trí 0, đầu ra lấy ở bit chỉ số cao [Slide, trang 47–48][2]. Đây chỉ là khác biệt về cách trình bày. Đồ án theo quy ước của slide.

## 4. Quy tắc quay theo hàm chiếm đa số (majority clocking)

Để phá tính tuyến tính của LFSR, A5/1 không cho cả ba thanh ghi quay đều mỗi nhịp. Thay vào đó, việc quay được điều khiển bởi chính dữ liệu trong thanh ghi; đây là một dạng bộ sinh có điều khiển nhịp (clock-controlled generator). Ý tưởng chung của loại bộ sinh này là khi thanh ghi quay không đều, các tấn công dựa trên chuyển động đều của LFSR sẽ khó thực hiện hơn [5, mục 6.3.3, trang 209].

Mỗi thanh ghi có một bit điều khiển quay (clocking bit): x8 của R1, y10 của R2 và z10 của R3 [Slide, trang 51][2][4]. Ở mỗi bước, ta tính m = maj(x8, y10, z10) bằng hàm chiếm đa số (majority function) [Slide, trang 51]. Thanh ghi nào có bit điều khiển quay bằng m thì quay, các thanh ghi còn lại đứng yên [6].

Quy tắc này dẫn tới hai hệ quả: mỗi bước luôn có 2 hoặc 3 thanh ghi được quay, và mỗi thanh ghi được quay với xác suất 3/4 [4, mục 2]. TinyA5/1 trên slide dùng đúng cơ chế này với các bit x₁, y₃, z₃. Hàm chiếm đa số trả về 0 nếu có từ hai bit 0 trở lên, ngược lại trả về 1 [Slide, trang 47].

## 5. Hệ mã A5/1 đầy đủ

Theo các nguồn dịch ngược, A5/1 gồm ba thanh ghi:

| Thanh ghi (register) | Độ dài | Bit điều khiển quay (clocking bit) | Vị trí tính bit t (feedback taps) | Bit đầu ra (output) |
|---|---|---|---|---|
| R1 | 19 bit | 8 | 13, 16, 17, 18 | 18 |
| R2 | 22 bit | 10 | 20, 21 | 21 |
| R3 | 23 bit | 10 | 7, 20, 21, 22 | 22 |

Nguồn: [2][4]; độ dài, vị trí tap và bit điều khiển quay khớp với [6] và slide [Slide, trang 51]. Theo nguồn ngoài, mỗi bit của dãy S là R1[18] ⊕ R2[21] ⊕ R3[22] [4, mục 2, công thức (1)], tức XOR các bit cao nhất của ba thanh ghi, lấy sau khi quay [2]. Slide ghi "sau khi quay bít xong thì bít sinh ra: sᵢ = x8 ⊕ y10 ⊕ z10" [Slide, trang 51], khác với nguồn ngoài. Chỗ lệch này được ghi thành CONFLICT-001 trong `references.md` và chuyển cho người chốt TD-001.

Quá trình khởi tạo cho mỗi khung như sau:

1. Nạp 64 bit khoá trong 64 chu kỳ.
2. Nạp 22 bit số khung (frame number) trong 22 chu kỳ. Ở bước 1 và 2, cả ba thanh ghi đều quay, không dùng hàm chiếm đa số.
3. Giai đoạn khởi động (warm-up): quay 100 chu kỳ theo hàm chiếm đa số và bỏ đầu ra.
4. Sinh 228 bit dãy S: 114 bit đầu cho chiều xuống (downlink), 114 bit sau cho chiều lên (uplink) [2][4][6].

Con số 2 × 114 bit khớp với BLOCK1 và BLOCK2 trong chuẩn ETSI [1, C.1.3]. Slide không mô tả các bước nạp khoá, nạp số khung và khởi động.

Về lịch sử, thiết kế chung của A5/1 bị lộ năm 1994 và được dịch ngược hoàn toàn năm 1999 [6]. Bản cài đặt C của Briceno, Goldberg và Wagner (1998–1999) được các tác giả xác nhận là khớp với test vector chính thức [2]. Về độ an toàn, A5/1 đã bị tấn công nhiều lần. Golić (1997) đưa ra tấn công có độ phức tạp thời gian 2^40.16 [6]. Biryukov, Shamir và Wagner (2000) dùng phương pháp đánh đổi thời gian – bộ nhớ (time-memory tradeoff): sau một giai đoạn tiền xử lý 2^48 bước, khoá có thể tìm được trong thời gian thực trên một PC [3]. Barkan, Biham và Keller (2003) công bố các tấn công chỉ cần bản mã trên GSM [6]. Năm 2009, dự án của Karsten Nohl công bố cách xây bảng cầu vồng (rainbow tables) để phá A5/1 [6]. Ngoài ra, một số triển khai cũ cố định 10 bit khoá bằng 0, khiến khoá hiệu dụng chỉ còn 54 bit [6]. Phần phân tích an toàn chi tiết sẽ viết ở mục 2.5 của báo cáo, và nên đọc trực tiếp các bài gốc (xem `references.md` mục 2).

## 6. Hệ mã TinyA5/1

TinyA5/1 là phiên bản thu nhỏ của A5/1 dùng trong bài giảng; slide nói rõ bài học chỉ "giới hạn xét mô hình thu nhỏ của A5/1, gọi tắt là TinyA5/1" [Slide, trang 45].

- **Thanh ghi:** bộ sinh số gồm 3 thanh ghi X, Y, Z dài 6, 8 và 9 bit (x₀…x₅, y₀…y₇, z₀…z₈) [Slide, trang 46].
- **Khoá:** K dài 23 bit, được phân bổ vào các thanh ghi theo K → XYZ [Slide, trang 46].
- **Mỗi bước sinh số:** tính m = maj(x₁, y₃, z₃); thanh ghi nào có bit bằng m thì quay; sau đó tính sᵢ = x₅ ⊕ y₇ ⊕ z₈ [Slide, trang 47].
- **Quay một thanh ghi:** tính bit t bằng XOR các bit quy định (ví dụ X: t = x₂ ⊕ x₄ ⊕ x₅), các bit chuyển từ chỉ số thấp sang chỉ số cao, rồi đưa t vào vị trí 0 [Slide, trang 48].
- **Mã hoá:** C = P XOR S [Slide, trang 47].
- **Khác A5/1 đầy đủ:** slide nạp khoá trực tiếp vào thanh ghi, không có bước nạp số khung hay giai đoạn khởi động [Slide, trang 46–47].

**Vì sao đồ án có TinyA5/1?**

TinyA5/1 chỉ có 23 bit trạng thái nên đủ nhỏ để tính tay. Nhờ vậy nhóm có thể:

- Kiểm tra logic từng bước: hàm chiếm đa số, bit t, dãy S.
- Đối chiếu kết quả với ví dụ tính tay trên slide [Slide, trang 49–50].
- Đáp ứng căn cứ chấm đầu tiên của đề bài: phiên bản thu nhỏ phải tái hiện đúng ví dụ trên lớp [8, mục 2]. TinyA5/1 và A5/1 hoạt động theo cùng nguyên tắc [Slide, trang 51], nên nếu TinyA5/1 sai thì A5/1 cũng sẽ sai.
- Sau khi nắm chắc cơ chế, mở rộng sang A5/1 (64 bit trạng thái), phiên bản không thể tính tay được nữa.
