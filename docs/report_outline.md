# Report Outline — A5/1 Project

Owner: Hoàng Yến Nhi · Nhánh: `docs/nhi-research`
Mục đích: khung cho phần "Mở đầu" và "Cơ sở lý thuyết / Phân tích thuật toán" của báo cáo cuối kỳ. Số `[n]` trỏ tới `docs/references.md`.
Bố cục báo cáo theo đề bài: Mở đầu → Cơ sở lý thuyết → Phân tích thuật toán → Cài đặt và kiểm thử → Kết quả demo và đánh giá → Kết luận → Tài liệu tham khảo [8, mục 2]. Mười chương dưới đây gồm 8 chương lý thuyết và thuật toán của Giai đoạn 1, cộng Chương 9 (phân tích an toàn) và Chương 10 (so sánh với RC4) đã được trưởng nhóm duyệt thêm. Các chương cài đặt, kiểm thử và demo sẽ bổ sung từ Giai đoạn 2.

## 1. Introduction

- Nội dung chính:
  1. Lý do chọn đề tài: A5/1 là mã dòng dùng thực tế trong GSM, minh họa rõ LFSR và clock không đều.
  2. Mục tiêu: tìm hiểu, cài đặt từ đầu TinyA5/1 và A5/1 đầy đủ, chạy demo mã hóa/giải mã.
  3. Phạm vi: làm cả hai phiên bản (bắt buộc theo đề bài [8, mục 1]); không dùng thư viện mật mã cho phần lõi.
  4. Cấu trúc báo cáo và bảng phân công, tỉ lệ đóng góp.
  5. Ghi rõ việc sử dụng công cụ AI (đề bài yêu cầu [8, mục 5]).
- File trong docs/ cung cấp dữ liệu: `README.md`, `task_tracker.xlsx`, `report_outline.md`.
- Hình/sơ đồ: không bắt buộc; có thể có sơ đồ tổng quan 5 giai đoạn của đồ án.
- Nguồn: [8].

## 2. GSM context

- Nội dung chính:
  1. GSM và vị trí của A5 trên đường truyền vô tuyến.
  2. Đầu vào và đầu ra của A5: Kc 64 bit, COUNT 22 bit từ số khung TDMA, hai khối 114 bit trong 4,615 ms [1, C.1.2–C.1.3].
  3. Kc được sinh từ Ki và RAND bằng A8; xác thực bằng A3 [1].
  4. Họ A5: A5/1 (1987), A5/2 (1989, bản làm yếu), A5/3; quy định cấm A5/2 [1, mục 4.9][6].
  5. Đặc tả A5 không công khai, nên phải dựa vào nguồn dịch ngược [1, C.1.4][2].
- File cung cấp dữ liệu: `background.md` mục 1.
- Hình/sơ đồ: sơ đồ khối Ki + RAND → A8 → Kc; Kc + COUNT → A5 → BLOCK1/BLOCK2 → XOR với dữ liệu (nhóm tự vẽ).
- Nguồn: [1], [3], [6].

## 3. Stream cipher

- Nội dung chính:
  1. Định nghĩa stream cipher; synchronous và binary additive stream cipher [5, trang 191–194].
  2. Mô hình cᵢ = pᵢ ⊕ sᵢ, pᵢ = cᵢ ⊕ sᵢ; ví dụ "HEAD" [Slide, trang 42–44].
  3. So sánh stream cipher và block cipher (nguyên lý, ưu và nhược điểm) [5, trang 191, 193].
  4. Yêu cầu đồng bộ giữa bên gửi và bên nhận [5, Ghi chú 6.3].
  5. Vì sao mã dòng hợp với kênh vô tuyến GSM.
- File cung cấp dữ liệu: `background.md` mục 2; `terminology.md` (plaintext, ciphertext, keystream).
- Hình/sơ đồ: sơ đồ khối "bộ sinh keystream → XOR → ciphertext" cho cả hai chiều mã hóa và giải mã.
- Nguồn: [5], [Slide].

## 4. LFSR

- Nội dung chính:
  1. Định nghĩa LFSR: ô nhớ, taps, bit phản hồi, connection polynomial [5, trang 195–196].
  2. Ưu điểm: hợp phần cứng, thống kê tốt [5, trang 195].
  3. Nhược điểm: tuyến tính, dễ dự đoán bằng Berlekamp–Massey [5, trang 200, 204].
  4. Quy ước hướng dịch: [5] khác slide; đồ án theo slide.
- File cung cấp dữ liệu: `background.md` mục 3; `register_shift_example.md`; `coding_convention.md` (mục hướng dịch, chỉ số bit).
- Hình/sơ đồ: sơ đồ một LFSR nhỏ có đánh dấu taps và chiều dịch; ví dụ dịch một bước.
- Nguồn: [5], [Slide].

## 5. Majority clocking

- Nội dung chính:
  1. Clock-controlled generator: lý do dùng clock không đều [5, trang 209].
  2. Hàm majority và quy tắc "register nào có clocking bit bằng majority thì được clock" [6][Slide, trang 47].
  3. Mỗi chu kỳ có 2 hoặc 3 register dịch; xác suất dịch của mỗi register là 3/4 [4].
  4. Bảng chân lý majority 8 dòng.
- File cung cấp dữ liệu: `background.md` mục 4; `majority_truth_table.md`.
- Hình/sơ đồ: bảng chân lý; sơ đồ ba clocking bit → khối maj → tín hiệu clock cho từng register.
- Nguồn: [4], [5], [6], [Slide].

## 6. A5/1 overview

- Nội dung chính:
  1. Lịch sử: phát triển năm 1987, lộ thiết kế năm 1994, dịch ngược năm 1999 [6][2].
  2. Cấu trúc tổng quát: 3 register 19/22/23 bit, majority clocking, output là XOR ba bit [2][4].
  3. Luồng xử lý mỗi khung: nạp key → nạp frame → warm-up → sinh 228 bit [2][4][6].
  4. Ứng dụng thực tế và quy mô sử dụng [3][Slide, trang 45].
  5. Tóm tắt các điểm slide khác nguồn ngoài (dẫn sang chương 8).
- File cung cấp dữ liệu: `background.md` mục 5; `a51_specification.md`.
- Hình/sơ đồ: sơ đồ khối A5/1 với ba register, clocking bit, taps và khối XOR output (nhóm tự vẽ, không chụp slide).
- Nguồn: [2], [3], [4], [6].

## 7. TinyA5/1

- Nội dung chính:
  1. Cấu trúc X/Y/Z 6/8/9 bit, khóa 23 bit, cách phân bổ khóa [Slide, trang 46].
  2. Thuật toán: majority trên x₁, y₃, z₃; quy tắc quay; sᵢ = x₅ ⊕ y₇ ⊕ z₈ [Slide, trang 47–48].
  3. Ví dụ tính tay đầy đủ: P = `111`, S = `100`, C = `011` [Slide, trang 49–50].
  4. Chỗ lệch Z ở bước 2 (TD-002), kèm cách nhóm xử lý.
  5. Vì sao dùng TinyA5/1: tính tay được và là căn cứ chấm tính đúng của chương trình.
- File cung cấp dữ liệu: `tiny_a51_specification.md`, `tiny_a51_hand_calculation.md`, `majority_truth_table.md`, `register_shift_example.md`, `audit/slide_blind_table.md`, `background.md` mục 6.
- Hình/sơ đồ: sơ đồ khối TinyA5/1; bảng trạng thái X/Y/Z qua từng bước của ví dụ tính tay.
- Nguồn: [Slide].

## 8. Full A5/1

- Nội dung chính:
  1. Đặc tả từng register R1/R2/R3: độ dài, clocking bit, taps, bit output [2][4].
  2. Nạp key 64 chu kỳ, nạp frame 22 chu kỳ, warm-up 100 chu kỳ, 228 bit keystream [2][4][6].
  3. Thứ tự bit khi nạp key, frame và khi ghép keystream thành byte (TD-003).
  4. Chỗ lệch bit output giữa slide và nguồn ngoài (CONFLICT-001, TD-001) và quyết định của nhóm.
  5. Test vector dùng để kiểm chứng và điều kiện áp dụng; xử lý dữ liệu dài hơn 228 bit (TD-005).
- File cung cấp dữ liệu: `a51_specification.md`, `a51_test_vector.md`, `technical_decisions.md`, `decision_log.md`, `references.md` (Ma trận nguồn).
- Hình/sơ đồ: sơ đồ timeline khởi tạo (64 → 22 → 100 → 228 chu kỳ); bảng so sánh slide và nguồn ngoài; bảng khác biệt TinyA5/1 và A5/1.
- Nguồn: [1], [2], [4], [6], [Slide].

## 9. Security analysis

- Nội dung chính:
  1. Không gian khóa: khóa 64 bit; một số triển khai cũ cố định 10 bit bằng 0 nên khóa hiệu dụng chỉ còn 54 bit [6].
  2. Các tấn công đã biết theo thời gian: Anderson 1994, Golić 1997, Biryukov–Shamir–Wagner 2000 (time-memory tradeoff), Barkan–Biham–Keller 2003 (chỉ cần bản mã), dự án bảng cầu vồng của Nohl 2009 [3][4][6].
  3. Chi phí tấn công: tiền xử lý 2^48 bước, sau đó phá khóa thời gian thực trên một PC [3].
  4. Điểm yếu cấu trúc: LFSR tuyến tính [5]; frame number công khai [6].
  5. Hiện trạng: A5/1 không còn được xem là an toàn; chuẩn ETSI đã thêm A5/3 và cấm A5/2 [1, mục 4.9].
- File cung cấp dữ liệu: `background.md` mục 5; `references.md` (mục 2: các bài cần đọc thêm).
- Hình/sơ đồ: bảng các tấn công (năm, tác giả, loại tấn công, dữ liệu cần có, chi phí); có thể minh họa tấn công dùng lại keystream trong demo.
- Nguồn: [1], [3], [4], [5], [6]; cần đọc thêm bài gốc của Barkan–Biham–Keller 2003, Gendrullis và cộng sự 2008, Golić 1997.

## 10. Comparison with RC4

- Nội dung chính:
  1. Giới thiệu RC4: mã dòng dùng trong SSL và WEP; đơn vị mã hoá TinyRC4 là 3 bit, dùng 2 mảng S và T [Slide, trang 53].
  2. So sánh nguyên lý: A5/1 dùng 3 LFSR với clock không đều; RC4 dùng hoán vị mảng S qua 2 giai đoạn khởi tạo và sinh số [Slide, trang 51, 53–62].
  3. So sánh tốc độ và hướng cài đặt: A5/1 hợp với phần cứng [Slide, trang 51]; RC4 thiết kế theo byte.
  4. So sánh độ an toàn và phạm vi ứng dụng (GSM so với SSL/WEP).
  5. Bảng tổng hợp giống và khác nhau.
- File cung cấp dữ liệu: `background.md` mục 2 và 5; tài liệu RC4 sẽ bổ sung ở giai đoạn sau.
- Hình/sơ đồ: bảng so sánh A5/1 và RC4 theo 4 tiêu chí (nguyên lý, tốc độ, độ an toàn, ứng dụng).
- Nguồn: [Slide], [8, mục 1]; cần tìm thêm nguồn ngoài về RC4 ở giai đoạn sau.

## Yêu cầu đề bài và chương đáp ứng

| Yêu cầu đề bài [8, mục 2] | Chương đáp ứng | Trạng thái |
|---|---|---|
| Bối cảnh ra đời: tác giả, năm công bố, vấn đề giải quyết, nơi sử dụng | Chương 2, Chương 6 | Đã có. Lưu ý: A5/1 không có "tác giả" công khai; ghi là do GSM phát triển năm 1987 [6], cấu trúc được Briceno và cộng sự công bố qua dịch ngược [2] |
| Mô tả đầy đủ thuật toán: tham số đầu vào, sinh khóa, mã hóa, giải mã | Chương 7, Chương 8 | Đã có |
| Sơ đồ khối do nhóm tự vẽ (không chụp slide) | Chương 3, 4, 5, 6, 7, 8 | Đã có trong khung; cần phân công người vẽ |
| Ví dụ tính tay đầy đủ trên phiên bản thu nhỏ, khớp với chương trình | Chương 7 | Đã có |
| Phân tích độ an toàn: không gian khóa, tấn công đã biết, chi phí, còn khuyến nghị hay không | Chương 9 | Đã có khung; cần đọc thêm các bài gốc ở `references.md` mục 2 |
| So sánh với ít nhất một hệ mã cùng loại | Chương 10 | Đã có khung; cần tìm thêm nguồn ngoài về RC4 |
| Cài đặt và kiểm thử; Kết quả demo và đánh giá; Kết luận | Ngoài phạm vi GĐ1 | Bổ sung từ Giai đoạn 2 |
| Tài liệu tham khảo; ghi rõ mã nguồn tham khảo ngoài | `references.md` | Đã có. Cần ghi rõ nếu dùng [2] để đối chiếu kết quả |
| Bảng phân công và tỉ lệ đóng góp | Chương 1 | Lấy từ `task_tracker.xlsx` |

