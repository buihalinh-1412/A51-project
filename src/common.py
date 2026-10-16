"""src/common.py — Tiện ích xử lý chuỗi bit dùng chung (Người phụ trách: Trần Đại Lộc).

Chỉ xử lý dữ liệu, KHÔNG dùng print() và KHÔNG dùng thư viện mật mã.
Quy ước: chuỗi bit là str gồm '0'/'1'; văn bản <-> bit qua UTF-8, mỗi byte 8 bit, MSB trước
(cùng quy ước với demo_cli.py; với ký tự ASCII cho kết quả giống hệt text_to_bits cũ).
"""
from __future__ import annotations


def validate_binary_string(s: str, expected_length: int | None = None) -> bool:
    """True nếu s là chuỗi không rỗng chỉ gồm '0'/'1' (và đúng độ dài nếu có yêu cầu)."""
    if not isinstance(s, str) or not s:
        return False
    if any(c not in "01" for c in s):
        return False
    return expected_length is None or len(s) == expected_length


def text_to_bits(text: str) -> str:
    """Văn bản -> chuỗi bit (UTF-8, mỗi byte 8 bit). Chuỗi rỗng -> chuỗi rỗng."""
    return "".join(f"{byte:08b}" for byte in text.encode("utf-8"))


def bits_to_text(bits: str) -> str:
    """Chuỗi bit -> văn bản UTF-8. Chuỗi rỗng -> chuỗi rỗng."""
    if bits and not validate_binary_string(bits):
        raise ValueError("Chuoi bit chi duoc chua ky tu 0 va 1.")
    if len(bits) % 8 != 0:
        raise ValueError("Do dai chuoi bit phai la boi so cua 8.")
    data = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Chuoi bit khong phai UTF-8 hop le.") from None


def xor_bit_strings(a: str, b: str) -> str:
    """XOR từng bit của hai chuỗi bit cùng độ dài."""
    if len(a) != len(b):
        raise ValueError("Hai chuoi bit phai co cung do dai.")
    if (a and not validate_binary_string(a)) or (b and not validate_binary_string(b)):
        raise ValueError("Chuoi bit chi duoc chua ky tu 0 va 1.")
    return "".join("1" if x != y else "0" for x, y in zip(a, b))
