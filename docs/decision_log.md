# Nhật ký Quyết định Kỹ thuật (Decision Log)

Tài liệu này ghi nhận các quyết định kỹ thuật quan trọng của đồ án A5/1. Các mục **Decision** và **Reason** sẽ do Trưởng nhóm (Hà Linh) chính thức chốt ở D6 [4, 5].

---

### 1. Quyết định TD-001

- **ID**: TD-001
- **Date**: 05/10/2026
- **Issue**: Bit output của A5/1 đầy đủ lấy ở vị trí nào của mỗi register (slide và nguồn ngoài có thể khác nhau) [5].
- **Options**: 
  - Phương án A: Lấy tại bit x8, y10, z10 theo Slide trang 51 [7].
  - Phương án B: Lấy tại bit MSB cuối cùng (x18, y21, z22) theo tài liệu kỹ thuật GSM chuẩn [7].
- **Evidence**: Slide trang 51 ghi x8 ⊕ y10 ⊕ z10 (trùng vị trí clocking) [7]; các nguồn ngoài (arXiv, Wikipedia, GSM spec) ghi XOR 3 bit MSB [7].
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh [5]
- **Status**: OPEN [8]

---

### 2. Quyết định TD-002

- **ID**: TD-002
- **Date**: 05/10/2026
- **Issue**: Trạng thái Z sau bước 2 trong ví dụ tính tay: slide ghi một giá trị, tính theo quy tắc ra giá trị khác [5].
- **Options**:
  - Phương án A: Giữ nguyên giá trị ghi trên Slide (101001100) [9].
  - Phương án B: Tính lại chuẩn theo quy tắc dịch bit feedback (001001100) [9].
- **Evidence**: Slide trang 50 ghi `101001100` [9]; tính lại theo công thức t = z2 ⊕ z7 ⊕ z8 = 0 ⊕ 0 ⊕ 0 = 0 cho ra `001001100` [9].
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh [5]
- **Status**: OPEN [8]

---

### 3. Quyết định TD-003

- **ID**: TD-003
- **Date**: 05/10/2026
- **Issue**: Quy ước chỉ số bit (x0 hay x1 là bit đầu) và thứ tự bit khi nạp key/frame [5].
- **Options**:
  - Phương án A: Chỉ số bit bắt đầu từ 0 (x0 đến x5 cho TinyA5/1) [5].
  - Phương án B: Chỉ số bit bắt đầu từ 1 (x1 đến x6) [5].
- **Evidence**: Slide dùng x1..x6 trên sơ đồ khối [10]; convention code Python thống nhất mảng từ index 0 [11, 12].
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh [5]
- **Status**: OPEN [8]

---

### 4. Quyết định TD-004

- **ID**: TD-004
- **Date**: 05/10/2026
- **Issue**: Key/frame/warm-up: số chu kỳ, register nào được clock trong từng giai đoạn, output có bị bỏ không [5].
- **Options**:
  - Phương án A: Nạp khóa thẳng không qua warm-up (theo Slide TinyA5/1) [7, 13].
  - Phương án B: Chạy đủ 64 chu kỳ nạp key, 22 chu kỳ nạp frame và 100 chu kỳ warm-up (theo GSM chuẩn) [7, 14].
- **Evidence**: Slide không đề cập giai đoạn warm-up cho A5/1 [7]; nguồn ngoài quy định rõ 100 chu kỳ trộn ban đầu [7, 14].
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh [5]
- **Status**: OPEN [8]

---

### 5. Quyết định TD-005

- **ID**: TD-005
- **Date**: 05/10/2026
- **Issue**: Dữ liệu dài hơn một đoạn keystream (file lớn): xử lý thế nào [5].
- **Options**:
  - Phương án A: Tăng bộ đếm khung (frame counter) cho mỗi khối 228 bit keystream [15, 16].
  - Phương án B: Quay liên tục bộ sinh khóa qua 228 bit mà không reset frame [15, 16].
- **Evidence**: Mỗi khung GSM chuẩn tạo 228 bit keystream [15, 17]; mã hóa file dữ liệu nhị phân cần cơ chế tạo dòng khóa dài tương ứng [15].
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh [5]
- **Status**: OPEN [8]
