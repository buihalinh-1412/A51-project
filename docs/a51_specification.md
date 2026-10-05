# Đặc tả A5/1

> **Owner:** Lại Hoàng Thế Vũ  
> **Branch:** `docs/vu-a51`  
> **Giai đoạn:** Phase 1 - Specification and Verification  
> **Nguồn nội bộ chính:** Slide Chương 2 - Mã hoá khoá đối xứng, trang 45-52  
> **Trạng thái:** Đang xây dựng

---

## 1. Tổng quan

### 1.1. A5/1 là gì?

A5/1 là một **mã dòng (Stream Cipher)** được sử dụng trong mạng điện thoại GSM để bảo mật dữ liệu trong quá trình liên lạc giữa điện thoại và trạm thu phát sóng vô tuyến.

Theo slide môn học:

- Đơn vị mã hoá của A5/1 là **1 bit**.
- Bộ sinh số mỗi lần sinh ra một bit `0` hoặc `1`.
- Bit sinh ra được sử dụng trong phép XOR với dữ liệu.
- Trong bài học, A5/1 đầy đủ được mô tả bằng cách tổng quát hóa từ TinyA5/1.

**Nguồn:** [S1, trang 45]

### 1.2. Cấu trúc tổng quát

A5/1 sử dụng ba thanh ghi:

```text
X
Y
Z
```

Độ dài của các thanh ghi trong A5/1 đầy đủ:

```text
X = 19 bit
Y = 22 bit
Z = 23 bit
```

**Nguồn:** [S1, trang 51]

### 1.3. Nguyên tắc hoạt động

Ở mỗi bước sinh số:

```text
Đọc các bit dùng cho majority
        ↓
Tính hàm majority
        ↓
Xác định thanh ghi được quay
        ↓
Tính feedback và quay thanh ghi
        ↓
Tính bit sinh ra
        ↓
Dùng bit sinh ra làm keystream
```

Theo slide, bit sinh ra được tính:

```text
sᵢ = x₈ XOR y₁₀ XOR z₁₀
```

**Nguồn:** [S1, trang 51]

---

## 2. Các thanh ghi

### 2.1. Bảng tổng hợp

| Thông số | X | Y | Z | Nguồn | Nhãn |
|---|---:|---:|---:|---|---|
| Độ dài | 19 bit | 22 bit | 23 bit | [S1, trang 51] | VERIFIED |
| Chỉ số | `x₀ ... x₁₈` | `y₀ ... y₂₁` | `z₀ ... z₂₂` | [S1, trang 51] | VERIFIED |
| Bit majority | `x₈` | `y₁₀` | `z₁₀` | [S1, trang 51] | VERIFIED |
| Feedback taps | `x₁₃, x₁₆, x₁₇, x₁₈` | `y₂₀, y₂₁` | `z₇, z₂₀, z₂₁, z₂₂` | [S1, trang 51] | VERIFIED |
| Hướng quay | `xⱼ = xⱼ₋₁` | `yⱼ = yⱼ₋₁` | `zⱼ = zⱼ₋₁` | [S1, trang 51] | VERIFIED |
| Bit mới | `x₀ = t` | `y₀ = t` | `z₀ = t` | [S1, trang 51] | VERIFIED |

### 2.2. Thanh ghi X

Thanh ghi X gồm 19 bit:

```text
x₀, x₁, x₂, ..., x₁₈
```

Feedback:

```text
t = x₁₃ XOR x₁₆ XOR x₁₇ XOR x₁₈
```

Sau khi tính `t`, thực hiện:

```text
xⱼ = xⱼ₋₁
```

với:

```text
j = 18, 17, ..., 1
```

Sau đó:

```text
x₀ = t
```

**Nguồn:** [S1, trang 51]

### 2.3. Thanh ghi Y

Thanh ghi Y gồm 22 bit:

```text
y₀, y₁, y₂, ..., y₂₁
```

Feedback:

```text
t = y₂₀ XOR y₂₁
```

Sau khi tính `t`, thực hiện:

```text
yⱼ = yⱼ₋₁
```

với:

```text
j = 21, 20, ..., 1
```

Sau đó:

```text
y₀ = t
```

**Nguồn:** [S1, trang 51]

### 2.4. Thanh ghi Z

Thanh ghi Z gồm 23 bit:

```text
z₀, z₁, z₂, ..., z₂₂
```

Feedback:

```text
t = z₇ XOR z₂₀ XOR z₂₁ XOR z₂₂
```

Sau khi tính `t`, thực hiện:

```text
zⱼ = zⱼ₋₁
```

với:

```text
j = 22, 21, ..., 1
```

Sau đó:

```text
z₀ = t
```

**Nguồn:** [S1, trang 51]

### 2.5. Kiểm tra tổng độ dài

```text
X = 19 bit
Y = 22 bit
Z = 23 bit
----------------
Tổng = 64 bit
```

Do đó:

```text
19 + 22 + 23 = 64 bit
```

---

## 3. Majority clocking

### 3.1. Các bit dùng cho hàm majority

Theo slide, hàm majority được tính trên ba bit:

```text
x₈
y₁₀
z₁₀
```

Công thức:

```text
m = maj(x₈, y₁₀, z₁₀)
```

**Nguồn:** [S1, trang 51]

### 3.2. Hàm majority

Hàm majority trả về giá trị xuất hiện ít nhất hai lần trong ba bit.

| x₈ | y₁₀ | z₁₀ | m |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

### 3.3. Quy tắc quay

Sau khi tính:

```text
m = maj(x₈, y₁₀, z₁₀)
```

thực hiện:

```text
Nếu x₈ = m → quay X

Nếu y₁₀ = m → quay Y

Nếu z₁₀ = m → quay Z
```

Như vậy, không phải lúc nào cả ba thanh ghi cũng được quay.

**Nguồn:** [S1, trang 47 và 51]

---

## 4. Nạp key

### 4.1. Thông tin từ slide

Slide cung cấp đầy đủ quy trình phân bổ key cho **TinyA5/1**, nhưng không trình bày chi tiết toàn bộ quy trình nạp key của **A5/1 đầy đủ**.

Vì vậy các thông tin sau chưa được lấy từ slide:

| Nội dung | Trạng thái |
|---|---|
| Độ dài key A5/1 đầy đủ | `UNVERIFIED` |
| Trạng thái ban đầu của X, Y, Z | `UNVERIFIED` |
| Số chu kỳ nạp key | `UNVERIFIED` |
| Thứ tự bit của key | `UNVERIFIED` |
| Cách đưa từng bit key vào các thanh ghi | `UNVERIFIED` |
| Cách quay các thanh ghi trong giai đoạn nạp key | `UNVERIFIED` |

### 4.2. Quy trình cần bổ sung

Bản đặc tả hoàn chỉnh phải trả lời:

1. Key có bao nhiêu bit?
2. Key được biểu diễn dưới dạng nào?
3. Bit nào được đưa vào trước?
4. Mỗi chu kỳ bit key được xử lý như thế nào?
5. X, Y và Z có quay đồng thời hay theo majority?
6. Có bao nhiêu chu kỳ nạp key?
7. Trạng thái của X, Y và Z trước khi nạp key là gì?

**Trạng thái hiện tại:** `UNVERIFIED`

---

## 5. Nạp frame

### 5.1. Thông tin từ slide

Slide được cung cấp không trình bày chi tiết quá trình nạp frame của A5/1 đầy đủ.

Các nội dung cần xác minh:

| Nội dung | Trạng thái |
|---|---|
| Độ dài frame | `UNVERIFIED` |
| Frame lấy từ đâu | `UNVERIFIED` |
| Thứ tự bit | `UNVERIFIED` |
| Số chu kỳ nạp frame | `UNVERIFIED` |
| Cách quay X, Y, Z khi nạp frame | `UNVERIFIED` |

### 5.2. Quy trình cần bổ sung

Bản đặc tả hoàn chỉnh phải mô tả:

```text
Trạng thái trước khi nạp frame
        ↓
Đọc bit frame
        ↓
Cập nhật X, Y, Z
        ↓
Lặp đủ số chu kỳ
        ↓
Trạng thái sau khi nạp frame
```

**Trạng thái hiện tại:** `UNVERIFIED`

---

## 6. Warm-up

Warm-up là giai đoạn chạy bộ sinh sau khi hoàn thành quá trình khởi tạo và trước khi lấy keystream sử dụng để mã hóa.

Slide được cung cấp **không nêu đầy đủ quy trình warm-up của A5/1 đầy đủ**.

Các nội dung cần xác minh từ nguồn ngoài:

| Nội dung | Trạng thái |
|---|---|
| Số chu kỳ warm-up | `UNVERIFIED` |
| Có sử dụng majority clocking hay không | `UNVERIFIED` |
| Output trong warm-up có bị bỏ hay không | `UNVERIFIED` |
| Trạng thái sau warm-up | `UNVERIFIED` |

> Không tự điền thông số warm-up khi chưa có nguồn.

---

## 7. Sinh keystream

### 7.1. Quy trình

Theo slide, mỗi bước sinh số thực hiện:

```text
Bước 1: Đọc x₈, y₁₀, z₁₀

Bước 2: Tính
m = maj(x₈, y₁₀, z₁₀)

Bước 3:
Nếu x₈ = m → quay X

Bước 4:
Nếu y₁₀ = m → quay Y

Bước 5:
Nếu z₁₀ = m → quay Z

Bước 6:
Tính bit sinh ra
sᵢ = x₈ XOR y₁₀ XOR z₁₀
```

**Nguồn:** [S1, trang 51]

### 7.2. Công thức bit sinh ra

```text
sᵢ = x₈ XOR y₁₀ XOR z₁₀
```

Trong đó:

- `x₈`: bit 8 của X;
- `y₁₀`: bit 10 của Y;
- `z₁₀`: bit 10 của Z.

**Nguồn:** [S1, trang 51]

### 7.3. Điểm cần chú ý

Vị trí các bit được sử dụng trong công thức trên là thông tin trực tiếp từ slide.

Do đó, trong bản đặc tả hiện tại:

```text
Output X = x₈
Output Y = y₁₀
Output Z = z₁₀
```

được hiểu theo công thức sinh bit của slide.

Nếu nguồn ngoài sử dụng vị trí output khác, phải ghi nhận thành `CONFLICT` thay vì tự xóa một nguồn.

---

## 8. Mã hóa

A5/1 là mã dòng và bit keystream được sử dụng trong phép XOR với bản rõ.

Công thức:

```text
C = P XOR S
```

Trong đó:

```text
P = Plaintext
S = Keystream
C = Ciphertext
```

**Nguồn:** [S1, trang 42 và 47]

### 8.1. Ví dụ

Ví dụ trong phần TinyA5/1 của slide:

```text
P = 111
S = 100

C = 111 XOR 100
C = 011
```

**Nguồn:** [S1, trang 49-50]

---

## 9. Giải mã

Giải mã sử dụng lại keystream:

```text
P = C XOR S
```

### 9.1. Ví dụ

```text
C = 011
S = 100

P = 011 XOR 100
P = 111
```

**Nguồn:** [S1, trang 50]

Do tính chất của phép XOR:

```text
(P XOR S) XOR S = P
```

---

## 10. Bit ordering

### 10.1. Chỉ số bit

Slide TinyA5/1 minh họa các bit theo chỉ số bắt đầu từ `0`.

Ví dụ:

```text
X:
0 1 2 3 4 5

Y:
0 1 2 3 4 5 6 7

Z:
0 1 2 3 4 5 6 7 8
```

Slide A5/1 đầy đủ sử dụng:

```text
X:
x₀ ... x₁₈

Y:
y₀ ... y₂₁

Z:
z₀ ... z₂₂
```

**Nguồn:** [S1, trang 48 và 51]

### 10.2. Quy tắc dịch

Đối với X:

```text
xⱼ = xⱼ₋₁
```

với:

```text
j = 18, 17, ..., 1
```

sau đó:

```text
x₀ = t
```

Đối với Y:

```text
yⱼ = yⱼ₋₁
```

với:

```text
j = 21, 20, ..., 1
```

sau đó:

```text
y₀ = t
```

Đối với Z:

```text
zⱼ = zⱼ₋₁
```

với:

```text
j = 22, 21, ..., 1
```

sau đó:

```text
z₀ = t
```

**Nguồn:** [S1, trang 51]

### 10.3. Ý nghĩa

Có thể hiểu đơn giản:

```text
        feedback t
             ↓
X:  [0] [1] [2] ... [18]
      ↑
   bit mới
```

Sau một lần quay, các bit cũ dịch sang vị trí có chỉ số lớn hơn và `t` được đưa vào vị trí `0`.

---

## 11. Sources

### S1 - Slide môn học

**Tên:** Chương 2 - MÃ HOÁ KHOÁ ĐỐI XỨNG (MÃ HOÁ KHOÁ BÍ MẬT)

**Đơn vị:** Đại học Kinh tế Quốc dân - Khoa Công nghệ Thông tin

**Giảng viên:** ThS. Nguyễn Quốc Thái

**Phần sử dụng:**

- Mã dòng
- A5/1
- TinyA5/1
- Majority
- Feedback
- Quay register
- Ví dụ TinyA5/1

**Các trang sử dụng:** 45-52

### S2 - Tài liệu phân công Phase 1

**Tên:** Tài liệu đặc tả và xác minh A5/1 / TinyA5/1

**Phần sử dụng:**

- Phân công nhiệm vụ V-01 đến V-07
- Cấu trúc `a51_specification.md`
- Các vấn đề TD-001 đến TD-005
- Các thông số cần xác minh
- Quy tắc nguồn và trạng thái `VERIFIED`, `SINGLE-SOURCE`, `CONFLICT`, `UNVERIFIED`

---

## 12. TinyA5/1 và A5/1 đầy đủ

| Thuộc tính | TinyA5/1 | A5/1 đầy đủ |
|---|---|---|
| Số register | 3 | 3 |
| Tên register | X, Y, Z | X, Y, Z |
| Độ dài X | 6 bit | 19 bit |
| Độ dài Y | 8 bit | 22 bit |
| Độ dài Z | 9 bit | 23 bit |
| Độ dài key | 23 bit | Chưa được nêu đầy đủ trong slide |
| Majority | `maj(x₂, y₃, z₃)` | `maj(x₈, y₁₀, z₁₀)` |
| Feedback X | Theo slide TinyA5/1 | `x₁₃ XOR x₁₆ XOR x₁₇ XOR x₁₈` |
| Feedback Y | Theo slide TinyA5/1 | `y₂₀ XOR y₂₁` |
| Feedback Z | Theo slide TinyA5/1 | `z₇ XOR z₂₀ XOR z₂₁ XOR z₂₂` |
| Bit sinh ra | Theo slide TinyA5/1 | `x₈ XOR y₁₀ XOR z₁₀` |
| Mục đích | Mô hình thu nhỏ để học và tính tay | Mô hình A5/1 đầy đủ |

**Nguồn:** [S1, trang 45-52]

### 12.1. Ví dụ TinyA5/1 trong slide

Bản rõ:

```text
P = 111
```

Khóa:

```text
K = 10010101001110100110000
```

Phân bổ:

```text
X = 100101
Y = 01001110
Z = 100110000
```

Kiểm tra:

```text
6 + 8 + 9 = 23 bit
```

**Nguồn:** [S1, trang 49]

### 12.2. Kết quả ví dụ

Sau ba bước sinh:

```text
S = 100
```

Mã hóa:

```text
C = P XOR S
C = 111 XOR 100
C = 011
```

Giải mã:

```text
P = C XOR S
P = 011 XOR 100
P = 111
```

**Nguồn:** [S1, trang 50]

---

## 13. Open issues

### TD-001 - Bit output của A5/1

**Issue:**

Cần xác minh quy ước bit output của A5/1 giữa slide và nguồn ngoài.

**Lecture/Slide:**

```text
sᵢ = x₈ XOR y₁₀ XOR z₁₀
```

**Nguồn:** [S1, trang 51]

**Impact:**

Ảnh hưởng trực tiếp đến keystream.

**Status:**

`OPEN`

---

### TD-002 - Điểm lệch trong ví dụ TinyA5/1

**Issue:**

Tài liệu nhóm ghi nhận có điểm cần đối chiếu giữa trạng thái Z trong ví dụ tính tay của slide và phép tính lại theo quy tắc.

**Impact:**

Cần xác định có ảnh hưởng đến keystream và ciphertext hay không.

**Status:**

`OPEN`

---

### TD-003 - Chỉ số và thứ tự bit

**Issue:**

Slide sử dụng chỉ số bắt đầu từ `0`, nhưng cần khóa cách ánh xạ ký hiệu slide sang quy ước code của nhóm.

**Lecture/Slide:**

```text
X: x₀ ... x₁₈
Y: y₀ ... y₂₁
Z: z₀ ... z₂₂
```

**Nguồn:** [S1, trang 51]

**Impact:**

Ảnh hưởng đến clocking bit, feedback tap, output và cách cài đặt.

**Status:**

`OPEN`

---

### TD-004 - Key, frame và warm-up

**Issue:**

Slide hiện tại không mô tả đầy đủ quy trình:

- Nạp key.
- Nạp frame.
- Warm-up.
- Số chu kỳ của từng giai đoạn.
- Register nào được quay trong từng giai đoạn.
- Output có bị bỏ trong warm-up hay không.

**Status:**

`OPEN`

---

### TD-005 - Dữ liệu dài hơn một đoạn keystream

**Issue:**

Slide không mô tả cách xử lý dữ liệu dài hơn một đoạn keystream.

**Cần xác minh:**

- Một lần sinh keystream tạo bao nhiêu bit.
- Khi dữ liệu dài hơn thì xử lý tiếp như thế nào.
- Có cần một frame mới hay không.
- Quy tắc chia dữ liệu thành các đoạn.

**Status:**

`OPEN`

---

## Kết luận

Từ slide môn học có thể xác định chắc chắn các thông số cốt lõi của A5/1 đầy đủ:

```text
X = 19 bit
Y = 22 bit
Z = 23 bit

m = maj(x₈, y₁₀, z₁₀)

Feedback X:
t = x₁₃ XOR x₁₆ XOR x₁₇ XOR x₁₈

Feedback Y:
t = y₂₀ XOR y₂₁

Feedback Z:
t = z₇ XOR z₂₀ XOR z₂₁ XOR z₂₂

Bit sinh ra:
sᵢ = x₈ XOR y₁₀ XOR z₁₀
```
