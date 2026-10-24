"""
attack_two_time_pad.py - Mô phỏng tấn công dùng lại dòng khoá (Two-Time Pad).

Người phụ trách: Hoàng Yến Nhi (việc 5.3, Giai đoạn 3).

Ý tưởng: nếu hai bản rõ P1, P2 được mã hoá bằng cùng một dòng khoá S thì
    C1 = P1 XOR S,  C2 = P2 XOR S
    => C1 XOR C2 = (P1 XOR S) XOR (P2 XOR S) = P1 XOR P2   (S triệt tiêu)
Kẻ nghe lén chỉ cần đoán một đoạn chữ (crib) của P1 là đọc được đoạn
tương ứng của P2.

Quy ước (docs/coding_convention.md): file trong src/ không in ra màn hình,
chỉ trả về giá trị. Mã hoá dùng crypt_bytes của src/file_crypto.py (Hà Linh).
"""

from __future__ import annotations

from src.file_crypto import crypt_bytes

# Các ký tự được coi là "đọc được": chữ cái, chữ số, dấu cách, dấu câu cơ bản.
_PUNCTUATION = set(b".,;:!?'\"()-/")
# Xuống dòng, về đầu dòng, tab cũng là ký tự đọc được (file mẫu có thể kết thúc bằng xuống dòng).
_WHITESPACE = set(b"\n\r\t")


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR từng byte của a và b, lấy theo độ dài của chuỗi ngắn hơn."""
    return bytes(x ^ y for x, y in zip(a, b))


def _is_letter(byte: int) -> bool:
    """True nếu byte là chữ cái ASCII hoặc dấu cách."""
    return byte == 0x20 or 0x41 <= byte <= 0x5A or 0x61 <= byte <= 0x7A


def _is_readable(byte: int) -> bool:
    """True nếu byte là ký tự đọc được (chữ, số, dấu cách, dấu câu cơ bản)."""
    return _is_letter(byte) or 0x30 <= byte <= 0x39 or byte in _PUNCTUATION
    """True nếu byte là ký tự đọc được (chữ, số, dấu cách, dấu câu cơ bản, \\n \\r \\t)."""
    return (_is_letter(byte) or 0x30 <= byte <= 0x39
            or byte in _PUNCTUATION or byte in _WHITESPACE)


def simulate_scenario(p1: bytes, p2: bytes, key_hex: str,
                      frame1: int, frame2: int) -> dict:
    """Mô phỏng trạm mã hoá hai tin nhắn P1, P2 rồi kẻ nghe lén thu 2 bản mã.

    Tham số:
        p1, p2: hai bản rõ (bytes).
        key_hex: khoá 16 ký tự hex (64 bit).
        frame1, frame2: số khung dùng cho P1 và P2. Hai số này bằng nhau
            nghĩa là trạm dùng lại dòng khoá.

    Trả về dict:
        "c1", "c2": hai bản mã.
        "c1_xor_c2": C1 XOR C2 (độ dài bằng bản ngắn hơn).
        "p1_xor_p2": P1 XOR P2 (độ dài bằng bản ngắn hơn).
        "reused": True nếu frame1 == frame2.
    """
    c1 = crypt_bytes(p1, key_hex, frame1)
    c2 = crypt_bytes(p2, key_hex, frame2)
    return {
        "c1": c1,
        "c2": c2,
        "c1_xor_c2": _xor_bytes(c1, c2),
        "p1_xor_p2": _xor_bytes(p1, p2),
        "reused": frame1 == frame2,
    }


def recover_with_known_plaintext(c1: bytes, p1: bytes, c2: bytes) -> bytes:
    """Khôi phục P2 khi biết cả C1, P1 và C2 (cùng dòng khoá).

    Tham số:
        c1: bản mã của P1.
        p1: bản rõ P1 mà kẻ tấn công đã biết.
        c2: bản mã của P2 (dùng cùng dòng khoá với C1).

    Trả về P2 (bytes): S = C1 XOR P1, P2 = C2 XOR S.
    Độ dài kết quả bằng độ dài ngắn nhất trong 3 đầu vào.
    """
    keystream = _xor_bytes(c1, p1)
    return _xor_bytes(c2, keystream)


def crib_drag(c1: bytes, c2: bytes, crib: bytes, top: int = 10) -> list:
    """Trượt một đoạn chữ đoán trước (crib) dọc theo C1 XOR C2.

    Với mỗi vị trí i, tính (C1 XOR C2)[i : i + len(crib)] XOR crib. Nếu crib
    đúng là đoạn chữ của P1 tại vị trí i thì kết quả là đoạn chữ của P2.

    Tham số:
        c1, c2: hai bản mã.
        crib: đoạn chữ đoán có trong P1 (bytes).
        top: số kết quả tốt nhất cần trả về.

    Trả về list các dict {"offset": int, "text": str, "score": float}, xếp
    theo điểm giảm dần (điểm = tỷ lệ ký tự đọc được, từ 0 đến 1; điểm bằng
    nhau thì ưu tiên đoạn có nhiều chữ cái/dấu cách hơn, rồi vị trí nhỏ hơn).
    """
    x = _xor_bytes(c1, c2)
    n = len(crib)
    if n == 0 or n > len(x):
        return []
    rows = []
    for i in range(len(x) - n + 1):
        piece = _xor_bytes(x[i:i + n], crib)
        score = sum(_is_readable(b) for b in piece) / n
        letters = sum(_is_letter(b) for b in piece) / n
        rows.append((score, letters, i, piece))
    rows.sort(key=lambda r: (-r[0], -r[1], r[2]))
    return [
        {"offset": i, "text": piece.decode("ascii", errors="replace"),
         "score": score}
        for score, _letters, i, piece in rows[:top]
    ]
