
# TinyA5/1 Specification

## 0. Ghi chú đọc thô 

### 0.1. Giới thiệu hệ mã A5/1 
* A5/1 được dùng trong mạng điện thoại GSM, để bảo mật dữ liệu trong quá trình liên lạc giữa máy tính điện thoại và trạm thu phát sóng vô tuyến.
* Đơn vị mã hoá của A5/1 là 1 bít. Bộ sinh số mỗi lần sẽ sinh ra hoặc bít 0 hoặc bít 1 để sử dụng trong phép XOR.
* Trong bài học giới hạn xét mô hình thu nhỏ của A5/1, gọi tắt là **TinyA5/1**.

---

### 0.2. Cấu trúc các thanh ghi và Khóa K 
Bộ sinh số gồm 3 thanh ghi X, Y, Z:
* X gồm 6 bít ($x_0, x_1, \dots, x_5$)
* Y gồm 8 bít ($y_0, y_1, \dots, y_7$)
* Z gồm 9 bít ($z_0, z_1, \dots, z_8$)
* Khoá K có chiều dài 23 bít là được phân bổ vào các thanh ghi: $K \longrightarrow XYZ$
* **Các thanh ghi X, Y, Z được biến đổi theo các quy tắc quay**

---

### 0.3. Nội dung thuật toán TinyA5/1 
* **Đầu vào:** $P, K$
* **Đầu ra:** $C$
* **Nội dung thuật toán:**
  * Phân bổ K vào các thanh ghi XYZ
  * Tại bước sinh số thứ i, thực hiện các phép tính:
    * Tính $m = \text{maj}(x_1, y_3, z_3)$ là "hàm chiếm đa số". Nếu trong 3 bít $x_1, y_3, z_3$ có từ hai bít 0 trở lên thì hàm trả về giá trị 0; Ngược lại, hàm trả về giá trị 1.
    * Kiểm tra:
      * Nếu $x_1 = m$ thì thực hiện **Quay X**;
      * Nếu $y_3 = m$ thì thực hiện **Quay Y**;
      * Nếu $z_3 = m$ thì thực hiện **Quay Z**;
    * Tính $s_i = x_5 \oplus y_7 \oplus z_8$
    * Bản mã $C = P \textbf{ XOR } S$

---

### 0.4. Chi tiết quy tắc quay các thanh ghi 
* **Quay X gồm các thao tác:**
  * $t = x_2 \oplus x_4 \oplus x_5$
  * $x_j = x_{j-1}$ với $j = 5, 4, 3, 2, 1$
  * $x_0 = t$
  * *Ví dụ:* `1 0 0 1 0 1` $\to t = 0 \oplus 0 \oplus 1 = 1 \to$ `1 1 0 0 1 0`

* **Quay Y gồm các thao tác:**
  * $t = y_6 \oplus y_7$
  * $y_j = y_{j-1}$ với $j = 7, 6, \dots, 1$
  * $y_0 = t$
  * *Ví dụ:* `0 1 0 0 1 1 1 0` $\to t = 0 \oplus 1 = 1 \to$ `1 0 1 0 0 1 1 1`

* **Quay Z gồm các thao tác:**
  * $t = z_2 \oplus z_7 \oplus z_8$
  * $z_j = z_{j-1}$ với $j = 8, 7, \dots, 1$
  * $z_0 = t$
  * *Ví dụ:* `1 0 0 1 1 0 0 0 0` $\to t = 0 \oplus 0 \oplus 0 = 0 \to$ `0 1 0 0 1 1 0 0 0`

---

### 0.5. Ví dụ tính tay từng bước 
**Bài tập: Cho bản rõ P = 111 (chữ H), khoá K = 10010101001110100110000**
* Phân bổ ban đầu:
  * X: `100101`
  * Y: `01001110`
  * Z: `100110000`

* **Bước 0 :**
  * $x_1 = 0, y_3 = 0, z_3 = 1 \to m = \text{maj}(0,0,1) = 0 \to$ quay X, quay Y
  * $X: 100101 \longrightarrow 110010$
  * $Y: 01001110 \longrightarrow 10100111$
  * $Z: 100110000$ (giữ nguyên)
  * $s_0 = 0 \oplus 1 \oplus 0 = 1$ *
* **Bước 1 :**
  * $x_1 = 1, y_3 = 0, z_3 = 1 \to m = \text{maj}(1,0,1) = 1 \to$ quay X, quay Z
  * $X: 110010 \longrightarrow 111001$
  * $Y: 10100111$ (giữ nguyên)
  * $Z: 100110000 \longrightarrow 010011000$
  * $s_1 = 1 \oplus 1 \oplus 0 = 0$

* **Bước 2 :**
  * $x_1 = 1, y_3 = 0, z_3 = 0 \to m = \text{maj}(1,0,0) = 0 \to$ quay Y, quay Z
  * $X: 111001$ (giữ nguyên)
  * $Y: 10100111 \longrightarrow 01010011$
  * $Z: 010011000 \longrightarrow 101001100$ 
  * $s_2 = 1 \oplus 1 \oplus 0 = 0$ 

* **Kết luận :**
  * Bản mã: $C = 111 \oplus 100 = 011$ (chữ D)
  * Giải mã: $P = C \oplus S = 011 \oplus 100 = 111$

---

### 0.6. Hệ mã A5/1 Tổng quát 
* **Đặc điểm:** Nguyên tắc bộ số A5/1 hoạt động giống TinyA5/1 nhưng kích thước thanh ghi X, Y, Z là 19, 22 và 23 bít.
* Hàm maj được tính trên 3 bít: $m = \text{maj}(x_8, y_{10}, z_{10})$
* Quay X, Y, Z với các bít như sau:
  * **Quay X:**
    * $t = x_{13} \oplus x_{16} \oplus x_{17} \oplus x_{18}$
    * $x_j = x_{j-1}$ với $j = 18, 17, \dots, 1$
    * $x_0 = t$
  * **Quay Y:**
    * $t = y_{20} \oplus y_{21}$
    * $y_j = y_{j-1}$ với $j = 21, 20, \dots, 1$
    * $y_0 = t$
  * **Quay Z:**
    * $t = z_7 \oplus z_{20} \oplus z_{21} \oplus z_{22}$
    * $z_j = z_{j-1}$ với $j = 22, 21, \dots, 1$
    * $z_0 = t$
* **Sau khi quay bít xong thì bít sinh ra:** $s_i = x_8 \oplus y_{10} \oplus z_{10}$ 
* A5/1 được thực hiện dễ dàng bằng các thiết bị phần hardware, tốc độ nhanh.
---

## 1. Input (Đầu vào)
Hệ mã TinyA5/1 sử dụng hai dữ liệu đầu vào chính:
- **Plaintext (Bản rõ - P):** Chuỗi bit nhị phân cần mã hóa (Ví dụ bài học: `P = 111` biểu diễn ký tự 'H' dạng 3-bit).
- **Key (Khóa bí mật - K):** Chuỗi nhị phân có chiều dài đúng 23 bit ($K \in \{0, 1\}^{23}$).

---

## 2. Registers (Cấu trúc thanh ghi)

Bảng đối chiếu thông số 3 thanh ghi từ Slide bài giảng:

| Thành phần | X | Y | Z | Nguồn (trang) |
| :--- | :---: | :---: | :---: | :---: |
| **Độ dài (bit)** | 6 | 8 | 9 | Trang 46 |
| **Chỉ số ký hiệu slide** | $x_0, x_1, x_2, x_3, x_4, x_5$ | $y_0, y_1, y_2, y_3, y_4, y_5, y_6, y_7$ | $z_0, z_1, z_2, z_3, z_4, z_5, z_6, z_7, z_8$ | Trang 46 |
| **Vị trí clocking bit** | $x_1$ | $y_3$ | $z_3$ | Trang 47 |
| **Feedback (bit nào XOR bit nào)** | $t = x_2 \oplus x_4 \oplus x_5$ | $t = y_6 \oplus y_7$ | $t = z_2 \oplus z_7 \oplus z_8$ | Trang 48 |
| **Hướng dịch** | Dịch phải ($x_j \leftarrow x_{j-1}$) | Dịch phải ($y_j \leftarrow y_{j-1}$) | Dịch phải ($z_j \leftarrow z_{j-1}$) | Trang 48 |
| **Bit mới vào vị trí** | $x_0$ | $y_0$ | $z_0$ | Trang 48 |
| **Bit output** | $x_5$ | $y_7$ | $z_8$ | Trang 47, 49 |

---

## 3. Key Distribution (Phân bổ khóa)

### 3.1. Quy tắc chia khóa
Khóa bí mật $K$ gồm 23 bit được chia theo tỉ lệ $6 + 8 + 9 = 23$ bit và nạp tuần tự từ trái sang phải:
- **6 bit đầu:** Nạp vào thanh ghi **X** ($x_0 \dots x_5$).
- **8 bit tiếp:** Nạp vào thanh ghi **Y** ($y_0 \dots y_7$).
- **9 bit cuối:** Nạp vào thanh ghi **Z** ($z_0 \dots z_8$).

### 3.2. Ví dụ nạp khóa và kiểm tra tính toàn vẹn
Khóa ví dụ từ Slide trang 49:
$$K = 10010101001110100110000$$

- **Cắt đoạn theo số lượng bit:**
  - $X$ (6 bit đầu): `100101` $\implies x_0=1, x_1=0, x_2=0, x_3=1, x_4=0, x_5=1$.
  - $Y$ (8 bit tiếp): `01001110` $\implies y_0=0, y_1=1, y_2=0, y_3=0, y_4=1, y_5=1, y_6=1, y_7=0$.
  - $Z$ (9 bit cuối): `100110000` $\implies z_0=1, z_1=0, z_2=0, z_3=1, z_4=1, z_5=0, z_6=0, z_7=0, z_8=0$.

- **Kiểm tra nối lại (Concatenation Check):**
  $$\text{Độ dài} = 6 + 8 + 9 = 23 \text{ bit}$$
  $$X \parallel Y \parallel Z = \text{"100101"} + \text{"01001110"} + \text{"100110000"} = \text{"10010101001110100110000"} \equiv K$$

---

## Bảng ánh xạ ký hiệu (Nháp)

Bảng đối chiếu giữa ký hiệu trên Slide và định danh biến dự kiến trong mã nguồn (giữ nguyên quy ước chỉ số ban đầu, không tự ý sửa đổi):

| Thành phần thuật toán | Slide ghi | Ký hiệu code dự kiến | Ghi chú / Kiểu dữ liệu |
| :--- | :---: | :---: | :--- |
| Khóa đầu vào (23 bit) | $K$ | `key` | `str` nhị phân ("0"/"1") |
| Bản rõ | $P$ | `plaintext` | `str` hoặc `List[int]` |
| Bản mã | $C$ | `ciphertext` | `str` hoặc `List[int]` |
| Dòng khóa | $S$ | `keystream` | `str` hoặc `List[int]` |
| Bit dòng khóa tại bước $i$ | $s_i$ | `s_i` / `keystream_bit` | `int` (0 hoặc 1) |
| Thanh ghi X | $X = (x_0, \dots, x_5)$ | `register_x` | `List[int]` (độ dài 6) |
| Thanh ghi Y | $Y = (y_0, \dots, y_7)$ | `register_y` | `List[int]` (độ dài 8) |
| Thanh ghi Z | $Z = (z_0, \dots, z_8)$ | `register_z` | `List[int]` (độ dài 9) |
| Clocking bit của X | $x_1$ | `register_x[1]` | `int` |
| Clocking bit của Y | $y_3$ | `register_y[3]` | `int` |
| Clocking bit của Z | $z_3$ | `register_z[3]` | `int` |
| Bit phản hồi mới (Feedback) | $t$ | `t` / `feedback_bit` | `int` |
| Output bit của X | $x_5$ | `register_x[5]` | `int` |
| Output bit của Y | $y_7$ | `register_y[7]` | `int` |
| Output bit của Z | $z_8$ | `register_z[8]` | `int` |
---
## 4. Majority function (Hàm chiếm đa số)

### 4.1. Định nghĩa và Quy tắc
- **Định nghĩa:** Hàm chiếm đa số $m = \text{maj}(a, b, c)$ nhận 3 bit đầu vào. Nếu có từ 2 bit `0` trở lên thì trả về `0`; ngược lại nếu có từ 2 bit `1` trở lên thì trả về `1`
- **Vị trí 3 bit clocking:**
  - Thanh ghi X: $x_1$
  - Thanh ghi Y: $y_3$ 
  - Thanh ghi Z: $z_3$
  $$\implies m = \text{maj}(x_1, y_3, z_3)$$
- **Quy tắc quay:**
  - Nếu clocking bit bằng $m$ thì thanh ghi đó **quay (dịch)** 
  - Nếu clocking bit khác $m$ thì thanh ghi đó **đứng yên (giữ nguyên)** 
  - Cụ thể:
    - Nếu $x_1 = m \implies$ Quay X.
    - Nếu $y_3 = m \implies$ Quay Y.
    - Nếu $z_3 = m \implies$ Quay Z.

### 4.2. Ví dụ bước đầu tiên từ Slide
- **Trạng thái ban đầu:**
  - $X = 1\mathbf{0}0101$
  - $Y = 010\mathbf{0}1110$
  - $Z = 100\mathbf{1}10000$
- **Đọc ba bit clocking:** $x_1 = 0$, $y_3 = 0$, $z_3 = 1$.
- **Tính majority:** $m = \text{maj}(0, 0, 1) = 0$ (vì có hai bit 0).
- **Xác định thanh ghi dịch:**
  - $x_1 = 0 = m \implies$ **X quay** (dịch).
  - $y_3 = 0 = m \implies$ **Y quay** (dịch).
  - $z_3 = 1 \ne m \implies$ **Z đứng yên** (không dịch).

---

## 5. Rotation (Cơ chế quay thanh ghi)

### 5.1. Quy tắc dịch bit
- **Hướng dịch:** Dịch từ trái sang phải, từ chỉ số thấp sang chỉ số cao ($x_j = x_{j-1}$)
- **Vị trí bit mới:** Bit phản hồi mới $t$ luôn nạp vào vị trí đầu tiên $x_0 = t, y_0 = t, z_0 = t$ 
- **Bit bị đẩy ra:** Bit ở vị trí cuối cùng ($x_5, y_7, z_8$) bị đẩy ra khỏi thanh ghi sau khi dịch 

---

### 5.2. Minh họa ví dụ dịch cụ thể từng thanh ghi từ Slide 

#### 1. Ví dụ thanh ghi X 
- **Register:** X (6 bit)
- **Before:** `1 0 0 1 0 1` ($x_0=1, x_1=0, x_2=0, x_3=1, x_4=0, x_5=1$)
- **Feedback:** $t = x_2 \oplus x_4 \oplus x_5 = 0 \oplus 0 \oplus 1 = \mathbf{1}$
- **Shift:** Dịch phải 1 vị trí: $x_j = x_{j-1}$ ($j = 5, 4, 3, 2, 1$). Bit cuối $x_5=1$ bị đẩy ra ngoài.
- **New bit:** $x_0 = t = \mathbf{1}$
- **After:** `1 1 0 0 1 0`
- **Đối chiếu Slide:** Slide ghi `1 1 0 0 1 0` $\implies$ **MATCH** (Khớp hoàn toàn).

#### 2. Ví dụ thanh ghi Y 
- **Register:** Y (8 bit)
- **Before:** `0 1 0 0 1 1 1 0` ($y_0=0, y_1=1, y_2=0, y_3=0, y_4=1, y_5=1, y_6=1, y_7=0$)
- **Feedback:** $t = y_6 \oplus y_7 = 1 \oplus 0 = \mathbf{1}$  
- **Shift:** Dịch phải 1 vị trí: $y_j = y_{j-1}$ ($j = 7, 6, \dots, 1$). Bit cuối $y_7=0$ bị đẩy ra ngoài.
- **New bit:** $y_0 = t = \mathbf{1}$
- **After:** `1 0 1 0 0 1 1 1`
- **Đối chiếu Slide:** Slide ghi `1 0 1 0 0 1 1 1` $\implies$ **MATCH** (Khớp hoàn toàn).

#### 3. Ví dụ thanh ghi Z 
- **Register:** Z (9 bit)
- **Before:** `1 0 0 1 1 0 0 0 0` ($z_0=1, z_1=0, z_2=0, z_3=1, z_4=1, z_5=0, z_6=0, z_7=0, z_8=0$)
- **Feedback:** $t = z_2 \oplus z_7 \oplus z_8 = 0 \oplus 0 \oplus 0 = \mathbf{0}$
- **Shift:** Dịch phải 1 vị trí: $z_j = z_{j-1}$ ($j = 8, 7, \dots, 1$). Bit cuối $z_8=0$ bị đẩy ra ngoài.
- **New bit:** $z_0 = t = \mathbf{0}$
- **After:** `0 1 0 0 1 1 0 0 0`
- **Đối chiếu Slide:** Slide ghi `0 1 0 0 1 1 0 0 0` $\implies$ **MATCH** (Khớp hoàn toàn).

---

### 5.3. Hồ sơ ghi nhận xung đột kỹ thuật (CONFLICT)

Khi đối chiếu bước quay của thanh ghi Z ở , phát hiện sai lệch:

## 6. Keystream Generation & Feedback

### 6.1. Công thức phản hồi (Feedback) cho từng thanh ghi
Công thức tính bit phản hồi $t$ được trích xuất trực tiếp từ Slide bài giảng Chương 2 :
- **Thanh ghi X:** 
  - Công thức: $t = x_2 \oplus x_4 \oplus x_5$ 
  - Giải thích: Bit mới nạp vào đầu thanh ghi X ($x_0$) bằng tổng XOR của 3 bit tại các vị trí tap index 2, 4 và 5.
- **Thanh ghi Y:** 
  - Công thức: $t = y_6 \oplus y_7$
  - Giải thích: Bit mới nạp vào đầu thanh ghi Y ($y_0$) bằng tổng XOR của 2 bit ở cuối thanh ghi tại các vị trí tap index 6 và 7.
- **Thanh ghi Z:** 
  - Công thức: $t = z_2 \oplus z_7 \oplus z_8$
  - Giải thích: Bit mới nạp vào đầu thanh ghi Z ($z_0$) bằng tổng XOR của 3 bit tại các vị trí tap index 2, 7 và 8.

---

### 6.2. Ví dụ tính bit feedback cụ thể từ Slide cho từng thanh ghi

- **Thanh ghi X (Trạng thái ban đầu: `1 0 0 1 0 1`):**
  - Đọc các bit tap: $x_2 = 0$, $x_4 = 0$, $x_5 = 1$.
  - Tính toán: $\text{bit } x_2 \oplus \text{bit } x_4 \oplus \text{bit } x_5 = 0 \oplus 0 \oplus 1 = (0 \oplus 0) \oplus 1 = 0 \oplus 1 = \mathbf{1}$.
  - Kết quả: `feedback_X` = 1.

- **Thanh ghi Y (Trạng thái ban đầu: `0 1 0 0 1 1 1 0`):**
  - Đọc các bit tap: $y_6 = 1$, $y_7 = 0$.
  - Tính toán: $\text{bit } y_6 \oplus \text{bit } y_7 = 1 \oplus 0 = \mathbf{1}$.  
  - Kết quả: `feedback_Y` = 1.

- **Thanh ghi Z (Trạng thái ban đầu: `1 0 0 1 1 0 0 0 0`):**
  - Đọc các bit tap: $z_2 = 0$, $z_7 = 0$, $z_8 = 0$.
  - Tính toán: $\text{bit } z_2 \oplus \text{bit } z_7 \oplus \text{bit } z_8 = 0 \oplus 0 \oplus 0 = (0 \oplus 0) \oplus 0 = 0 \oplus 0 = \mathbf{0}$.
  - Kết quả: `feedback_Z` = 0.

---

### 6.3. Thứ tự các thao tác trong một bước sinh số (Keystream Generation)
Tại mỗi bước sinh số thứ $i$ ($i = 0, 1, 2, \dots$), quy trình thực hiện tuần tự đúng theo thứ tự Slide bài giảng quy định :

1. **Đọc clocking bit:** Đọc 3 bit điều khiển nhịp từ các thanh ghi: $x_1, y_3, z_3$ .
2. **Tính majority:** Tính hàm đa số $m = \text{maj}(x_1, y_3, z_3)$ (nếu có từ hai bit 0 trở lên thì $m = 0$, ngược lại $m = 1$) .
3. **Chọn register dịch:** So sánh độc lập từng thanh ghi: thanh ghi nào có clocking bit bằng $m$ thì được chọn để quay; thanh ghi có bit khác $m$ thì đứng yên (giữ nguyên trạng thái) .
4. **Tính feedback:** Đối với mỗi thanh ghi được chọn quay, tính bit phản hồi $t$ ($t_x, t_y, t_z$) theo các công thức tương ứng tại mục 6.1 .
5. **Dịch (Shift):** 
   - Dịch chuyển các bit của thanh ghi sang phải một vị trí ($j \leftarrow j-1$) .
   - Nạp bit mới $t$ vào ô đầu tiên ($x_0 = t, y_0 = t, z_0 = t$) .
   - Bit cuối cùng ở vị trí cũ ($x_5, y_7, z_8$) bị đẩy ra khỏi thanh ghi.
6. **Lấy output:** Trích xuất bit ở vị trí cuối cùng của cả 3 thanh ghi: $x_5$ (từ X), $y_7$ (từ Y), $z_8$ (từ Z).  
   - **THỜI ĐIỂM LẤY OUTPUT:** Bit output được lấy **SAU KHI THANH GHI ĐÃ QUAY (DỊCH XONG)** .  

7. **XOR ba output tạo bit keystream:** Tạo bit dòng khóa cho bước hiện tại bằng phép XOR 3 bit output vừa lấy :
   $$s_i = x_5 \oplus y_7 \oplus z_8$$

## 7. Encryption (Mã hóa)

### 7.1. Nguyên tắc mã hóa
Bản mã $C$ được tạo ra bằng cách thực hiện phép XOR từng bit (bitwise XOR) giữa bản rõ $P$ và dòng khóa $S$ (Keystream) :
$$C = P \oplus S$$

### 7.2. Ví dụ cụ thể từ Slide

- **Bản rõ (Plaintext):** $P = 111$ (đại diện cho chữ cái "H" trong bảng mã hóa 3-bit).
- **Dòng khóa sinh ra (Keystream):** $S = 100$ (tổng hợp từ $s_0=1, s_1=0, s_2=0$).
- **Phép toán mã hóa:**
  - $P = 111$
  - $S = 100$
  - $C = P \oplus S = 111 \oplus 100 = 011$
- **Kết quả:** $C = 011$ (tương ứng chữ cái "D" trong bảng mã hóa 3-bit) 

---

## 8. Decryption (Giải mã)

### 8.1. Nguyên tắc giải mã
Do tính chất đối xứng của phép toán XOR ($A \oplus B \oplus B = A$), bản rõ ban đầu $P$ được khôi phục bằng cách XOR từng bit giữa bản mã $C$ và chính dòng khóa $S$ đã dùng để mã hóa:
$$P = C \oplus S$$

### 8.2. Ví dụ cụ thể từ Slide

- **Bản mã nhận được (Ciphertext):** $C = 011$ (chữ cái "D").
- **Dòng khóa tái tạo (Keystream):** $S = 100$.
- **Phép toán giải mã:**
  - $C = 011$
  - $S = 100$
  - $P = C \oplus S = 011 \oplus 100 = 111$
- **Kết quả:** $P = 111$ (khôi phục chính xác chữ cái "H" ban đầu) 

---

## 9. Source (Danh sách nguồn trích dẫn)

Mọi thông số kỹ thuật, ký hiệu và ví dụ tính toán của đặc tả TinyA5/1 được trích dẫn trực tiếp từ Slide bài giảng môn học An toàn và Bảo mật thông tin (Chương 2):

| STT | Trang Slide | Nội dung trích dẫn kỹ thuật |
| :---: | :---: | :--- |
| 1 | **Trang 45** | Bối cảnh ứng dụng GSM, đơn vị mã hóa 1 bit, giới thiệu mô hình thu nhỏ TinyA5/1. |
| 2 | **Trang 46** | Số lượng thanh ghi (3), độ dài bit ($X=6, Y=8, Z=9$), ký hiệu chỉ số ($x_0..x_5, y_0..y_7, z_0..z_8$), độ dài khóa $K$ (23 bit) và quy tắc phân bổ $K \longrightarrow XYZ$. |
| 3 | **Trang 47** | Đầu vào $P, K$, đầu ra $C$; định nghĩa hàm đa số $\text{maj}(x_1, y_3, z_3)$; quy tắc quay thanh ghi độc lập; công thức bit đầu ra $s_i = x_5 \oplus y_7 \oplus z_8$ và bản mã $C = P \oplus S$. |
| 4 | **Trang 48** | Chi tiết phép quay: công thức feedback của X, Y, Z; hướng dịch sang phải ($j \leftarrow j-1$); vị trí nhận bit mới $x_0, y_0, z_0$; ví dụ dịch bit cụ thể cho từng thanh ghi. |
| 5 | **Trang 49** | Ví dụ tính tay thực tế: $P = 111, K = 10010101001110100110000$; chi tiết tính toán trạng thái và bit sinh ra tại Bước 0 ($s_0=1$) và Bước 1 ($s_1=0$). |
| 6 | **Trang 50** | Chi tiết tính toán tại Bước 2 ($s_2=0$); kết luận bản mã $C = 011$ và công thức giải mã $P = C \oplus S = 111$. |
| 7 | **Trang 51** | Tổng quát hóa lên hệ mã A5/1 đầy đủ (19, 22, 23 bit) dùng làm cơ sở đối chiếu. |

---

## 10. Open issues (Các vấn đề kỹ thuật và xung đột)

Các vấn đề sai lệch, xung đột phát hiện trong quá trình bóc tách slide và đối chiếu kỹ thuật:

| Mã vấn đề | Trạng thái | Vị trí phát hiện | Nội dung chi tiết | Hướng xử lý của nhóm |
| :---: | :---: | :---: | :--- | :--- |
| **TD-002** | `CONFLICT` | Slide trang 50 (Bước 2 của Z) | Trạng thái thanh ghi Z trước khi quay là `010011000` ($z_2=0, z_7=0, z_8=0$). Phép tính feedback đúng quy tắc là $t = 0 \oplus 0 \oplus 0 = 0$, sau khi dịch thì $Z$ phải là `001001100`. Tuy nhiên Slide ghi nhầm thành `101001100` (nhầm $z_0=1$). | Giữ nguyên ghi nhận trên slide trong bảng khảo sát; khi cài đặt mã nguồn thì tính đúng quy tắc toán ($Z = 001001100$). Giá trị bit keystream $s_2$ không bị ảnh hưởng do $z_8=0$. |
| **TD-003** | `RESOLVED` | Toàn bộ Slide và Code | Xác định quy ước chỉ số bit bắt đầu từ 0 hay 1. Slide gốc dùng $x_0 \dots x_5, y_0 \dots y_7, z_0 \dots z_8$. | Thống nhất toàn nhóm áp dụng quy ước chỉ số 0-based indexing (khớp 100% với danh sách mảng trong Python). |

---
