"""
demo_cli.py — Công cụ demo dòng lệnh tương tác cho TinyA5/1.

Người phụ trách: Nguyễn Thị Nhật Linh (việc 2.6, Giai đoạn 2).

Chạy từ thư mục gốc của repo:
    python demo_cli.py             # menu tương tác
    python demo_cli.py --example   # chạy ví dụ slide (K, P = 111) rồi thoát

Tệp này chỉ làm phần nhập/xuất. Mọi phép tính nằm trong src/tiny_a51.py
(TinyA51); lõi không in gì ra màn hình, nên toàn bộ lệnh print() nằm ở đây
(docs/coding_convention.md mục 8).

Ví dụ trên lớp [slide Chương 2, trang 49–50]:
    K = 10010101001110100110000, P = 111  ->  S = 100, C = 011
Slide trang 50 in Z sau Bước 2 là 101001100, nhưng tính theo quy tắc quay
là 001001100 (TD-002). Demo sẽ báo rõ chỗ lệch này, không tự sửa.
"""

from __future__ import annotations

import argparse
import sys

try:
    from src.tiny_a51 import KEY_LENGTH, SLIDE_KEY, SLIDE_PLAINTEXT, TinyA51
except ImportError:  # chạy khi đứng trong thư mục src/
    from tiny_a51 import KEY_LENGTH, SLIDE_KEY, SLIDE_PLAINTEXT, TinyA51

SLIDE_KEYSTREAM = "100"      # S theo slide trang 50
SLIDE_CIPHERTEXT = "011"     # C theo slide trang 50

MENU = """
================ DEMO TinyA5/1 ================
 1. Nhập khoá K (23 bit)         [hiện tại: {key}]
 2. Dùng khoá ví dụ trên slide
 3. Xem trạng thái ba thanh ghi X, Y, Z
 4. Chạy từng bước (Enter = bước tiếp theo, q = dừng)
 5. Sinh dãy số S gồm n bit, hiện nhật ký (trace)
 6. Mã hoá bản rõ P            (C = P XOR S)
 7. Giải mã bản mã C           (P = C XOR S)
 8. Chạy ví dụ slide và đối chiếu kết quả
 0. Thoát
===============================================
"""


# ---------------------------------------------------------------------------
# Định dạng đầu ra
# ---------------------------------------------------------------------------

def format_state(state: dict[str, str]) -> str:
    """'X=100101  Y=01001110  Z=100110000'."""
    return "  ".join(f"{name}={bits}" for name, bits in state.items())


def format_step(record: dict) -> str:
    """Biến một bản ghi trace thành đoạn văn bản nhiều dòng."""
    clock = record["clock_bits"]
    rotated = record["rotated_registers"]
    lines = [
        f"--- Bước {record['step']} ---",
        f"  Bit điều khiển quay : x1={clock['x1']}  y3={clock['y3']}  z3={clock['z3']}",
        f"  m = maj(x1, y3, z3) : {record['majority']}",
        "  Thanh ghi được quay : " + (", ".join(rotated) if rotated else "(không có)"),
    ]
    for name in rotated:
        lines.append(f"    bit t của {name}      : {record['feedback_bits'][name]}")
    lines += [
        f"  Trước khi quay      : {format_state(record['state_before'])}",
        f"  Sau khi quay        : {format_state(record['state_after'])}",
        f"  Bit s_i = x5^y7^z8  : {record['output_bit']}",
    ]
    note = record.get("slide_mismatch")
    if note:
        lines.append(
            f"  [Lưu ý] Thanh ghi {note['register']}: tính theo quy tắc = {note['computed']}, "
            f"slide trang {note['slide_page']} in = {note['slide']} (TD-002); "
            f"không ảnh hưởng bit s_i."
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Các chức năng của menu (nhận hàm nhập/xuất để có thể kiểm thử)
# ---------------------------------------------------------------------------

def read_bits(prompt: str, input_fn=input, length: int | None = None) -> str | None:
    """Đọc chuỗi 0/1 từ người dùng; trả về None nếu để trống."""
    text = input_fn(prompt).strip().replace(" ", "")
    if not text:
        return None
    if any(ch not in "01" for ch in text):
        raise ValueError("Chỉ được nhập ký tự 0 và 1.")
    if length is not None and len(text) != length:
        raise ValueError(f"Cần đúng {length} bit, bạn nhập {len(text)} bit.")
    return text


def run_slide_example(output_fn=print) -> bool:
    """Chạy ví dụ slide, in từng bước và đối chiếu S, C. Trả về True nếu khớp."""
    cipher = TinyA51(SLIDE_KEY, annotate_slide=True)
    output_fn(f"Khoá K = {SLIDE_KEY}")
    output_fn(f"Trạng thái ban đầu: {format_state(cipher.get_state())}")
    keystream, trace = cipher.generate_keystream(len(SLIDE_PLAINTEXT))
    for record in trace:
        output_fn(format_step(record))
    cipher.reset()
    ciphertext = cipher.encrypt(SLIDE_PLAINTEXT)
    ok = keystream == SLIDE_KEYSTREAM and ciphertext == SLIDE_CIPHERTEXT
    output_fn("")
    output_fn(f"Bản rõ P = {SLIDE_PLAINTEXT}")
    output_fn(f"Dãy S    = {keystream}   (slide: {SLIDE_KEYSTREAM})")
    output_fn(f"Bản mã C = {ciphertext}   (slide: {SLIDE_CIPHERTEXT})")
    output_fn("Kết quả: KHỚP slide." if ok else "Kết quả: KHÔNG khớp slide!")
    return ok


def step_through(cipher: TinyA51, input_fn=input, output_fn=print) -> None:
    """Chạy từng bước theo yêu cầu người dùng."""
    cipher.reset()
    output_fn(f"Bắt đầu từ: {format_state(cipher.get_state())}")
    keystream = ""
    while True:
        answer = input_fn("Enter để chạy bước tiếp, q để dừng: ").strip().lower()
        if answer == "q":
            break
        bit, record = cipher.step_with_trace()
        keystream += str(bit)
        output_fn(format_step(record))
        output_fn(f"  Dãy S hiện có       : {keystream}")


def handle_choice(choice: str, cipher: TinyA51, input_fn=input, output_fn=print) -> TinyA51:
    """Xử lý một lựa chọn trong menu; trả về bộ sinh (có thể là bộ mới)."""
    if choice == "1":
        key = read_bits(f"Nhập khoá K ({KEY_LENGTH} bit): ", input_fn, KEY_LENGTH)
        if key is None:
            output_fn("Giữ nguyên khoá cũ.")
        else:
            cipher = TinyA51(key, annotate_slide=(key == SLIDE_KEY))
            output_fn(f"Đã nạp khoá. Trạng thái: {format_state(cipher.get_state())}")
    elif choice == "2":
        cipher = TinyA51(SLIDE_KEY, annotate_slide=True)
        output_fn(f"Đã nạp khoá ví dụ. Trạng thái: {format_state(cipher.get_state())}")
    elif choice == "3":
        output_fn(f"Khoá K    : {cipher.key}")
        output_fn(f"Trạng thái: {format_state(cipher.get_state())}")
    elif choice == "4":
        step_through(cipher, input_fn, output_fn)
    elif choice == "5":
        text = input_fn("Số bit n cần sinh: ").strip()
        if not text.isdigit() or int(text) == 0:
            raise ValueError("n phải là số nguyên dương.")
        cipher.reset()
        keystream, trace = cipher.generate_keystream(int(text))
        for record in trace:
            output_fn(format_step(record))
        output_fn(f"Dãy S ({len(keystream)} bit) = {keystream}")
    elif choice in ("6", "7"):
        encrypting = choice == "6"
        label = "bản rõ P" if encrypting else "bản mã C"
        data = read_bits(f"Nhập {label} (chuỗi 0/1): ", input_fn)
        if data is None:
            output_fn("Chưa nhập dữ liệu.")
        else:
            result = cipher.encrypt(data) if encrypting else cipher.decrypt(data)
            output_fn(f"Dãy S     = {cipher.keystream}")
            output_fn(f"{'Bản mã C' if encrypting else 'Bản rõ P'} = {result}")
            if input_fn("Xem nhật ký từng bước? (y/N): ").strip().lower() == "y":
                for record in cipher.export_trace():
                    output_fn(format_step(record))
    elif choice == "8":
        run_slide_example(output_fn)
    else:
        output_fn("Lựa chọn không hợp lệ, hãy nhập số từ 0 đến 8.")
    return cipher


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Demo dòng lệnh TinyA5/1")
    parser.add_argument("--example", action="store_true",
                        help="chạy ví dụ slide rồi thoát (không cần nhập)")
    args = parser.parse_args(argv)

    if args.example:
        return 0 if run_slide_example() else 1

    cipher = TinyA51(SLIDE_KEY, annotate_slide=True)
    while True:
        print(MENU.format(key=cipher.key))
        try:
            choice = input("Chọn chức năng: ").strip()
        except EOFError:
            print()
            return 0
        if choice == "0":
            print("Tạm biệt!")
            return 0
        try:
            cipher = handle_choice(choice, cipher)
        except ValueError as error:
            print(f"Lỗi: {error}")
        except EOFError:
            print()
            return 0


if __name__ == "__main__":
    sys.exit(main())
