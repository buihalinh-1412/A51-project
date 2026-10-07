# Ví dụ minh họa dịch register TinyA5/1 (Register Shift Examples)

Tài liệu này minh họa cách tính feedback bit và dịch bit cho 3 register X, Y, Z, lấy số liệu từ slide Chương 2. Công thức feedback và hướng dịch theo slide trang 48: xⱼ = xⱼ₋₁ (j từ chỉ số cao nhất xuống 1), sau đó x₀ = t; bit ở chỉ số cao nhất bị đẩy ra và bỏ đi.

## 1. Register X (Bước 0, slide trang 48–49)

- **Before:** X = `100101` (x₀=1, x₁=0, x₂=0, x₃=1, x₄=0, x₅=1)
- **Feedback:** t = x₂ ⊕ x₄ ⊕ x₅ = 0 ⊕ 0 ⊕ 1 = `1`
- **Shift:** mỗi bit chuyển từ vị trí i sang vị trí i+1 (xⱼ = xⱼ₋₁ với j = 5…1); bit x₅ = `1` bị đẩy ra.
- **New bit:** t = `1` vào vị trí x₀.
- **After:** X = `110010`
- **Slide:** slide ghi `110010` [Slide, trang 48, 49]
- **Kết luận:** Trùng khớp

## 2. Register Y (Bước 0, slide trang 48–49)

- **Before:** Y = `01001110` (y₀=0, y₁=1, y₂=0, y₃=0, y₄=1, y₅=1, y₆=1, y₇=0)
- **Feedback:** t = y₆ ⊕ y₇ = 1 ⊕ 0 = `1`
- **Shift:** mỗi bit chuyển từ vị trí i sang vị trí i+1 (yⱼ = yⱼ₋₁ với j = 7…1); bit y₇ = `0` bị đẩy ra.
- **New bit:** t = `1` vào vị trí y₀.
- **After:** Y = `10100111`
- **Slide:** slide ghi `10100111` [Slide, trang 48, 49]
- **Kết luận:** Trùng khớp

## 3. Register Z (Bước 1, slide trang 48–49)

- **Before:** Z = `100110000` (z₀=1, z₁=0, z₂=0, z₃=1, z₄=1, z₅=0, z₆=0, z₇=0, z₈=0)
- **Feedback:** t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = `0`
- **Shift:** mỗi bit chuyển từ vị trí i sang vị trí i+1 (zⱼ = zⱼ₋₁ với j = 8…1); bit z₈ = `0` bị đẩy ra.
- **New bit:** t = `0` vào vị trí z₀.
- **After:** Z = `010011000`
- **Slide:** slide ghi `010011000` [Slide, trang 48, 49]
- **Kết luận:** Trùng khớp

## 4. Register Z (Bước 2, slide trang 50) — có chỗ lệch

- **Before:** Z = `010011000` (z₀=0, z₁=1, z₂=0, z₃=0, z₄=1, z₅=1, z₆=0, z₇=0, z₈=0)
- **Feedback:** t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = `0`
- **Shift:** zⱼ = zⱼ₋₁ với j = 8…1; bit z₈ = `0` bị đẩy ra.
- **New bit:** t = `0` vào vị trí z₀.
- **After (tính theo quy tắc):** Z = `001001100`
- **Slide:** slide ghi `101001100` [Slide, trang 50]
- **Kết luận:** Không khớp → ghi nhận CONFLICT bên dưới, chuyển Hà Linh chốt ở TD-002.

```
CONFLICT-NL-001
Issue:            Giá trị Z sau Bước 2 của ví dụ TinyA5/1.
Lecture/Slide:    Z = 101001100 [Slide, trang 50].
Recalculation:    t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = 0, nên Z = 001001100.
Possible reason:  Lỗi đánh máy ở bit đầu (z₀) trên slide.
Impact:           Không ảnh hưởng keystream và bản mã của ví dụ, vì s₂ dùng z₈ = 0 ở cả hai cách. Có ảnh hưởng nếu chạy tiếp Bước 3 trở đi.
Status:           OPEN (TD-002)
```
