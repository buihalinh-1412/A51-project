"""Module cung cap cac ham tien ich xu ly chuoi bit va xac thuc du lieu."""


def text_to_bits(text: str) -> str:
    """Chuyen doi chuoi van ban ASCII thanh chuoi bit nhi phan."""
    return "".join(f"{ord(c):08b}" for c in text)


def bits_to_text(bits: str) -> str:
    """Chuyen doi chuoi bit nhi phan ve chuoi van ban ASCII."""
    if len(bits) % 8 != 0:
        raise ValueError("Do dai chuoi bit phai la boi so cua 8.")
    chars = [chr(int(bits[i : i + 8], 2)) for i in range(0, len(bits), 8)]
    return "".join(chars)
  """Module cung cap cac ham tien ich xu ly chuoi bit va xac thuc du lieu."""


def text_to_bits(text: str) -> str:
    """Chuyen doi chuoi van ban ASCII thanh chuoi bit nhi phan."""
    return "".join(f"{ord(c):08b}" for c in text)


def bits_to_text(bits: str) -> str:
    """Chuyen doi chuoi bit nhi phan ve chuoi van ban ASCII."""
    if len(bits) % 8 != 0:
        raise ValueError("Do dai chuoi bit phai la boi so cua 8.")
    chars = [chr(int(bits[i : i + 8], 2)) for i in range(0, len(bits), 8)]
    return "".join(chars)


def xor_bit_strings(a: str, b: str) -> str:
    """Thuc hien phep XOR tung bit giua hai chuoi bit cung do dai."""
    if len(a) != len(b):
        raise ValueError("Hai chuoi bit phai co cung do dai.")
    return "".join(str(int(bit_a) ^ int(bit_b)) for bit_a, bit_b in zip(a, b))


def validate_binary_string(s: str, expected_length: int | None = None) -> bool:
    """Kiem tra chuoi co hop le (chi gom '0' va '1') va dung do dai yeu cau."""
    if not isinstance(s, str) or not s:
        return False
    if not all(c in "01" for c in s):
        return False
    if expected_length is not None and len(s) != expected_length:
        return False
    return True
