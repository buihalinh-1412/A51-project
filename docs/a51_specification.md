# Đặc tả A5/1

> **Owner:** Lại Hoàng Thế Vũ  
> **Branch:** `docs/vu-a51`  
> **Giai đoạn:** Phase 1 - Specification and Verification  
> **File:** `docs/a51_specification.md`  
> **Trạng thái:** Bản đặc tả Phase 1, đã đối chiếu slide và các nguồn kỹ thuật bên ngoài
>
> **Quy ước nguồn trong tài liệu:**
>
> - `[S1]` = Slide môn học, Chương 2 - Mã hoá khoá đối xứng, trang 45-52.
> - `[S2]` = Marc Briceno, Ian Goldberg, David Wagner, A5/1 Pedagogical Implementation (`A5.1.c`).
> - `[S3]` = Alex Biryukov, Adi Shamir, David Wagner, *Real Time Cryptanalysis of A5/1 on a PC*.
> - `[S4]` = Thomas Gendrullis, Michael Novotný, Andreas Rupp, *A Real-World Attack Breaking A5/1*.
> - `[S5]` = 3GPP TS 43.020 / ETSI TS 143 020, phần giao diện Algorithm A5.

---

## 1. Overview

### 1.1. Hệ mã A5/1

A5/1 là một **mã dòng (Stream Cipher)** được sử dụng trong mạng điện thoại GSM để bảo mật dữ liệu trong quá trình liên lạc giữa máy điện thoại và trạm thu phát sóng vô tuyến.

Đơn vị mã hoá của A5/1 là **1 bít**. Bộ sinh số mỗi lần sinh ra một bít `0` hoặc `1` để sử dụng trong phép XOR với dữ liệu.

Trong phạm vi bài học, mô hình thu nhỏ của A5/1 được gọi là **TinyA5/1**.

**Nguồn:** `[S1, trang 45]`  
**Nhãn:** `VERIFIED`

---

### 1.2. Cấu trúc tổng quát

A5/1 sử dụng ba thanh ghi:

```text
X
Y
Z
```

Độ dài:

```text
X = 19 bít
Y = 22 bít
Z = 23 bít
```

Tổng số bít:

```text
19 + 22 + 23 = 64 bít
```

Trong các nguồn kỹ thuật bên ngoài, ba thanh ghi này thường được ký hiệu tương ứng:

```text
X ↔ R1
Y ↔ R2
Z ↔ R3
```

Trong tài liệu này, ký hiệu `X`, `Y`, `Z` được sử dụng làm ký hiệu chính.

**Nguồn:** `[S1, trang 51]`; `[S2]`; `[S3]`  
**Nhãn:** `VERIFIED`

---

### 1.3. Quy trình hoạt động

Quy trình tổng quát của A5/1:

```text
Khởi tạo X, Y, Z
        ↓
Nạp khóa K
        ↓
Nạp frame
        ↓
Warm-up
        ↓
Sinh dãy bít S
        ↓
P XOR S
        ↓
C
```

Trong đó:

```text
P = bản rõ
S = dãy bít sinh ra
C = bản mã
```

---

## 2. Registers

### 2.1. Bảng tổng hợp

| Thông số | X | Y | Z | Nguồn | Nhãn |
|---|---:|---:|---:|---|---|
| Độ dài | 19 bít | 22 bít | 23 bít | [S1, trang 51]; [S2]; [S3] | VERIFIED |
| Chỉ số | `x_0 ... x_18` | `y_0 ... y_21` | `z_0 ... z_22` | [S1, trang 51]; [S2]; [S4] | VERIFIED |
| Bít dùng cho hàm `maj` | `x_8` | `y_10` | `z_10` | [S1, trang 51]; [S2]; [S4] | VERIFIED |
| Feedback taps | `x_13, x_16, x_17, x_18` | `y_20, y_21` | `z_7, z_20, z_21, z_22` | [S1, trang 51]; [S2]; [S4] | VERIFIED |
| Quy tắc quay | `x_j = x_{j-1}` | `y_j = y_{j-1}` | `z_j = z_{j-1}` | [S1, trang 51]; [S2] | VERIFIED |
| Bít mới | `x_0 = t` | `y_0 = t` | `z_0 = t` | [S1, trang 51]; [S2] | VERIFIED |
| Bít sinh ra theo slide | `x_8` | `y_10` | `z_10` | [S1, trang 51] | VERIFIED theo slide |

---

### 2.2. Quy ước đánh số bít

Các thanh ghi được đánh số bắt đầu từ `0`:

```text
X: x_0, x_1, ..., x_18
Y: y_0, y_1, ..., y_21
Z: z_0, z_1, ..., z_22
```

**Nguồn:** `[S1, trang 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

### 2.3. Thanh ghi X

Thanh ghi X có:

```text
19 bít
```

Các vị trí:

```text
x_0, x_1, ..., x_18
```

Bít feedback:

```text
t = x_13 XOR x_16 XOR x_17 XOR x_18
```

Quay X:

```text
x_j = x_{j-1}
```

với:

```text
j = 18, 17, ..., 1
```

Sau đó:

```text
x_0 = t
```

Bít mới `t` được đưa vào vị trí `x_0`.

**Nguồn:** `[S1, trang 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

### 2.4. Thanh ghi Y

Thanh ghi Y có:

```text
22 bít
```

Các vị trí:

```text
y_0, y_1, ..., y_21
```

Bít feedback:

```text
t = y_20 XOR y_21
```

Quay Y:

```text
y_j = y_{j-1}
```

với:

```text
j = 21, 20, ..., 1
```

Sau đó:

```text
y_0 = t
```

**Nguồn:** `[S1, trang 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

### 2.5. Thanh ghi Z

Thanh ghi Z có:

```text
23 bít
```

Các vị trí:

```text
z_0, z_1, ..., z_22
```

Bít feedback:

```text
t = z_7 XOR z_20 XOR z_21 XOR z_22
```

Quay Z:

```text
z_j = z_{j-1}
```

với:

```text
j = 22, 21, ..., 1
```

Sau đó:

```text
z_0 = t
```

**Nguồn:** `[S1, trang 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

### 2.6. Quy tắc quay chung

Với mỗi thanh ghi:

1. Tính bít feedback `t`.
2. Dịch các bít sang vị trí có chỉ số lớn hơn.
3. Đưa `t` vào vị trí chỉ số `0`.

Ví dụ với X:

```text
t = x_13 XOR x_16 XOR x_17 XOR x_18

x_18 = old x_17
x_17 = old x_16
...
x_1 = old x_0

x_0 = t
```

---

### 2.7. Kiểm tra tổng độ dài

```text
X = 19 bít
Y = 22 bít
Z = 23 bít
----------------
Tổng = 64 bít
```

Kết quả:

```text
19 + 22 + 23 = 64 bít
```

**Nhãn:** `VERIFIED`

---

## 3. Majority clocking

### 3.1. Hàm `maj`

Ba bít dùng để tính hàm chiếm đa số:

```text
x_8
y_10
z_10
```

Công thức:

```text
m = maj(x_8, y_10, z_10)
```

Nếu trong ba bít có ít nhất hai bít `0`:

```text
m = 0
```

Nếu trong ba bít có ít nhất hai bít `1`:

```text
m = 1
```

**Nguồn:** `[S1, trang 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

### 3.2. Bảng hàm `maj`

| x_8 | y_10 | z_10 | m |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

---

### 3.3. Quy tắc quay

Sau khi tính:

```text
m = maj(x_8, y_10, z_10)
```

thực hiện:

```text
Nếu x_8 = m → Quay X
Nếu y_10 = m → Quay Y
Nếu z_10 = m → Quay Z
```

Do `m` là giá trị chiếm đa số nên trong mỗi bước có ít nhất hai trong ba thanh ghi được quay.

**Nguồn:** `[S1, trang 47, 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

## 4. Key loading

### 4.1. Khóa K

Đối với TinyA5/1:

```text
K = 23 bít
```

Khóa được phân bổ vào ba thanh ghi:

```text
K → XYZ
```

**Nguồn:** `[S1, trang 46-47]`

Đối với A5/1 đầy đủ:

```text
K = 64 bít
```

S2 biểu diễn khóa dưới dạng:

```text
8 byte
```

S5 quy định:

```text
Kc = 64 bít
```

**Nguồn:** `[S2]`; `[S5]`  
**Nhãn:** `VERIFIED`

---

### 4.2. Trạng thái ban đầu

Trước khi nạp khóa:

```text
X = 0
Y = 0
Z = 0
```

**Nguồn:** `[S2]`  
**Nhãn:** `SINGLE-SOURCE`

---

### 4.3. Số lần nạp

Quá trình nạp khóa thực hiện:

```text
64 lần
```

Mỗi lần xử lý một bít của khóa.

Trong giai đoạn này:

- X, Y, Z đều được quay;
- không sử dụng điều kiện `maj`;
- bít khóa hiện tại được XOR vào cả ba thanh ghi.

**Nguồn:** `[S2]`; `[S3]`  
**Nhãn:** `VERIFIED`

---

### 4.4. Thứ tự bít của khóa

S2 lấy bít khóa bằng:

```text
(key[i/8] >> (i & 7)) & 1
```

với:

```text
i = 0 ... 63
```

Trong từng byte, các bít được xử lý theo:

```text
LSB → MSB
```

tức:

```text
b_0 → b_1 → ... → b_7
```

**Nguồn:** `[S2]`  
**Nhãn:** `SINGLE-SOURCE`

---

### 4.5. Quy trình nạp khóa

```text
Khởi tạo:

X = 0
Y = 0
Z = 0

Lặp i = 0 ... 63:

    Quay X
    Quay Y
    Quay Z

    Đọc key_bit

    XOR key_bit vào X
    XOR key_bit vào Y
    XOR key_bit vào Z
```

**Nguồn:** `[S2]`; `[S3]`

---

### 4.6. Ví dụ ba bít đầu

Với byte đầu:

```text
0x12 = 00010010
```

Theo thứ tự LSB-first:

```text
bít 0 = 0
bít 1 = 1
bít 2 = 0
```

Ba lần đầu:

```text
Lần 0:
Quay X, Y, Z
XOR 0 vào X, Y, Z

Lần 1:
Quay X, Y, Z
XOR 1 vào X, Y, Z

Lần 2:
Quay X, Y, Z
XOR 0 vào X, Y, Z
```

**Nguồn:** `[S2]`

---

### 4.7. Bảng kiểm chứng key loading

| Nội dung | Kết luận | Nguồn | Nhãn |
|---|---|---|---|
| Độ dài khóa | 64 bít | [S2]; [S5] | VERIFIED |
| Trạng thái ban đầu | X = Y = Z = 0 | [S2] | SINGLE-SOURCE |
| Số lần nạp | 64 | [S2]; [S3] | VERIFIED |
| Thứ tự bít | LSB-first trong từng byte | [S2] | SINGLE-SOURCE |
| Quy tắc quay | Quay cả X, Y, Z | [S2]; [S3] | VERIFIED |
| Hàm `maj` | Không sử dụng | [S2]; [S3] | VERIFIED |
| Bít khóa | XOR vào X, Y, Z | [S2] | SINGLE-SOURCE |

---

## 5. Frame loading

### 5.1. Độ dài frame

Frame của A5/1 có độ dài:

```text
22 bít
```

S5 sử dụng tham số:

```text
COUNT = 22 bít
```

**Nguồn:** `[S2]`; `[S5]`  
**Nhãn:** `VERIFIED`

---

### 5.2. Số lần nạp

Frame được nạp trong:

```text
22 lần
```

Trong quá trình này:

- X, Y, Z đều được quay;
- không sử dụng điều kiện `maj`.

**Nguồn:** `[S2]`; `[S3]`  
**Nhãn:** `VERIFIED`

---

### 5.3. Thứ tự bít

S2 lấy bít frame bằng:

```text
(frame >> i) & 1
```

với:

```text
i = 0 ... 21
```

Do đó:

```text
Frame loading = LSB-first
```

**Nguồn:** `[S2]`  
**Nhãn:** `SINGLE-SOURCE`

---

### 5.4. Quy trình nạp frame

```text
Lặp i = 0 ... 21:

    Quay X
    Quay Y
    Quay Z

    Đọc frame_bit

    XOR frame_bit vào X
    XOR frame_bit vào Y
    XOR frame_bit vào Z
```

**Nguồn:** `[S2]`; `[S3]`

---

### 5.5. Bảng kiểm chứng frame loading

| Nội dung | Kết luận | Nguồn | Nhãn |
|---|---|---|---|
| Độ dài frame | 22 bít | [S2]; [S5] | VERIFIED |
| Số lần nạp | 22 | [S2]; [S3] | VERIFIED |
| Thứ tự bít | LSB-first | [S2] | SINGLE-SOURCE |
| Quy tắc quay | Quay cả X, Y, Z | [S2]; [S3] | VERIFIED |
| Hàm `maj` | Không sử dụng | [S2]; [S3] | VERIFIED |
| Bít frame | XOR vào X, Y, Z | [S2] | SINGLE-SOURCE |

---

## 6. Warm-up

Sau khi hoàn thành quá trình nạp khóa và frame, A5/1 thực hiện:

```text
100 lần warm-up
```

Trong giai đoạn này, hàm `maj` được sử dụng:

```text
m = maj(x_8, y_10, z_10)
```

Sau đó:

```text
Nếu x_8 = m → Quay X
Nếu y_10 = m → Quay Y
Nếu z_10 = m → Quay Z
```

Các bít sinh ra trong 100 lần này không được sử dụng.

**Nguồn:** `[S2]`; `[S3]`  
**Nhãn:** `VERIFIED`

---

### 6.1. Quy trình

```text
Nạp xong frame
        ↓
Tính maj
        ↓
Quay X/Y/Z theo maj
        ↓
Lặp 100 lần
        ↓
Không sử dụng bít sinh ra
        ↓
Sinh keystream
```

---

### 6.2. Bảng kiểm chứng

| Nội dung | Kết luận | Nguồn | Nhãn |
|---|---|---|---|
| Số lần warm-up | 100 | [S2]; [S3] | VERIFIED |
| Hàm `maj` | Có sử dụng | [S2]; [S3] | VERIFIED |
| Bít sinh ra | Không sử dụng | [S2]; [S3] | VERIFIED |

---

## 7. Keystream generation

### 7.1. Quy trình sinh một bít

Mỗi bước sinh bít thực hiện:

```text
1. Đọc x_8, y_10, z_10

2. Tính:
   m = maj(x_8, y_10, z_10)

3. Nếu x_8 = m:
   Quay X

4. Nếu y_10 = m:
   Quay Y

5. Nếu z_10 = m:
   Quay Z

6. Sau khi quay:
   s_i = x_8 XOR y_10 XOR z_10
```

**Nguồn:** `[S1, trang 51]`  
**Nhãn:** `VERIFIED theo slide`

---

### 7.2. Bít sinh ra

Theo S1:

```text
s_i = x_8 XOR y_10 XOR z_10
```

Phép tính được thực hiện sau khi các thanh ghi cần thiết đã được quay.

**Nguồn:** `[S1, trang 51]`

---

### 7.3. Đối chiếu nguồn ngoài

S2 sử dụng:

```text
X / R1: bit 18
Y / R2: bit 21
Z / R3: bit 22
```

Bít keystream:

```text
s_i = x_18 XOR y_21 XOR z_22
```

S4 cũng mô tả output bằng XOR các bít cao nhất của ba thanh ghi.

**Nguồn:** `[S2]`; `[S4]`

---

### 7.4. TD-001 - Bít sinh ra

Hai cách biểu diễn hiện tại:

**S1:**

```text
s_i = x_8 XOR y_10 XOR z_10
```

**S2/S4:**

```text
s_i = x_18 XOR y_21 XOR z_22
```

Sự khác biệt này ảnh hưởng trực tiếp đến:

```text
keystream
bản mã
test vector
```

**Trạng thái:**

```text
CONFLICT - OPEN
```

---

### 7.5. Số lượng keystream

Theo S2 và S4, mỗi lần thiết lập theo frame sinh tổng cộng:

```text
228 bít
```

gồm:

```text
114 bít A → B
114 bít B → A
```

**Nguồn:** `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

## 8. Encryption

A5/1 là mã dòng nên dãy bít sinh ra được XOR với bản rõ.

Công thức:

```text
C = P XOR S
```

Trong đó:

```text
P = bản rõ
S = dãy bít sinh ra
C = bản mã
```

**Nguồn:** `[S1, trang 42, 45, 47]`  
**Nhãn:** `VERIFIED`

---

### 8.1. Ví dụ

Cho:

```text
P = 111
S = 100
```

Mã hóa:

```text
C = P XOR S
  = 111 XOR 100
  = 011
```

**Nguồn:** `[S1, trang 49-50]`

---

## 9. Decryption

Giải mã sử dụng cùng dãy bít `S`:

```text
P = C XOR S
```

Ví dụ:

```text
C = 011
S = 100
```

Ta có:

```text
P = 011 XOR 100
  = 111
```

Do XOR là phép tự nghịch đảo:

```text
(P XOR S) XOR S = P
```

**Nguồn:** `[S1, trang 50]`  
**Nhãn:** `VERIFIED`

---

## 10. Bit ordering

### 10.1. Đánh số bít

Các thanh ghi sử dụng chỉ số bắt đầu từ `0`:

```text
X: x_0 ... x_18
Y: y_0 ... y_21
Z: z_0 ... z_22
```

TinyA5/1 cũng sử dụng:

```text
X: 0 1 2 3 4 5
Y: 0 1 2 3 4 5 6 7
Z: 0 1 2 3 4 5 6 7 8
```

**Nguồn:** `[S1, trang 48, 51]`; `[S2]`; `[S4]`  
**Nhãn:** `VERIFIED`

---

### 10.2. Hướng quay

X:

```text
x_j = x_{j-1}
j = 18, 17, ..., 1

x_0 = t
```

Y:

```text
y_j = y_{j-1}
j = 21, 20, ..., 1

y_0 = t
```

Z:

```text
z_j = z_{j-1}
j = 22, 21, ..., 1

z_0 = t
```

Bít feedback `t` được đưa vào vị trí chỉ số `0`.

**Nguồn:** `[S1, trang 51]`  
**Nhãn:** `VERIFIED`

---

### 10.3. Thứ tự bít của khóa

Trong S2:

```text
Key loading = LSB-first trong từng byte
```

**Nguồn:** `[S2]`  
**Nhãn:** `SINGLE-SOURCE`

---

### 10.4. Thứ tự bít của frame

Trong S2:

```text
Frame loading = LSB-first
```

**Nguồn:** `[S2]`  
**Nhãn:** `SINGLE-SOURCE`

---

### 10.5. Đóng gói keystream

S2 sử dụng:

```text
getbit() << (7 - (i & 7))
```

Do đó keystream được đóng gói:

```text
MSB-first trong từng byte
```

Tóm tắt:

```text
Key input:
LSB-first

Frame input:
LSB-first

Keystream byte packing:
MSB-first
```

**Nguồn:** `[S2]`

---

## 11. Pseudocode

### 11.1. Quay X

```text
t = x_13 XOR x_16 XOR x_17 XOR x_18

for j = 18 down to 1:
    x_j = x_{j-1}

x_0 = t
```

---

### 11.2. Quay Y

```text
t = y_20 XOR y_21

for j = 21 down to 1:
    y_j = y_{j-1}

y_0 = t
```

---

### 11.3. Quay Z

```text
t = z_7 XOR z_20 XOR z_21 XOR z_22

for j = 22 down to 1:
    z_j = z_{j-1}

z_0 = t
```

---

### 11.4. Sinh một bít

```text
m = maj(x_8, y_10, z_10)

if x_8 == m:
    Quay X

if y_10 == m:
    Quay Y

if z_10 == m:
    Quay Z

s_i = x_8 XOR y_10 XOR z_10
```

**Nguồn:** `[S1, trang 51]`

---

### 11.5. Quy trình A5/1

```text
INITIALIZE

X = 0
Y = 0
Z = 0


KEY LOADING

for i = 0 .. 63:

    Quay X
    Quay Y
    Quay Z

    key_bit = key[i]

    XOR key_bit vào X
    XOR key_bit vào Y
    XOR key_bit vào Z


FRAME LOADING

for i = 0 .. 21:

    Quay X
    Quay Y
    Quay Z

    frame_bit = frame[i]

    XOR frame_bit vào X
    XOR frame_bit vào Y
    XOR frame_bit vào Z


WARM-UP

for i = 0 .. 99:

    m = maj(x_8, y_10, z_10)

    if x_8 == m:
        Quay X

    if y_10 == m:
        Quay Y

    if z_10 == m:
        Quay Z


KEYSTREAM GENERATION

repeat:

    m = maj(x_8, y_10, z_10)

    if x_8 == m:
        Quay X

    if y_10 == m:
        Quay Y

    if z_10 == m:
        Quay Z

    s_i = x_8 XOR y_10 XOR z_10

    lưu s_i
```

> Công thức `s_i` trong pseudocode trên sử dụng quy ước của S1. Quy ước output cuối cùng cần được xác nhận sau khi TD-001 được chốt.

---

## 12. TinyA5/1 và A5/1 tổng quát

### 12.1. Cấu trúc TinyA5/1

TinyA5/1 sử dụng:

```text
X = 6 bít
Y = 8 bít
Z = 9 bít
```

Khóa:

```text
K = 23 bít
```

Phân bổ:

```text
K → XYZ
```

**Nguồn:** `[S1, trang 46]`

---

### 12.2. Hàm `maj`

TinyA5/1 sử dụng:

```text
m = maj(x_1, y_3, z_3)
```

Quy tắc:

```text
Nếu x_1 = m → Quay X
Nếu y_3 = m → Quay Y
Nếu z_3 = m → Quay Z
```

**Nguồn:** `[S1, trang 47]`

---

### 12.3. Quay X

```text
t = x_2 XOR x_4 XOR x_5

x_j = x_{j-1}
j = 5, 4, 3, 2, 1

x_0 = t
```

**Nguồn:** `[S1, trang 48]`

---

### 12.4. Quay Y

```text
t = y_6 XOR y_7

y_j = y_{j-1}
j = 7, 6, ..., 1

y_0 = t
```

**Nguồn:** `[S1, trang 48]`

---

### 12.5. Quay Z

```text
t = z_2 XOR z_7 XOR z_8

z_j = z_{j-1}
j = 8, 7, ..., 1

z_0 = t
```

**Nguồn:** `[S1, trang 48]`

---

### 12.6. Bít sinh ra

TinyA5/1 sinh:

```text
s_i = x_5 XOR y_7 XOR z_8
```

**Nguồn:** `[S1, trang 47]`

---

### 12.7. So sánh TinyA5/1 và A5/1

| Thuộc tính | TinyA5/1 | A5/1 tổng quát | Nguồn |
|---|---|---|---|
| Số thanh ghi | 3 | 3 | [S1] |
| Tên thanh ghi | X, Y, Z | X, Y, Z | [S1] |
| Độ dài X | 6 bít | 19 bít | [S1, trang 46, 51] |
| Độ dài Y | 8 bít | 22 bít | [S1, trang 46, 51] |
| Độ dài Z | 9 bít | 23 bít | [S1, trang 46, 51] |
| Độ dài khóa | 23 bít | 64 bít theo S2/S5 | [S1]; [S2]; [S5] |
| Bít dùng cho `maj` | `x_1, y_3, z_3` | `x_8, y_10, z_10` | [S1] |
| Feedback X | `x_2, x_4, x_5` | `x_13, x_16, x_17, x_18` | [S1] |
| Feedback Y | `y_6, y_7` | `y_20, y_21` | [S1] |
| Feedback Z | `z_2, z_7, z_8` | `z_7, z_20, z_21, z_22` | [S1] |
| Bít sinh ra | `x_5 XOR y_7 XOR z_8` | `x_8 XOR y_10 XOR z_10` theo S1 | [S1] |
| Mã hóa | `C = P XOR S` | `C = P XOR S` | [S1] |
| Giải mã | `P = C XOR S` | `P = C XOR S` | [S1] |

---

### 12.8. Ví dụ TinyA5/1

Cho:

```text
P = 111
K = 10010101001110100110000
```

Phân bổ:

```text
X = 100101
Y = 01001110
Z = 100110000
```

#### Bước 0

```text
x_1 = 0
y_3 = 0
z_3 = 1

m = maj(0,0,1) = 0
```

Do đó:

```text
Quay X
Quay Y
```

Bít sinh ra:

```text
s_0 = 1
```

---

#### Bước 1

```text
x_1 = 1
y_3 = 0
z_3 = 1

m = maj(1,0,1) = 1
```

Do đó:

```text
Quay X
Quay Z
```

Bít sinh ra:

```text
s_1 = 0
```

---

#### Bước 2

```text
x_1 = 1
y_3 = 0
z_3 = 0

m = maj(1,0,0) = 0
```

Do đó:

```text
Quay Y
Quay Z
```

Bít sinh ra:

```text
s_2 = 0
```

Dãy bít sinh ra:

```text
S = 100
```

Mã hóa:

```text
C = 111 XOR 100
  = 011
```

Giải mã:

```text
P = 011 XOR 100
  = 111
```

**Nguồn:** `[S1, trang 49-50]`

---

## 13. Sources

### S1 - Slide môn học

**Tên:**

`Chương 2 - MÃ HOÁ KHOÁ ĐỐI XỨNG (MÃ HOÁ KHOÁ BÍ MẬT)`

**Đơn vị:**

Đại học Kinh tế Quốc dân - Khoa Công nghệ Thông tin

**Giảng viên:**

ThS. Nguyễn Quốc Thái

**Phần sử dụng:**

- Mã dòng.
- A5/1.
- TinyA5/1.
- Hàm `maj`.
- Quay X, Y, Z.
- Feedback.
- Bít sinh ra.
- Mã hóa và giải mã.
- Ví dụ tính tay.

**Trang sử dụng:**

```text
Trang 45:
Giới thiệu A5/1

Trang 46:
Cấu trúc TinyA5/1

Trang 47:
Hàm maj và quá trình sinh bít

Trang 48:
Quay X, Y, Z

Trang 49-50:
Ví dụ TinyA5/1

Trang 51-52:
A5/1 tổng quát
```

**Trạng thái:**

`PRIMARY INTERNAL SOURCE`

---

### S2 - A5/1 Pedagogical Implementation

**Tác giả:**

Marc Briceno, Ian Goldberg, David Wagner

**Tên file:**

`A5.1.c`

**URL:**

https://github.com/NSAPlayset/TWILIGHTVEGETABLE/blob/master/A5.1/C/A5.1.c

**Dùng để xác minh:**

- cấu trúc thanh ghi;
- các bít dùng cho majority;
- feedback taps;
- output taps;
- trạng thái ban đầu;
- key loading;
- frame loading;
- warm-up;
- bit ordering;
- 228 bít keystream;
- test vector.

**Trạng thái:**

`EXTERNAL TECHNICAL SOURCE`

---

### S3 - Real Time Cryptanalysis of A5/1 on a PC

**Tác giả:**

Alex Biryukov, Adi Shamir, David Wagner

**Tên tài liệu:**

`Real Time Cryptanalysis of A5/1 on a PC`

**Năm:**

2000 / xuất bản trong FSE 2000 proceedings năm 2001

**URL:**

https://www.iacr.org/archive/fse2000/19780071/19780071.pdf

**Dùng để đối chiếu:**

- cấu trúc A5/1;
- majority clocking;
- key setup;
- frame setup;
- warm-up;
- keystream.

**Trạng thái:**

`EXTERNAL ACADEMIC SOURCE`

---

### S4 - A Real-World Attack Breaking A5/1

**Tác giả:**

Thomas Gendrullis, Michael Novotný, Andreas Rupp

**Tên tài liệu:**

`A Real-World Attack Breaking A5/1`

**Nơi xuất bản:**

CHES 2008

**URL:**

https://www.iacr.org/archive/ches2008/51540262/51540262.pdf

**Dùng để đối chiếu:**

- bít dùng cho majority;
- majority clocking;
- feedback taps;
- output;
- 228 bít keystream;
- 114 bít cho mỗi hướng.

**Trạng thái:**

`EXTERNAL TECHNICAL SOURCE`

---

### S5 - 3GPP TS 43.020 / ETSI TS 143 020

**Tên:**

`Digital cellular telecommunications system (Phase 2+); Security-related network functions`

**URL:**

https://www.etsi.org/deliver/etsi_ts/143000_143099/143020/07.01.00_60/ts_143020v070100p.pdf

**Dùng để đối chiếu:**

- `Kc = 64 bít`;
- `COUNT = 22 bít`;
- BLOCK1 / BLOCK2;
- thông tin giao diện của Algorithm A5.

**Trạng thái:**

`EXTERNAL STANDARD SOURCE`

---

## 14. Technical Decisions / Open Issues

### TD-001 - Bít sinh ra của A5/1

#### S1

```text
s_i = x_8 XOR y_10 XOR z_10
```

**Nguồn:** `[S1, trang 51]`

#### S2/S4

```text
s_i = x_18 XOR y_21 XOR z_22
```

**Nguồn:** `[S2]`; `[S4]`

#### Impact

Ảnh hưởng trực tiếp đến:

```text
keystream
bản mã
test vector
```

#### Status

```text
CONFLICT - OPEN
```

---

### TD-003 - Chỉ số và thứ tự bít

Các thanh ghi sử dụng cơ sở chỉ số `0`:

```text
X: x_0 ... x_18
Y: y_0 ... y_21
Z: z_0 ... z_22
```

S2 và S4 cũng sử dụng cách đánh số bắt đầu từ `0`.

Ánh xạ:

```text
X ↔ R1
Y ↔ R2
Z ↔ R3
```

cần được thống nhất với `coding_convention.md`.

#### Status

```text
VERIFIED / NEED LOCKING
```

---

### TD-004 - Key loading, frame loading và warm-up

Các thông số:

```text
Key = 64 bít
Key loading = 64 lần

Frame = 22 bít
Frame loading = 22 lần

Warm-up = 100 lần
```

Key loading:

```text
- Quay cả X, Y, Z
- Không sử dụng maj
- Xử lý 64 bít khóa
- XOR từng bít khóa vào X, Y, Z
```

Frame loading:

```text
- Quay cả X, Y, Z
- Không sử dụng maj
- Xử lý 22 bít frame
- XOR từng bít frame vào X, Y, Z
```

Warm-up:

```text
- Sử dụng maj
- 100 lần
- Không sử dụng bít sinh ra
```

**Nguồn:** `[S2]`; `[S3]`

#### Status

```text
VERIFIED
```

---

### TD-005 - Dữ liệu dài hơn một đoạn keystream

Mỗi frame tạo:

```text
114 bít A → B
114 bít B → A
```

Tổng:

```text
228 bít
```

Quy tắc xử lý một file có độ dài lớn hơn một frame chưa được chốt trong Phase 1.

Các vấn đề cần xác định khi triển khai:

- cách chia dữ liệu;
- cách xác định frame tiếp theo;
- cách sinh keystream tiếp theo;
- cách ghép kết quả.

#### Status

```text
OPEN
```

---

## 15. Test vector tham khảo

Test vector chi tiết:

```text
docs/a51_test_vector.md
```

### Key

```text
0x1223456789ABCDEF
```

### Frame

```text
0x134
```

### Keystream A → B

```text
0x534EAA582FE8151AB6E1855A728C00
```

### Keystream B → A

```text
0x24FD35A35D5FB6526D32F906DF1AC0
```

**Nguồn:** `[S2]`

Test vector trên sử dụng quy ước output:

```text
x_18 XOR y_21 XOR z_22
```

Do TD-001 chưa được chốt, trạng thái test vector là:

```text
SINGLE-SOURCE
```

---

## 16. Kiểm tra nhất quán

### 16.1. Cấu trúc thanh ghi

```text
X = 19 bít
Y = 22 bít
Z = 23 bít

19 + 22 + 23 = 64 bít
```

Kết quả:

```text
PASS
```

---

### 16.2. Hàm `maj`

```text
m = maj(x_8, y_10, z_10)
```

Kết quả:

```text
PASS
```

---

### 16.3. Feedback

```text
X:
x_13, x_16, x_17, x_18

Y:
y_20, y_21

Z:
z_7, z_20, z_21, z_22
```

Kết quả:

```text
PASS
```

---

### 16.4. Hướng quay

```text
t → vị trí 0
các bít cũ → vị trí có chỉ số lớn hơn
```

Kết quả:

```text
PASS
```

---

### 16.5. Initialization

```text
Key:
64 bít

Frame:
22 bít

Warm-up:
100 lần
```

Kết quả:

```text
PASS
```

---

### 16.6. Output

```text
S1:
x_8 XOR y_10 XOR z_10

S2/S4:
x_18 XOR y_21 XOR z_22
```

Kết quả:

```text
TD-001 = CONFLICT
```

---

### 16.7. TinyA5/1

```text
maj:
x_1, y_3, z_3

Feedback X:
x_2, x_4, x_5

Feedback Y:
y_6, y_7

Feedback Z:
z_2, z_7, z_8

Bít sinh ra:
x_5 XOR y_7 XOR z_8
```

Kết quả:

```text
PASS
```

---

## 17. Trạng thái hoàn thành Phase 1

### Đã xác minh

- [x] A5/1 là mã dòng được sử dụng trong GSM.
- [x] Đơn vị mã hóa là 1 bít.
- [x] X có 19 bít.
- [x] Y có 22 bít.
- [x] Z có 23 bít.
- [x] Chỉ số bắt đầu từ 0.
- [x] Hàm `maj` sử dụng `x_8`, `y_10`, `z_10`.
- [x] Feedback X.
- [x] Feedback Y.
- [x] Feedback Z.
- [x] Quy tắc Quay X/Y/Z.
- [x] Bít feedback đi vào vị trí 0.
- [x] Key có 64 bít.
- [x] Key loading có 64 lần.
- [x] Frame có 22 bít.
- [x] Frame loading có 22 lần.
- [x] Warm-up có 100 lần.
- [x] Bít sinh ra không được sử dụng trong warm-up.
- [x] 228 bít keystream theo nguồn ngoài.
- [x] 114 bít A → B.
- [x] 114 bít B → A.
- [x] Có test vector tham khảo.

### Còn phải chốt

- [ ] TD-001: bít sinh ra giữa S1 và S2/S4.
- [ ] TD-003: ánh xạ cuối cùng giữa ký hiệu tài liệu và code.
- [ ] TD-005: xử lý dữ liệu dài hơn một frame.
- [ ] Test vector cuối cùng sau khi TD-001 được chốt.

---

## 18. Kết luận

A5/1 sử dụng ba thanh ghi:

```text
X = 19 bít
Y = 22 bít
Z = 23 bít
```

Hàm chiếm đa số:

```text
m = maj(x_8, y_10, z_10)
```

Quay X:

```text
t = x_13 XOR x_16 XOR x_17 XOR x_18

x_j = x_{j-1}
j = 18,17,...,1

x_0 = t
```

Quay Y:

```text
t = y_20 XOR y_21

y_j = y_{j-1}
j = 21,20,...,1

y_0 = t
```

Quay Z:

```text
t = z_7 XOR z_20 XOR z_21 XOR z_22

z_j = z_{j-1}
j = 22,21,...,1

z_0 = t
```

Bít sinh ra theo S1:

```text
s_i = x_8 XOR y_10 XOR z_10
```

Mã hóa:

```text
C = P XOR S
```

Giải mã:

```text
P = C XOR S
```

Các thông số thiết lập:

```text
Key = 64 bít
Key loading = 64 lần

Frame = 22 bít
Frame loading = 22 lần

Warm-up = 100 lần
```

Điểm còn xung đột là công thức bít sinh ra:

```text
S1:
x_8 XOR y_10 XOR z_10

S2/S4:
x_18 XOR y_21 XOR z_22
```

Vấn đề này được giữ tại:

```text
TD-001 - CONFLICT
```

---

## 19. Tham chiếu nhanh các thông số

| Thành phần | Giá trị | Trạng thái |
|---|---|---|
| X | 19 bít | VERIFIED |
| Y | 22 bít | VERIFIED |
| Z | 23 bít | VERIFIED |
| Tổng trạng thái | 64 bít | VERIFIED |
| Bít `maj` của X | `x_8` | VERIFIED |
| Bít `maj` của Y | `y_10` | VERIFIED |
| Bít `maj` của Z | `z_10` | VERIFIED |
| Feedback X | `x_13, x_16, x_17, x_18` | VERIFIED |
| Feedback Y | `y_20, y_21` | VERIFIED |
| Feedback Z | `z_7, z_20, z_21, z_22` | VERIFIED |
| Key | 64 bít | VERIFIED |
| Key loading | 64 lần | VERIFIED |
| Frame | 22 bít | VERIFIED |
| Frame loading | 22 lần | VERIFIED |
| Warm-up | 100 lần | VERIFIED |
| Output theo S1 | `x_8 XOR y_10 XOR z_10` | CONFLICT |
| Output theo S2/S4 | `x_18 XOR y_21 XOR z_22` | CONFLICT |
| Keystream / frame | 228 bít | VERIFIED |
| A → B | 114 bít | VERIFIED |
| B → A | 114 bít | VERIFIED |
| File dài | Chưa chốt quy tắc | OPEN |
