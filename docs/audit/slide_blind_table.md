# Bảng Đọc Slide Độc Lập (Slide Blind Table) - TinyA5/1

## 1. Thông số thanh ghi (Trích xuất nguyên văn từ Slide)

| Thông số | Thanh ghi X | Thanh ghi Y | Thanh ghi Z | Trang Slide |
| :--- | :--- | :--- | :--- | :--- |
| **Độ dài** | 6 bit | 8 bit | 9 bit | Trang 46 |
| **Vị trí bit điều khiển clock** | x₁ | y₃ | z₃ | Trang 47 |
| **Công thức tính bit phản hồi (t)** | t = x₂ ⊕ x₄ ⊕ x₅ | t = y₆ ⊕ y₇ | t = z₂ ⊕ z₇ ⊕ z₈ | Trang 48 |
| **Quy tắc quay thanh ghi (Dịch chuyển bit)** | Từ thấp sang cao (xⱼ = xⱼ₋₁), t vào vị trí 0 | Từ thấp sang cao (yⱼ = yⱼ₋₁), t vào vị trí 0 | Từ thấp sang cao (zⱼ = zⱼ₋₁), t vào vị trí 0 | Trang 48 |
| **Bit đầu ra tạo dòng khóa** | x₅ | y₇ | z₈ | Trang 49 |

- **Độ dài khóa K:** 23 bit (Trang 46).
- **Quy tắc phân bổ khóa:** 6 bit đầu vào thanh ghi X, 8 bit tiếp theo vào thanh ghi Y, 9 bit cuối vào thanh ghi Z (Ký tự đầu tiên mỗi đoạn là chỉ số 0) (Trang 46).
- **Ký hiệu chỉ số bit Slide sử dụng:** Đánh số từ 0 (x₀ đến x₅, y₀ đến y₇, z₀ đến z₈).

---

## 2. Dữ liệu ví dụ tính tay trong Slide (Trang 49–50)

- **Bản rõ (Plaintext - P):** `111` (Mã hóa cho ký tự "H")
- **Khóa (Key - K):** `10010101001110100110000`
- **Trạng thái ban đầu:**
  - Thanh ghi X = `100101` (6 bit)
  - Thanh ghi Y = `01001110` (8 bit)
  - Thanh ghi Z = `100110000` (9 bit)
- **Dòng khóa kỳ vọng (S):** `100`
- **Bản mã kỳ vọng (Ciphertext - C):** `011` (Mã hóa cho ký tự "D")

## 3. Kiểm tra tính toàn vẹn độc lập (Self-check)
- Phân bổ khóa K: `100101` + `01001110` + `100110000` = đúng 23 bit K.
- Mã hoá: P ⊕ S = `111` ⊕ `100` = `011` (Khớp C).
- Giải mã: C ⊕ S = `011` ⊕ `100` = `111` (Khớp P).