# Khung báo cáo (Report Outline) — A5/1 Project

Owner: Hoàng Yến Nhi · Nhánh: `docs/nhi-research`

Khung này bám theo bố cục báo cáo trong thẻ "Bản docs hoàn chỉnh" của Hà Linh và bố cục đề bài yêu cầu: Mở đầu → Cơ sở lý thuyết → Phân tích thuật toán → Cài đặt và kiểm thử → Kết quả demo và đánh giá → Kết luận → Tài liệu tham khảo [8, mục 2]. Mỗi mục ghi: người phụ trách, nội dung chính, file trong `docs/` cung cấp dữ liệu, hình hoặc sơ đồ cần có, nguồn dùng. Số `[n]` trỏ tới `docs/references.md`.

Quy ước thuật ngữ trong báo cáo: dùng tiếng Việt trước, tiếng Anh trong ngoặc, bám đúng từ của slide. Ví dụ: thanh ghi (register), quay thanh ghi (clock/shift), hàm chiếm đa số (majority function), dãy số ngẫu nhiên S (keystream), mã dòng (stream cipher).

## Lời nói đầu

- Người phụ trách: Hà Linh (đã có bản nháp).
- Nội dung chính:
  1. Nhu cầu bảo mật đường truyền vô tuyến.
  2. Vai trò của mã dòng (stream cipher) và A5/1 trong mạng GSM.
  3. Giá trị học tập của TinyA5/1.
  4. Tên đề tài và cách nhóm thực hiện.
- File cung cấp dữ liệu: `background.md` mục 1, 2.
- Hình/sơ đồ: không cần.
- Nguồn: [1], [3], [6].

## Chương 1. Giới thiệu đề tài

### 1.1. Đặt vấn đề và lý do chọn đề tài

- Người phụ trách: Hà Linh (đã có bản nháp).
- Nội dung chính:
  1. Bối cảnh GSM: bản tin truyền qua kênh vô tuyến nên cần mã hóa; GSM dùng họ thuật toán A5 [1].
  2. A5/1 dùng 3 thanh ghi 19, 22, 23 bit và quy tắc quay theo hàm chiếm đa số [2][4][Slide, trang 51].
  3. Vì sao cần TinyA5/1: A5/1 đầy đủ không tính tay được; bài học trên lớp chỉ xét bản thu nhỏ [Slide, trang 45].
  4. Đề bài bắt buộc làm cả hai phiên bản [8, mục 1].
- File cung cấp dữ liệu: `background.md` mục 1, 5, 6.
- Hình/sơ đồ: không cần.
- Nguồn: [1], [2], [4], [8], [Slide].

### 1.2. Mục đích và ý nghĩa nghiên cứu

- Người phụ trách: Hà Linh (đã có bản nháp).
- Nội dung chính:
  1. Mục đích lý thuyết: hiểu mã dòng, thanh ghi dịch phản hồi tuyến tính (LFSR), hàm chiếm đa số.
  2. Mục đích cài đặt: tự viết TinyA5/1 và A5/1 từ đầu, có trace, có kiểm thử.
  3. Mục đích ứng dụng: mã hóa tệp thật, minh họa tấn công dùng lại dãy khóa.
  4. Ý nghĩa: hiểu vì sao một hệ mã từng dùng rộng rãi lại bị phá.
- File cung cấp dữ liệu: `background.md`; `report_outline.md`.
- Hình/sơ đồ: không cần.
- Nguồn: [8].

### 1.3. Đối tượng và phạm vi nghiên cứu

- Người phụ trách: Hà Linh (đã có bản nháp).
- Nội dung chính:
  1. Đối tượng: TinyA5/1 (3 thanh ghi 6, 8, 9 bit) [Slide, trang 46] và A5/1 đầy đủ (19, 22, 23 bit) [2][Slide, trang 51].
  2. Phạm vi: thuật toán sinh dãy khóa, mã hóa và giải mã bằng XOR; không đi vào tầng vô tuyến của GSM.
  3. Công cụ: Python 3.10 trở lên, không dùng thư viện mật mã cho phần lõi [8, mục 2].
- File cung cấp dữ liệu: `coding_convention.md`.
- Hình/sơ đồ: không cần.
- Nguồn: [2], [8], [Slide].

### 1.4. Phương pháp nghiên cứu

- Người phụ trách: Hà Linh (đã có bản nháp).
- Nội dung chính:
  1. Nghiên cứu tài liệu: slide bài giảng, sách Handbook of Applied Cryptography, đặc tả ETSI, các bài báo về A5/1.
  2. Tính tay trên TinyA5/1 và đối chiếu từng trang slide; ghi lại chỗ slide lệch (không tự sửa slide).
  3. Cài đặt, kiểm thử và đối chiếu chéo với kết quả tính tay và test vector.
- File cung cấp dữ liệu: `references.md`; `tiny_a51_hand_calculation.md`; `audit/slide_blind_table.md`.
- Hình/sơ đồ: không cần.
- Nguồn: [1], [2], [3], [5], [Slide].

## Chương 2. Cơ sở lý thuyết và phân tích thuật toán

### 2.1. Tổng quan về mã dòng (stream cipher)

- Người phụ trách: **Nhi**.
- Nội dung chính:
  1. Định nghĩa bản rõ (plaintext), dãy số ngẫu nhiên S (keystream), bản mã (ciphertext), phép XOR [Slide, trang 42][5][12][13].
  2. Mô hình mã hóa cᵢ = pᵢ ⊕ sᵢ và giải mã pᵢ = cᵢ ⊕ sᵢ, kèm ví dụ chữ "HEAD" [Slide, trang 42–44].
  3. So sánh mã dòng và mã khối (block cipher): nguyên lý, ưu điểm, nhược điểm, ví dụ [5][9][10][11][Slide, trang 15].
  4. Thanh ghi dịch phản hồi tuyến tính (LFSR): cấu tạo, bit phản hồi t, điểm yếu tuyến tính [5, trang 195–204].
  5. Quy tắc quay theo hàm chiếm đa số (majority clocking) [4][5, trang 209][Slide, trang 47].
- File cung cấp dữ liệu: `background.md` mục 2, 3, 4; `terminology.md`.
- Hình/sơ đồ: sơ đồ mã hóa/giải mã có mũi tên (nhóm tự vẽ); sơ đồ một LFSR nhỏ.
- Nguồn: [5], [9], [10], [11], [12], [13], [Slide].

### 2.2. Thuật toán A5/1 đầy đủ (full A5/1)

- Người phụ trách: Vũ.
- Nội dung chính:
  1. Bối cảnh: phát triển năm 1987, dùng trong GSM; cấu trúc bên trong không công bố trong chuẩn, được biết qua dịch ngược [1, C.1.4][2][6].
  2. Cấu trúc 3 thanh ghi R1, R2, R3: độ dài, bit điều khiển quay, các vị trí tap [2][4][Slide, trang 51].
  3. Quy trình: nạp khóa 64 chu kỳ → nạp số khung 22 chu kỳ → khởi động 100 chu kỳ bỏ đầu ra → sinh 228 bit [2][4][6].
  4. Chỗ lệch bit đầu ra giữa slide và nguồn ngoài (CONFLICT-001, TD-001).
- File cung cấp dữ liệu: `a51_specification.md`; `a51_test_vector.md`; `references.md` (Ma trận nguồn).
- Hình/sơ đồ: sơ đồ khối A5/1 (Nhật Linh vẽ); sơ đồ thời gian 64 → 22 → 100 → 228.
- Nguồn: [1], [2], [4], [6], [Slide].

### 2.3. Thuật toán TinyA5/1 (bản rút gọn trên lớp)

- Người phụ trách: Lộc.
- Nội dung chính:
  1. Thanh ghi X, Y, Z dài 6, 8, 9 bit; khóa K 23 bit chia 6 + 8 + 9 [Slide, trang 46].
  2. Hàm chiếm đa số m = maj(x₁, y₃, z₃); thanh ghi nào có bit bằng m thì quay [Slide, trang 47].
  3. Công thức bit t của X, Y, Z và cách quay [Slide, trang 48].
  4. Bit sinh ra sᵢ = x₅ ⊕ y₇ ⊕ z₈, tính sau khi quay [Slide, trang 47, 49].
- File cung cấp dữ liệu: `tiny_a51_specification.md`; `majority_truth_table.md`; `register_shift_example.md`.
- Hình/sơ đồ: sơ đồ khối TinyA5/1 (Nhật Linh vẽ).
- Nguồn: [Slide].

### 2.4. Ví dụ tính tay chi tiết từng bước trên TinyA5/1

- Người phụ trách: Hà Linh.
- Nội dung chính:
  1. Đầu vào P = `111` (chữ H), K = `10010101001110100110000` [Slide, trang 49].
  2. Bảng trạng thái X, Y, Z qua Bước 0, 1, 2.
  3. S = `100`; C = `111` ⊕ `100` = `011` (chữ D); giải mã lại `111` [Slide, trang 50].
  4. Chỗ lệch Z sau Bước 2 (slide ghi `101001100`, tính lại được `001001100`) và lý do không đổi S (TD-002).
- File cung cấp dữ liệu: `tiny_a51_hand_calculation.md`; `register_shift_example.md` mục 4.
- Hình/sơ đồ: bảng 12 cột trạng thái từng bước.
- Nguồn: [Slide].

### 2.5. Phân tích độ an toàn của hệ mã A5/1

- Người phụ trách: chưa ghi trong thẻ "Bản docs hoàn chỉnh" (đề xuất Nhi, vì đã có nguồn ở `background.md` mục 5).
- Nội dung chính:
  1. Không gian khóa 2^64; một số triển khai cũ cố định 10 bit khóa bằng 0 nên khóa hiệu dụng còn 54 bit [6].
  2. Các tấn công đã công bố: Golić 1997 (độ phức tạp 2^40.16) [6]; Biryukov–Shamir–Wagner 2000 (đánh đổi thời gian – bộ nhớ, tiền xử lý 2^48 bước) [3]; Barkan–Biham–Keller 2003 (chỉ cần bản mã) [6]; dự án bảng cầu vồng (rainbow tables) của Nohl 2009 [6].
  3. Điểm yếu cấu trúc: LFSR tuyến tính [5]; số khung công khai [6].
  4. Hiện trạng: chuẩn ETSI bắt buộc A5/3 và cấm A5/2 trên máy di động [1, mục 4.9].
- File cung cấp dữ liệu: `background.md` mục 5; `references.md` mục 2 (bài cần đọc thêm).
- Hình/sơ đồ: bảng các tấn công (năm, tác giả, loại tấn công, dữ liệu cần, chi phí).
- Nguồn: [1], [3], [5], [6]; cần đọc thêm bài gốc của Barkan–Biham–Keller và Golić trước khi viết.

### 2.6. So sánh hệ mã A5/1 với hệ mã cùng loại (RC4)

- Người phụ trách: **Nhi**.
- Nội dung chính:
  1. Giới thiệu RC4: dùng trong SSL và WEP; bản thu nhỏ TinyRC4 có đơn vị mã hóa 3 bit, dùng 2 mảng S và T [Slide, trang 53].
  2. Nguyên lý: A5/1 dùng 3 thanh ghi quay theo hàm chiếm đa số; RC4 hoán vị mảng S qua 2 giai đoạn khởi tạo và sinh số [Slide, trang 51, 53–62].
  3. Đơn vị xử lý và hướng cài đặt: A5/1 sinh từng bit, dễ làm bằng phần cứng [Slide, trang 45, 51]; RC4 sinh theo byte.
  4. Độ an toàn và phạm vi ứng dụng (GSM so với SSL/WEP).
  5. Bảng tổng hợp giống và khác nhau.
- File cung cấp dữ liệu: `background.md` mục 2, 5; nguồn RC4 bổ sung sau.
- Hình/sơ đồ: bảng so sánh theo 5 tiêu chí.
- Nguồn: [Slide], [8]; cần tìm thêm nguồn ngoài về RC4.

## Chương 3. Cài đặt hệ mã và kiểm thử phần mềm

### 3.1. Kiến trúc phần mềm và tổ chức mã nguồn

- Người phụ trách: chưa phân công (GĐ2–GĐ4).
- Nội dung chính:
  1. Cấu trúc thư mục `src/`, `tests/`, `demo/`; tên file theo `coding_convention.md`.
  2. Lõi viết bằng Python thuần, không dùng thư viện mật mã [8, mục 2].
  3. Chế độ trace lưu trạng thái thanh ghi từng bước.
- File cung cấp dữ liệu: `coding_convention.md`.
- Hình/sơ đồ: sơ đồ các module.
- Nguồn: [8].

### 3.2. Cài đặt thuật toán TinyA5/1 và A5/1 đầy đủ

- Người phụ trách: chưa phân công.
- Nội dung chính:
  1. Đoạn code chính: hàm chiếm đa số, quay thanh ghi, sinh dãy S.
  2. Mã hóa/giải mã tệp: đọc byte → tách bit → XOR với dãy S → ghi tệp.
- File cung cấp dữ liệu: `tiny_a51_specification.md`; `a51_specification.md`; `technical_decisions.md`.
- Hình/sơ đồ: lưu đồ (flowchart) một bước sinh bit.
- Nguồn: [Slide], [2].

### 3.3. Kịch bản và kết quả kiểm thử

- Người phụ trách: chưa phân công.
- Nội dung chính:
  1. Ca 1: tái hiện ví dụ trên lớp (S = `100`, C = `011`) [Slide, trang 49–50].
  2. Ca 2: mã hóa rồi giải mã lại đúng bản rõ.
  3. Ca 3: khóa sai độ dài, ký tự khác `0`/`1`.
  4. Ca 4: đối chiếu test vector A5/1 (key `0x1223456789ABCDEF`, frame `0x134`) [2].
- File cung cấp dữ liệu: `a51_test_vector.md`; `tiny_a51_hand_calculation.md`.
- Hình/sơ đồ: bảng kết quả kiểm thử.
- Nguồn: [2], [Slide].

## Chương 4. Kết quả demo và đánh giá

### 4.1. Giao diện chương trình và hướng dẫn sử dụng

- Người phụ trách: chưa phân công.
- Nội dung chính: ảnh giao diện CLI/GUI; các bước nhập bản rõ, khóa, mã hóa, giải mã, chọn tệp.
- Hình/sơ đồ: ảnh chụp màn hình.

### 4.2. Demo trên dữ liệu thật

- Người phụ trách: chưa phân công.
- Nội dung chính: trace TinyA5/1 từng bước; mã hóa và giải mã một tệp `.txt` và một ảnh nhỏ [8, mục 2].
- Hình/sơ đồ: ảnh chụp trace; so sánh tệp gốc và tệp giải mã.

### 4.3. Mô phỏng tấn công dùng lại dãy khóa (keystream reuse)

- Người phụ trách: chưa phân công.
- Nội dung chính:
  1. Nếu C₁ = P₁ ⊕ S và C₂ = P₂ ⊕ S thì C₁ ⊕ C₂ = P₁ ⊕ P₂, dãy S bị triệt tiêu.
  2. Mã dòng không được dùng lại cùng một dãy khóa [9].
  3. Kết quả chạy thử trên chương trình.
- Nguồn: [9].

### 4.4. Đánh giá ưu điểm và hạn chế của phần mềm

- Người phụ trách: chưa phân công.
- Nội dung chính: điểm mạnh (tái hiện đúng slide, có trace); hạn chế (tốc độ Python với tệp lớn).

## Kết luận và hướng phát triển

- Người phụ trách: chưa phân công.
- Nội dung chính: tóm tắt kết quả; các chỗ lệch slide đã phát hiện; bài học làm việc nhóm qua Git.

## Tài liệu tham khảo

- Người phụ trách: Nhi.
- Nội dung chính: lấy từ `references.md`, trình bày theo một chuẩn trích dẫn thống nhất (ví dụ APA).

## Phụ lục: kê khai sử dụng công cụ AI

- Người phụ trách: cả nhóm.
- Nội dung chính: ghi rõ AI dùng vào việc gì; mọi thành viên phải giải thích được toàn bộ mã nguồn [8, mục 5].

## Yêu cầu đề bài và mục đáp ứng

| Yêu cầu đề bài [8, mục 2] | Mục đáp ứng | Trạng thái |
|---|---|---|
| Bối cảnh ra đời: tác giả, năm, vấn đề giải quyết, nơi sử dụng | 1.1, 2.2 | Đã có khung. A5/1 không có tác giả công bố; ghi "phát triển năm 1987 cho GSM" [6], cấu trúc biết được qua dịch ngược [2] |
| Mô tả đầy đủ thuật toán: đầu vào, sinh khóa, mã hóa, giải mã | 2.2, 2.3 | Đã có khung |
| Sơ đồ khối nhóm tự vẽ | 2.1, 2.2, 2.3 | Cần Nhật Linh vẽ |
| Ví dụ tính tay đầy đủ, khớp chương trình | 2.4, 3.3 | Đã có tính tay; chờ code GĐ2 |
| Phân tích độ an toàn | 2.5 | Đã có khung; chưa có người phụ trách |
| So sánh với ít nhất một hệ mã cùng loại | 2.6 | Đã có khung; cần thêm nguồn RC4 |
| Cài đặt, kiểm thử, demo | Chương 3, 4 | Làm từ GĐ2 |
| Tài liệu tham khảo; ghi rõ mã tham khảo ngoài | Tài liệu tham khảo | Đã có `references.md` |
| Bảng phân công và tỉ lệ đóng góp | Chương 1 hoặc phụ lục | Lấy từ task tracker |
| Kê khai dùng AI | Phụ lục | Đã có khung |

## Ghi chú cho Hà Linh (điểm cần sửa trong thẻ "Bản docs hoàn chỉnh")

1. Mục 1.4 ghi slide của "TS. Lưu Minh Tuấn"; slide nhóm dùng là của **ThS. Nguyễn Quốc Thái** (trang bìa Chương 2).
2. Mục 2.5 ghi khóa hiệu dụng 2^54 "do cấu trúc nạp khóa"; nguồn [6] ghi lý do là một số triển khai cũ cố định 10 bit khóa bằng 0.
3. Mục 2.5 xếp Barkan–Biham–Keller vào nhóm đánh đổi thời gian – bộ nhớ; nguồn [6] mô tả đây là tấn công chỉ cần bản mã. Câu "Kraken phá khóa trong vài giây" chưa có nguồn.
4. Nhiều chỗ còn dấu `[cite: 6, 7]`, `ATBMTT - A51`, `PDF+ 1`, `DOCX+ 1` (dấu vết công cụ AI), cần xóa trước khi nộp.
5. Dòng "[DÁN BÀI CỦA YẾN NHI VÀO CÁC MỤC 2.1, 2.6, 2.7]" nhắc mục 2.7, nhưng báo cáo hiện chỉ có tới 2.6. Nhi đề xuất nhận thêm 2.5 (phân tích an toàn).
