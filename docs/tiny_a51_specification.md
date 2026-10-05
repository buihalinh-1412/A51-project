
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
