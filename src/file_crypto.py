import os
import math
from src.a51 import A51

def _hex_to_key_bits(key_hex: str) -> list:
    """Kiểm tra khóa hex 16 ký tự (64 bit) và đổi thành list 64 bit."""
    if len(key_hex) != 16:
        raise ValueError("Khóa hex phải đúng 16 ký tự (64 bit).")
    try:
        val = int(key_hex, 16)
    except ValueError:
        raise ValueError("Khóa chứa ký tự hex không hợp lệ.")
    
    bits = []
    for i in range(63, -1, -1):
        bits.append((val >> i) & 1)
    return bits

def _bits_to_bytes(bits: list) -> bytes:
    """Gom mỗi 8 bit thành 1 byte (bit đầu là bit cao nhất)."""
    byte_list = bytearray()
    for i in range(0, len(bits), 8):
        byte_val = 0
        chunk = bits[i:i+8]
        for b in chunk:
            byte_val = (byte_val << 1) | b
        if len(chunk) < 8:
            byte_val <<= (8 - len(chunk))
        byte_list.append(byte_val)
    return bytes(byte_list)

def crypt_bytes(data: bytes, key_hex: str, start_frame: int = 0) -> bytes:
    """XOR dữ liệu với dòng khóa A5/1 theo từng đoạn 57 byte (2 khung/đoạn)."""
    key_bits = _hex_to_key_bits(key_hex)
    encrypted_blocks = bytearray()
    chunk_size = 57  

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        f1 = start_frame + 2 * (i // chunk_size)
        f2 = f1 + 1

        a5_1 = A51(key_bits, f1)
        down1, up1 = a5_1.generate_keystream()
        
        a5_2 = A51(key_bits, f2)
        down2, up2 = a5_2.generate_keystream()

        keystream_bits = down1 + up1 + down2 + up2
        keystream_bytes = _bits_to_bytes(keystream_bits)

        encrypted_chunk = bytearray(b ^ keystream_bytes[j] for j, b in enumerate(chunk))
        encrypted_blocks.extend(encrypted_chunk)

    return bytes(encrypted_blocks)

def encrypt_file(in_path: str, out_path: str, key_hex: str, start_frame: int = 0, progress=None):
    """Mã hóa file thật và ghi 4 byte đầu là start_frame."""
    if in_path == out_path:
        raise ValueError("File đầu vào và file đầu ra không được trùng nhau.")
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Không tìm thấy file nguồn: {in_path}")

    with open(in_path, "rb") as f:
        data = f.read()

    total_bytes = len(data)
    num_chunks = math.ceil(total_bytes / 57) if total_bytes > 0 else 0
    if start_frame + num_chunks * 2 > 2**22:
        raise ValueError("Số hiệu khung vượt quá giới hạn GSM (2^22 khung).")

    encrypted_data = crypt_bytes(data, key_hex, start_frame)
    header = start_frame.to_bytes(4, "big")

    with open(out_path, "wb") as f_out:
        f_out.write(header)
        chunk_size = 57
        for i in range(0, total_bytes, chunk_size):
            f_out.write(encrypted_data[i:i+chunk_size])
            if progress:
                progress(min(i + chunk_size, total_bytes), total_bytes)
        if total_bytes == 0 and progress:
            progress(0, 0)

def decrypt_file(in_path: str, out_path: str, key_hex: str, progress=None):
    """Đọc 4 byte đầu lấy start_frame và giải mã file."""
    if in_path == out_path:
        raise ValueError("File đầu vào và file đầu ra không được trùng nhau.")
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Không tìm thấy file mã hóa: {in_path}")

    with open(in_path, "rb") as f_in:
        header = f_in.read(4)
        if len(header) < 4:
            raise ValueError("File mã hóa không hợp lệ (thiếu header 4 byte).")
        start_frame = int.from_bytes(header, "big")
        encrypted_data = f_in.read()

    decrypted_data = crypt_bytes(encrypted_data, key_hex, start_frame)
    total_bytes = len(decrypted_data)

    with open(out_path, "wb") as f_out:
        chunk_size = 57
        for i in range(0, total_bytes, chunk_size):
            f_out.write(decrypted_data[i:i+chunk_size])
            if progress:
                progress(min(i + chunk_size, total_bytes), total_bytes)
        if total_bytes == 0 and progress:
            progress(0, 0)