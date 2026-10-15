"""
tests/test_a51.py

Bộ kiểm thử chính cho hệ mã A5/1.

Người phụ trách:
Lại Hoàng Thế Vũ

Giao diện của module src/a51.py:

    A51(key, frame)

và:

    generate_keystream()

trả về:

    (downlink_bits, uplink_bits)

Mỗi luồng gồm 114 bít.
"""

from src.a51 import A51


# ============================================================
# TEST VECTOR THAM CHIẾU
# ============================================================

# Khóa tham chiếu được giữ ở dạng hexadecimal để hiển thị.
KEY_HEX = "1223456789ABCDEF"

# src/a51.py xử lý khóa dạng bytes theo đúng quy ước:
# byte đầu tiên trước, trong mỗi byte nạp bít LSB trước.
KEY = bytes.fromhex(KEY_HEX)

FRAME = 0x134

# Số khung biểu diễn dưới dạng 22 bít.
FRAME_BIN = f"{FRAME:022b}"


# Test vector tham chiếu.
EXPECTED_UPLINK_HEX = "534EAA582FE8151AB6E1855A728C00"

EXPECTED_DOWNLINK_HEX = "24FD35A35D5FB6526D32F906DF1AC0"


# ============================================================
# HÀM HỖ TRỢ
# ============================================================

def normalize_bits(bits):
    """
    Chuẩn hóa dữ liệu bít về dạng list[int].

    Hỗ trợ:
    - chuỗi "010101..."
    - list[int]
    - tuple[int]
    """

    if isinstance(bits, str):

        if any(bit not in "01" for bit in bits):
            raise AssertionError(
                "Dãy bít chỉ được chứa ký tự 0 hoặc 1."
            )

        return [int(bit) for bit in bits]

    result = [int(bit) for bit in bits]

    if any(bit not in (0, 1) for bit in result):
        raise AssertionError(
            "Dãy bít chỉ được chứa giá trị 0 hoặc 1."
        )

    return result


def reference_hex_to_114_bits(hex_string):
    """
    Chuyển test vector hexadecimal thành 114 bít.

    Test vector được lưu trong 15 byte = 120 bít.
    Chỉ 114 bít đầu có ý nghĩa.
    6 bít cuối là phần đệm.
    """

    packed_bits = bin(
        int(hex_string, 16)
    )[2:].zfill(120)

    meaningful_bits = packed_bits[:114]

    return [
        int(bit)
        for bit in meaningful_bits
    ]


EXPECTED_UPLINK_BITS = reference_hex_to_114_bits(
    EXPECTED_UPLINK_HEX
)

EXPECTED_DOWNLINK_BITS = reference_hex_to_114_bits(
    EXPECTED_DOWNLINK_HEX
)


def text_to_bits(text):
    """
    Chuyển văn bản UTF-8 thành danh sách bít.
    """

    data = text.encode("utf-8")

    bits = []

    for byte in data:

        for shift in range(7, -1, -1):

            bit = (byte >> shift) & 1

            bits.append(bit)

    return bits


def xor_bits(data_bits, keystream_bits):
    """
    XOR dữ liệu với dãy bít sinh ra.
    """

    if len(data_bits) != len(keystream_bits):
        raise ValueError(
            "Dữ liệu và keystream phải có cùng độ dài."
        )

    return [
        data_bit ^ stream_bit
        for data_bit, stream_bit
        in zip(data_bits, keystream_bits)
    ]


def generate_test_keystream(length):
    """
    Sinh đủ keystream cho kiểm thử round-trip.

    Mỗi frame sinh:
        114 bít Downlink
        114 bít Uplink

    Tổng:
        228 bít
    """

    keystream = []

    current_frame = FRAME

    while len(keystream) < length:

        cipher = A51(
            KEY,
            current_frame
        )

        downlink_bits, uplink_bits = (
            cipher.generate_keystream()
        )

        downlink_bits = normalize_bits(
            downlink_bits
        )

        uplink_bits = normalize_bits(
            uplink_bits
        )

        keystream.extend(
            downlink_bits
        )

        keystream.extend(
            uplink_bits
        )

        # Frame có 22 bít.
        current_frame = (
            current_frame + 1
        ) % (1 << 22)

    return keystream[:length]


# ============================================================
# TEST 1
# TEST VECTOR THAM CHIẾU
# ============================================================

def test_reference_gsm_vector():
    """
    Kiểm tra A5/1 với test vector tham chiếu.

    Key:
        0x1223456789ABCDEF

    Frame:
        0x134
    """

    cipher = A51(
        KEY,
        FRAME
    )

    downlink_bits, uplink_bits = (
        cipher.generate_keystream()
    )

    downlink_bits = normalize_bits(
        downlink_bits
    )

    uplink_bits = normalize_bits(
        uplink_bits
    )

    assert uplink_bits == EXPECTED_UPLINK_BITS, (
        "Uplink không khớp với test vector tham chiếu."
    )

    assert downlink_bits == EXPECTED_DOWNLINK_BITS, (
        "Downlink không khớp với test vector tham chiếu."
    )


# ============================================================
# TEST 2
# KIỂM TRA ĐỘ DÀI KEYSTREAM
# ============================================================

def test_keystream_length():
    """
    Mỗi hướng phải sinh đúng 114 bít.
    """

    cipher = A51(
        KEY,
        FRAME
    )

    downlink_bits, uplink_bits = (
        cipher.generate_keystream()
    )

    downlink_bits = normalize_bits(
        downlink_bits
    )

    uplink_bits = normalize_bits(
        uplink_bits
    )

    assert len(downlink_bits) == 114

    assert len(uplink_bits) == 114


# ============================================================
# TEST 3
# KIỂM TRA KEYSTREAM CHỈ CHỨA 0 VÀ 1
# ============================================================

def test_keystream_is_binary():
    """
    Mọi phần tử của keystream phải là 0 hoặc 1.
    """

    cipher = A51(
        KEY,
        FRAME
    )

    downlink_bits, uplink_bits = (
        cipher.generate_keystream()
    )

    downlink_bits = normalize_bits(
        downlink_bits
    )

    uplink_bits = normalize_bits(
        uplink_bits
    )

    assert set(
        downlink_bits
    ).issubset({0, 1})

    assert set(
        uplink_bits
    ).issubset({0, 1})


# ============================================================
# TEST 4
# KIỂM TRA DỮ LIỆU TEST VECTOR
# ============================================================

def test_reference_input_lengths():
    """
    Khóa tham chiếu:
        8 byte = 64 bít

    Chuỗi hex:
        16 ký tự

    Frame:
        22 bít
    """

    assert len(KEY) == 8

    assert len(KEY_HEX) == 16

    assert len(FRAME_BIN) == 22

    assert set(FRAME_BIN).issubset(
        {"0", "1"}
    )


# ============================================================
# TEST 5
# ROUND-TRIP MÃ HÓA → GIẢI MÃ
# ============================================================

def test_text_round_trip_100_characters():
    """
    Kiểm tra:

        P → C → P'

    với:

        C  = P XOR S
        P' = C XOR S

    Kết quả yêu cầu:

        P' == P
    """

    plaintext = (
        "A5/1 round-trip test for NEU information "
        "security project. Encryption and decryption "
        "must recover original data."
    )

    plaintext = plaintext[:100]

    plaintext = plaintext.ljust(
        100,
        " "
    )

    assert len(plaintext) == 100

    plaintext_bits = text_to_bits(
        plaintext
    )

    keystream = generate_test_keystream(
        len(plaintext_bits)
    )

    ciphertext_bits = xor_bits(
        plaintext_bits,
        keystream
    )

    recovered_bits = xor_bits(
        ciphertext_bits,
        keystream
    )

    assert recovered_bits == plaintext_bits
