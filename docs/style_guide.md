# Quy chuẩn trình bày tài liệu (Style Guide)

## 1. Tiêu đề
- Tiêu đề file sử dụng `#` (cấp H1).
- Tiêu đề mục lớn sử dụng `##` (cấp H2).
- Tiêu đề mục con sử dụng `###` (cấp H3).

## 2. Cách đánh số mục
- Sử dụng số thứ tự cho các mục lớn: `## 1.`, `## 2.`, `## 3.`...

## 3. Quy cách viết tên Thanh ghi (Register)
- Tên thanh ghi cho thuật toán TinyA5/1: Viết hoa `X`, `Y`, `Z`.
- Tên thanh ghi cho thuật toán A5/1 đầy đủ: Viết hoa `R1`, `R2`, `R3`.
- Chỉ số bit: Giữ ký hiệu nguyên gốc của nguồn trong file spec (ví dụ: x1, y3, z3); chỉ chuyển sang ký hiệu mảng lập trình (bắt đầu từ 0) khi có bảng ánh xạ chính thức.
- **Ví dụ ĐÚNG**: `X`, `Y`, `Z`, `R1`, `R2`, `R3`.
- **Ví dụ SAI**: `x`, `y`, `z`, `r1`, `r2`, `r3`, `register 1`, `thanh ghi thứ nhất`.
- Trong câu văn được viết "register X" hoặc "thanh ghi X"; quy định trên chỉ áp dụng cho **tên** của register (luôn là X, Y, Z, R1, R2, R3).

## 4. Quy cách gọi tên Thuật toán
- Chỉ sử dụng hai tên chính thức: `TinyA5/1` và `A5/1`.
- **Ví dụ ĐÚNG**: `TinyA5/1`, `A5/1`.
- **Ví dụ SAI**: `A51`, `a5/1`, `Tiny A5/1`, `tinyA51`, `A5/1 full`.

## 5. Quy cách trích dẫn nguồn
- Mọi thông số kỹ thuật đều phải kèm nguồn trích dẫn trong ngoặc vuông ngay sau thông số.
- Định dạng chuẩn: `[S1, trang 5]`, `[Slide, trang 23]`.

## 6. Quy cách biểu diễn chuỗi Bit
- Đặt chuỗi bit trong dấu nháy ngược (backticks).
- Ví dụ: `100101`, `0`, `1`.

## 7. Nhãn trạng thái dữ liệu
Mỗi thông số kỹ thuật bắt buộc phải đi kèm một trong 4 nhãn trạng thái sau:
- `VERIFIED`: Đã xác minh qua ít nhất 2 nguồn độc lập hoặc 1 nguồn chuẩn khớp slide.
- `SINGLE-SOURCE`: Chỉ có từ 1 nguồn duy nhất (cần kiểm chứng lại bằng cài đặt).
- `CONFLICT`: Mâu thuẫn giữa các nguồn (phải trình bày theo khối mẫu CONFLICT).
- `UNVERIFIED`: Chưa có nguồn xác minh (tuyệt đối không tự đoán giá trị).

## 8. Quy chuẩn về Bảng biểu
- Mọi bảng bắt buộc phải có hàng tiêu đề (header row).
- Tuyệt đối không để ô trống trong bảng. Nếu thông tin thiếu hoặc không có, ghi rõ `"không áp dụng"` hoặc `"chưa có"`.

## 9. Thuật ngữ
- Dùng thuật ngữ theo `terminology.md`.
- Thao tác chuyển bit sang vị trí kế bên viết là **dịch** (shift). Slide gọi là "quay"; chỉ giữ chữ "quay" khi trích nguyên văn slide.
- Không dùng "rotate" / "xoay vòng" cho TinyA5/1 và A5/1.
