"""
tests/test_a51.py

Bộ kiểm thử chính cho hệ mã A5/1.

Người phụ trách:
Lại Hoàng Thế Vũ

Giả định giao diện của module src/a51.py:

    A51(key_bin, frame_int)

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

KEY_HEX = 0x1223456789ABCDEF

# Khóa K chuẩn hóa thành chuỗi nhị phân 64 bít.
KEY_BIN = f"{KEY_HEX:064b}"

FRAME = 0x134

# Số khung biểu diễn dưới dạng 22 bít.
FRAME_BIN = f"{FRAME:022b}"


# Theo bộ test vector được nhóm sử dụng.
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

    Kết quả:
    [0, 1, 0, 1, ...]
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
    Chuyển test vector dạng hexadecimal thành 114 bít.

    Test vector được lưu trong 15 byte:

        15 byte = 120 bít

    Trong đó chỉ 114 bít đầu có ý nghĩa.
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
    Chuyển văn bản thành danh sách bít UTF-8.

    Mỗi byte được biểu diễn bằng 8 bít.
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
    Sinh đủ keystream cho ca kiểm thử round-trip.

    Mỗi lần A5/1 sinh:

        114 bít Downlink
        114 bít Uplink

    Tổng:

        228 bít / frame

    Nếu dữ liệu dài hơn 228 bít thì sử dụng frame tiếp theo
    cho đến khi đủ số bít cần kiểm thử.
    """

    keystream = []

    current_frame = FRAME

    while len(keystream) < length:

        cipher = A51(
            KEY_BIN,
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

        # Chuyển sang frame tiếp theo.
        # Frame A5/1 có 22 bít.
        current_frame = (
            current_frame + 1
        ) % (1 << 22)

    return keystream[:length]


# ============================================================
# TEST 1
# KIỂM TRA TEST VECTOR A5/1
# ============================================================

def test_reference_gsm_vector():
    """
    Kiểm tra kết quả A5/1 với test vector tham chiếu.

    Key:
        0x1223456789ABCDEF

    Frame:
        0x134

    Expected Uplink:
        534EAA582FE8151AB6E1855A728C00

    Expected Downlink:
        24FD35A35D5FB6526D32F906DF1AC0
    """

    cipher = A51(
        KEY_BIN,
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
# KIỂM TRA ĐỘ DÀI DÒNG KHÓA
# ============================================================

def test_keystream_length():
    """
    Mỗi hướng phải sinh đúng 114 bít.
    """

    cipher = A51(
        KEY_BIN,
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
# KIỂM TRA DÒNG KHÓA CHỈ CHỨA BÍT 0 VÀ 1
# ============================================================

def test_keystream_is_binary():
    """
    Mọi phần tử của keystream phải là 0 hoặc 1.
    """

    cipher = A51(
        KEY_BIN,
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
# KIỂM TRA KEY VÀ FRAME ĐÃ ĐƯỢC CHUẨN HÓA
# ============================================================

def test_reference_input_lengths():
    """
    Kiểm tra dữ liệu test vector:

    Key:
        64 bít

    Frame:
        22 bít
    """

    assert len(KEY_BIN) == 64

    assert len(FRAME_BIN) == 22

    assert set(KEY_BIN).issubset(
        {"0", "1"}
    )

    assert set(FRAME_BIN).issubset(
        {"0", "1"}
    )


# ============================================================
# TEST 5
# ROUND-TRIP MÃ HÓA → GIẢI MÃ
# ============================================================

def test_text_round_trip_100_characters():
    """
    Kiểm tra tính đúng đắn của phép XOR:

        P → C → P'

    Sau khi mã hóa rồi giải mã bằng cùng keystream:

        P' == P

    Văn bản kiểm thử có đúng 100 ký tự ASCII.
    """

    plaintext = (
        "A5/1 round-trip test for NEU information "
        "security project. Encryption and decryption "
        "must recover original data."
    )

    # Chuẩn hóa đúng 100 ký tự.
    plaintext = plaintext[:100]

    plaintext = plaintext.ljust(
        100,
        " "
    )

    assert len(plaintext) == 100

    # Chuyển bản rõ sang bít.
    plaintext_bits = text_to_bits(
        plaintext
    )

    # Sinh đủ keystream.
    keystream = generate_test_keystream(
        len(plaintext_bits)
    )

    # Mã hóa:
    #
    # C = P XOR S
    ciphertext_bits = xor_bits(
        plaintext_bits,
        keystream
    )

    # Giải mã:
    #
    # P' = C XOR S
    recovered_bits = xor_bits(
        ciphertext_bits,
        keystream
    )

    # Kiểm tra dữ liệu sau giải mã
    # phải giống hoàn toàn bản rõ ban đầu.
    assert recovered_bits == plaintext_bits
