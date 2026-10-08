# Bộ kiểm thử A5/1 (A5/1 Test Vector)

> **Owner:** Lại Hoàng Thế Vũ  
> **Branch:** `docs/vu-a51`  
> **Giai đoạn:** Phase 1 - Specification and Verification  
> **File:** `docs/a51_test_vector.md`  
> **Trạng thái:** `SINGLE-SOURCE`

---

## 1. Nguồn (Source)

Bộ kiểm thử sử dụng nguồn tham chiếu:

**Marc Briceno, Ian Goldberg, David Wagner — A5/1 Pedagogical Implementation (`A5.1.c`)**

Ký hiệu trong tài liệu:

```text
[S2]
```

Nguồn cung cấp trực tiếp:

- khóa K;
- số khung (frame number);
- quy trình nạp khóa;
- quy trình nạp số khung;
- thứ tự bít;
- giai đoạn khởi động (warm-up);
- dãy bít sinh ra (keystream);
- đầu ra đúng đã biết trước để kiểm tra implementation.

**Trạng thái:** `SINGLE-SOURCE`

---

## 2. Tài liệu / URL (URL / Document)

**Tên tài liệu:**

```text
A5/1 Pedagogical Implementation
```

**Tác giả:**

```text
Marc Briceno
Ian Goldberg
David Wagner
```

**File:**

```text
A5.1.c
```

**URL:**

https://github.com/NSAPlayset/TWILIGHTVEGETABLE/blob/master/A5.1/C/A5.1.c

---

## 3. Khóa K (Key)

Khóa sử dụng trong bộ kiểm thử:

```text
K = 0x1223456789ABCDEF
```

Khóa gồm:

```text
8 byte = 64 bít
```

Biểu diễn theo byte:

```text
12 23 45 67 89 AB CD EF
```

Biểu diễn nhị phân:

```text
00010010 00100011 01000101 01100111
10001001 10101011 11001101 11101111
```

**Nguồn:** `[S2]`  
**Nhãn:** `VERIFIED`

---

## 4. Số khung (Frame Number)

Số khung sử dụng:

```text
Frame = 0x134
```

Độ dài:

```text
22 bít
```

Trong source:

```c
word frame = 0x134;
```

**Nguồn:** `[S2]`  
**Nhãn:** `VERIFIED`

---

## 5. Thứ tự bít (Bit Ordering)

### 5.1. Khóa K

Trong quá trình nạp khóa, source lấy:

```text
bít ít quan trọng nhất trước (LSB-first)
```

Công thức:

```text
(key[i/8] >> (i & 7)) & 1
```

với:

```text
i = 0 ... 63
```

Do đó trong từng byte:

```text
bít 0
→ bít 1
→ bít 2
→ ...
→ bít 7
```

Ví dụ:

```text
0x12 = 00010010
```

Ba bít đầu được xử lý:

```text
bít 0 = 0
bít 1 = 1
bít 2 = 0
```

**Nguồn:** `[S2]`

---

### 5.2. Số khung

Các bít của số khung cũng được xử lý theo:

```text
bít ít quan trọng nhất trước (LSB-first)
```

Công thức:

```text
(frame >> i) & 1
```

với:

```text
i = 0 ... 21
```

Thứ tự:

```text
frame bit 0
→ frame bit 1
→ ...
→ frame bit 21
```

**Nguồn:** `[S2]`

---

### 5.3. Dãy bít sinh ra

Khi lưu dãy bít sinh ra (keystream) vào byte, source sử dụng:

```text
bít có trọng số cao nhất trước (MSB-first)
```

Công thức:

```text
getbit() << (7 - (i & 7))
```

Tóm tắt:

```text
Khóa K:
LSB-first

Số khung:
LSB-first

Keystream khi lưu vào byte:
MSB-first
```

**Nguồn:** `[S2]`

---

## 6. Nạp khóa K (Key Loading)

### 6.1. Khởi tạo

Ba thanh ghi (register) được đưa về `0`:

```text
R1 = 0
R2 = 0
R3 = 0
```

**Nguồn:** `[S2]`

---

### 6.2. Số lần nạp

Khóa có:

```text
64 bít
```

nên quá trình nạp khóa thực hiện:

```text
64 lần
```

Mỗi lần xử lý một bít của khóa.

---

### 6.3. Quy trình

Trong mỗi lần:

```text
1. Quay R1.
2. Quay R2.
3. Quay R3.
4. Lấy một bít của khóa theo thứ tự LSB-first.
5. XOR bít khóa vào R1, R2 và R3.
```

Pseudocode:

```text
for i = 0 .. 63:

    Quay R1
    Quay R2
    Quay R3

    key_bit = (key[i/8] >> (i & 7)) & 1

    R1 = R1 XOR key_bit
    R2 = R2 XOR key_bit
    R3 = R3 XOR key_bit
```

Trong giai đoạn này, quy tắc quay dựa trên hàm `maj` tạm thời không được sử dụng.

**Nguồn:** `[S2]`

---

## 7. Nạp số khung (Frame Loading)

Sau khi nạp khóa, số khung được nạp trong:

```text
22 lần
```

Mỗi lần:

```text
1. Quay R1.
2. Quay R2.
3. Quay R3.
4. Lấy một bít của số khung theo thứ tự LSB-first.
5. XOR bít đó vào R1, R2 và R3.
```

Pseudocode:

```text
for i = 0 .. 21:

    Quay R1
    Quay R2
    Quay R3

    frame_bit = (frame >> i) & 1

    R1 = R1 XOR frame_bit
    R2 = R2 XOR frame_bit
    R3 = R3 XOR frame_bit
```

Quy tắc quay dựa trên hàm `maj` vẫn chưa được sử dụng trong giai đoạn này.

**Nguồn:** `[S2]`

---

## 8. Giai đoạn khởi động (Warm-up)

Sau khi nạp khóa K và số khung, A5/1 thực hiện:

```text
100 lần
```

Trong giai đoạn này, quy tắc quay dựa trên **hàm maj (hàm chiếm đa số)** được sử dụng.

Ba bít dùng để tính hàm `maj`:

```text
R1[8]
R2[10]
R3[10]
```

Tính:

```text
m = maj(R1[8], R2[10], R3[10])
```

Sau đó:

```text
Nếu R1[8] = m → Quay R1
Nếu R2[10] = m → Quay R2
Nếu R3[10] = m → Quay R3
```

Quá trình trên được lặp:

```text
100 lần
```

Trong 100 lần này:

```text
không sử dụng bít sinh ra
```

**Nguồn:** `[S2]`

---

## 9. Điều kiện kiểm thử (Conditions)

| Thành phần | Giá trị |
|---|---|
| Khóa K | `0x1223456789ABCDEF` |
| Độ dài khóa | 64 bít |
| Số khung | `0x134` |
| Độ dài số khung | 22 bít |
| Trạng thái ban đầu | `R1 = R2 = R3 = 0` |
| Nạp khóa | 64 lần |
| Thứ tự bít khóa | LSB-first |
| Nạp số khung | 22 lần |
| Thứ tự bít số khung | LSB-first |
| Giai đoạn khởi động | 100 lần |
| Quy tắc quay khi khởi động | Theo hàm `maj` |
| Bít sinh ra trong warm-up | Không sử dụng |
| Keystream A → B | 114 bít |
| Keystream B → A | 114 bít |
| Tổng keystream | 228 bít |
| Cách lưu keystream | MSB-first trong từng byte |

---

## 10. Sinh dãy bít (Keystream Generation)

Sau giai đoạn khởi động, mỗi bít của dãy bít sinh ra được tạo theo thứ tự:

```text
1. Đọc R1[8], R2[10], R3[10].

2. Tính:
   m = maj(R1[8], R2[10], R3[10])

3. Nếu R1[8] = m:
   Quay R1.

4. Nếu R2[10] = m:
   Quay R2.

5. Nếu R3[10] = m:
   Quay R3.

6. Sau khi quay, lấy bít sinh ra của mỗi thanh ghi.

7. XOR ba bít để thu được một bít keystream.
```

Theo S2, các bít sinh ra được lấy tại:

```text
R1[18]
R2[21]
R3[22]
```

Do đó:

```text
KS[i] = R1[18] XOR R2[21] XOR R3[22]
```

Bít keystream được lấy:

```text
sau khi quay các thanh ghi
```

**Nguồn:** `[S2]`

---

### 10.1. Hướng A → B

Số bít:

```text
114 bít
```

---

### 10.2. Hướng B → A

Số bít:

```text
114 bít
```

---

### 10.3. Tổng

```text
114 + 114 = 228 bít
```

**Nguồn:** `[S2]`

---

## 11. Dãy bít mong đợi (Expected Keystream)

### 11.1. A → B

```text
0x534EAA582FE8151AB6E1855A728C00
```

Biểu diễn theo byte:

```text
53 4E AA 58 2F E8 15 1A B6 E1 85 5A 72 8C 00
```

---

### 11.2. B → A

```text
0x24FD35A35D5FB6526D32F906DF1AC0
```

Biểu diễn theo byte:

```text
24 FD 35 A3 5D 5F B6 52 6D 32 F9 06 DF 1A C0
```

**Nguồn:** `[S2]`

---

### 11.3. Độ dài

Mỗi hướng có:

```text
114 bít
```

Bộ đệm dùng:

```text
15 byte
```

Trong đó:

```text
14 byte = 112 bít
```

và còn:

```text
2 bít
```

ở byte cuối.

Hai bít còn lại được lưu ở các vị trí có trọng số cao nhất của byte cuối.

**Nguồn:** `[S2]`

---

## 12. Bảng bộ kiểm thử

| Nguồn | Tài liệu | Khóa K | Số khung | Keystream mong đợi | Thứ tự bít | Trạng thái |
|---|---|---|---|---|---|---|
| S2 | `A5.1.c` | `0x1223456789ABCDEF` | `0x134` | A→B: `0x534EAA582FE8151AB6E1855A728C00`; B→A: `0x24FD35A35D5FB6526D32F906DF1AC0` | Key/frame LSB-first; keystream MSB-first khi lưu | `SINGLE-SOURCE` |
| Nguồn độc lập thứ hai | Chưa có cùng bộ điều kiện | Không áp dụng | Không áp dụng | Không áp dụng | Không áp dụng | `UNVERIFIED` |
| Kết luận Phase 1 | Kiểm chứng lại ở GĐ3 | Theo S2 | Theo S2 | Theo S2 | Theo S2 | `SINGLE-SOURCE` |

---

## 13. Xác minh (Verification)

S2 thực hiện kiểm tra bằng các giá trị:

```text
Khóa K:
0x1223456789ABCDEF

Số khung:
0x134

A → B:
0x534EAA582FE8151AB6E1855A728C00

B → A:
0x24FD35A35D5FB6526D32F906DF1AC0
```

Quy trình kiểm tra:

```text
1. Khởi tạo khóa K.
2. Khởi tạo số khung.
3. Thiết lập trạng thái A5/1.
4. Sinh 114 bít cho hướng A → B.
5. Sinh 114 bít cho hướng B → A.
6. So sánh kết quả thực tế với các giá trị tham chiếu.
```

Nếu kết quả khớp hoàn toàn với hai chuỗi tham chiếu thì implementation theo quy ước S2 vượt qua bộ kiểm thử.

Bộ kiểm thử hiện có một nguồn cung cấp trực tiếp đầy đủ:

- khóa K;
- số khung;
- thứ tự bít;
- giai đoạn khởi động;
- dãy bít sinh ra mong đợi.

Do đó trạng thái hiện tại:

```text
SINGLE-SOURCE
```

Bộ kiểm thử cần được kiểm chứng lại bằng implementation của nhóm ở GĐ3.

---

## 14. TD-001 - Bít sinh ra của A5/1

Trong slide môn học:

```text
s_i = x_8 XOR y_10 XOR z_10
```

Trong S2:

```text
KS[i] = R1[18] XOR R2[21] XOR R3[22]
```

Hai quy tắc khác nhau.

**Trạng thái:**

```text
CONFLICT
```

Sự khác biệt này ảnh hưởng trực tiếp đến:

```text
dãy bít sinh ra (keystream)
bản mã (ciphertext)
kết quả của bộ kiểm thử
```

Bộ kiểm thử hiện tại sử dụng quy ước của S2.

---

## 15. TD-003 - Thứ tự bít

Quy ước trong S2:

```text
R1: bít 0 ... 18
R2: bít 0 ... 21
R3: bít 0 ... 22
```

Thứ tự dữ liệu:

```text
Khóa K:
LSB-first

Số khung:
LSB-first

Keystream khi lưu:
MSB-first
```

**Trạng thái:**

```text
VERIFIED theo S2
```

---

## 16. TD-004 - Khóa, số khung và giai đoạn khởi động

```text
Khóa K:
64 bít

Nạp khóa:
64 lần

Số khung:
22 bít

Nạp số khung:
22 lần

Giai đoạn khởi động:
100 lần
```

Trong quá trình nạp khóa và số khung:

```text
Quay cả R1, R2, R3
Không dùng quy tắc quay theo hàm maj
```

Trong giai đoạn khởi động:

```text
Dùng quy tắc quay theo hàm maj
Không sử dụng bít sinh ra
```

**Nguồn:** `[S2]`

**Trạng thái:**

```text
VERIFIED
```

---

## 17. Ghi chú (Notes)

Các ký hiệu chính:

```text
R1 = thanh ghi 19 bít
R2 = thanh ghi 22 bít
R3 = thanh ghi 23 bít
```

Các thuật ngữ sử dụng:

```text
thanh ghi (register)
bít điều khiển quay (clocking bit)
hàm maj / hàm chiếm đa số (majority)
giá trị phản hồi (feedback)
dãy bít sinh ra (keystream)
bản rõ (plaintext)
bản mã (ciphertext)
số khung (frame number)
giai đoạn khởi động (warm-up)
thứ tự bít (bit ordering)
```

Trạng thái bộ kiểm thử:

```text
SINGLE-SOURCE
```

Điều kiện để chuyển sang bộ kiểm thử cuối cùng:

```text
1. TD-001 được chốt.
2. Thứ tự bít của implementation khớp với đặc tả.
3. Implementation của nhóm tái tạo được keystream mong đợi.
4. Các quy ước trong coding_convention.md được khóa.
```

---

## 18. Tóm tắt

```text
Khóa K:
0x1223456789ABCDEF

Số khung:
0x134

Nạp khóa:
64 lần
LSB-first

Nạp số khung:
22 lần
LSB-first

Giai đoạn khởi động:
100 lần

Dãy bít sinh ra:
228 bít

A → B:
114 bít
0x534EAA582FE8151AB6E1855A728C00

B → A:
114 bít
0x24FD35A35D5FB6526D32F906DF1AC0

Cách lưu keystream:
MSB-first

Trạng thái:
SINGLE-SOURCE

TD-001:
CONFLICT
```
