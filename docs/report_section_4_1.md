# 4.1. Giao diện và hướng dẫn sử dụng

Chương trình có hai cách dùng: giao diện đồ họa (GUI, Tkinter) và dòng lệnh (CLI). Cả hai đều chạy từ thư mục gốc của dự án, cần Python 3.10 trở lên.

## 4.1.1. Giao diện đồ họa

Chạy bằng lệnh `python -m gui.app`. Cửa sổ chính có 4 tab: TinyA5/1, A5/1 Text, Mã hóa File, Tấn công. Tab nào chưa có file thì hiện chữ "Chưa có", ứng dụng vẫn mở bình thường.

**Tab TinyA5/1** (hình `docs/figures/gui_tab_tiny.png`). Dùng để xem từng bước chạy của bản Tiny.

1. Nhập khóa K gồm 23 bit và bản rõ P (các bit 0/1), hoặc bấm "Chạy ví dụ slide" để tự điền K = 10010101001110100110000, P = 111.
2. Bấm "Bước tiếp" để chạy một bước (thêm một dòng vào bảng), hoặc "Chạy hết" để chạy đủ số bit của P.
3. Bảng hiện X, Y, Z sau mỗi bước, giá trị m, các thanh ghi được quay và bit sᵢ. Khi chạy đủ, dưới bảng hiện dòng khóa S và bản mã C. Với ví dụ slide kết quả là S = 100, C = 011.
4. Bấm "Reset" để xóa bảng và làm lại.

Số bước đánh số từ 0, giống bảng tính tay ở mục 2.4. Dòng ghi chú dưới bảng nhắc rằng slide in Z sau bước 2 là 101001100 nhưng tính theo quy tắc quay thì Z đúng là 001001100.

**Tab A5/1 Text** (hình `docs/figures/gui_tab_text.png`). Dùng để mã hóa, giải mã một đoạn văn bản ngắn.

1. Nhập khóa 16 ký tự hex và số khung (số thập phân hoặc dạng 0x...), hoặc bấm "Nạp khóa mẫu" để điền 1223456789ABCDEF và khung 308 (0x134).
2. Gõ văn bản vào ô trên, bấm "Mã hóa" để ra bản mã dạng hex ở ô dưới.
3. Để giải mã, dán hex vào ô dưới và bấm "Giải mã"; văn bản hiện lại ở ô trên. Cần đúng cả khóa lẫn số khung.
4. Nhập sai (khóa không đủ 16 ký tự hex, hex không hợp lệ) thì chương trình báo lỗi bằng một dòng thông báo, không bị dừng.

**Tab Mã hóa File** và **tab Tấn công** do Lộc phụ trách (xem mục 4.2 và 4.3); phần hướng dẫn hai tab này sẽ bổ sung sau khi hai tab được gộp vào khung chính.

## 4.1.2. Giao diện dòng lệnh

Chạy bằng `python demo_cli.py`. Menu chính có các mục:

```
 1. TinyA5/1: mô phỏng từng bước (Trace Log)
 2. A5/1 đầy đủ: mã hóa / giải mã văn bản
 3. Mã hóa / giải mã file (A5/1)
 4. Tấn công Two-Time Pad (dùng lại số khung)
 5. Đo tốc độ A5/1
 0. Thoát
```

- Mục 3: chọn mã hóa hoặc giải mã, nhập đường dẫn file và khóa (Enter để dùng khóa mẫu). Mã hóa tạo file `<tên>.enc`, giải mã tạo file `<tên>.dec`.
- Mục 4: chạy sẵn kịch bản với `examples/p1.txt` và `examples/p2.txt`, in kết quả hai trường hợp (dùng lại số khung và đổi số khung) cùng 3 kết quả dò crib tốt nhất.
- Mục 5: in bảng thời gian mã hóa theo kích thước dữ liệu.

## 4.1.3. Sơ đồ khối

- Mã hóa file: `docs/diagrams/so_do_ma_hoa_file.png`
- Tấn công Two-Time Pad: `docs/diagrams/so_do_tan_cong.png`

*Ghi chú cho nhóm: ảnh menu CLI và ảnh GUI đủ 4 tab cần chụp lại sau khi các nhánh được gộp (ảnh trong `docs/figures/` là bản chạy thử trước khi gộp).*
