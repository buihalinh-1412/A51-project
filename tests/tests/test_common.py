
"""Kiểm thử src/common.py (Trần Đại Lộc)."""
import pytest

from src.common import bits_to_text, text_to_bits, validate_binary_string, xor_bit_strings


def test_text_bits_round_trip_ascii_and_unicode():
    assert text_to_bits("H") == "01001000"
    for s in ("Hello GSM", "Xin chào A5/1 — ✓", ""):
        assert bits_to_text(text_to_bits(s)) == s


def test_xor_and_validate():
    assert xor_bit_strings("111", "100") == "011"
    assert xor_bit_strings("", "") == ""
    with pytest.raises(ValueError):
        xor_bit_strings("1", "10")
    with pytest.raises(ValueError):
        xor_bit_strings("1a", "10")
    assert validate_binary_string("0101", 4) and not validate_binary_string("")
    assert not validate_binary_string("0102") and not validate_binary_string("01", 3)


def test_bits_to_text_errors():
    with pytest.raises(ValueError):
        bits_to_text("101")
    with pytest.raises(ValueError):
        bits_to_text("0000000x")
