# Nhật ký Quyết định Kỹ thuật (Decision Log)

Tài liệu này ghi nhận các quyết định kỹ thuật quan trọng của đồ án A5/1. Các mục **Decision** và **Reason** sẽ do Trưởng nhóm (Hà Linh) chính thức chốt ở D6.

---

## 1. Quyết định TD-001

- **ID**: TD-001
- **Date**: 05/10/2026
- **Issue**: Bit output của A5/1 đầy đủ lấy ở vị trí nào của mỗi register (slide và nguồn ngoài có thể khác nhau).
- **Options**: 
  - Phương án A: Lấy tại bit x8, y10, z10 theo slide [Slide, trang 51].
  - Phương án B: Lấy tại bit cao nhất của mỗi register (x18, y21, z22) theo các nguồn dịch ngược công khai (Briceno–Goldberg–Wagner; Shah–Mahalanobis; Wikipedia), xem `references.md` [2][4][6]. Lưu ý: chuẩn GSM (ETSI) không công bố cấu trúc bên trong A5/1.
- **Evidence**: Slide ghi "sᵢ = x8 ⊕ y10 ⊕ z10" [Slide, trang 51], trùng vị trí clocking bit; ba nguồn ngoài ghi R1[18] ⊕ R2[21] ⊕ R3[22] (`references.md` [2][4][6], CONFLICT-001).
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh
- **Status**: OPEN

---

## 2. Quyết định TD-002

- **ID**: TD-002
- **Date**: 05/10/2026
- **Issue**: Trạng thái Z sau bước 2 trong ví dụ tính tay: slide ghi một giá trị, tính theo quy tắc ra giá trị khác.
- **Options**:
  - Phương án A: Giữ nguyên giá trị ghi trên slide (`101001100`) [Slide, trang 50].
  - Phương án B: Tính lại theo quy tắc dịch và feedback (`001001100`).
- **Evidence**: Slide ghi `101001100` [Slide, trang 50]; tính lại với Z trước bước 2 = `010011000`: t = z₂ ⊕ z₇ ⊕ z₈ = 0 ⊕ 0 ⊕ 0 = 0, cho ra `001001100` (xem `register_shift_example.md` mục 4).
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh
- **Status**: OPEN

---

## 3. Quyết định TD-003

- **ID**: TD-003
- **Date**: 05/10/2026
- **Issue**: Quy ước chỉ số bit (x0 hay x1 là bit đầu) và thứ tự bit khi nạp key/frame.
- **Options**:
  - Phương án A: Chỉ số bit bắt đầu từ 0 (x₀ đến x₅ cho TinyA5/1).
  - Phương án B: Chỉ số bit bắt đầu từ 1 (x₁ đến x₆).
- **Evidence**: Slide đánh số từ 0: X gồm x₀…x₅, Y gồm y₀…y₇, Z gồm z₀…z₈ [Slide, trang 46]; list Python cũng bắt đầu từ chỉ số 0 (`coding_convention.md` mục 5–6). Thứ tự bit khi nạp key/frame của A5/1: xem ghi chú TD-003 trong `references.md` của Nhi.
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh
- **Status**: OPEN

---

## 4. Quyết định TD-004

- **ID**: TD-004
- **Date**: 05/10/2026
- **Issue**: Key/frame/warm-up: số chu kỳ, register nào được clock trong từng giai đoạn, output có bị bỏ không.
- **Options**:
  - Phương án A: Nạp khóa thẳng vào register, không có nạp frame và warm-up (theo slide; slide không mô tả các bước này) [Slide, trang 46, 51].
  - Phương án B: Chạy 64 chu kỳ nạp key, 22 chu kỳ nạp frame, rồi 100 chu kỳ warm-up bỏ đầu ra (theo nguồn ngoài, `references.md` [2][4][6]).
- **Evidence**: Slide không đề cập nạp frame và warm-up cho A5/1 [Slide, trang 51]; ba nguồn ngoài thống nhất 64 + 22 + 100 chu kỳ (`references.md`, Ma trận nguồn).
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh
- **Status**: OPEN

---

## 5. Quyết định TD-005

- **ID**: TD-005
- **Date**: 05/10/2026
- **Issue**: Dữ liệu dài hơn một đoạn keystream (file lớn): xử lý thế nào.
- **Options**:
  - Phương án A: Tăng bộ đếm khung (frame counter) cho mỗi khối 228 bit keystream.
  - Phương án B: Cho bộ sinh keystream chạy tiếp quá 228 bit, không đổi frame.
- **Evidence**: Mỗi khung GSM tạo 228 bit keystream (2 × 114 bit) (`references.md` [1][2]); cả hai phương án đều là đề xuất của nhóm, không phải chuẩn GSM.
- **Decision**: 
- **Reason**: 
- **Person responsible**: Hà Linh
- **Status**: OPEN
