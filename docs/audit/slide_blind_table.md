# Bảng Đọc Slide Độc Lập (Slide Blind Table) - TinyA5/1

## 1. Thông số thanh ghi (Trích xuất nguyên văn từ Slide Chương 2)

| Thông số | Thanh ghi X | Thanh ghi Y | Thanh ghi Z | Vị trí Slide |
| :--- | :--- | :--- | :--- | :--- |
| **Độ dài (Length)** | 6 bit | 8 bit | 9 bit | Trang 46 |
| **Bit điều khiển nhịp (Clocking bit)** | x₁ | y₃ | z₃ | Trang 47 |
| **Vị trí khai thác (Tapping positions)** | x₂, x₄, x₅ | y₆, y₇ | z₂, z₇, z₈ | Trang 48 |
| **Công thức tính bit phản hồi (Feedback bit - t)** | t = x₂ ⊕ x₄ ⊕ x₅ | t = y₆ ⊕ y₇ | t = z₂ ⊕ z₇ ⊕ z₈ | Trang 48 |
| **Quy tắc dịch thanh ghi (Shift)** | Dịch sang phải (xⱼ = xⱼ₋₁), t vào vị trí x₀ | Dịch sang phải (yⱼ = yⱼ₋₁), t vào vị trí y₀ | Dịch sang phải (zⱼ = zⱼ₋₁), t vào vị trí z₀ | Trang 48 |
| **Bit đầu ra tạo dòng khóa (Keystream output bit)** | x₅ | y₇ | z₈ | Trang 49 |

- **Độ dài khóa (Key - K):** 23 bit (Trang 46).
- **Quy tắc phân bổ khóa vào thanh ghi:** 6 bit đầu vào thanh ghi X, 8 bit tiếp theo vào thanh ghi Y, 9 bit cuối vào thanh ghi Z (Ký tự đầu tiên mỗi đoạn nạp vào vị trí chỉ số 0) (Trang 46).
- **Quy ước đánh số chỉ số bit trong Slide:** Bắt đầu từ 0 (x₀ đến x₅, y₀ đến y₇, z₀ đến z₈) (Trang 46, 48).
- **Hàm chiếm đa số (Majority function):** $m = \text{maj}(x_1, y_3, z_3)$ (nếu có từ hai bit 0 trở lên thì $m = 0$, ngược lại $m = 1$) (Trang 47).
- **Công thức sinh bit dòng khóa (Keystream bit):** $s_i = x_5 \oplus y_7 \oplus z_8$ (tính sau khi các thanh ghi được chọn đã thực hiện dịch) (Trang 47, 49).

---

## 2. Dữ liệu ví dụ tính tay trong Slide (Trang 49–50)

- **Bản rõ (Plaintext - P):** `111` (Mã hóa cho ký tự "H")
- **Khóa (Key - K):** `10010101001110100110000` (23 bit)
- **Khởi tạo trạng thái ban đầu (Initial State):**
  - Thanh ghi X = `100101` (6 bit)
  - Thanh ghi Y = `01001110` (8 bit)
  - Thanh ghi Z = `100110000` (9 bit)
- **Dòng khóa kỳ vọng (Keystream - S):** `100` (gồm 3 bit: $s_0 = 1, s_1 = 0, s_2 = 0$)
- **Bản mã kỳ vọng (Ciphertext - C):** `011` (Mã hóa cho ký tự "D")

---

## 3. Kiểm tra tính toàn vẹn độc lập (Self-check)

- **Phân bổ khóa K:** `100101` (X) + `01001110` (Y) + `100110000` (Z) = `10010101001110100110000` (Đúng đủ 23 bit K).
- **Mã hóa (Encryption):** $C = P \oplus S = 111 \oplus 100 = 011$ (Khớp bản mã C).
- **Giải mã (Decryption):** $P = C \oplus S = 011 \oplus 100 = 111$ (Khôi phục chính xác bản rõ P).