"""
demo_cli.py — Công cụ demo dòng lệnh tương tác cho TinyA5/1 và A5/1.

Người phụ trách: Nguyễn Thị Nhật Linh (việc 2.6, Giai đoạn 2). Bản rà soát: dùng lõi A51
cho mọi phép mã hóa/giải mã dữ liệu dài (không tự chia khung nữa), mặc định luồng Downlink.

Chạy từ thư mục gốc của repo:
    python demo_cli.py             # menu chính (chọn TinyA5/1 hoặc A5/1)
    python demo_cli.py --example   # chạy ví dụ slide TinyA5/1 rồi thoát

Tệp này chỉ làm phần nhập/xuất và chuyển đổi định dạng (văn bản <-> bit <-> hex).
Mọi phép tính mật mã nằm trong src/tiny_a51.py (TinyA51) và src/a51.py (A51);
tệp này không import thư viện mật mã và không sao chép thuật toán
(docs/coding_convention.md mục 8). Toàn bộ lệnh print() nằm ở đây.

Ví dụ trên lớp [slide Chương 2, trang 49–50]:
    K = 10010101001110100110000, P = 111  ->  S = 100, C = 011
Slide trang 50 in Z sau Bước 2 là 101001100, đây là lỗi in của slide: tính theo
quy tắc quay (t = z2^z7^z8 = 0) thì Z đúng là 001001100 (TD-002). Demo luôn dùng
giá trị tính theo quy tắc và ghi chú rõ chỗ slide in sai; lỗi này không ảnh hưởng
bit s_i vì s_i chỉ dùng z8 (cả hai giá trị đều có z8 = 0).

Lưu ý về A5/1 [TD-005]: một khung GSM chỉ mã được 114 bít. Với văn bản dài, lõi A51
chia thành nhiều khung liên tiếp (số khung = frame + k). Đây là quy ước tạm của nhóm,
KHÔNG phải chuẩn GSM; báo cáo cần ghi chú rõ điều này.
Hướng: Downlink = 114 bít đầu = Trạm phát (BTS) -> Máy di động (MS);
       Uplink   = 114 bít sau = Máy di động (MS) -> Trạm phát (BTS).
"""

from __future__ import annotations

import argparse
import sys

try:
    from src.tiny_a51 import KEY_LENGTH, SLIDE_KEY, SLIDE_PLAINTEXT, TinyA51
except ImportError:  # chạy khi đứng trong thư mục src/
    from tiny_a51 import KEY_LENGTH, SLIDE_KEY, SLIDE_PLAINTEXT, TinyA51

try:
    from src.a51 import A51
except ImportError:
    try:
        from a51 import A51
    except ImportError:  # src/a51.py chưa được merge: TinyA5/1 vẫn chạy bình thường
        A51 = None

SLIDE_KEYSTREAM = "100"      # S theo slide trang 50
SLIDE_CIPHERTEXT = "011"     # C theo slide trang 50

A51_FRAME_COUNT_BITS = 22    # độ dài số khung (bít)
A51_KEY_EXAMPLE = "1223456789ABCDEF"
A51_FRAME_EXAMPLE = "0x134"
# Mặc định giống lõi A51 (encrypt_bytes dùng Downlink) để CLI, file_crypto (GĐ3) và test cùng một quy ước
A51_USE_UPLINK = False
# Test vector Briceno [S2] cho khoá/khung ví dụ ở trên (docs/a51_test_vector.md)
A51_EXPECTED_DOWNLINK = "534EAA582FE8151AB6E1855A728C00"
A51_EXPECTED_UPLINK = "24FD35A35D5FB6526D32F906DF1AC0"

MAIN_MENU = """
==========================================
   DEMO HỆ MÃ DÒNG A5/1 VÀ TinyA5/1
   (Chương trình mô phỏng phục vụ học tập)
==========================================
 1. TinyA5/1: mô phỏng từng bước (Trace Log)
 2. A5/1 đầy đủ: mã hóa / giải mã văn bản
 3. Mã hóa / giải mã file (A5/1)
 4. Tấn công Two-Time Pad (dùng lại số khung)
 5. Đo tốc độ A5/1
 0. Thoát
==========================================
"""

MENU = """
================ DEMO TinyA5/1 ================
 1. Nhập khoá K (23 bit)         [hiện tại: {key}]
 2. Dùng khoá ví dụ trên slide
 3. Xem trạng thái ba thanh ghi X, Y, Z
 4. Chạy từng bước (Enter = bước tiếp theo, q = dừng)
 5. Sinh dãy số S gồm n bit, hiện bảng nhật ký (trace)
 6. Mã hoá bản rõ P            (C = P XOR S)
 7. Giải mã bản mã C           (P = C XOR S)
 8. Chạy ví dụ slide và đối chiếu kết quả
 0. Quay lại menu chính
===============================================
"""

A51_MENU = """
=========== A5/1 ĐẦY ĐỦ (GSM) ===========
 1. Mã hóa văn bản
 2. Giải mã bản mã (hex)
 3. Round-trip: mã hóa rồi giải mã ngay
 4. Xem dòng khoá 228 bit (downlink / uplink, hex)
 0. Quay lại menu chính
=========================================
"""

def setup_console() -> None:
    """Ép stdin/stdout/stderr dùng UTF-8 để không lỗi tiếng Việt trên Windows."""
    for stream in (sys.stdout, sys.stderr, sys.stdin):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass

# ---------------------------------------------------------------------------
# TinyA5/1 — định dạng đầu ra
# ---------------------------------------------------------------------------

def format_state(state: dict[str, str]) -> str:
    """'X=100101  Y=01001110  Z=100110000'."""
    return "  ".join(f"{name}={bits}" for name, bits in state.items())

def format_step(record: dict) -> str:
    """Biến một bản ghi trace thành đoạn văn bản nhiều dòng (chế độ chạy từng bước)."""
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
            f"  [Lưu ý] Thanh ghi {note['register']}: ĐÚNG theo quy tắc quay = {note['computed']}; "
            f"slide trang {note['slide_page']} in SAI = {note['slide']} (lỗi in, TD-002); "
            f"không ảnh hưởng bit s_i."
        )
    return "\n".join(lines)

TABLE_HEADER = ["Bước", "X trước", "Y trước", "Z trước", "x1 y3 z3",
                "m", "Quay", "X sau", "Y sau", "Z sau", "s_i"]

def format_trace_table(trace: list[dict]) -> str:
    """Bảng trace căn lề, chỉ dùng ký tự + - | (không vỡ trên terminal Windows cũ)."""
    rows = []
    for r in trace:
        c = r["clock_bits"]
        before, after = r["state_before"], r["state_after"]
        rows.append([
            str(r["step"]), before["X"], before["Y"], before["Z"],
            f"{c['x1']}  {c['y3']}  {c['z3']}", str(r["majority"]),
            ",".join(r["rotated_registers"]) or "-",
            after["X"], after["Y"], after["Z"], str(r["output_bit"]),
        ])
    widths = [max([len(h)] + [len(row[i]) for row in rows])
              for i, h in enumerate(TABLE_HEADER)]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(cells: list[str]) -> str:
        return "| " + " | ".join(t.center(w) for t, w in zip(cells, widths)) + " |"

    out = [sep, line(TABLE_HEADER), sep] + [line(row) for row in rows] + [sep]
    for r in trace:
        note = r.get("slide_mismatch")
        if note:
            out.append(
                f"* Bước {r['step']}: {note['register']} ĐÚNG theo quy tắc quay = {note['computed']}; "
                f"slide trang {note['slide_page']} in SAI = {note['slide']} (lỗi in, TD-002); "
                f"không ảnh hưởng s_i."
            )
    return "\n".join(out)

# ---------------------------------------------------------------------------
# TinyA5/1 — các chức năng của menu (nhận hàm nhập/xuất để có thể kiểm thử)
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
    """Chạy ví dụ slide, in bảng trace và đối chiếu S, C. Trả về True nếu khớp."""
    cipher = TinyA51(SLIDE_KEY, annotate_slide=True)
    output_fn(f"Khoá K = {SLIDE_KEY}")
    output_fn(f"Trạng thái ban đầu: {format_state(cipher.get_state())}")
    keystream, trace = cipher.generate_keystream(len(SLIDE_PLAINTEXT))
    output_fn(format_trace_table(trace))
    cipher.reset()
    ciphertext = cipher.encrypt(SLIDE_PLAINTEXT)
    decrypted = cipher.decrypt(ciphertext)
    ok = (keystream == SLIDE_KEYSTREAM and ciphertext == SLIDE_CIPHERTEXT
          and decrypted == SLIDE_PLAINTEXT)
    output_fn("")
    output_fn(f"Bản rõ P = {SLIDE_PLAINTEXT}")
    output_fn(f"Dãy S    = {keystream}   (slide: {SLIDE_KEYSTREAM})")
    output_fn(f"Bản mã C = {ciphertext}   (slide: {SLIDE_CIPHERTEXT})")
    output_fn(f"Giải mã  = {decrypted}   (phải bằng P)")
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
    """Xử lý một lựa chọn trong menu TinyA5/1; trả về bộ sinh (có thể là bộ mới)."""
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
        output_fn(format_trace_table(trace))
        output_fn(f"Dãy S ({len(keystream)} bit) = {keystream}")
    elif choice in ("6", "7"):
        encrypting = choice == "6"
        default = SLIDE_PLAINTEXT if encrypting else SLIDE_CIPHERTEXT
        label = "bản rõ P" if encrypting else "bản mã C"
        data = read_bits(f"Nhập {label} (chuỗi 0/1) [Enter = {default}]: ", input_fn) or default
        result = cipher.encrypt(data) if encrypting else cipher.decrypt(data)
        output_fn(f"Dãy S     = {cipher.keystream}")
        output_fn(f"{'Bản mã C' if encrypting else 'Bản rõ P'} = {result}")
        output_fn(format_trace_table(cipher.export_trace()))
    elif choice == "8":
        run_slide_example(output_fn)
    else:
        output_fn("Lựa chọn không hợp lệ, hãy nhập số từ 0 đến 8.")
    return cipher

def tiny_menu(cipher: TinyA51, input_fn=input, output_fn=print) -> TinyA51:
    """Vòng lặp menu TinyA5/1; '0' quay lại menu chính."""
    while True:
        output_fn(MENU.format(key=cipher.key))
        choice = input_fn("Chọn chức năng: ").strip()
        if choice == "0":
            return cipher
        try:
            cipher = handle_choice(choice, cipher, input_fn, output_fn)
        except ValueError as error:
            output_fn(f"Lỗi: {error}")

# ---------------------------------------------------------------------------
# A5/1 — chuyển đổi định dạng và kiểm tra đầu vào (adapter)
# Lõi A51 lo toàn bộ keystream, chia khung (encrypt_bytes) và XOR;
# văn bản <-> byte <-> hex là việc của CLI.
# ---------------------------------------------------------------------------

def bytes_to_bits(data: bytes) -> list[int]:
    """Bytes -> danh sách bít, MSB-first (bít cao của mỗi byte đi trước)."""
    return [(byte >> (7 - i)) & 1 for byte in data for i in range(8)]

def bits_to_bytes(bits: list[int]) -> bytes:
    """Danh sách bít (MSB-first) -> bytes; số bít phải chia hết cho 8."""
    if len(bits) % 8:
        raise ValueError("Số bit phải chia hết cho 8.")
    out = bytearray()
    for i in range(0, len(bits), 8):
        value = 0
        for bit in bits[i:i + 8]:
            value = (value << 1) | bit
        out.append(value)
    return bytes(out)

def bits_to_hex(bits) -> str:
    """Danh sách bít -> chuỗi hex in hoa; đệm 0 vào cuối nếu chưa đủ byte."""
    return bits_to_bytes(list(bits) + [0] * (-len(bits) % 8)).hex().upper()

def parse_key_hex(text: str) -> str:
    """Khoá phải là ĐÚNG 16 ký tự hex (64 bít). Không tự cắt/đệm."""
    t = text.strip().replace(" ", "")
    if t.lower().startswith("0x"):
        t = t[2:]
    if len(t) != 16 or any(ch not in "0123456789abcdefABCDEF" for ch in t):
        raise ValueError("Khoá phiên phải đúng 16 ký tự hex (64 bit), ví dụ 1223456789ABCDEF.")
    return "0x" + t

def parse_frame(text: str) -> int:
    """Số khung: số nguyên thập phân hoặc dạng 0x..., trong [0, 2^22 - 1]."""
    t = text.strip().lower()
    try:
        value = int(t, 16) if t.startswith("0x") else int(t)
    except ValueError:
        raise ValueError("Số khung phải là số nguyên (thập phân hoặc dạng 0x...).") from None
    if not 0 <= value < (1 << A51_FRAME_COUNT_BITS):
        raise ValueError("Số khung phải nằm trong khoảng 0 đến 4194303 (22 bit).")
    return value

def a51_encrypt_text(text: str, key_hex: str, frame: int, use_uplink: bool = A51_USE_UPLINK) -> str:
    """Văn bản -> UTF-8 -> A51.encrypt_bytes -> hex in hoa."""
    return A51(key_hex, frame).encrypt_bytes(text.encode("utf-8"), use_uplink).hex().upper()

def a51_decrypt_hex(hex_text: str, key_hex: str, frame: int, use_uplink: bool = A51_USE_UPLINK) -> str:
    """Hex -> bytes -> A51.decrypt_bytes -> văn bản UTF-8."""
    try:
        data = bytes.fromhex(hex_text.strip().replace(" ", ""))
    except ValueError:
        raise ValueError("Bản mã phải là chuỗi hex hợp lệ (số ký tự chẵn, chỉ 0-9 và A-F).") from None
    plain = A51(key_hex, frame).decrypt_bytes(data, use_uplink)
    try:
        return plain.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Kết quả không phải UTF-8 hợp lệ: có thể sai khoá, sai số khung hoặc sai chiều.") from None

# ---------------------------------------------------------------------------
# A5/1 — menu
# ---------------------------------------------------------------------------

def ask_a51_params(input_fn, output_fn=print) -> tuple[str, int]:
    """Hỏi khoá và số khung; Enter để dùng giá trị ví dụ."""
    key_text = input_fn(f"Khoá phiên 64 bit (16 hex) [Enter = {A51_KEY_EXAMPLE}]: ").strip() or A51_KEY_EXAMPLE
    frame_text = input_fn(f"Số khung (thập phân hoặc 0x...) [Enter = {A51_FRAME_EXAMPLE}]: ").strip() or A51_FRAME_EXAMPLE
    return parse_key_hex(key_text), parse_frame(frame_text)

def handle_a51_choice(choice: str, input_fn=input, output_fn=print) -> None:
    """Xử lý một lựa chọn trong menu A5/1."""
    direction = "Uplink (MS -> BTS, 114 bit sau)" if A51_USE_UPLINK else "Downlink (BTS -> MS, 114 bit đầu)"
    if choice == "1":
        key, frame = ask_a51_params(input_fn, output_fn)
        text = input_fn("Nhập bản rõ: ")
        if not text:
            output_fn("Chưa nhập bản rõ.")
            return
        output_fn(f"Bản mã (hex) : {a51_encrypt_text(text, key, frame)}")
        output_fn(f"Dùng luồng    : {direction}; khoá={key}, khung={frame}")
        output_fn("Hãy ghi nhớ khoá và số khung: cần đúng cả hai để giải mã.")
    elif choice == "2":
        key, frame = ask_a51_params(input_fn, output_fn)
        hex_text = input_fn("Nhập bản mã (hex): ")
        output_fn(f"Bản rõ sau giải mã: {a51_decrypt_hex(hex_text, key, frame)}")
    elif choice == "3":
        key, frame = ask_a51_params(input_fn, output_fn)
        text = input_fn("Nhập bản rõ: ")
        if not text:
            output_fn("Chưa nhập bản rõ.")
            return
        cipher_hex = a51_encrypt_text(text, key, frame)
        recovered = a51_decrypt_hex(cipher_hex, key, frame)
        output_fn(f"Bản rõ gốc  : {text}")
        output_fn(f"Bản mã (hex): {cipher_hex}")
        output_fn(f"Sau giải mã : {recovered}")
        output_fn("Kết quả: ĐÚNG (P' == P)." if recovered == text else "Kết quả: SAI (P' != P)!")
    elif choice == "4":
        key, frame = ask_a51_params(input_fn, output_fn)
        downlink, uplink = A51(key, frame).generate_keystream()
        down_hex, up_hex = bits_to_hex(downlink), bits_to_hex(uplink)
        output_fn(f"Downlink (114 bit đầu, BTS -> MS): {down_hex}")
        output_fn(f"Uplink   (114 bit sau, MS -> BTS): {up_hex}")
        if key.upper() == "0X" + A51_KEY_EXAMPLE and frame == int(A51_FRAME_EXAMPLE, 16):
            same = down_hex == A51_EXPECTED_DOWNLINK and up_hex == A51_EXPECTED_UPLINK
            output_fn("Đối chiếu test vector Briceno [S2]: " + ("KHỚP." if same else "KHÔNG KHỚP!"))
    else:
        output_fn("Lựa chọn không hợp lệ, hãy nhập số từ 0 đến 4.")

def a51_menu(input_fn=input, output_fn=print) -> None:
    """Vòng lặp menu A5/1; '0' quay lại menu chính."""
    if A51 is None:
        output_fn("Chưa tìm thấy src/a51.py (có thể chưa được merge). Hãy dùng menu TinyA5/1.")
        return
    while True:
        output_fn(A51_MENU)
        choice = input_fn("Chọn chức năng: ").strip()
        if choice == "0":
            return
        try:
            handle_a51_choice(choice, input_fn, output_fn)
        except (ValueError, TypeError) as error:
            output_fn(f"Lỗi: {error}")


# ---------------------------------------------------------------------------
# Giai đoạn 3: file, tấn công Two-Time Pad, đo tốc độ
# Các hàm này chỉ nhập/xuất; phần tính toán nằm trong src/file_crypto.py,
# src/attack_two_time_pad.py và src/benchmark.py (nạp khi cần để thiếu file
# nào thì chỉ báo "chưa có" chứ không làm sập menu).
# ---------------------------------------------------------------------------

P1_PATH = "examples/p1.txt"
P2_PATH = "examples/p2.txt"
ATTACK_KEY = A51_KEY_EXAMPLE
ATTACK_FRAME = 0x134
DEFAULT_CRIB = "meeting"


def file_menu(input_fn=input, output_fn=print) -> None:
    """Mục 3: mã hóa hoặc giải mã một file thật bằng encrypt_file / decrypt_file."""
    try:
        from src.file_crypto import decrypt_file, encrypt_file
    except ImportError:
        output_fn("Chưa tìm thấy src/file_crypto.py (có thể chưa được merge).")
        return
    mode = input_fn("Chọn (1 = mã hóa, 2 = giải mã): ").strip()
    if mode not in ("1", "2"):
        output_fn("Lựa chọn không hợp lệ, hãy nhập 1 hoặc 2.")
        return
    path = input_fn("Đường dẫn file: ").strip().strip('"')
    key_text = input_fn(f"Khóa 16 ký tự hex [Enter = {A51_KEY_EXAMPLE}]: ").strip() or A51_KEY_EXAMPLE
    try:
        key = parse_key_hex(key_text)[2:]
        if mode == "1":
            frame = parse_frame(input_fn("Số khung bắt đầu [Enter = 0]: ").strip() or "0")
            out_path = path + ".enc"
            encrypt_file(path, out_path, key, frame)
        else:
            out_path = path + ".dec"
            decrypt_file(path, out_path, key)
    except (OSError, ValueError) as error:
        output_fn(f"Lỗi: {error}")
        return
    output_fn(f"Xong. File kết quả: {out_path}")


def attack_demo(output_fn=print) -> None:
    """Mục 4: demo Two-Time Pad với examples/p1.txt và p2.txt."""
    try:
        from src.attack_two_time_pad import crib_drag, simulate_scenario
    except ImportError:
        output_fn("Chưa tìm thấy src/attack_two_time_pad.py (có thể chưa được merge).")
        return
    try:
        with open(P1_PATH, "rb") as f1, open(P2_PATH, "rb") as f2:
            p1, p2 = f1.read(), f2.read()
    except OSError as error:
        output_fn(f"Lỗi: không đọc được file mẫu ({error}).")
        return
    output_fn(f"P1 = {p1.decode('utf-8', errors='replace')}")
    output_fn(f"P2 = {p2.decode('utf-8', errors='replace')}")
    for title, frame2 in (("Dùng lại số khung (frame2 = frame1)", ATTACK_FRAME),
                          ("Đổi số khung (frame2 = frame1 + 1)", ATTACK_FRAME + 1)):
        result = simulate_scenario(p1, p2, ATTACK_KEY, ATTACK_FRAME, frame2)
        output_fn(f"\n--- {title} ---")
        output_fn(f"reused = {result['reused']}")
        output_fn(f"C1 xor C2 == P1 xor P2 ? {result['c1_xor_c2'] == result['p1_xor_p2']}")
        hits = crib_drag(result["c1"], result["c2"], DEFAULT_CRIB.encode("ascii"), top=3)
        output_fn(f"Dò crib '{DEFAULT_CRIB}' trong P1, 3 kết quả tốt nhất:")
        for hit in hits:
            output_fn(f"  offset {hit['offset']:>3}  điểm {hit['score']:.2f}  đoạn P2: {hit['text']!r}")
    output_fn("\nKết luận: dùng lại số khung thì lộ chữ của P2; đổi số khung thì ra rác.")


def benchmark_demo(output_fn=print) -> None:
    """Mục 5: in bảng kết quả run_benchmark."""
    try:
        from src.benchmark import run_benchmark
    except ImportError:
        output_fn("Chưa tìm thấy src/benchmark.py (có thể chưa được merge).")
        return
    output_fn(f"{'Kích thước (byte)':>18} {'Thời gian (s)':>14} {'KiB/s':>10}")
    for row in run_benchmark():
        output_fn(f"{row['size']:>18} {row['seconds']:>14.4f} {row['kib_per_s']:>10.1f}")

# ---------------------------------------------------------------------------
# Chương trình chính
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    setup_console()
    parser = argparse.ArgumentParser(description="Demo dòng lệnh A5/1 và TinyA5/1")
    parser.add_argument("--example", action="store_true",
                        help="chạy ví dụ slide TinyA5/1 rồi thoát (không cần nhập)")
    args = parser.parse_args(argv)
    if args.example:
        return 0 if run_slide_example() else 1

    cipher = TinyA51(SLIDE_KEY, annotate_slide=True)
    try:
        while True:
            print(MAIN_MENU)
            choice = input("Chọn: ").strip()
            if choice == "0":
                print("Tạm biệt!")
                return 0
            if choice == "1":
                cipher = tiny_menu(cipher)
            elif choice == "2":
                a51_menu()
            elif choice == "3":
                file_menu()
            elif choice == "4":
                attack_demo()
            elif choice == "5":
                benchmark_demo()
            else:
                print("Lựa chọn không hợp lệ, hãy nhập số từ 0 đến 5.")
    except (EOFError, KeyboardInterrupt):
        print()
        return 0

if __name__ == "__main__":
    sys.exit(main())
