"""
file_crypto.py: Mã hóa và giải mã file bằng A5/1.
Cơ chế: chia dữ liệu thành đoạn 57 byte. Đoạn thứ i dùng hai khung
start_frame + 2i và start_frame + 2i + 1 (mỗi khung 228 bit = 114 downlink
+ 114 uplink, hai khung = 456 bit = 57 byte), rồi XOR với đoạn dữ liệu.
Mã hóa và giải mã dùng chung hàm crypt_bytes.
Cấu trúc file mã hóa: 4 byte đầu là start_frame (big-endian) + dữ liệu mã hóa.
Khóa hex được A51 tự kiểm tra và đổi sang bit (quy ước Briceno); file này
không tự đổi khóa nên không thể lệch với A51.
File này KHÔNG dùng print().
"""

import math
import os

from src.a51 import A51

CHUNK_SIZE = 57          # byte mỗi đoạn (2 khung x 228 bit = 456 bit)
MAX_FRAMES = 1 << 22     # số khung GSM tối đa (22 bit)


def _bits_to_bytes(bits: list) -> bytes:
    """Gom mỗi 8 bit thành 1 byte (bit đầu tiên là bit cao nhất của byte)."""
    out = bytearray()
    for i in range(0, len(bits), 8):
        value = 0
        chunk = bits[i:i + 8]
        for b in chunk:
            value = (value << 1) | b
        if len(chunk) < 8:
            value <<= 8 - len(chunk)
        out.append(value)
    return bytes(out)


def crypt_bytes(data: bytes, key_hex: str, start_frame: int = 0) -> bytes:
    """XOR dữ liệu với dòng khóa A5/1 theo từng đoạn 57 byte (2 khung mỗi đoạn).
    Tham số:
        data: dữ liệu cần mã hóa hoặc giải mã.
        key_hex: khóa 16 ký tự hex (64 bit), ví dụ "1223456789ABCDEF".
        start_frame: số khung bắt đầu.
    Trả về: bytes cùng độ dài với data. Sai khóa hoặc số khung thì ném ValueError.
    """
    # Tạo thử một A51 để kiểm tra khóa và số khung ngay cả khi data rỗng.
    A51(key_hex, start_frame)

    out = bytearray()
    for i in range(0, len(data), CHUNK_SIZE):
        chunk = data[i:i + CHUNK_SIZE]
        f1 = start_frame + 2 * (i // CHUNK_SIZE)
        f2 = f1 + 1

        down1, up1 = A51(key_hex, f1).generate_keystream()
        down2, up2 = A51(key_hex, f2).generate_keystream()

        keystream = _bits_to_bytes(down1 + up1 + down2 + up2)   # 456 bit -> 57 byte
        out.extend(b ^ keystream[j] for j, b in enumerate(chunk))
    return bytes(out)


def _write_chunks(out_path: str, header: bytes, data: bytes, progress) -> None:
    """Ghi header (nếu có) rồi ghi data theo từng đoạn, gọi progress sau mỗi đoạn."""
    total = len(data)
    with open(out_path, "wb") as f_out:
        f_out.write(header)
        for i in range(0, total, CHUNK_SIZE):
            f_out.write(data[i:i + CHUNK_SIZE])
            if progress:
                progress(min(i + CHUNK_SIZE, total), total)
        if total == 0 and progress:
            progress(0, 0)


def encrypt_file(in_path, out_path, key_hex, start_frame=0, progress=None):
    """Mã hóa file: ghi 4 byte start_frame (big-endian) rồi dữ liệu đã mã hóa.
    progress(da_xong, tong): hàm gọi lại sau mỗi đoạn, có thể để None.
    """
    if in_path == out_path:
        raise ValueError("File đầu vào và file đầu ra không được trùng nhau.")
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Không tìm thấy file nguồn: {in_path}")

    with open(in_path, "rb") as f:
        data = f.read()

    num_chunks = math.ceil(len(data) / CHUNK_SIZE)
    if start_frame + num_chunks * 2 > MAX_FRAMES:
        raise ValueError("Số hiệu khung vượt quá giới hạn GSM (2^22 khung).")

    encrypted = crypt_bytes(data, key_hex, start_frame)
    header = start_frame.to_bytes(4, "big")
    _write_chunks(out_path, header, encrypted, progress)


def decrypt_file(in_path, out_path, key_hex, progress=None):
    """Giải mã file: đọc 4 byte đầu lấy start_frame, giải phần còn lại."""
    if in_path == out_path:
        raise ValueError("File đầu vào và file đầu ra không được trùng nhau.")
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Không tìm thấy file mã hóa: {in_path}")

    with open(in_path, "rb") as f_in:
        header = f_in.read(4)
        if len(header) < 4:
            raise ValueError("File mã hóa không hợp lệ (thiếu header 4 byte).")
        start_frame = int.from_bytes(header, "big")
        encrypted = f_in.read()

    decrypted = crypt_bytes(encrypted, key_hex, start_frame)
    _write_chunks(out_path, b"", decrypted, progress)
