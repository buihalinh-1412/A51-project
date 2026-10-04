# Tính tay TinyA5/1 (Hand Calculation)

## 1. Dữ liệu đầu vào

- **Bản rõ (Plaintext - P):** `111` (Mã hóa cho ký tự "H")
- **Khóa (Key - K):** `10010101001110100110000` (23 bit)
- **Khởi tạo trạng thái ban đầu (Initial State):**
  - Thanh ghi X (6 bit, chỉ số x₀ đến x₅): `100101`
  - Thanh ghi Y (8 bit, chỉ số y₀ đến y₇): `01001110`
  - Thanh ghi Z (9 bit, chỉ số z₀ đến z₈): `100110000`
- **Vị trí khai thác (Tapping positions) tính bit phản hồi (Feedback bit - t):**
  - Thanh ghi X: taps tại x₂, x₄, x₅ → t = x₂ ⊕ x₄ ⊕ x₅
  - Thanh ghi Y: taps tại y₆, y₇ → t = y₆ ⊕ y₇
  - Thanh ghi Z: taps tại z₂, z₇, z₈ → t = z₂ ⊕ z₇ ⊕ z₈
- **Bit điều khiển nhịp (Clocking bit):** x₁, y₃, z₃

---

## 2. Quá trình tính toán chi tiết theo từng chu kỳ dịch (Clock cycle)

### Chu kỳ 0
- **Trạng thái trước chu kỳ:**
  - X = `100101`, Y = `01001110`, Z = `100110000`
- **Trích xuất bit điều khiển nhịp:**
  - x₁ = 0, y₃ = 0, z₃ = 1
- **Tính hàm chiếm đa số (Majority function):**
  - m = maj(0, 0, 1) = 0
- **Xác định thanh ghi được dịch:**
  - x₁ = 0 = m → Thanh ghi X dịch
  - y₃ = 0 = m → Thanh ghi Y dịch
  - z₃ = 1 ≠ m → Thanh ghi Z đứng yên
- **Thực hiện dịch thanh ghi (Shift):**
  - **Dịch X:**
    - Bit phản hồi: t = x₂ ⊕ x₄ ⊕ x₅ = 0 ⊕ 0 ⊕ 1 = 1
    - Dịch các bit sang phải, đưa t = 1 vào x₀: X = `110010`
  - **Dịch Y:**
    - Bit phản hồi: t = y₆ ⊕ y₇ = 1 ⊕ 0 = 1
    - Dịch các bit sang phải, đưa t = 1 vào y₀: Y = `10100111`
  - **Thanh ghi Z đứng yên:**
    - Z = `100110000`
- **Bit dòng khóa sinh ra (Keystream bit):**
  - s₀ = x₅ ⊕ y₇ ⊕ z₈ = 0 ⊕ 1 ⊕ 0 = **1**

---

### Chu kỳ 1
- **Trạng thái trước chu kỳ:**
  - X = `110010`, Y = `10100111`, Z = `100110000`
- **Trích xuất bit điều khiển nhịp:**
  - x₁ = 1, y₃ = 0, z₃ = 1
- **Tính hàm chiếm đa số (Majority function):**
  - m = maj(1, 0, 1) = 1
- **Xác định thanh ghi được dịch:**
  - x₁ = 1 = m → Thanh ghi X dịch
  - y₃ = 0 ≠ m → Thanh ghi Y đứng yên
  - z₃ = 1 = m → Thanh ghi Z dịch
- **Thực hiện dịch thanh ghi (Shift):**
  - **Dịch X:**
    - Các bit tại vị trí tap: x₂ = 0, x₄ = 1, x₅ = 0
    - Bit phản hồi: t = x₂ ⊕ x₄ ⊕ x₅ = 0 ⊕ 1 ⊕ 0 = 1
    - Dịch các bit sang phải, đưa t = 1 vào x₀: X = `111001`
  - **Thanh ghi Y đứng yên:**
    - Y = `10100111`
  - **Dịch Z:**
    - Các bit tại vị trí tap: z₂ = 0, z₇ = 0, z₈ = 0
    - Bit phản hồi: t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = 0
    - Dịch các bit sang phải, đưa t = 0 vào z₀: Z = `010011000`
- **Bit dòng khóa sinh ra (Keystream bit):**
  - s₁ = x₅ ⊕ y₇ ⊕ z₈ = 1 ⊕ 1 ⊕ 0 = **0**

---

### Chu kỳ 2
- **Trạng thái trước chu kỳ:**
  - X = `111001`, Y = `10100111`, Z = `010011000`
- **Trích xuất bit điều khiển nhịp:**
  - x₁ = 1, y₃ = 0, z₃ = 0
- **Tính hàm chiếm đa số (Majority function):**
  - m = maj(1, 0, 0) = 0
- **Xác định thanh ghi được dịch:**
  - x₁ = 1 ≠ m → Thanh ghi X đứng yên
  - y₃ = 0 = m → Thanh ghi Y dịch
  - z₃ = 0 = m → Thanh ghi Z dịch
- **Thực hiện dịch thanh ghi (Shift):**
  - **Thanh ghi X đứng yên:**
    - X = `111001`
  - **Dịch Y:**
    - Các bit tại vị trí tap: y₆ = 1, y₇ = 1
    - Bit phản hồi: t = y₆ ⊕ y₇ = 1 ⊕ 1 = 0
    - Dịch các bit sang phải, đưa t = 0 vào y₀: Y = `01010011`
  - **Dịch Z:**
    - Các bit tại vị trí tap: z₂ = 0, z₇ = 0, z₈ = 0
    - Bit phản hồi theo quy tắc: t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = 0
    - Dịch các bit sang phải, đưa t = 0 vào z₀: Z = `001001100` *(Lưu ý: Slide in là `101001100`, xem mục DISCREPANCY bên dưới)*
- **Bit dòng khóa sinh ra (Keystream bit):**
  - s₂ = x₅ ⊕ y₇ ⊕ z₈ = 1 ⊕ 1 ⊕ 0 = **0**

---

## 3. Bảng tổng hợp trạng thái đầy đủ 3 bước (12 cột)

| Bước | X (trước) | Y (trước) | Z (trước) | Bít xét (x₁, y₃, z₃) | Hàm chiếm đa số (m) | Thanh ghi được dịch | X (sau) | Y (sau) | Z (sau) | Bít cuối (x₅, y₇, z₈) | Bít sinh ra (sᵢ) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | 100101 | 01001110 | 100110000 | 0, 0, 1 | 0 | X, Y | 110010 | 10100111 | 100110000 | 0, 1, 0 | **1** |
| **1** | 110010 | 10100111 | 100110000 | 1, 0, 1 | 1 | X, Z | 111001 | 10100111 | 010011000 | 1, 1, 0 | **0** |
| **2** | 111001 | 10100111 | 010011000 | 1, 0, 0 | 0 | Y, Z | 111001 | 01010011 | 001001100* | 1, 1, 0 | **0** |


---

## 4. Dòng khóa, Mã hóa và Giải mã

- **Dòng khóa hoàn chỉnh (Keystream - S):**
  - Ghép các bit dòng khóa qua 3 bước: S = s₀s₁s₂ = `100`
  - So sánh với Slide trang 50: S = `100` (**Đã khớp*)
- **Mã hóa (Encryption):**
  - C = P ⊕ S = `111` ⊕ `100` = `011` (Mã hóa ký tự "H" thành "D")
  - So sánh với Slide trang 50: C = `011` (**Đã khớp**)
- **Giải mã (Decryption):**
  - P = C ⊕ S = `011` ⊕ `100` = `111` (Khôi phục ký tự "H")
  - So sánh với bản rõ ban đầu: P = `111` (**Đã khớp**)

---

## 5. Điểm sai lệch Slide (DISCREPANCY)

```text
DISCREPANCY

Slide:                  Z sau bước 2 = 101001100

Recalculation:          Z sau bước 2 = 001001100
                        Các bước tính chi tiết:
                        - Z trước bước 2 = 010011000 (z₀=0, z₁=1, z₂=0, z₃=0, z₄=1, z₅=1, z₆=0, z₇=0, z₈=0)
                        - Vị trí tap theo công thức Trang 48: z₂, z₇, z₈
                        - Giá trị trích xuất: z₂ = 0, z₇ = 0, z₈ = 0
                        - Bit phản hồi: t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = 0
                        - Dịch phải 1 bit và nạp t vào đầu: z₀ = 0
                        - Kết quả tính toán chuẩn xác: 001001100

Possible reason:        Có thể do lỗi đánh máy.
Effect on final output: Không ảnh hưởng quá nhiều.