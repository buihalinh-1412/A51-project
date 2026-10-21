from src.a51 import A51
from src.file_crypto import crypt_bytes, _bits_to_bytes


def test_crypt_bytes_khop_voi_a51():
    key, frame = "1223456789ABCDEF", 0x134
    # Mã hóa 57 byte 0 thì kết quả chính là dòng khóa của 2 khung
    ks = crypt_bytes(bytes(57), key, frame)
    down1, up1 = A51(key, frame).generate_keystream()
    down2, up2 = A51(key, frame + 1).generate_keystream()
    assert ks == _bits_to_bytes(down1 + up1 + down2 + up2)