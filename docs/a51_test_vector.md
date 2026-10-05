# A5/1 Test Vector

> **Owner:** Vũ  
> **Branch:** `docs/vu-a51`  
> **File:** `docs/a51_test_vector.md`  
> **Phase:** Phase 1  
> **Overall Status:** `SINGLE-SOURCE`  
> **Related Technical Decisions:** `TD-001`, `TD-003`, `TD-004`, `TD-005`

---

## 1. Mục đích

File này ghi lại test vector tham chiếu cho thuật toán A5/1 nhằm kiểm tra:

- quá trình khởi tạo các thanh ghi;
- quá trình nạp khóa (`key loading`);
- quá trình nạp frame (`frame loading`);
- quá trình warm-up;
- cơ chế majority clocking;
- thứ tự bit đầu vào;
- quy tắc sinh keystream;
- độ dài keystream;
- kết quả output kỳ vọng;
- khả năng đối chiếu giữa implementation và test vector tham chiếu.

Test vector trong file này được lấy từ implementation A5/1 pedagogical implementation của Marc Briceno, Ian Goldberg và David Wagner.

---

# 2. Trạng thái verification

## Overall Status

```text
SINGLE-SOURCE
```

## Lý do

Test vector hiện tại được lấy từ một implementation tham khảo bên ngoài và có đầy đủ các thông tin cần thiết về:

- key;
- frame;
- key loading;
- frame loading;
- warm-up;
- output;
- reference keystream.

Tuy nhiên, Phase 1 hiện vẫn có vấn đề `TD-001` liên quan đến quy tắc sinh output bit:

- slide môn học mô tả output theo một quy tắc;
- implementation tham khảo bên ngoài sử dụng quy tắc khác.

Vì vậy test vector này **chưa được đánh dấu `FINAL`**.

Trạng thái hiện tại là:

```text
SINGLE-SOURCE
```

Sau khi nhóm giải quyết `TD-001` và thống nhất quy ước bit ordering, test vector mới có thể được chuyển sang trạng thái cuối cùng.

---

# 3. Source

## [S1] Course Slides

**Document:**

`Chương 2 - Mã hóa khóa đối xứng`

Nội dung liên quan:

- cấu trúc TinyA5/1;
- cấu trúc A5/1;
- majority clocking;
- feedback taps;
- output generation;
- bit indexing.

---

## [S2] Briceno, Goldberg, Wagner

**Title:**

`A5/1 Pedagogical Implementation`

**URL:**

https://github.com/NSAPlayset/TWILIGHTVEGETABLE/blob/master/A5.1/C/A5.1.c

Nội dung được sử dụng trong test vector:

- khởi tạo các register;
- key loading;
- frame loading;
- warm-up;
- majority clocking;
- output taps;
- reference test vector.

---

## [S3] Biryukov, Shamir, Wagner

**Title:**

`Real Time Cryptanalysis of A5/1 on a PC`

**URL:**

https://www.iacr.org/archive/fse2000/19780071/19780071.pdf

Nội dung tham khảo:

- cấu trúc A5/1;
- clocking mechanism;
- key/frame setup;
- warm-up;
- keystream generation.

---

## [S4] Gendrullis, Novotný, Rupp

**Title:**

`A Real-World Attack Breaking A5/1`

**URL:**

https://www.iacr.org/archive/ches2008/51540262/51540262.pdf

Nội dung tham khảo:

- clocking bits;
- feedback taps;
- output taps;
- cấu trúc A5/1;
- keystream generation.

---

## [S5] 3GPP TS 43.020

**Title:**

`Security related network functions`

**URL:**

https://www.etsi.org/deliver/etsi_ts/143000_143099/143020/07.01.00_60/ts_143020v070100p.pdf

Nội dung tham khảo:

- key length;
- frame/count input length;
- payload length.

---

# 4. Input

## 4.1. Key

```text
Key = 0x1223456789ABCDEF
```

Độ dài key:

```text
64 bits
```

### Hexadecimal

```text
12 23 45 67 89 AB CD EF
```

### Binary

```text
00010010 00100011 01000101 01100111
10001001 10101011 11001101 11101111
```

---

## 4.2. Frame

```text
Frame = 0x134
```

Độ dài:

```text
22 bits
```

Frame được biểu diễn dưới dạng hexadecimal. Khi thực hiện frame loading, các bit của frame được sử dụng theo quy ước bit ordering của implementation tham khảo.

---

# 5. Tổng quan điều kiện chạy

Test vector được thực hiện theo thứ tự:

```text
1. Khởi tạo R1 = 0
2. Khởi tạo R2 = 0
3. Khởi tạo R3 = 0
4. Key loading: 64 cycles
5. Frame loading: 22 cycles
6. Warm-up: 100 cycles
7. Sinh keystream: 228 bits
```

Tóm tắt:

| Thành phần | Giá trị |
|---|---:|
| Key | `0x1223456789ABCDEF` |
| Key length | 64 bits |
| Frame | `0x134` |
| Frame length | 22 bits |
| Key loading | 64 cycles |
| Frame loading | 22 cycles |
| Warm-up | 100 cycles |
| Keystream | 228 bits |
| A → B | 114 bits |
| B → A | 114 bits |

---

# 6. Khởi tạo các thanh ghi

Trước khi bắt đầu key loading:

```text
R1 = 0000000000000000000
R2 = 0000000000000000000000
R3 = 00000000000000000000000
```

Độ dài các thanh ghi:

```text
R1 = 19 bits
R2 = 22 bits
R3 = 23 bits
```

Các register được khởi tạo về 0.

---

# 7. Key loading

## 7.1. Số vòng

Key có:

```text
64 bits
```

Do đó key loading được thực hiện trong:

```text
64 cycles
```

---

## 7.2. Cách nạp key

Ở mỗi cycle:

1. Lấy một bit của key.
2. XOR bit đó vào R1.
3. XOR bit đó vào R2.
4. XOR bit đó vào R3.
5. Clock cả ba register.

Trong giai đoạn key loading, không sử dụng majority clocking như giai đoạn sinh keystream.

Pseudocode:

```text
for i = 0 to 63:
    key_bit = key[i]

    R1 = R1 XOR key_bit
    R2 = R2 XOR key_bit
    R3 = R3 XOR key_bit

    clock R1
    clock R2
    clock R3
```

---

# 8. Bit ordering của key

Implementation tham khảo đọc bit key theo thứ tự:

```text
LSB-first
```

trong từng byte.

Cách lấy bit trong implementation:

```c
(key[i/8] >> (i&7)) & 1
```

Điều này có nghĩa với một byte:

```text
b7 b6 b5 b4 b3 b2 b1 b0
```

thứ tự các bit được đưa vào là:

```text
b0 → b1 → b2 → b3 → b4 → b5 → b6 → b7
```

---

# 9. Frame loading

Sau khi hoàn thành key loading, thực hiện frame loading.

Frame có:

```text
22 bits
```

Do đó frame loading gồm:

```text
22 cycles
```

---

## 9.1. Cách nạp frame

Ở mỗi cycle:

1. Lấy một bit của frame.
2. XOR bit đó vào R1.
3. XOR bit đó vào R2.
4. XOR bit đó vào R3.
5. Clock cả ba register.

Pseudocode:

```text
for i = 0 to 21:
    frame_bit = frame[i]

    R1 = R1 XOR frame_bit
    R2 = R2 XOR frame_bit
    R3 = R3 XOR frame_bit

    clock R1
    clock R2
    clock R3
```

---

# 10. Bit ordering của frame

Trong implementation tham khảo, frame cũng được đọc theo:

```text
LSB-first
```

Do đó thứ tự sử dụng là:

```text
frame bit 0
→ frame bit 1
→ frame bit 2
→ ...
→ frame bit 21
```

---

# 11. Warm-up

Sau khi hoàn thành:

```text
64 cycles key loading
+
22 cycles frame loading
```

tiến hành:

```text
100 warm-up cycles
```

Trong warm-up:

- majority clocking được bật;
- các register được clock theo majority bit;
- output được tạo ra nhưng không được sử dụng;
- output trong 100 cycle warm-up bị discard.

Mục đích của warm-up là đưa trạng thái của các register đến trạng thái dùng để sinh keystream.

Pseudocode:

```text
for i = 0 to 99:
    m = majority(R1[8], R2[10], R3[10])

    if R1[8] == m:
        clock R1

    if R2[10] == m:
        clock R2

    if R3[10] == m:
        clock R3

    discard output
```

---

# 12. Majority clocking

Ba register sử dụng các clocking bit:

```text
R1[8]
R2[10]
R3[10]
```

Majority bit được xác định bởi:

```text
m = majority(R1[8], R2[10], R3[10])
```

Majority có nghĩa:

```text
m = 1
```

nếu ít nhất 2 trong 3 bit bằng 1.

Ngược lại:

```text
m = 0
```

nếu ít nhất 2 trong 3 bit bằng 0.

Sau đó:

```text
if R1[8] == m:
    clock R1

if R2[10] == m:
    clock R2

if R3[10] == m:
    clock R3
```

Vì vậy trong mỗi cycle:

- có thể clock cả 3 register;
- hoặc clock 2 register;

tùy thuộc vào majority bit.

---

# 13. Sinh keystream

Sau warm-up bắt đầu sinh keystream thực tế.

Tổng số output:

```text
228 bits
```

Bao gồm:

```text
114 bits A → B
+
114 bits B → A
```

Do đó:

```text
228 = 114 + 114
```

---

# 14. Output bit theo implementation tham khảo

Implementation tham khảo sử dụng các output taps:

```text
R1[18]
R2[21]
R3[22]
```

Output được tính:

```text
s = R1[18] XOR R2[21] XOR R3[22]
```

Quy tắc này là quy tắc được sử dụng để tạo reference test vector ở file này.

---

# 15. Conflict với slide môn học

Đây là technical decision quan trọng của Phase 1.

Slide môn học mô tả generated bit theo:

```text
s_i = x8 XOR y10 XOR z10
```

Trong khi implementation tham khảo sử dụng:

```text
s_i = R1[18] XOR R2[21] XOR R3[22]
```

Vì vậy hiện tại tồn tại:

```text
TD-001
```

với trạng thái:

```text
CONFLICT
```

## Course slide

```text
x8 XOR y10 XOR z10
```

## External reference

```text
R1[18] XOR R2[21] XOR R3[22]
```

Hai quy tắc này không được tự ý hợp nhất hoặc tự chọn một bên.

Nhóm cần chốt quy ước chính thức trước khi test vector được đánh dấu `FINAL`.

---

# 16. Reference test vector

## 16.1. Key

```text
0x1223456789ABCDEF
```

## 16.2. Frame

```text
0x134
```

## 16.3. Keystream A → B

```text
0x534EAA582FE8151AB6E1855A728C00
```

## 16.4. Keystream B → A

```text
0x24FD35A35D5FB6526D32F906DF1AC0
```

---

# 17. Kết quả kỳ vọng đầy đủ

```text
Key   = 0x1223456789ABCDEF
Frame = 0x134
```

Sau:

```text
64 key-loading cycles
22 frame-loading cycles
100 warm-up cycles
```

expected output theo external reference là:

```text
A → B
0x534EAA582FE8151AB6E1855A728C00
```

và:

```text
B → A
0x24FD35A35D5FB6526D32F906DF1AC0
```

---

# 18. Độ dài output

| Output | Length |
|---|---:|
| A → B | 114 bits |
| B → A | 114 bits |
| Total | 228 bits |

Do đó:

```text
114 + 114 = 228 bits
```

---

# 19. Verification procedure

Có thể dùng quy trình sau để kiểm tra implementation:

```text
INPUT
  |
  v
Key = 0x1223456789ABCDEF
  |
  v
Initialize R1 = R2 = R3 = 0
  |
  v
Key loading
64 cycles
  |
  v
Frame = 0x134
  |
  v
Frame loading
22 cycles
  |
  v
Warm-up
100 cycles
  |
  v
Generate keystream
228 bits
  |
  +-----------------------+
  |                       |
  v                       v
A → B                   B → A
114 bits                114 bits
  |                       |
  +-----------+-----------+
              |
              v
        Compare reference
```

Reference:

```text
A → B = 0x534EAA582FE8151AB6E1855A728C00

B → A = 0x24FD35A35D5FB6526D32F906DF1AC0
```

---

# 20. Điều kiện để implementation được coi là match

Implementation chỉ được coi là match test vector khi các điều kiện chính sau được thống nhất và thực hiện đúng:

1. Register initialization đúng.
2. Key loading = 64 cycles.
3. Frame loading = 22 cycles.
4. Key bit ordering đúng.
5. Frame bit ordering đúng.
6. Warm-up = 100 cycles.
7. Majority clocking đúng.
8. Output tap convention đúng.
9. Sinh đủ 228 output bits.
10. Output match reference vector.

Nếu output khác reference, cần kiểm tra lần lượt:

```text
1. Key input
2. Frame input
3. Bit ordering
4. Register indexing
5. Feedback taps
6. Majority clocking
7. Warm-up
8. Output taps
9. Number of generated bits
```

Không được kết luận implementation sai trước khi xác định implementation đang sử dụng cùng convention với test vector hay chưa.

---

# 21. Reference pseudocode

Pseudocode dưới đây mô tả convention của external reference được sử dụng để tạo test vector:

```text
R1 = 0
R2 = 0
R3 = 0

for i = 0..63:
    k = key[i]

    R1 = R1 XOR k
    R2 = R2 XOR k
    R3 = R3 XOR k

    clock R1
    clock R2
    clock R3

for i = 0..21:
    f = frame[i]

    R1 = R1 XOR f
    R2 = R2 XOR f
    R3 = R3 XOR f

    clock R1
    clock R2
    clock R3

repeat 100 times:
    m = majority(R1[8], R2[10], R3[10])

    if R1[8] == m:
        clock R1

    if R2[10] == m:
        clock R2

    if R3[10] == m:
        clock R3

    discard output

repeat 228 times:
    m = majority(R1[8], R2[10], R3[10])

    if R1[8] == m:
        clock R1

    if R2[10] == m:
        clock R2

    if R3[10] == m:
        clock R3

    output =
        R1[18] XOR
        R2[21] XOR
        R3[22]
```

> **Important:** Pseudocode trên mô tả external reference convention. Không sử dụng pseudocode này để tự động thay thế quy ước trong course slide khi `TD-001` chưa được nhóm chốt.

---

# 22. Technical Decisions / Open Issues

## TD-001 - Output bit discrepancy

### Problem

Course slide:

```text
s_i = x8 XOR y10 XOR z10
```

External reference:

```text
s_i = R1[18] XOR R2[21] XOR R3[22]
```

### Status

```text
CONFLICT
```

### Action

Không tự ý chọn một trong hai.

Cần nhóm/GĐ3 xác nhận quy ước chính thức trước khi đánh dấu test vector là:

```text
FINAL
```

---

## TD-003 - Bit indexing / bit ordering

### Problem

Cần thống nhất:

- cách đánh số bit trong register;
- cách đọc key;
- cách đọc frame;
- cách biểu diễn giá trị hexadecimal;
- cách biểu diễn output keystream.

### Current external reference

Bit của key/frame được đọc theo:

```text
LSB-first
```

trong quá trình loading.

### Status

```text
NEED LOCKING
```

### Action

Đặc tả chính thức phải ghi rõ một convention duy nhất và implementation/test phải sử dụng cùng convention đó.

---

## TD-004 - Key / Frame / Warm-up

### Reference condition

```text
Key loading  = 64 cycles
Frame loading = 22 cycles
Warm-up       = 100 cycles
```

### Status

```text
REFERENCE
```

Các giá trị này được lấy từ external implementation được sử dụng để xây dựng test vector.

---

## TD-005 - Data longer than one keystream segment

Reference test vector tạo:

```text
228 bits
```

trong đó:

```text
114 bits A → B
114 bits B → A
```

Khi implementation xử lý dữ liệu dài hơn một đoạn keystream, specification cần nêu rõ cách tiếp tục sinh keystream và cách áp dụng keystream cho phần dữ liệu tiếp theo.

### Status

```text
OPEN
```

---

# 23. Test vector status

| Item | Value | Status |
|---|---|---|
| Key | `0x1223456789ABCDEF` | Available |
| Key length | 64 bits | Reference |
| Frame | `0x134` | Available |
| Frame length | 22 bits | Reference |
| Key loading | 64 cycles | Reference |
| Frame loading | 22 cycles | Reference |
| Warm-up | 100 cycles | Reference |
| Keystream | 228 bits | Reference |
| A → B | 114 bits | Reference |
| B → A | 114 bits | Reference |
| Input bit order | LSB-first | Reference |
| Clocking bits | R1[8], R2[10], R3[10] | Reference |
| External output taps | R1[18], R2[21], R3[22] | Reference |
| Slide output rule | x8 XOR y10 XOR z10 | Course slide |
| Output convention | Different between sources | `CONFLICT` |
| Overall verification | One main test-vector source | `SINGLE-SOURCE` |

---

# 24. Why this test vector is not FINAL

Test vector hiện tại không được đánh dấu `FINAL` vì còn tồn tại sự khác nhau giữa:

```text
Course slide
x8 XOR y10 XOR z10
```

và:

```text
External reference
R1[18] XOR R2[21] XOR R3[22]
```

Do đó trạng thái đúng của file tại Phase 1 là:

```text
SINGLE-SOURCE
```

và:

```text
TD-001 = CONFLICT
```

Không được tự ý sửa thành:

```text
VERIFIED
```

hoặc:

```text
FINAL
```

cho đến khi nhóm chốt quy ước.

---

# 25. Final checklist

## Input

- [x] Key được ghi đầy đủ.
- [x] Frame được ghi đầy đủ.
- [x] Key length = 64 bits.
- [x] Frame length = 22 bits.

## Loading

- [x] Key loading = 64 cycles.
- [x] Frame loading = 22 cycles.
- [x] Key bit ordering được ghi.
- [x] Frame bit ordering được ghi.

## Warm-up

- [x] Warm-up = 100 cycles.
- [x] Output trong warm-up bị discard.

## Keystream

- [x] Keystream length = 228 bits.
- [x] A → B = 114 bits.
- [x] B → A = 114 bits.
- [x] Reference output được ghi đầy đủ.

## Verification

- [x] Source được ghi.
- [x] Source URL được ghi.
- [x] Overall status = `SINGLE-SOURCE`.
- [x] TD-001 được ghi nhận.
- [x] TD-003 được ghi nhận.
- [x] TD-004 được ghi nhận.
- [x] TD-005 được ghi nhận.
- [x] Không tự ý giải quyết conflict.
- [ ] Chưa đánh dấu `FINAL`.
- [ ] Chưa khóa output convention.
- [ ] Chưa hoàn tất cross-check độc lập.

---

# 26. Conclusion

Test vector tham chiếu sử dụng:

```text
Key   = 0x1223456789ABCDEF
Frame = 0x134
```

với:

```text
Key loading   = 64 cycles
Frame loading = 22 cycles
Warm-up       = 100 cycles
Keystream     = 228 bits
```

Reference output:

```text
A → B = 0x534EAA582FE8151AB6E1855A728C00

B → A = 0x24FD35A35D5FB6526D32F906DF1AC0
```

Trạng thái hiện tại:

```text
SINGLE-SOURCE
```

Technical decision còn mở:

```text
TD-001 = CONFLICT
TD-003 = NEED LOCKING
TD-004 = REFERENCE
TD-005 = OPEN
```

Test vector chỉ được chuyển sang `FINAL` sau khi nhóm thống nhất:

```text
1. Output bit convention
2. Bit indexing
3. Bit ordering
4. Reference implementation convention
```

---

# 27. Sources

## [S1] Course Slides

`Chương 2 - Mã hóa khóa đối xứng`

Nội dung sử dụng:

- TinyA5/1;
- A5/1;
- majority clocking;
- register structure;
- feedback taps;
- output generation.

---

## [S2] Briceno, Goldberg, Wagner

`A5/1 Pedagogical Implementation`

https://github.com/NSAPlayset/TWILIGHTVEGETABLE/blob/master/A5.1/C/A5.1.c

Reference:

```text
Key   = 0x1223456789ABCDEF
Frame = 0x134

A → B = 0x534EAA582FE8151AB6E1855A728C00

B → A = 0x24FD35A35D5FB6526D32F906DF1AC0
```

---

## [S3] Biryukov, Shamir, Wagner

`Real Time Cryptanalysis of A5/1 on a PC`

https://www.iacr.org/archive/fse2000/19780071/19780071.pdf

---

## [S4] Gendrullis, Novotný, Rupp

`A Real-World Attack Breaking A5/1`

https://www.iacr.org/archive/ches2008/51540262/51540262.pdf

---

## [S5] 3GPP TS 43.020

`Security related network functions`

https://www.etsi.org/deliver/etsi_ts/143000_143099/143020/07.01.00_60/ts_143020v070100p.pdf

---

# 28. File status

```text
Owner: Vũ
Branch: docs/vu-a51
File: docs/a51_test_vector.md

Overall Status:
SINGLE-SOURCE

Open:
TD-001
TD-003
TD-005

Reference:
TD-004

Final:
NO
```
