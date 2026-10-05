
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
  * $s_1 = 1 \oplus 1 \oplus 0 = 0$ *(trên slide ghi nhãn: $s_2 = 1 \oplus 1 \oplus 0 = 0$)*

* **Bước 2 :**
  * $x_1 = 1, y_3 = 0, z_3 = 0 \to m = \text{maj}(1,0,0) = 0 \to$ quay Y, quay Z
  * $X: 111001$ (giữ nguyên)
  * $Y: 10100111 \longrightarrow 01010011$
  * $Z: 010011000 \longrightarrow 101001100$ *(Ghi chú: theo công thức quay Z thì t = 0 và Z sau phải là 001001100, slide ghi nhầm bit đầu là 1)*
  * $s_2 = 1 \oplus 1 \oplus 0 = 0$ *(trên slide ghi nhãn: $s_3 = 1 \oplus 1 \oplus 0 = 0$)*

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
* **Sau khi quay bít xong thì bít sinh ra:** $s_i = x_8 \oplus y_{10} \oplus z_{10}$ *(Lưu ý: Nguồn GSM chuẩn là $x_{18} \oplus y_{21} \oplus z_{22}$)*
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

*(Ghi chú: Bit keystream tổng hợp được tính sau khi quay: $s_i = x_5 \oplus y_7 \oplus z_8$ - Slide trang 47).*

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
  *(Nối lại khớp 100% với khóa $K$ ban đầu).*

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
- **Định nghĩa:** Hàm chiếm đa số $m = \text{maj}(a, b, c)$ nhận 3 bit đầu vào. Nếu có từ 2 bit `0` trở lên thì trả về `0`; ngược lại nếu có từ 2 bit `1` trở lên thì trả về `1` [Slide, trang 47].
- **Vị trí 3 bit clocking (đã xác định ở mục 2):**
  - Thanh ghi X: $x_1$ [Slide, trang 47]
  - Thanh ghi Y: $y_3$ [Slide, trang 47]
  - Thanh ghi Z: $z_3$ [Slide, trang 47]
  $$\implies m = \text{maj}(x_1, y_3, z_3)$$
- **Quy tắc quay:**
  - Nếu clocking bit bằng $m$ thì thanh ghi đó **quay (dịch)** [Slide, trang 47].
  - Nếu clocking bit khác $m$ thì thanh ghi đó **đứng yên (giữ nguyên)** [Slide, trang 47].
  - Cụ thể:
    - Nếu $x_1 = m \implies$ Quay X.
    - Nếu $y_3 = m \implies$ Quay Y.
    - Nếu $z_3 = m \implies$ Quay Z.

### 4.2. Ví dụ bước đầu tiên từ Slide (Bước 0 - Slide trang 49)
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
- **Hướng dịch:** Dịch từ trái sang phải, từ chỉ số thấp sang chỉ số cao ($x_j = x_{j-1}$) [Slide, trang 48].
- **Vị trí bit mới:** Bit phản hồi mới $t$ luôn nạp vào vị trí đầu tiên $x_0 = t, y_0 = t, z_0 = t$ [Slide, trang 48].
- **Bit bị đẩy ra:** Bit ở vị trí cuối cùng ($x_5, y_7, z_8$) bị đẩy ra khỏi thanh ghi sau khi dịch [Slide, trang 48].

---

### 5.2. Minh họa ví dụ dịch cụ thể từng thanh ghi từ Slide (Trang 48, 49, 50)

#### 1. Ví dụ thanh ghi X (Slide trang 48)
- **Register:** X (6 bit)
- **Before:** `1 0 0 1 0 1` ($x_0=1, x_1=0, x_2=0, x_3=1, x_4=0, x_5=1$)
- **Feedback:** $t = x_2 \oplus x_4 \oplus x_5 = 0 \oplus 0 \oplus 1 = \mathbf{1}$
- **Shift:** Dịch phải 1 vị trí: $x_j = x_{j-1}$ ($j = 5, 4, 3, 2, 1$). Bit cuối $x_5=1$ bị đẩy ra ngoài.
- **New bit:** $x_0 = t = \mathbf{1}$
- **After:** `1 1 0 0 1 0`
- **Đối chiếu Slide:** Slide ghi `1 1 0 0 1 0` $\implies$ **MATCH** (Khớp hoàn toàn).

#### 2. Ví dụ thanh ghi Y (Slide trang 48)
- **Register:** Y (8 bit)
- **Before:** `0 1 0 0 1 1 1 0` ($y_0=0, y_1=1, y_2=0, y_3=0, y_4=1, y_5=1, y_6=1, y_7=0$)
- **Feedback:** $t = y_6 \oplus y_7 = 1 \oplus 0 = \mathbf{1}$  
  *(Ghi chú: Slide trang 48 ghi nhầm thứ tự là $t = 0 \oplus 1 = 1$, nhưng kết quả phép XOR vẫn đúng bằng 1).*
- **Shift:** Dịch phải 1 vị trí: $y_j = y_{j-1}$ ($j = 7, 6, \dots, 1$). Bit cuối $y_7=0$ bị đẩy ra ngoài.
- **New bit:** $y_0 = t = \mathbf{1}$
- **After:** `1 0 1 0 0 1 1 1`
- **Đối chiếu Slide:** Slide ghi `1 0 1 0 0 1 1 1` $\implies$ **MATCH** (Khớp hoàn toàn).

#### 3. Ví dụ thanh ghi Z (Slide trang 48 - hoặc Bước 1 trang 49)
- **Register:** Z (9 bit)
- **Before:** `1 0 0 1 1 0 0 0 0` ($z_0=1, z_1=0, z_2=0, z_3=1, z_4=1, z_5=0, z_6=0, z_7=0, z_8=0$)
- **Feedback:** $t = z_2 \oplus z_7 \oplus z_8 = 0 \oplus 0 \oplus 0 = \mathbf{0}$
- **Shift:** Dịch phải 1 vị trí: $z_j = z_{j-1}$ ($j = 8, 7, \dots, 1$). Bit cuối $z_8=0$ bị đẩy ra ngoài.
- **New bit:** $z_0 = t = \mathbf{0}$
- **After:** `0 1 0 0 1 1 0 0 0`
- **Đối chiếu Slide:** Slide ghi `0 1 0 0 1 1 0 0 0` $\implies$ **MATCH** (Khớp hoàn toàn).

---

### 5.3. Hồ sơ ghi nhận xung đột kỹ thuật (CONFLICT)

Khi đối chiếu bước quay của thanh ghi Z ở **Bước 2 (Slide trang 50)**, phát hiện sai lệch:
