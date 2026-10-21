# Mục 4.2. Demo trên dữ liệu thực tế

*(Nháp, người viết: Trần Đại Lộc. Mã nguồn giao diện: `gui/tab_file.py`, `gui/tab_attack.py`. Ảnh chụp: thư mục `docs/evidence/`.)*

Phần này chạy chương trình trên dữ liệu thật: mã hóa và giải mã một file văn bản và một ảnh PNG bằng A5/1, sau đó mô phỏng tấn công khi dùng lại số khung. Mọi lần chạy dùng khóa `1223456789ABCDEF`. Giao diện chạy bằng lệnh `python -m gui.tab_file` và `python -m gui.tab_attack` từ thư mục gốc của dự án.

## 4.2.1. Mã hóa và giải mã file văn bản

**Hình 4.2.1 (ảnh 1: `Loc_report_1_before.png`).** Mở tab "Mã hóa File", chọn file `loc_test.txt`, nhập khóa `1223456789ABCDEF` và số khung bắt đầu `0`. Ô "Xem trước" hiện nội dung file: `Hello A5/1, day la thu nghiem cua Loc`.

**Hình 4.2.2 (ảnh 2: `Loc_report_2_encrypted.png`).** Bấm "Mã hóa". Thanh tiến trình chạy hết và chương trình báo "Đã mã hóa xong" với file `loc_test.txt.enc`. Ô "Xem trước" không hiện nội dung của file mã hóa mà ghi "(file đã mã hóa, không xem trước)". Theo thiết kế ở Mục 3.2, file mã hóa gồm 4 byte đầu là số khung bắt đầu, sau đó là dữ liệu đã mã hóa.

**Hình 4.2.3 (ảnh 3: `Loc_selfcheck_D1.png`).** Chọn `loc_test.txt.enc`, bấm "Giải mã". Chương trình báo "Đã giải mã xong" với file `loc_test.txt.enc.dec` (không cần nhập lại số khung vì đã nằm trong 4 byte đầu của file). Ô "Xem trước" hiện lại `Hello A5/1, day la thu nghiem cua Loc`, giống file gốc.

*Kiểm tra file giải mã so với file gốc:* dùng lệnh `Get-FileHash loc_test.txt, loc_test.txt.enc.dec` (PowerShell). Mã băm SHA256 của cả hai file đều là `7D3EC0DAC2204DDC2BF8677CC8485B0AC26727B23FB36ADEA9AFF23D073C5DB1`, nên file giải mã giống hệt file gốc.

## 4.2.2. Mã hóa và giải mã ảnh PNG

Làm tương tự với ảnh `loc_test.png` (240 x 160 điểm ảnh, khoảng 1 KB). Sau khi mã hóa rồi giải mã (**ảnh `Loc_selfcheck_D2.png`**), ô "Xem trước" hiện lại ảnh nhiều ô màu như ảnh gốc. File giải mã mang đuôi `.enc.dec` nên giao diện nhận ra đó là ảnh PNG bằng phần đầu của file chứ không dựa vào tên file.

## 4.2.3. Tấn công khi dùng lại số khung

Mở tab "Tấn công", bấm "Nạp file mẫu" (P1 = `The meeting will start at nine in the morning tomorrow.`, P2 = `Please send the final report to the manager on Friday.`), nhập khóa `1223456789ABCDEF`, số khung `7`.

**Hình 4.2.4 (ảnh 4: `Loc_selfcheck_D3_reuse.png`).** Tick "Dùng lại số khung" và bấm "Chạy mô phỏng": hai tin dùng cùng số khung 7 nên cùng một dòng khóa. Chương trình hiện C1 ⊕ C2 dạng hex (bắt đầu bằng `040400411e0045070c...`). Với crib `The meeting` (có trong P1), bảng dò crib cho dòng đầu tiên: vị trí `0`, đoạn chữ lộ ra `Please send`, điểm `1.00`. Đây chính là phần đầu của P2, kẻ tấn công đọc được mà không cần biết khóa.

**Hình 4.2.5 (ảnh 5: `Loc_selfcheck_D3_diff.png`).** Bỏ tick "Dùng lại số khung" (số khung của P2 là 8), bấm "Chạy mô phỏng" lại: chương trình báo hai dòng khóa khác nhau. C1 ⊕ C2 lúc này bắt đầu bằng `8e406c25e4911f...`, khác hẳn trường hợp dùng lại số khung. Dò crib `The meeting`: bảng chỉ hiện các chuỗi ký tự vô nghĩa, không có chữ đọc được nào, điểm cao nhất chỉ là `0.45` (các vị trí 21, 23, 13), các dòng còn lại `0.36`. Vì hai dòng khóa khác nhau nên không còn triệt tiêu nhau, C1 ⊕ C2 không còn bằng P1 ⊕ P2.

## 4.2.4. Kết quả dò crib

**Hình 4.2.6 (ảnh 6: `Loc_report_6_crib.png`).** Dùng lại số khung 7, crib ` the ` (có dấu cách hai đầu). Bảng cho:

| Vị trí | Đoạn chữ lộ ra | Điểm | Ghi chú |
|---|---|---|---|
| 11 | ` will` | 1.00 | chữ của P1 (crib ` the ` nằm trong P2 ở vị trí này) |
| 31 | `in th` | 1.00 | chữ của P1 |
| 33 | `he ma` | 1.00 | chữ của P2 (crib ` the ` nằm trong P1 ở vị trí này) |

Các dòng còn lại cũng có điểm 1.00 nhưng là chuỗi vô nghĩa. Cách chấm điểm coi dấu câu là "đọc được" nên điểm chỉ là gợi ý, người tấn công phải tự nhìn để chọn kết quả có nghĩa.

## 4.2.5. Nhận xét

- Chương trình mã hóa và giải mã đúng với file văn bản và ảnh PNG nhỏ.
- Khi hai tin dùng chung số khung, dò crib làm lộ chữ của tin còn lại. Khi đổi số khung thì không lộ.
- Vì vậy mỗi lần mã hóa phải dùng số khung khác nhau (hoặc khóa khác), như đã nêu ở Mục 4.3.
