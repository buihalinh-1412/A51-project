"""tests/test_a51.py - Bộ kiểm thử chính cho hệ mã A5/1 (bản chỉnh theo rà soát GĐ2).
Người phụ trách: Lại Hoàng Thế Vũ.

Giao diện src/a51.py:  A51(key, frame).generate_keystream() -> (downlink_bits, uplink_bits)
Mỗi luồng 114 bít: 114 bít ĐẦU = Downlink, 114 bít SAU = Uplink.
Dữ liệu dài (TD-005): nối các khung liên tiếp frame, frame+1, ...; mỗi khung lấy 114 bít
của MỘT hướng (mặc định Downlink), đóng gói MSB-first (giống A51.encrypt_bytes và demo_cli).
"""
from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:       # để `pytest tests/` chạy được ở mọi nơi
    sys.path.insert(0, str(PROJECT_ROOT))

from src.a51 import A51

# ------------------------- TEST VECTOR THAM CHIẾU (Briceno) -------------------------
KEY_HEX = "1223456789ABCDEF"
KEY = bytes.fromhex(KEY_HEX)         # byte đầu trước, mỗi byte LSB-first
FRAME = 0x134
FRAME_BIN = f"{FRAME:022b}"

EXPECTED_DOWNLINK_HEX = "534EAA582FE8151AB6E1855A728C00"   # 114 bít đầu
EXPECTED_UPLINK_HEX = "24FD35A35D5FB6526D32F906DF1AC0"     # 114 bít sau


# ------------------------------ HÀM HỖ TRỢ ------------------------------
def normalize_bits(bits):
    result = [int(b) for b in bits]
    if any(b not in (0, 1) for b in result):
        raise AssertionError("Dãy bít chỉ được chứa giá trị 0 hoặc 1.")
    return result


def reference_hex_to_114_bits(hex_string):
    """15 byte = 120 bít; chỉ 114 bít đầu có nghĩa."""
    return [int(b) for b in bin(int(hex_string, 16))[2:].zfill(120)[:114]]


EXPECTED_DOWNLINK_BITS = reference_hex_to_114_bits(EXPECTED_DOWNLINK_HEX)
EXPECTED_UPLINK_BITS = reference_hex_to_114_bits(EXPECTED_UPLINK_HEX)


def text_to_bits(text):
    """Văn bản UTF-8 -> danh sách bít (MSB trước)."""
    return [(byte >> s) & 1 for byte in text.encode("utf-8") for s in range(7, -1, -1)]


def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        v = 0
        for b in bits[i:i + 8]:
            v = (v << 1) | b
        out.append(v)
    return bytes(out)


def reference_keystream_bytes(nbytes, key=KEY, first_frame=FRAME, use_uplink=False):
    """Oracle độc lập: ghép thủ công 114 bít/khung của các khung liên tiếp, đóng gói MSB-first.
    Chỉ dùng generate_keystream() của lõi, KHÔNG dùng keystream_bytes()/encrypt_bytes()."""
    bits, frame = [], first_frame
    while len(bits) < nbytes * 8:
        down, up = A51(key, frame).generate_keystream()
        bits.extend(normalize_bits(up if use_uplink else down))
        frame += 1
    return bits_to_bytes(bits[:nbytes * 8])


# ------------------------------ CÁC TEST ------------------------------
def test_reference_gsm_vector():
    """Test 1: đối chiếu test vector chuẩn (Key 0x1223456789ABCDEF, Frame 0x134)."""
    downlink_bits, uplink_bits = A51(KEY, FRAME).generate_keystream()
    assert normalize_bits(downlink_bits) == EXPECTED_DOWNLINK_BITS, "Downlink không khớp test vector."
    assert normalize_bits(uplink_bits) == EXPECTED_UPLINK_BITS, "Uplink không khớp test vector."


def test_keystream_length():
    """Test 2: mỗi hướng đúng 114 bít."""
    downlink_bits, uplink_bits = A51(KEY, FRAME).generate_keystream()
    assert len(downlink_bits) == 114
    assert len(uplink_bits) == 114


def test_keystream_is_binary():
    """Test 3: keystream chỉ chứa 0 và 1."""
    downlink_bits, uplink_bits = A51(KEY, FRAME).generate_keystream()
    assert set(normalize_bits(downlink_bits)).issubset({0, 1})
    assert set(normalize_bits(uplink_bits)).issubset({0, 1})


def test_downlink_uplink_frames_are_different_streams():
    """Test 4: Downlink khác Uplink; hai khung kế tiếp cho keystream khác nhau;
    use_uplink=True chọn đúng luồng Uplink."""
    down, up = A51(KEY, FRAME).generate_keystream()
    assert down != up
    assert A51(KEY, FRAME).generate_keystream() != A51(KEY, FRAME + 1).generate_keystream()
    assert A51(KEY, FRAME).encrypt_bits([0] * 114, use_uplink=True) == up
    assert A51(KEY, FRAME).encrypt_bits([0] * 114) == down      # mặc định Downlink


def test_text_round_trip_100_characters():
    """Test 5: P -> C -> P' với văn bản đúng 100 ký tự, dùng API mã hoá của lõi (nhiều khung)."""
    plaintext = ("A5/1 round-trip test for NEU information security project. "
                 "Encryption and decryption must recover original data.")
    plaintext = plaintext[:100].ljust(100, " ")
    assert len(plaintext) == 100
    data = plaintext.encode("utf-8")
    ciphertext = A51(KEY, FRAME).encrypt_bytes(data)
    assert ciphertext != data and len(ciphertext) == len(data)
    assert A51(KEY, FRAME).decrypt_bytes(ciphertext).decode("utf-8") == plaintext
    # đối chiếu với oracle độc lập (ghép tay các khung)
    keystream = reference_keystream_bytes(len(data))
    assert ciphertext == bytes(d ^ k for d, k in zip(data, keystream))


def test_key_hex_string_equals_bytes():
    """Test 6: khóa dạng chuỗi hex (có/không '0x') cho cùng keystream với dạng bytes."""
    expected = A51(KEY, FRAME).generate_keystream()
    assert A51(KEY_HEX, FRAME).generate_keystream() == expected
    assert A51("0x" + KEY_HEX, FRAME).generate_keystream() == expected


def test_binary_key_convention_matches_hex():
    """Test 7 (TD-003): chuỗi 64 ký tự 0/1 có K0 ở ĐẦU; muốn khớp khoá hex Briceno phải đảo bít
    trong từng byte (LSB-first). Dạng nhị phân 'thẳng' của số 0x1223... là KHOÁ KHÁC."""
    key_bin = "".join(f"{b:08b}"[::-1] for b in KEY)
    assert A51(key_bin, FRAME).generate_keystream() == A51(KEY, FRAME).generate_keystream()
    naive_bin = f"{int(KEY_HEX, 16):064b}"
    assert A51(naive_bin, FRAME).generate_keystream() != A51(KEY, FRAME).generate_keystream()


def test_core_encrypt_decrypt_bytes_round_trip():
    """Test 8: encrypt_bytes / decrypt_bytes khôi phục đúng bản rõ (nhiều khung)."""
    data = bytes(range(256)) * 2          # 512 byte = 4096 bít > 114 bít/khung
    cipher_text = A51(KEY, FRAME).encrypt_bytes(data)
    assert cipher_text != data and len(cipher_text) == len(data)
    assert A51(KEY, FRAME).decrypt_bytes(cipher_text) == data


def test_core_keystream_bytes_matches_independent_oracle():
    """Test 9 (TD-005): keystream_bytes == ghép tay 114 bít/khung; kiểm cả độ dài không chia hết
    cho 57 byte và hướng Uplink."""
    for nbytes in (1, 15, 57, 58, 100, 400):
        assert A51(KEY, FRAME).keystream_bytes(nbytes) == reference_keystream_bytes(nbytes)
    assert A51(KEY, FRAME).keystream_bytes(60, use_uplink=True) == \
        reference_keystream_bytes(60, use_uplink=True)


def test_core_encrypt_decrypt_bits_round_trip():
    """Test 10: encrypt_bits / decrypt_bits trên một khung (<= 114 bít)."""
    bits = text_to_bits("A5/1 test")      # 72 bít
    cipher_bits = A51(KEY, FRAME).encrypt_bits(bits)
    assert cipher_bits != bits
    assert A51(KEY, FRAME).decrypt_bits(cipher_bits) == bits


def test_one_frame_limit_and_frame_wraparound_guard():
    """Test 11 (TD-005): >114 bít trong một khung bị từ chối; dữ liệu làm số khung vượt 2^22 bị từ chối."""
    with pytest.raises(ValueError):
        A51(KEY, FRAME).encrypt_bits([0] * 115)
    with pytest.raises(ValueError):
        A51(KEY, (1 << 22) - 1).keystream_bytes(30)      # cần 3 khung, chỉ còn 1
    assert len(A51(KEY, (1 << 22) - 1).keystream_bytes(14)) == 14   # vừa đủ 1 khung
