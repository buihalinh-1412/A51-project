# Mục 4.3. Tấn công dùng lại dòng khóa (Two-Time Pad)

*(Nháp, người viết: Hoàng Yến Nhi. Mã nguồn: `src/attack_two_time_pad.py`, dữ liệu mẫu: `examples/p1.txt`, `examples/p2.txt`.)*

## 4.3.1. Ý tưởng và chứng minh

Hệ mã dòng mã hóa bằng cách XOR bản rõ với dòng khóa S. Nếu trạm dùng lại cùng một dòng khóa S cho hai tin nhắn P1 và P2 thì kẻ nghe lén thu được hai bản mã:

- C1 = P1 ⊕ S
- C2 = P2 ⊕ S

Lấy XOR hai bản mã:

- C1 ⊕ C2 = (P1 ⊕ S) ⊕ (P2 ⊕ S)
- = P1 ⊕ P2 ⊕ (S ⊕ S)  (XOR có tính giao hoán và kết hợp)
- = P1 ⊕ P2  (vì S ⊕ S = 0)

Vậy dòng khóa bị triệt tiêu. Kẻ tấn công không cần biết khóa mà vẫn có P1 ⊕ P2. Chỉ cần đoán một đoạn chữ (crib) có trong P1, XOR đoạn đó vào đúng vị trí của P1 ⊕ P2 là lộ ra đoạn chữ tương ứng của P2. Nếu biết trọn P1 thì có S = C1 ⊕ P1, từ đó P2 = C2 ⊕ S.

## 4.3.2. Kịch bản

Trong A5/1, dòng khóa của mỗi khung chỉ phụ thuộc vào khóa phiên K (64 bit) và số khung (22 bit). Giả sử trạm mã hóa hai tin nhắn khác nhau nhưng dùng cùng khóa và cùng số khung. Kẻ nghe lén ghi lại hai bản mã C1, C2 trên đường truyền, đoán rằng tin nhắn đầu chứa từ "meeting" rồi dò từ này dọc theo C1 ⊕ C2.

Dữ liệu thử (khóa `1223456789ABCDEF`, hai tin cùng số khung 7):

- P1 = `The meeting will start at nine in the morning tomorrow.`
- P2 = `Please send the final report to the manager on Friday.`

## 4.3.3. Kết quả chạy thử

Hàm `simulate_scenario(p1, p2, "1223456789ABCDEF", 7, 7)` cho `reused = True` và `c1_xor_c2 == p1_xor_p2` là `True`. Một phần C1 ⊕ C2 (hex): `040400411e0045070c0003000301094c...`.

Hàm `recover_with_known_plaintext(c1, p1, c2)` khôi phục đúng P2 = `Please send the final report to the manager on Friday.`

Hàm `crib_drag` với crib `meeting` cho kết quả đứng đầu:

| Vị trí | Đoạn chữ lộ ra | Điểm |
|---|---|---|
| 4 | `se send` | 1.0 |

Đoạn `se send` đúng là ký tự thứ 4 đến 10 của P2 (`Plea|se send|...`), vì từ `meeting` nằm ở vị trí 4 trong P1. Các dòng sau (`m bximg`, `jiewimf`) cũng có điểm 1.0 nhưng là chuỗi vô nghĩa; người tấn công nhìn là loại được. Điều này cho thấy điểm "đọc được" chỉ là gợi ý, cần mắt người chọn kết quả có nghĩa.

*(Chèn ảnh chụp màn hình Terminal chạy tự kiểm tra D2 vào đây: `Nhi_selfcheck_D2.png`.)*

## 4.3.4. Cách phòng chống

Mỗi lần mã hóa phải dùng số khung khác nhau (hoặc khóa khác). Chạy lại với khung khác nhau (`frame1 = 7`, `frame2 = 8`):

- `reused = False`, `c1_xor_c2 == p1_xor_p2` là `False`.
- `crib_drag` với crib `meeting` cho điểm thấp (cao nhất chỉ khoảng 0.57, tại vị trí 25) và đoạn chữ là ký tự rác, không đọc được.

Vì hai dòng khóa khác nhau, S1 và S2 không còn triệt tiêu nhau, C1 ⊕ C2 = P1 ⊕ P2 ⊕ S1 ⊕ S2 trông như dữ liệu ngẫu nhiên.

Lưu ý: số khung chỉ có 22 bit (2^22 giá trị) nên với cùng một khóa phiên, số khung sẽ lặp lại sau 2^22 khung. Vì vậy khóa phiên cần được đổi trước khi số khung quay vòng.
