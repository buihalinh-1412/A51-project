"""Chạy: python tests/run_verification.py  -- đối chiếu A5/1 với test vector Briceno."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.a51 import A51, bits_to_hex  # noqa: E402

KEY, FRAME = "0x1223456789ABCDEF", 0x134
EXPECTED_DOWN = "534EAA582FE8151AB6E1855A728C00"
EXPECTED_UP = "24FD35A35D5FB6526D32F906DF1AC0"


def main() -> int:
    down, up = A51(KEY, FRAME).generate_keystream()
    got_down, got_up = bits_to_hex(down), bits_to_hex(up)
    print(f"Khoá: {KEY}   Số khung: {FRAME:#x}")
    print(f"{'':10}{'Mong đợi':34}{'Thực tế':34}Kết quả")
    for name, exp, got in (("Downlink", EXPECTED_DOWN, got_down),
                           ("Uplink", EXPECTED_UP, got_up)):
        print(f"{name:10}{exp:34}{got:34}{'ĐÚNG' if exp == got else 'SAI'}")
    ok = got_down == EXPECTED_DOWN and got_up == EXPECTED_UP
    print("KHỚP test vector Briceno" if ok else "KHÔNG KHỚP")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
