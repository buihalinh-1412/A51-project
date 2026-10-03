# Bảng Chân lý Hàm Đa số (Majority Truth Table)

## 1. Bảng Chân lý 8 Trường hợp
Hàm chiếm đa số `m = maj(x, y, z)` kiểm tra 3 bit điều khiển nhịp (clocking bits) `x1, y3, z3` của 3 thanh ghi.

| x | y | z | majority |
| :-: | :-: | :-: | :-: |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

## 2. Ghi chú & Ý nghĩa Kỹ thuật
- **Định nghĩa**: `majority` = giá trị xuất hiện ít nhất 2 trong 3 bit.
- **Hỗ trợ Debug**: Bảng này giúp khoanh vùng lỗi khi debug (xác định lỗi nằm ở hàm majority hay ở dịch register).

## 3. Ví dụ Số thật từ Slide (Bước 0 - Slide trang 47, 50)
- **Đọc 3 clocking bits ban đầu**: `x1 = 0`, `y3 = 0`, `z3 = 1`.
- **Tra bảng chân lý**: Với tổ hợp `(0, 0, 1)`, tra bảng được `maj(0, 0, 1) = 0`.
- **Kết quả điều khiển quay**:
  - Thanh ghi X có `x1 = 0 = m` → **Quay X**.
  - Thanh ghi Y có `y3 = 0 = m` → **Quay Y**.
  - Thanh ghi Z có `z3 = 1 ≠ m` → **Giữ nguyên Z**.
