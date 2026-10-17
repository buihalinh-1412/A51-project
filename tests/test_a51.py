"""Kiểm thử A5/1 đầy đủ. Chạy: pytest tests/test_a51.py -v"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.a51 import A51, bits_to_hex  # noqa: E402

KEY = "0x1223456789ABCDEF"
FRAME = 0x134
# Test vector: Marc Briceno (cài đặt tham chiếu A5/1), keystream đóng gói MSB-first
EXPECTED_DOWN = "534EAA582FE8151AB6E1855A728C00"
EXPECTED_UP = "24FD35A35D5FB6526D32F906DF1AC0"


def test_reference_vector():
    d, u = A51(KEY, FRAME).generate_keystream()
    assert len(d) == len(u) == 114
    assert bits_to_hex(d) == EXPECTED_DOWN
    assert bits_to_hex(u) == EXPECTED_UP


def test_key_formats_equivalent():
    ref = A51(KEY, FRAME).generate_keystream()
    assert A51("1223456789abcdef", FRAME).generate_keystream() == ref
    assert A51(bytes.fromhex("1223456789ABCDEF"), FRAME).generate_keystream() == ref


def test_bits_roundtrip():
    p = [1, 0, 1, 1, 0, 0, 1] * 16
    c = A51(KEY, 5).encrypt_bits(p)
    assert c != p
    assert A51(KEY, 5).decrypt_bits(c) == p


def test_text_roundtrip_100_chars():
    text = ("An toan va bao mat thong tin - A5/1 " * 4)[:100].encode()
    c = A51(KEY, 0).encrypt_bytes(text)
    assert c != text and len(c) == 100
    assert A51(KEY, 0).decrypt_bytes(c) == text


def test_binary_file_roundtrip_multi_frame():
    data = bytes(range(256)) * 10          # 2560 byte -> nhiều khung
    c = A51(KEY, 1000).encrypt_bytes(data)
    assert A51(KEY, 1000).decrypt_bytes(c) == data


def test_empty_data():
    assert A51(KEY).encrypt_bytes(b"") == b""


@pytest.mark.parametrize("bad_key", [
    "12", "0x123456789ABCDEF", "1223456789ABCDEF00", "ZZ23456789ABCDEF", b"\x00" * 7, [0] * 63,
])
def test_bad_key_raises(bad_key):
    with pytest.raises(ValueError):
        A51(bad_key, 0)


@pytest.mark.parametrize("bad_frame", [-1, 1 << 22, "101", [0] * 21])
def test_bad_frame_raises(bad_frame):
    with pytest.raises(ValueError):
        A51(KEY, bad_frame)


def test_frame_limit_raises():
    with pytest.raises(ValueError):
        A51(KEY, (1 << 22) - 1).keystream_bytes(100)


def test_too_many_bits_one_frame():
    with pytest.raises(ValueError):
        A51(KEY).encrypt_bits([0] * 115)


def test_all_zero_key_and_frame_is_degenerate():
    """Khoá 0 + khung 0: 3 thanh ghi toàn 0 -> keystream toàn 0 (điểm yếu đặc trưng)."""
    d, u = A51("0x" + "00" * 8, 0).generate_keystream()
    assert set(d) | set(u) == {0}


@pytest.mark.parametrize("key,frame", [("0x" + "00" * 8, 1), ("0x" + "FF" * 8, 0)])
def test_extreme_keys_not_degenerate(key, frame):
    d, u = A51(key, frame).generate_keystream()
    assert len(d) == 114 and (set(d) | set(u)) == {0, 1}


def test_key_avalanche_over_40_percent():
    a = A51("0x1223456789ABCDEF", FRAME).generate_keystream()[0]
    b = A51("0x1223456789ABCDEE", FRAME).generate_keystream()[0]
    diff = sum(x != y for x, y in zip(a, b)) / 114
    assert diff > 0.40


def test_different_frames_differ():
    assert A51(KEY, 1).generate_keystream() != A51(KEY, 2).generate_keystream()
