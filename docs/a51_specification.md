# Đặc tả A5/1

> **Owner:** Lại Hoàng Thế Vũ  
> **Branch:** `docs/vu-a51`  
> **Giai đoạn:** Phase 1 - Specification and Verification  
> **File:** `docs/a51_specification.md`  
> **Trạng thái:** Bản đặc tả Phase 1, đã đối chiếu slide và nguồn kỹ thuật bên ngoài
>
> **Quy ước nguồn trong tài liệu:**
>
> - `[S1]` = Slide môn học, Chương 2 - Mã hoá khoá đối xứng, trang 45-52.
> - `[S2]` = Marc Briceno, Ian Goldberg, David Wagner, A5/1 Pedagogical Implementation (`A5.1.c`).
> - `[S3]` = Alex Biryukov, Adi Shamir, David Wagner, *Real Time Cryptanalysis of A5/1 on a PC*.
> - `[S4]` = Thomas Gendrullis, Michael Novotný, Andreas Rupp, *A Real-World Attack Breaking A5/1*.
> - `[S5]` = 3GPP TS 43.020 / ETSI TS 143 020, phần đặc tả giao diện Algorithm A5.

---

## 1. Overview

### 1.1. A5/1 là gì?

A5/1 là một **mã dòng (Stream Cipher)** được sử dụng trong mạng điện thoại GSM để bảo mật dữ liệu trong quá trình liên lạc giữa điện thoại và trạm thu phát sóng vô tuyến.

Theo slide môn học:

- Đơn vị mã hoá của A5/1 là **1 bit**.
- Bộ sinh số mỗi lần sinh ra một bit `0` hoặc `1`.
- Bit sinh ra được sử dụng trong phép XOR với dữ liệu.
- Trong phạm vi bài học, A5/1 đầy đủ được mô tả bằng cách tổng quát hóa từ TinyA5/1.

**Nguồn:** [S1, trang 45]

### 1.2. Cấu trúc tổng quát

A5/1 sử dụng ba thanh ghi dịch phản hồi:

```text
X
Y
Z
```

Trong quy ước thường dùng của nguồn ngoài, ba thanh ghi này được gọi tương ứng là:

```text
R1
R2
R3
```

Độ dài của ba thanh ghi:

```text
X / R1 = 19 bit
Y / R2 = 22 bit
Z / R3 = 23 bit
```

Do đó:

```text
19 + 22 + 23 = 64 bit
```

**Nguồn:** [S1, trang 51]; [S2]; [S3]

### 1.3. Quy trình hoạt động tổng quát

Quy trình A5/1 đầy đủ:

```text
Khởi tạo các register
        ↓
Nạp key
        ↓
Nạp frame
        ↓
Warm-up
        ↓
Sinh keystream
        ↓
XOR với plaintext
        ↓
Ciphertext
```

Theo S2, sau khi thiết lập trạng thái, A5/1 sinh tổng cộng 228 bit keystream:

```text
114 bit → hướng A → B
114 bit → hướng B → A
```

[S2]

3GPP/ETSI xác định ở mức giao diện A5 rằng khóa `Kc` có 64 bit và `COUNT` có 22 bit; với GMSK, mỗi burst có 114 payload bits. [S5]

---

## 2. Registers

## 2.1. Bảng tổng hợp

| Thông số | X / R1 | Y / R2 | Z / R3 | Nguồn | Nhãn |
|---|---:|---:|---:|---|---|
| Độ dài | 19 bit | 22 bit | 23 bit | [S1, trang 51]; [S2]; [S3] | VERIFIED |
| Chỉ số bit | 0 ... 18 | 0 ... 21 | 0 ... 22 | [S1, trang 51]; [S2]; [S4] | VERIFIED |
| Clocking bit | 8 | 10 | 10 | [S1, trang 51]; [S2]; [S4] | VERIFIED |
| Feedback taps | 13, 16, 17, 18 | 20, 21 | 7, 20, 21, 22 | [S1, trang 51]; [S2]; [S4] | VERIFIED |
| Hướng dịch | `xj = x(j-1)` | `yj = y(j-1)` | `zj = z(j-1)` | [S1, trang 51]; [S2] | VERIFIED |
| Bit mới | `x0 = t` | `y0 = t` | `z0 = t` | [S1, trang 51]; [S2] | VERIFIED |
| Bit output | `x8`, `y10`, `z10` theo slide | bit 18, 21, 22 theo nguồn ngoài | [S1, trang 51]; [S2]; [S4] | CONFLICT |

### 2.2. Quy ước đánh số bit

Trong slide, A5/1 đầy đủ được ký hiệu:

```text
X: x0 ... x18
Y: y0 ... y21
Z: z0 ... z22
```

Nguồn S2 biểu diễn các register dưới dạng các số nguyên với:

```text
R1: 19 bit, đánh số 0 ... 18
R2: 22 bit, đánh số 0 ... 21
R3: 23 bit, đánh số 0 ... 22
```

S4 cũng sử dụng cùng quy ước chỉ số.

**Nguồn:** [S1, trang 51]; [S2]; [S4]

**Nhãn:** `VERIFIED`

### 2.3. Thanh ghi X / R1

Độ dài:

```text
19 bit
```

Clocking bit:

```text
x8
```

Feedback taps:

```text
x13
x16
x17
x18
```

Feedback:

```text
t = x13 XOR x16 XOR x17 XOR x18
```

Sau khi tính `t`:

```text
xj = x(j-1)
```

với:

```text
j = 18, 17, ..., 1
```

Sau đó:

```text
x0 = t
```

Trong implementation S2, các feedback taps tương ứng là:

```text
18, 17, 16, 13
```

và register được dịch trái, sau đó feedback được đưa vào bit 0.

**Nguồn:** [S1, trang 51]; [S2]; [S4]

### 2.4. Thanh ghi Y / R2

Độ dài:

```text
22 bit
```

Clocking bit:

```text
y10
```

Feedback taps:

```text
y20
y21
```

Feedback:

```text
t = y20 XOR y21
```

Sau khi tính `t`:

```text
yj = y(j-1)
```

với:

```text
j = 21, 20, ..., 1
```

Sau đó:

```text
y0 = t
```

**Nguồn:** [S1, trang 51]; [S2]; [S4]

### 2.5. Thanh ghi Z / R3

Độ dài:

```text
23 bit
```

Clocking bit:

```text
z10
```

Feedback taps:

```text
z7
z20
z21
z22
```

Feedback:

```text
t = z7 XOR z20 XOR z21 XOR z22
```

Sau khi tính `t`:

```text
zj = z(j-1)
```

với:

```text
j = 22, 21, ..., 1
```

Sau đó:

```text
z0 = t
```

**Nguồn:** [S1, trang 51]; [S2]; [S4]

### 2.6. Kiểm tra tổng độ dài

```text
X = 19 bit
Y = 22 bit
Z = 23 bit
----------------
Tổng = 64 bit
```

Kết quả:

```text
19 + 22 + 23 = 64 bit
```

---

## 3. Majority clocking

### 3.1. Các bit dùng cho majority

Ba clocking bit:

```text
x8
y10
z10
```

Công thức:

```text
m = maj(x8, y10, z10)
```

**Nguồn:** [S1, trang 51]; [S2]; [S4]

### 3.2. Hàm majority

Majority trả về giá trị xuất hiện ít nhất hai lần trong ba bit.

| x8 | y10 | z10 | m |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

### 3.3. Quy tắc clock

Sau khi tính:

```text
m = maj(x8, y10, z10)
```

thực hiện:

```text
Nếu x8 = m → clock X / R1

Nếu y10 = m → clock Y / R2

Nếu z10 = m → clock Z / R3
```

S2 mô tả chính xác:

> Thanh ghi `Ri` được clock khi bit giữa của `Ri` trùng với giá trị majority của ba bit giữa.

S4 mô tả cùng nguyên tắc và cho biết trong mỗi chu kỳ ít nhất hai trong ba register được clock.

**Nguồn:** [S2]; [S4]

**Nhãn:** `VERIFIED`

---

## 4. Key loading

### 4.1. Độ dài key

Khóa phiên A5/1 có độ dài:

```text
64 bit
```

S2 nhận key dưới dạng 8 byte:

```text
byte key[8]
```

S5 cũng quy định:

```text
length of Kc = 64 bits
```

**Nguồn:** [S2]; [S5]

**Nhãn:** `VERIFIED`

### 4.2. Trạng thái ban đầu

Trước khi nạp key:

```text
R1 = 0
R2 = 0
R3 = 0
```

S2 thực hiện trực tiếp việc đưa cả ba register về 0 trước khi setup.

**Nguồn:** [S2]

**Nhãn:** `SINGLE-SOURCE`

### 4.3. Số chu kỳ

Nạp key thực hiện trong:

```text
64 chu kỳ
```

Trong mỗi chu kỳ:

- cả ba register đều được clock;
- majority clocking bị vô hiệu hóa;
- một bit key được XOR vào cả ba register.

**Nguồn:** [S2]; [S3]

**Nhãn:** `VERIFIED`

### 4.4. Thứ tự bit của key

S2 ghi rõ:

```text
LSB của byte đầu tiên được xử lý trước.
```

Bit thứ `i` được lấy bằng:

```text
key_bit = (key[i/8] >> (i&7)) & 1
```

với:

```text
i = 0 ... 63
```

Do đó key được xử lý theo:

```text
LSB → MSB
```

trong từng byte theo cách biểu diễn của implementation.

**Nguồn:** [S2]

### 4.5. Quy trình nạp key

```text
Khởi tạo:

R1 = 0
R2 = 0
R3 = 0

Lặp i = 0 ... 63:

    Clock R1
    Clock R2
    Clock R3

    Đọc key_bit

    R1 = R1 XOR key_bit
    R2 = R2 XOR key_bit
    R3 = R3 XOR key_bit
```

Trong key loading, cơ chế clocking theo majority được tạm thời tắt và cả ba register luôn được clock.

**Nguồn:** [S2]

### 4.6. Bảng kiểm chứng key loading

| Thông số | Kết luận | Nguồn | Nhãn |
|---|---|---|---|
| Độ dài key | 64 bit | [S2]; [S5] | VERIFIED |
| Trạng thái ban đầu | R1 = R2 = R3 = 0 | [S2] | SINGLE-SOURCE |
| Số chu kỳ | 64 | [S2]; [S3] | VERIFIED |
| Thứ tự bit | LSB-first | [S2]; [S3] | VERIFIED |
| Clocking | Clock cả 3 register | [S2]; [S3] | VERIFIED |
| Majority clocking | Không dùng | [S2]; [S3] | VERIFIED |
| XOR key bit | Vào cả 3 register | [S2] | SINGLE-SOURCE |

---

## 5. Frame loading

### 5.1. Độ dài frame

Frame number của A5/1 có độ dài:

```text
22 bit
```

S2 nhận tham số `word frame` và nạp 22 bit.

S5 xác định `COUNT` của Algorithm A5 có:

```text
22 bits
```

**Nguồn:** [S2]; [S5]

**Nhãn:** `VERIFIED`

### 5.2. Số chu kỳ

Nạp frame thực hiện trong:

```text
22 chu kỳ
```

Trong giai đoạn này:

- cả ba register đều được clock;
- majority clocking vẫn bị vô hiệu hóa.

**Nguồn:** [S2]; [S3]

**Nhãn:** `VERIFIED`

### 5.3. Thứ tự bit

S2 xử lý frame bằng:

```text
framebit = (frame >> i) & 1
```

với:

```text
i = 0 ... 21
```

Do đó implementation sử dụng:

```text
LSB → MSB
```

**Nguồn:** [S2]

**Nhãn:** `SINGLE-SOURCE`

### 5.4. Quy trình nạp frame

```text
Lặp i = 0 ... 21:

    Clock R1
    Clock R2
    Clock R3

    Đọc frame_bit

    R1 = R1 XOR frame_bit
    R2 = R2 XOR frame_bit
    R3 = R3 XOR frame_bit
```

**Nguồn:** [S2]; [S3]

### 5.5. Bảng kiểm chứng frame loading

| Thông số | Kết luận | Nguồn | Nhãn |
|---|---|---|---|
| Độ dài frame | 22 bit | [S2]; [S5] | VERIFIED |
| Số chu kỳ | 22 | [S2]; [S3] | VERIFIED |
| Thứ tự bit | LSB-first | [S2] | SINGLE-SOURCE |
| Clocking | Clock cả 3 register | [S2]; [S3] | VERIFIED |
| Majority clocking | Không dùng | [S2]; [S3] | VERIFIED |
| XOR frame bit | Vào cả 3 register | [S2] | SINGLE-SOURCE |

---

## 6. Warm-up

Sau khi hoàn thành key loading và frame loading, A5/1 thực hiện:

```text
100 chu kỳ warm-up
```

S2 mô tả 100 lần clock để trộn key material và frame number vào trạng thái của các register.

Trong giai đoạn này:

- majority-based clock control được bật lại;
- output generation bị vô hiệu hóa;
- sau 100 chu kỳ hệ thống chuyển sang trạng thái sẵn sàng sinh keystream.

**Nguồn:** [S2]; [S3]

### 6.1. Quy trình

```text
Sau frame loading
        ↓
Bật majority clocking
        ↓
Clock 100 lần
        ↓
Bỏ output
        ↓
Kết thúc warm-up
        ↓
Sinh keystream
```

### 6.2. Bảng kiểm chứng

| Thông số | Kết luận | Nguồn | Nhãn |
|---|---|---|---|
| Số chu kỳ | 100 | [S2]; [S3] | VERIFIED |
| Majority clocking | Bật | [S2]; [S3] | VERIFIED |
| Output | Không sử dụng | [S2]; [S3] | VERIFIED |

---

## 7. Keystream generation

### 7.1. Quy trình clock

Sau warm-up, mỗi chu kỳ sinh keystream thực hiện:

```text
1. Đọc x8, y10, z10.

2. Tính:
   m = maj(x8, y10, z10)

3. Nếu x8 = m:
   clock X.

4. Nếu y10 = m:
   clock Y.

5. Nếu z10 = m:
   clock Z.

6. Sinh output bit.

7. XOR output của ba register.
```

**Nguồn:** [S1, trang 51]; [S2]; [S4]

### 7.2. Output theo slide

Slide môn học ghi:

```text
s_i = x8 XOR y10 XOR z10
```

Do đó, theo slide:

```text
Output X = x8
Output Y = y10
Output Z = z10
```

**Nguồn:** [S1, trang 51]

### 7.3. Output theo nguồn ngoài

S2 định nghĩa output taps:

```text
R1OUT = bit 18
R2OUT = bit 21
R3OUT = bit 22
```

và hàm sinh output:

```text
keystream_bit =
    R1[18] XOR R2[21] XOR R3[22]
```

S4 cũng mô tả output sau clocking bằng XOR của các bit quan trọng nhất của R1, R2 và R3 và hình thiết kế ghi output taps tương ứng với:

```text
R1[18]
R2[21]
R3[22]
```

**Nguồn:** [S2]; [S4]

### 7.4. TD-001 - CONFLICT

Hai nhóm nguồn đang có sự khác nhau:

**Lecture/Slide:**

```text
s_i = x8 XOR y10 XOR z10
```

**External implementation / research:**

```text
s_i = R1[18] XOR R2[21] XOR R3[22]
```

Đây không phải là khác biệt có thể tự động xóa bỏ.

Có thể nguyên nhân là:

- khác quy ước ký hiệu bit;
- khác cách biểu diễn thanh ghi;
- khác cách đánh số bit;
- hoặc slide môn học đang dùng quy ước output riêng.

**Impact:**

Ảnh hưởng trực tiếp đến:

```text
keystream
    ↓
ciphertext
    ↓
test vector
```

**Status:**

```text
CONFLICT - OPEN
```

Không chốt một phía cho đến khi nhóm quyết định TD-001.

---

## 8. Encryption

A5/1 là mã dòng. Keystream được XOR với plaintext.

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

### 8.1. Ví dụ từ slide

```text
P = 111
S = 100

C = P XOR S
C = 111 XOR 100
C = 011
```

**Nguồn:** [S1, trang 49-50]

---

## 9. Decryption

Giải mã sử dụng cùng keystream:

```text
P = C XOR S
```

Ví dụ:

```text
C = 011
S = 100

P = 011 XOR 100
P = 111
```

**Nguồn:** [S1, trang 50]

Do XOR là phép tự nghịch đảo:

```text
(P XOR S) XOR S = P
```

---

## 10. Bit ordering

### 10.1. Đánh số bit

Quy ước được sử dụng:

```text
R1:
0 ... 18

R2:
0 ... 21

R3:
0 ... 22
```

Slide sử dụng ký hiệu tương ứng:

```text
x0 ... x18
y0 ... y21
z0 ... z22
```

**Nguồn:** [S1, trang 51]; [S2]; [S4]

### 10.2. Hướng dịch

Trong slide:

```text
X:

xj = x(j-1)
j = 18,17,...,1

x0 = t
```

```text
Y:

yj = y(j-1)
j = 21,20,...,1

y0 = t
```

```text
Z:

zj = z(j-1)
j = 22,21,...,1

z0 = t
```

**Nguồn:** [S1, trang 51]

### 10.3. Biểu diễn trong implementation

S2 dùng:

```text
reg = (reg << 1) & mask
reg |= parity(t)
```

Điều này tương ứng với:

```text
dịch sang trái
+
đưa feedback vào bit 0
```

**Nguồn:** [S2]

### 10.4. Thứ tự key

Trong S2:

```text
LSB của byte đầu tiên trước
```

Do đó:

```text
Key loading = LSB-first
```

**Nguồn:** [S2]

### 10.5. Thứ tự frame

S2 xử lý:

```text
framebit = (frame >> i) & 1
```

với:

```text
i = 0 ... 21
```

Do đó:

```text
Frame loading = LSB-first
```

**Nguồn:** [S2]

### 10.6. Đóng gói keystream thành byte

S2 tạo:

```text
114 bit A → B
```

và:

```text
114 bit B → A
```

Khi đưa vào buffer byte, source sử dụng:

```text
getbit() << (7-(i&7))
```

tức là các bit được đóng gói **MSB-first trong từng byte output**.

**Nguồn:** [S2]

Do đó phải phân biệt:

```text
Key input:
LSB-first

Frame input:
LSB-first

Keystream byte packing:
MSB-first
```

---

## 11. Pseudocode

### 11.1. Core algorithm theo quy trình đã xác minh

```text
INITIALIZE

R1 = 0
R2 = 0
R3 = 0


KEY LOADING

for i = 0 .. 63:

    clock R1
    clock R2
    clock R3

    key_bit = key[i]

    R1 = R1 XOR key_bit
    R2 = R2 XOR key_bit
    R3 = R3 XOR key_bit


FRAME LOADING

for i = 0 .. 21:

    clock R1
    clock R2
    clock R3

    frame_bit = frame[i]

    R1 = R1 XOR frame_bit
    R2 = R2 XOR frame_bit
    R3 = R3 XOR frame_bit


WARM-UP

for i = 0 .. 99:

    read clocking bits
    calculate majority
    clock registers whose clocking bit equals majority
    discard output


KEYSTREAM GENERATION

repeat:

    read R1 clocking bit
    read R2 clocking bit
    read R3 clocking bit

    m = majority(R1_clock, R2_clock, R3_clock)

    if R1_clock == m:
        clock R1

    if R2_clock == m:
        clock R2

    if R3_clock == m:
        clock R3

    obtain output bit
    XOR the three output bits

    store keystream bit
```

> **Lưu ý:** dòng `obtain output bit` chưa được khóa do TD-001.

---

## 12. TinyA5/1 và A5/1 đầy đủ

| Thuộc tính | TinyA5/1 | A5/1 đầy đủ |
|---|---|---|
| Số register | 3 | 3 |
| Tên register | X, Y, Z | X, Y, Z |
| Độ dài X | 6 bit | 19 bit |
| Độ dài Y | 8 bit | 22 bit |
| Độ dài Z | 9 bit | 23 bit |
| Độ dài key | 23 bit | 64 bit |
| Majority | Tiny theo slide | `x8, y10, z10` |
| Feedback X | `x3, x4, x5` theo Tiny | `x13, x16, x17, x18` |
| Feedback Y | `y4, y7` theo Tiny | `y20, y21` |
| Feedback Z | `z5, z7, z8` theo Tiny | `z7, z20, z21, z22` |
| Clocking | Majority | Majority |
| Mục đích | Mô hình thu nhỏ để tính tay | Mã dòng A5/1 đầy đủ |

**Nguồn:** [S1, trang 46-52]

### 12.1. Ví dụ TinyA5/1

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

Theo slide:

```text
S = 100
```

Mã hóa:

```text
C = 111 XOR 100
C = 011
```

Giải mã:

```text
P = 011 XOR 100
P = 111
```

**Nguồn:** [S1, trang 49-50]

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
- Majority.
- Feedback.
- Quay thanh ghi.
- Ví dụ tính tay.

**Trang sử dụng:**

```text
Trang 45:
Giới thiệu A5/1

Trang 46:
Cấu trúc TinyA5/1

Trang 47:
Majority và quy trình sinh số

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

- độ dài register;
- clocking bits;
- feedback taps;
- output taps;
- trạng thái ban đầu;
- key loading;
- frame loading;
- warm-up;
- sinh 228 bit;
- thứ tự đóng gói output;
- test vector.

**Trạng thái:**

`EXTERNAL TECHNICAL SOURCE`

---

### S3 - Real Time Cryptanalysis of A5/1 on a PC

**Tác giả:**

Alex Biryukov, Adi Shamir, David Wagner

**Năm:**

2000 / xuất bản trong FSE 2000 proceedings năm 2001

**Tên tài liệu:**

`Real Time Cryptanalysis of A5/1 on a PC`

**Thông tin xuất bản:**

Fast Software Encryption, FSE 2000, Lecture Notes in Computer Science, volume 1978, pages 1-18.

**URL:**

https://link.springer.com/book/10.1007/3-540-44706-7

**Dùng để tham khảo:**

- cấu trúc A5/1;
- độ dài register;
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

- R1[8], R2[10], R3[10];
- majority clocking;
- feedback taps;
- output từ các bit cao nhất;
- 228 output bits;
- 114 bit cho uplink và 114 bit cho downlink.

**Trạng thái:**

`EXTERNAL TECHNICAL SOURCE`

---

### S5 - 3GPP TS 43.020 / ETSI TS 143 020

**Tên:**

`Digital cellular telecommunications system (Phase 2+); Security-related network functions`

**Phần sử dụng:**

- Kc = 64 bit;
- COUNT = 22 bit;
- BLOCK1 / BLOCK2;
- 114 payload bits cho GMSK.

**URL:**

https://www.etsi.org/deliver/etsi_ts/143000_143099/143020/07.01.00_60/ts_143020v070100p.pdf

**Lưu ý:**

Tài liệu này cung cấp các tham số giao diện của Algorithm A5; đặc tả nội bộ chi tiết của A5 được GSM Association quản lý, không được công khai đầy đủ trong tài liệu này.

**Trạng thái:**

`EXTERNAL STANDARD SOURCE`

---

## 14. Technical Decisions / Open Issues

### TD-001 - Bit output của A5/1

#### Lecture / Slide

Slide ghi:

```text
s_i = x8 XOR y10 XOR z10
```

**Nguồn:**

[S1, trang 51]

#### External sources

S2 ghi:

```text
R1 output = bit 18
R2 output = bit 21
R3 output = bit 22
```

S4 cũng mô tả output được tạo từ các bit cao nhất của ba register.

**Nguồn:**

[S2]; [S4]

#### Possible reason

Có thể có sự khác biệt về:

- quy ước ký hiệu bit;
- cách biểu diễn register;
- cách ánh xạ vị trí bit;
- hoặc mô hình giảng dạy của slide và implementation/reference.

#### Impact

Ảnh hưởng trực tiếp đến:

```text
keystream
ciphertext
test vector
```

#### Status

`CONFLICT - OPEN`

---

### TD-003 - Chỉ số và thứ tự bit

#### Lecture / Slide

```text
X: x0 ... x18
Y: y0 ... y21
Z: z0 ... z22
```

#### External sources

S2 và S4 cũng sử dụng bit numbering bắt đầu từ 0.

#### Kết luận tạm thời

Cơ sở đánh số `0` được hỗ trợ bởi nhiều nguồn.

Tuy nhiên, bảng ánh xạ cuối cùng giữa:

```text
ký hiệu slide
        ↕
ký hiệu code
```

phải được khóa trong `coding_convention.md`.

#### Status

`VERIFIED / NEED LOCKING`

---

### TD-004 - Key loading, frame loading và warm-up

Đã xác minh:

```text
Key loading   = 64 chu kỳ
Frame loading = 22 chu kỳ
Warm-up       = 100 chu kỳ
```

Key loading:

```text
- clock cả ba register
- không dùng majority
- xử lý 64 bit key
- XOR từng key bit vào cả ba register
```

Frame loading:

```text
- clock cả ba register
- không dùng majority
- xử lý 22 bit frame
- XOR từng frame bit vào cả ba register
```

Warm-up:

```text
- bật majority clocking
- 100 chu kỳ
- không sử dụng output
```

**Nguồn:** [S2]; [S3]

**Status:**

`VERIFIED`

---

### TD-005 - Dữ liệu dài hơn một đoạn keystream

Một frame A5/1 tạo:

```text
114 bit A → B
114 bit B → A
```

Tổng:

```text
228 bit
```

Các nguồn đã xác minh quy mô keystream của một frame.

Tuy nhiên, các nguồn hiện tại không cung cấp một giao thức tổng quát cho việc nhận một **file tùy ý dài hơn một frame** ở cấp độ ứng dụng của đồ án.

Vì vậy:

```text
Không tự giả định cách chia file.
```

Quy tắc xử lý file dài cần được nhóm quyết định khi bước sang phần triển khai.

**Status:**

`OPEN`

---

## 15. Test vector tham khảo

Nguồn S2 cung cấp test vector đã được chính implementation tự kiểm tra.

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

Nguồn S2 đặt các giá trị trên vào `goodAtoB` và `goodBtoA`, sau đó chạy `keysetup()` và `run()` để so sánh output thực tế với test vector. [S2]

**Trạng thái:**

`SINGLE-SOURCE`

> Test vector này chỉ được đánh dấu `FINAL` trong project sau khi quy ước output bit tại TD-001 đã được nhóm chốt và điều kiện bit ordering trong spec khớp với test vector.

---

## 16. Kiểm tra nhất quán

### 16.1. Cấu trúc register

```text
R1 = 19 bit
R2 = 22 bit
R3 = 23 bit

Tổng = 64 bit
```

### 16.2. Clocking

```text
R1 clocking bit = 8
R2 clocking bit = 10
R3 clocking bit = 10
```

### 16.3. Feedback

```text
R1:
13, 16, 17, 18

R2:
20, 21

R3:
7, 20, 21, 22
```

### 16.4. Initialization

```text
Key:
64 bit

Frame:
22 bit

Warm-up:
100 chu kỳ
```

### 16.5. Output

```text
Slide:
x8 XOR y10 XOR z10

External:
R1[18] XOR R2[21] XOR R3[22]

→ TD-001 = CONFLICT
```

### 16.6. Frame keystream

```text
A → B:
114 bit

B → A:
114 bit

Tổng:
228 bit
```

---

## 17. Trạng thái hoàn thành Phase 1

### Đã xác minh

- [x] A5/1 là mã dòng trong GSM.
- [x] Đơn vị mã hóa là 1 bit.
- [x] Ba register có độ dài 19/22/23 bit.
- [x] Tổng trạng thái là 64 bit.
- [x] Clocking bits là 8/10/10.
- [x] Feedback taps của ba register.
- [x] Majority clocking.
- [x] Key có 64 bit.
- [x] Key loading có 64 chu kỳ.
- [x] Frame có 22 bit.
- [x] Frame loading có 22 chu kỳ.
- [x] Warm-up có 100 chu kỳ.
- [x] Output bị bỏ trong warm-up.
- [x] Một frame tạo 228 bit keystream theo nguồn ngoài.
- [x] 114 bit cho hướng A → B.
- [x] 114 bit cho hướng B → A.
- [x] Có test vector tham khảo từ S2.

### Còn phải chốt

- [ ] TD-001: output bit giữa slide và nguồn ngoài.
- [ ] TD-003: bảng ánh xạ cuối cùng giữa ký hiệu slide và code.
- [ ] TD-005: cách xử lý dữ liệu dài hơn một frame.
- [ ] Test vector cuối cùng sau khi TD-001 được chốt.

---

## 18. Kết luận

Bản đặc tả Phase 1 hiện mô tả đầy đủ các thành phần chính của A5/1:

```text
R1 / X
19 bit

R2 / Y
22 bit

R3 / Z
23 bit

        ↓

Majority clocking
R1[8], R2[10], R3[10]

        ↓

Feedback
R1: 13,16,17,18
R2: 20,21
R3: 7,20,21,22

        ↓

Key loading
64 chu kỳ

        ↓

Frame loading
22 chu kỳ

        ↓

Warm-up
100 chu kỳ

        ↓

Keystream
228 bit / frame
```

Điểm kỹ thuật duy nhất hiện đang có xung đột trực tiếp giữa slide và nguồn ngoài là **bit output**:

```text
Slide:
x8 XOR y10 XOR z10

External references:
R1[18] XOR R2[21] XOR R3[22]
```

Vấn đề này được giữ nguyên dưới dạng `TD-001 - CONFLICT` để nhóm quyết định ở D6, theo đúng quy tắc Phase 1.

---

## 19. Tham chiếu nhanh các thông số

| Thành phần | Giá trị hiện tại | Trạng thái |
|---|---|---|
| R1 / X | 19 bit | VERIFIED |
| R2 / Y | 22 bit | VERIFIED |
| R3 / Z | 23 bit | VERIFIED |
| Tổng state | 64 bit | VERIFIED |
| R1 clocking | bit 8 | VERIFIED |
| R2 clocking | bit 10 | VERIFIED |
| R3 clocking | bit 10 | VERIFIED |
| R1 feedback | 13,16,17,18 | VERIFIED |
| R2 feedback | 20,21 | VERIFIED |
| R3 feedback | 7,20,21,22 | VERIFIED |
| Key | 64 bit | VERIFIED |
| Key loading | 64 chu kỳ | VERIFIED |
| Frame | 22 bit | VERIFIED |
| Frame loading | 22 chu kỳ | VERIFIED |
| Warm-up | 100 chu kỳ | VERIFIED |
| Output / keystream | Slide và nguồn ngoài khác nhau | CONFLICT |
| Keystream / frame | 228 bit | VERIFIED |
| A → B | 114 bit | VERIFIED |
| B → A | 114 bit | VERIFIED |
| File dài | Chưa có quy tắc ở Phase 1 | OPEN |
