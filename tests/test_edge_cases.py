"""
tests/test_edge_cases.py  -  Các ca kiểm thử biên cho A5/1.
Người phụ trách: Lại Hoàng Thế Vũ.

1. Khóa không đủ 64 bít -> ValueError        2. Frame âm -> ValueError
3. Khóa toàn 0 / toàn 1 -> vẫn hoạt động     4. Hai khóa lệch 1 bít -> khác > 40% bít keystream
5. Cùng khóa + frame -> cùng keystream        6. Frame >= 2^22 -> ValueError; frame bool -> TypeError
"""
from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.a51 import A51

FRAME = 0x134
KEY_ALL_ZERO = "0" * 64
KEY_ALL_ONE = "1" * 64
REFERENCE_KEY_INT = 0x1223456789ABCDEF
REFERENCE_KEY_BIN = f"{REFERENCE_KEY_INT:064b}"   # chuỗi 64 ký tự 0/1 (K0 = ký tự đầu)


def normalize_bits(bits):
    result = [int(b) for b in bits]
    if any(b not in (0, 1) for b in result):
        raise AssertionError("Keystream chỉ được chứa giá trị 0 hoặc 1.")
    return result


def generate_full_keystream(key_bin, frame=FRAME):
    """228 bít = 114 Downlink + 114 Uplink của một frame."""
    downlink_bits, uplink_bits = A51(key_bin, frame).generate_keystream()
    downlink_bits, uplink_bits = normalize_bits(downlink_bits), normalize_bits(uplink_bits)
    assert len(downlink_bits) == 114, f"Downlink phải có 114 bít, nhận {len(downlink_bits)}."
    assert len(uplink_bits) == 114, f"Uplink phải có 114 bít, nhận {len(uplink_bits)}."
    return downlink_bits + uplink_bits


def flip_last_bit(key_bin):
    """Đảo đúng bít cuối của khóa 64 bít (dạng chuỗi 0/1)."""
    if len(key_bin) != 64:
        raise ValueError("Khóa phải có đúng 64 bít.")
    return key_bin[:-1] + ("1" if key_bin[-1] == "0" else "0")


def calculate_difference_ratio(stream_a, stream_b):
    if len(stream_a) != len(stream_b):
        raise ValueError("Hai keystream phải có cùng độ dài.")
    different_bits = sum(a != b for a, b in zip(stream_a, stream_b))
    return different_bits, different_bits / len(stream_a)


def test_short_key_raises_value_error():
    """Test 1: khóa 63 bít bị từ chối."""
    with pytest.raises(ValueError):
        A51("0" * 63, FRAME)


def test_negative_frame_raises_value_error():
    """Test 2: frame âm bị từ chối."""
    with pytest.raises(ValueError):
        A51(REFERENCE_KEY_BIN, -1)


def test_all_zero_key():
    """Test 3: khóa toàn 0 vẫn sinh đủ 228 bít 0/1."""
    keystream = generate_full_keystream(KEY_ALL_ZERO)
    assert len(keystream) == 228
    assert set(keystream).issubset({0, 1})


def test_all_one_key():
    """Test 4: khóa toàn 1 vẫn sinh đủ 228 bít 0/1."""
    keystream = generate_full_keystream(KEY_ALL_ONE)
    assert len(keystream) == 228
    assert set(keystream).issubset({0, 1})


def test_zero_and_one_keys_produce_different_keystreams():
    """Test 5: khóa toàn 0 và toàn 1 không sinh cùng keystream."""
    assert generate_full_keystream(KEY_ALL_ZERO) != generate_full_keystream(KEY_ALL_ONE)


def test_keys_differ_by_exactly_one_bit():
    """Test 6: hai khóa dùng cho avalanche khác nhau đúng 1 bít."""
    key_a = REFERENCE_KEY_BIN
    key_b = flip_last_bit(key_a)
    assert len(key_a) == len(key_b) == 64
    assert sum(a != b for a, b in zip(key_a, key_b)) == 1


def test_one_bit_key_change_has_high_sensitivity():
    """Test 7: avalanche - khóa lệch 1 bít, tỷ lệ bít keystream khác nhau phải > 40%."""
    key_a = REFERENCE_KEY_BIN
    key_b = flip_last_bit(key_a)
    different_bits, ratio = calculate_difference_ratio(
        generate_full_keystream(key_a, FRAME), generate_full_keystream(key_b, FRAME))
    assert ratio > 0.40, (f"\nĐộ nhạy khóa chưa đạt.\nSố bít khác nhau: {different_bits}/228\n"
                          f"Tỷ lệ: {ratio:.2%}\nYêu cầu: > 40%")


def test_same_key_and_frame_are_deterministic():
    """Test 8: cùng khóa + cùng frame -> cùng keystream."""
    stream_1 = generate_full_keystream(REFERENCE_KEY_BIN, FRAME)
    stream_2 = generate_full_keystream(REFERENCE_KEY_BIN, FRAME)
    # SỬA: assert này trước đây bị rơi nhầm vào cuối Test 10 (gây NameError)
    assert stream_1 == stream_2, "Cùng khóa và cùng frame phải sinh cùng một keystream."


def test_frame_too_large_raises_value_error():
    """Test 9: frame = 2^22 vượt giới hạn 22 bít."""
    with pytest.raises(ValueError):
        A51(REFERENCE_KEY_BIN, 1 << 22)


def test_boolean_frame_raises_type_error():
    """Test 10: True/False không phải số khung hợp lệ."""
    with pytest.raises(TypeError):
        A51(REFERENCE_KEY_BIN, True)
