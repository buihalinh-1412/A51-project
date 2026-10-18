from src.a51 import A51

def _hex_to_key_bits(key_hex: str) -> list:
    if len(key_hex) != 16:
        raise ValueError("Khóa hex phải đúng 16 ký tự (64 bit).")
    try:
        val = int(key_hex, 16)
    except ValueError:
        raise ValueError("Khóa chứa ký tự hex không hợp lệ.")
    
    bits = []
    # Quét từ bit 63 lùi về 0 để lấy bit cao (MSB) trước
    for i in range(63, -1, -1):
        bits.append((val >> i) & 1)
    return bits

def _bits_to_bytes(bits: list) -> bytes:
    byte_list = bytearray()
    for i in range(0, len(bits), 8):
        byte_val = 0
        chunk = bits[i:i+8]
        for b in chunk:
            byte_val = (byte_val << 1) | b
        
        # Xử lý đoạn bit lẻ cuối cùng (nếu có)
        if len(chunk) < 8:
            byte_val <<= (8 - len(chunk))
        byte_list.append(byte_val)
    return bytes(byte_list)

def crypt_bytes(data: bytes, key_hex: str, start_frame: int = 0) -> bytes:
    key_bits = _hex_to_key_bits(key_hex)
    encrypted_blocks = bytearray()
    chunk_size = 57  

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        
        # Tính số khung cho đoạn hiện tại
        f1 = start_frame + 2 * (i // chunk_size)
        f2 = f1 + 1

        # Sinh dòng khóa từ 2 khung
        a5_1 = A51(key_bits, f1)
        down1, up1 = a5_1.generate_keystream()
        
        a5_2 = A51(key_bits, f2)
        down2, up2 = a5_2.generate_keystream()

        # Nối và ép về byte
        keystream_bits = down1 + up1 + down2 + up2
        keystream_bytes = _bits_to_bytes(keystream_bits)

        # XOR từng byte dữ liệu với byte dòng khóa
        encrypted_chunk = bytearray(b ^ keystream_bytes[j] for j, b in enumerate(chunk))
        encrypted_blocks.extend(encrypted_chunk)

    return bytes(encrypted_blocks)