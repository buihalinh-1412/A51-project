# Bảng chân lý hàm đa số (Majority Truth Table)

## 1. Bảng chân lý 8 trường hợp

Hàm đa số m = maj(x₁, y₃, z₃) nhận 3 clocking bit của 3 register X, Y, Z [Slide, trang 47]. Trong bảng, cột `x`, `y`, `z` lần lượt là giá trị của x₁, y₃, z₃.

| x | y | z | majority |
| :-: | :-: | :-: | :-: |
| `0` | `0` | `0` | `0` |
| `0` | `0` | `1` | `0` |
| `0` | `1` | `0` | `0` |
| `0` | `1` | `1` | `1` |
| `1` | `0` | `0` | `0` |
| `1` | `0` | `1` | `1` |
| `1` | `1` | `0` | `1` |
| `1` | `1` | `1` | `1` |

## 2. Ghi chú và ý nghĩa kỹ thuật

- **Định nghĩa:** majority là giá trị xuất hiện ít nhất 2 lần trong 3 bit. Slide phát biểu: có từ hai bit 0 trở lên thì trả về 0, ngược lại trả về 1 [Slide, trang 47].
- **Dùng khi debug:** bảng này giúp khoanh vùng lỗi (lỗi nằm ở hàm majority hay ở bước dịch register).
- **Phạm vi áp dụng:** bảng trên dùng cho **TinyA5/1** (3 register X, Y, Z dài 6, 8, 9 bit).
- **Với A5/1 đầy đủ:** 3 register dài 19, 22, 23 bit và hàm majority lấy trên 3 clocking bit khác là x8, y10, z10 [Slide, trang 51]. Bảng chân lý **không thay đổi**, chỉ thay vị trí clocking bit.

## 3. Ví dụ từ slide (Bước 0, slide trang 49)

- **Đọc 3 clocking bit ban đầu:** x₁ = `0`, y₃ = `0`, z₃ = `1` [Slide, trang 49].
- **Tra bảng:** tổ hợp (`0`, `0`, `1`) cho maj(0, 0, 1) = `0`.
- **Kết quả:**
  - X có x₁ = `0` = m → **dịch X** (slide ghi "quay X").
  - Y có y₃ = `0` = m → **dịch Y** (slide ghi "quay Y").
  - Z có z₃ = `1` ≠ m → **Z giữ nguyên**.
- Kết quả này trùng với slide: "m = maj(0,0,1) = 0 → quay X, quay Y" [Slide, trang 49].
