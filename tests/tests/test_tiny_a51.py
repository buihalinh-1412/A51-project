"""Bo kiem thu tu dong xac minh TinyA5/1 theo cac chu ky trong Slide."""
import pytest
from src.common import xor_bit_strings
from src.tiny_a51 import TinyA51
from src.tiny_a51 import TinyA51
KEY_SLIDE = "10010101001110100110000"
PLAINTEXT_SLIDE = "111"
EXPECTED_S = "100"
EXPECTED_C = "011"


def test_setup_structure():
    """Kiem tra khoi tao khung pytest va import module TinyA51."""
    cipher = TinyA51(KEY_SLIDE)
    assert cipher is not None
"""Bo kiem thu tu dong xac minh TinyA5/1 theo cac chu ky trong Slide."""
import pytest
from src.common import xor_bit_strings
from src.tiny_a51 import TinyA51

KEY_SLIDE = "10010101001110100110000"
PLAINTEXT_SLIDE = "111"
EXPECTED_S = "100"
EXPECTED_C = "011"


def test_slide_cycle_0_1_2():
    """Kiem tra doi chieu chinh xac tung buoc voi Slide 49-50."""
    cipher = TinyA51(KEY_SLIDE)
    keystream, trace = cipher.generate_keystream(3)

    # Bước 0: s_0 == 1, X == 110010, Y == 10100111
    assert trace[0]["output_bit"] == 1
    assert trace[0]["state_after"]["X"] == "110010"
    assert trace[0]["state_after"]["Y"] == "10100111"

    # Bước 1: s_1 == 0, X == 111001, Z == 010011000
    assert trace[1]["output_bit"] == 0
    assert trace[1]["state_after"]["X"] == "111001"
    assert trace[1]["state_after"]["Z"] == "010011000"

    # Bước 2: s_2 == 0, Y == 01010011
    assert trace[2]["output_bit"] == 0
    assert trace[2]["state_after"]["Y"] == "01010011"
  def test_round_trip():
    """Kiem tra P = 111 -> C = 011 -> P = 111 voi dong khoa S = 100."""
    cipher = TinyA51(KEY_SLIDE)
    keystream, _ = cipher.generate_keystream(3)
    assert keystream == EXPECTED_S

    # Ma hoa: C = P XOR S
    ciphertext = xor_bit_strings(PLAINTEXT_SLIDE, keystream)
    assert ciphertext == EXPECTED_C

    # Giai ma: P = C XOR S
    decrypted = xor_bit_strings(ciphertext, keystream)
    assert decrypted == PLAINTEXT_SLIDE
    def test_extended_keystream_50_bits():
    """Kiem tra sinh dong khoa 50 bit va kiem tra tinh nhat quan."""
    cipher = TinyA51(KEY_SLIDE)
    keystream, trace = cipher.generate_keystream(50)
    assert len(keystream) == 50
    assert len(trace) == 50
    assert all(bit in "01" for bit in keystream)
