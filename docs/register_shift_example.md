# Ví dụ Minh họa Dịch Thanh ghi TinyA5/1 (Register Shift Examples)

Tài liệu này minh họa chi tiết quá trình tính bit phản hồi (feedback bit) và dịch bit cho cả 3 thanh ghi X, Y, Z dựa trên các bước tính toán trong Slide bài giảng Chương 2.

---

### 1. Register: X (Ví dụ Bước 0 từ Slide trang 48, 50)

- **Before**: `X = 100101` (chỉ số: `x0=1, x1=0, x2=0, x3=1, x4=0, x5=1`)
- **Feedback**: `t = x2 ⊕ x4 ⊕ x5 = 0 ⊕ 0 ⊕ 1 = 1`
- **Shift**: Mỗi bit chuyển từ vị trí `i` sang vị trí `i+1` (`xj = xj-1` với `j = 5..1`), bit cuối `x5 = 1` ra khỏi register.
- **New bit**: Feedback `t = 1` nạp vào vị trí `x0`.
- **After**: `X = 110010`
- **Slide**: Slide ghi kết quả `110010` [Slide, trang 48, 50]
- **Khớp?**: Có

---

### 2. Register: Y (Ví dụ Bước 0 từ Slide trang 48, 50)

- **Before**: `Y = 01001110` (chỉ số: `y0=0, y1=1, y2=0, y3=0, y4=1, y5=1, y6=1, y7=0`)
- **Feedback**: `t = y6 ⊕ y7 = 1 ⊕ 0 = 1`
- **Shift**: Mỗi bit chuyển từ vị trí `i` sang vị trí `i+1` (`yj = yj-1` với `j = 7..1`), bit cuối `y7 = 0` ra khỏi register.
- **New bit**: Feedback `t = 1` nạp vào vị trí `y0`.
- **After**: `Y = 10100111`
- **Slide**: Slide ghi kết quả `10100111` [Slide, trang 48, 50]
- **Khớp?**: Có

---

### 3. Register: Z (Ví dụ Bước 1 từ Slide trang 48, 50)

- **Before**: `Z = 100110000` (chỉ số: `z0=1, z1=0, z2=0, z3=1, z4=1, z5=0, z6=0, z7=0, z8=0`)
- **Feedback**: `t = z2 ⊕ z7 ⊕ z8 = 0 ⊕ 0 ⊕ 0 = 0`
- **Shift**: Mỗi bit chuyển từ vị trí `i` sang vị trí `i+1` (`zj = zj-1` với `j = 8..1`), bit cuối `z8 = 0` ra khỏi register.
- **New bit**: Feedback `t = 0` nạp vào vị trí `z0`.
- **After**: `Z = 010011000`
- **Slide**: Slide ghi kết quả `010011000` [Slide, trang 48, 50]
- **Khớp?**: Có
