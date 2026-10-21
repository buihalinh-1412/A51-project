"""Bộ kiểm thử tự động TinyA5/1 đối chiếu slide Chương 2 (trang 49-50).
Người phụ trách: Trần Đại Lộc.   Chạy: pytest tests/test_tiny_a51.py -v
Lưu ý TD-002: slide trang 50 in Z sau Bước 2 = 101001100 là lỗi in; theo quy tắc quay
(t = z2^z7^z8 = 0) giá trị đúng là 001001100, test dùng giá trị đúng.
"""
import pytest

from src.common import xor_bit_strings
from src.tiny_a51 import TinyA51

KEY_SLIDE = "10010101001110100110000"
PLAINTEXT_SLIDE = "111"
EXPECTED_S = "100"
EXPECTED_C = "011"


@pytest.fixture
def cipher():
    return TinyA51(KEY_SLIDE)


def test_setup_structure(cipher):
    assert cipher.get_state() == {"X": "100101", "Y": "01001110", "Z": "100110000"}


def test_slide_cycle_0_1_2(cipher):
    keystream, trace = cipher.generate_keystream(3)
    # Chu kỳ 0: m=0, quay X,Y; s0=1
    assert trace[0]["majority"] == 0 and trace[0]["rotated_registers"] == ["X", "Y"]
    assert trace[0]["output_bit"] == 1
    assert trace[0]["state_after"] == {"X": "110010", "Y": "10100111", "Z": "100110000"}
    # Chu kỳ 1: m=1, quay X,Z; s1=0
    assert trace[1]["majority"] == 1 and trace[1]["rotated_registers"] == ["X", "Z"]
    assert trace[1]["output_bit"] == 0
    assert trace[1]["state_after"] == {"X": "111001", "Y": "10100111", "Z": "010011000"}
    # Chu kỳ 2: m=0, quay Y,Z; s2=0; Z đúng theo quy tắc = 001001100 (slide in sai, TD-002)
    assert trace[2]["majority"] == 0 and trace[2]["rotated_registers"] == ["Y", "Z"]
    assert trace[2]["output_bit"] == 0
    assert trace[2]["state_after"] == {"X": "111001", "Y": "01010011", "Z": "001001100"}
    assert keystream == EXPECTED_S


def test_z_step2_follows_rule_not_slide_typo(cipher):
    _, trace = cipher.generate_keystream(3)
    assert trace[2]["state_after"]["Z"] == "001001100"
    assert trace[2]["state_after"]["Z"] != "101001100"


def test_round_trip_with_xor_helper(cipher):
    keystream, _ = cipher.generate_keystream(3)
    assert keystream == EXPECTED_S
    ciphertext = xor_bit_strings(PLAINTEXT_SLIDE, keystream)
    assert ciphertext == EXPECTED_C
    assert xor_bit_strings(ciphertext, keystream) == PLAINTEXT_SLIDE


def test_encrypt_decrypt_api(cipher):
    assert cipher.encrypt(PLAINTEXT_SLIDE) == EXPECTED_C
    assert cipher.keystream == EXPECTED_S
    assert cipher.decrypt(EXPECTED_C) == PLAINTEXT_SLIDE


def test_extended_keystream_50_bits(cipher):
    keystream, trace = cipher.generate_keystream(50)
    assert len(keystream) == 50 and len(trace) == 50
    assert set(keystream) <= {"0", "1"}
    assert keystream.startswith(EXPECTED_S)
    assert [r["step"] for r in trace] == list(range(50))
    assert all(len(r["rotated_registers"]) >= 2 for r in trace)  # luôn >= 2 thanh ghi quay


def test_extended_keystream_is_consistent():
    ref, _ = TinyA51(KEY_SLIDE).generate_keystream(50)
    # cùng khoá -> cùng dãy S
    assert TinyA51(KEY_SLIDE).generate_keystream(50)[0] == ref
    # sinh một lần 50 bit == sinh 3 bit rồi 47 bit tiếp theo
    c = TinyA51(KEY_SLIDE)
    assert c.generate_keystream(3)[0] + c.generate_keystream(47)[0] == ref
    # reset() quay lại đầu dãy
    c.reset()
    assert c.generate_keystream(50)[0] == ref
    # mã hoá/giải mã 50 bit khôi phục bản rõ
    p = "10" * 25
    assert TinyA51(KEY_SLIDE).decrypt(TinyA51(KEY_SLIDE).encrypt(p)) == p


@pytest.mark.parametrize("bad", ["", "1010", "1" * 24, "2" * 23])
def test_invalid_key_rejected(bad):
    with pytest.raises(ValueError):
        TinyA51(bad)
