# Bảng Thuật ngữ Kỹ thuật (Terminology - Bản hoàn chỉnh)

| Thuật ngữ (Tiếng Anh) | Từ trong Slide | Thuật ngữ kỹ thuật | Định nghĩa ngắn gọn | Vị trí trong Slide Chương 2 |
| :--- | :--- | :--- | :--- | :--- |
| **Register** | Thanh ghi | Thanh ghi (Shift Register) | Bộ nhớ lưu trữ chuỗi bit (ví dụ các thanh ghi X, Y, Z trong TinyA5/1 hoặc R1, R2, R3 trong A5/1). | Trang 46, 51 |
| **Shift / Rotate** | Quay thanh ghi (Quy tắc quay) | Dịch thanh ghi (Shift) | Thao tác dịch các bit sang vị trí tiếp theo (từ chỉ số thấp sang chỉ số cao) và đưa bit mới vào vị trí 0. | Trang 46, 47, 48 |
| **Majority** | Hàm chiếm đa số | Hàm đa số (Majority function) | Hàm kiểm tra 3 bit: nếu có từ hai bit 0 trở lên thì trả về 0, ngược lại trả về 1. | Trang 47 |
| **Clocking bit** | Bít xét điều kiện quay | Bit điều khiển nhịp (Clocking bit) | Các bit tại vị trí cố định (x1, y3, z3) dùng để so khớp với hàm chiếm đa số; bit nào bằng giá trị đa số thì thanh ghi đó quay. | Trang 47, 51 |
| **Feedback bit** | Bít t (Bít đưa vào vị trí 0) | Bit phản hồi (Feedback bit) | Bit mới sinh ra từ phép XOR các vị trí quy định để nạp vào đầu thanh ghi khi quay. | Trang 48, 51 |
| **Keystream** | Dãy số ngẫu nhiên S / Bít sinh ra | Dòng khóa / Chuỗi khóa (Keystream) | Dãy bit ngẫu nhiên sinh ra từ bộ sinh số sau mỗi bước quay để đem XOR với bản rõ. | Trang 42, 47, 51 |
| **Plaintext** | Bản rõ / Văn bản rõ | Bản rõ (Plaintext) | Dữ liệu gốc ban đầu cần được mã hóa để bảo vệ. | Trang 6, 7, 8, 42 |
| **Ciphertext** | Bản mã / Văn bản mã hoá | Bản mã (Ciphertext) | Kết quả sau khi lấy bản rõ XOR với dòng khóa. | Trang 6, 7, 8, 47 |
| **LFSR** | Slide không dùng từ này (Slide gọi chung là 3 thanh ghi X, Y, Z) | Thanh ghi dịch phản hồi tuyến tính (Linear-Feedback Shift Register) | Cơ chế phần cứng dịch bit có tính toán bit phản hồi bằng hàm tuyến tính (phép XOR). | Trang 46 |
| **Frame** | Slide không đề cập | Khung truyền GSM (Frame / Frame number) | Bộ đếm khung 22-bit công khai trong mạng GSM dùng để khởi tạo trạng thái mã hóa cho từng khung đàm thoại. | Slide thiếu bước này |
| **Warm-up** | Slide không đề cập | Giai đoạn khởi động (Warm-up / Mixing) | Quá trình chạy 100 chu kỳ quay thanh ghi theo quy tắc majority và loại bỏ bit đầu ra trước khi sinh keystream thật. | Slide thiếu bước này |
| **Stream Cipher** | Mã hoá dòng / Mã dòng | Mã dòng (Stream Cipher) | Hệ mã hóa thực hiện mã hóa từng bit hoặc từng đơn vị dữ liệu liên tục bằng phép XOR. | Trang 15, 39, 42 |
| **Encryption / Decryption** | Mã hoá / Giải mã | Mã hóa (Encryption) / Giải mã (Decryption) | Quá trình chuyển từ bản rõ sang bản mã và ngược lại. | Trang 7, 8, 47, 50 |
