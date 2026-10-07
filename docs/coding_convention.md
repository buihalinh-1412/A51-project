# Quy ước lập trình Python và Git commit (Coding Convention)

Trạng thái: bản nháp. Mục 6 và 7 là **PROVISIONAL**, Hà Linh khóa chính thức ở D6.

## 1. Phiên bản Python

- Dùng **Python 3.10 trở lên** (quyết định của nhóm; đề bài cho tự chọn ngôn ngữ).

## 2. Đặt tên file

- Kiểu `snake_case`, chữ thường hoàn toàn.
- Các file quy định trong dự án:
  - `tiny_a51.py`
  - `a51.py`
  - `file_crypto.py`
  - `test_tiny_a51.py`
  - `test_a51.py`

## 3. Đặt tên lớp

- Kiểu `PascalCase`.
- Tên các lớp chuẩn:
  - `TinyA51`
  - `A51`

## 4. Đặt tên biến

- Kiểu `snake_case`, thể hiện rõ ý nghĩa kỹ thuật:
  - `register_x`, `register_y`, `register_z`
  - `clock_bit`
  - `majority_bit`
  - `keystream`

## 5. Biểu diễn register

- Trong file spec (`docs/`): giữ ký hiệu của nguồn, ví dụ x₀…x₅ theo slide [Slide, trang 46].
- Trong code: mỗi register là một `list` Python các số nguyên `0`/`1`; phần tử đầu `register_x[0]` ứng với x₀.
- Ví dụ: X = `100101` → `register_x = [1, 0, 0, 1, 0, 1]`.

## 6. Đánh số chỉ số bit — PROVISIONAL

- **Phương án A (bắt đầu từ 0):** x₀ là bit đầu. Ví dụ clocking bit của X là `register_x[1]` (= x₁).
- **Phương án B (bắt đầu từ 1):** bit đầu gọi là x₁. Khi viết code phải trừ 1: bit thứ k ứng với `register_x[k - 1]`, dễ nhầm khi đối chiếu với slide.
- Bằng chứng: slide đánh số từ 0 (x₀…x₅, y₀…y₇, z₀…z₈) [Slide, trang 46], trùng với chỉ số list Python. Nhóm nghiêng về phương án A.
- Hà Linh khóa chính thức ở D6 (TD-003).

## 7. Hướng dịch — PROVISIONAL

- Theo slide: xⱼ = xⱼ₋₁ với j = 5, 4, 3, 2, 1, sau đó x₀ = t [Slide, trang 48]. Tương tự cho Y (j = 7…1) và Z (j = 8…1).
- Nghĩa là: bit dịch từ chỉ số thấp sang chỉ số cao; feedback bit vào vị trí 0; bit ở chỉ số cao nhất bị đẩy ra.
- Trong code: `register_x = [t] + register_x[:-1]`.
- Hà Linh khóa chính thức ở D6.

## 8. Dữ liệu vào và ra

- **Kiểu dữ liệu bên trong:** list số nguyên `0`/`1`. Lý do: XOR trực tiếp bằng toán tử `^`, chỉ số khớp ký hiệu slide, dễ in trạng thái từng bước khi demo.
- **Hàm sinh keystream:** nhận số bit cần sinh, trả về `list[int]` (các bit `0`/`1`).
- **Phép XOR với dữ liệu:** làm ở lớp ngoài (`file_crypto.py`), không làm trong lõi. Lõi (`tiny_a51.py`, `a51.py`) chỉ sinh keystream.

## 9. Thông điệp commit Git

- Định dạng: `<type>: <mô tả ngắn bằng tiếng Anh>`.
- `type` dùng: `docs` (tài liệu), `feat` (tính năng), `fix` (sửa lỗi), `test` (kiểm thử), `chore` (việc lặt vặt như cấu hình repo).
- Mẫu commit cho phần tài liệu của Nhật Linh:
  - `docs: add style guide`
  - `docs: add terminology`
  - `docs: add coding convention draft`
  - `docs: add majority truth table`
  - `docs: document register shifts`
  - `docs: add decision log`
  - `docs: integrate phase 1 documentation`
