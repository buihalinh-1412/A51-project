# Report Outline — A5/1 Project

Owner: Hoàng Yến Nhi · Nhánh: `docs/nhi-research`
Mục đích: khung cho phần "Mở đầu" và "Cơ sở lý thuyết / Phân tích thuật toán" của báo cáo cuối kỳ. Số `[n]` trỏ tới `docs/references.md`.
Bố cục báo cáo theo đề bài: Mở đầu → Cơ sở lý thuyết → Phân tích thuật toán → Cài đặt và kiểm thử → Kết quả demo và đánh giá → Kết luận → Tài liệu tham khảo [8, mục 2]. Tám chương dưới đây là phần lý thuyết và thuật toán của Giai đoạn 1. Các chương cài đặt, demo và an toàn được đề xuất ở cuối file.

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

## Yêu cầu đề bài và chương đáp ứng

| Yêu cầu đề bài [8, mục 2] | Chương đáp ứng | Trạng thái |
|---|---|---|
| Bối cảnh ra đời: tác giả, năm công bố, vấn đề giải quyết, nơi sử dụng | Chương 2, Chương 6 | Đã có. Lưu ý: A5/1 không có "tác giả" công khai; ghi là do GSM phát triển năm 1987 [6], cấu trúc được Briceno và cộng sự công bố qua dịch ngược [2] |
| Mô tả đầy đủ thuật toán: tham số đầu vào, sinh khóa, mã hóa, giải mã | Chương 7, Chương 8 | Đã có |
| Sơ đồ khối do nhóm tự vẽ (không chụp slide) | Chương 3, 4, 5, 6, 7, 8 | Đã có trong khung; cần phân công người vẽ |
| Ví dụ tính tay đầy đủ trên phiên bản thu nhỏ, khớp với chương trình | Chương 7 | Đã có |
| Phân tích độ an toàn: không gian khóa, tấn công đã biết, chi phí, còn khuyến nghị hay không | Chưa có chương riêng | **Đề xuất:** thêm Chương 9 "Security analysis" (không gian khóa 2^64, khóa hiệu dụng 54 bit ở triển khai cũ, các tấn công 1994–2009, A5/1 không còn được khuyến nghị). Dùng [3], [4], [6] và cần đọc thêm các bài ở `references.md` mục 2 |
| So sánh với ít nhất một hệ mã cùng loại | Chưa có chương riêng | **Đề xuất:** thêm Chương 10 "Comparison with RC4". RC4 là mã dòng cùng nhóm A trong đề bài [8, mục 1]; so sánh nguyên lý (LFSR so với hoán vị mảng S), tốc độ, độ an toàn, phạm vi ứng dụng. Cần tìm nguồn về RC4 ở giai đoạn sau |
| Cài đặt và kiểm thử; Kết quả demo và đánh giá; Kết luận | Ngoài phạm vi GĐ1 | Đề xuất thêm các chương tương ứng từ GĐ2 trở đi |
| Tài liệu tham khảo; ghi rõ mã nguồn tham khảo ngoài | `references.md` | Đã có. Cần ghi rõ nếu dùng [2] để đối chiếu kết quả |
| Bảng phân công và tỉ lệ đóng góp | Chương 1 | Lấy từ `task_tracker.xlsx` |

Ghi chú cho người kiểm tra: việc thêm Chương 9 và Chương 10 là đề xuất. Hà Linh quyết định ở D6.
