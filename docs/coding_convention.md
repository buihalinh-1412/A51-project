# Quy ước Lập trình Python & Git Commit (Coding Convention)

## 1. Phiên bản Python (Python Version)
- Yêu cầu sử dụng **Python 3.10 trở lên** [Slide, trang 51].

## 2. Quy tắc đặt tên File (File Naming)
- Sử dụng kiểu `snake_case`, chữ thường hoàn toàn.
- Các file quy định trong dự án bao gồm:
  - `tiny_a51.py`
  - `a51.py`
  - `file_crypto.py`
  - `test_tiny_a51.py`
  - `test_a51.py`

## 3. Quy tắc đặt tên Lớp (Class Naming)
- Sử dụng kiểu `PascalCase`.
- Tên các lớp chuẩn bao gồm:
  - `TinyA51`
  - `A51`

## 4. Quy tắc đặt tên Biến (Variable Naming)
- Sử dụng kiểu `snake_case`, thể hiện rõ ý nghĩa kỹ thuật:
  - `register_x`
  - `register_y`
  - `register_z`
  - `clock_bit`
  - `majority_bit`
  - `keystream`

## 9. Quy ước Thông điệp Commit Git (Git Commit Convention)
- Định dạng chuẩn: `<type>: <description ngắn bằng tiếng Anh>`.
- Mẫu commit quy định cho phần tài liệu (`docs`):
  - `docs: add style guide`
  - `docs: add terminology`
  - `docs: add coding convention draft`
  - `docs: add majority truth table`
  - `docs: document register shifts`
