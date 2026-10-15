"""
tests/test_edge_cases.py

Các ca kiểm thử biên (edge cases) cho A5/1.

Người phụ trách:
Lại Hoàng Thế Vũ

Các ca kiểm thử:
1. Khóa không đủ 64 bít -> phải raise ValueError.
2. Số khung (frame) âm -> phải raise ValueError.
3. Khóa toàn bít 0 -> thuật toán vẫn phải hoạt động.
4. Khóa toàn bít 1 -> thuật toán vẫn phải hoạt động.
5. Hai khóa chỉ khác nhau đúng 1 bít -> kiểm tra độ nhạy khóa
   (avalanche effect), tỷ lệ bít keystream khác nhau phải > 40%.

Giả định giao diện của module src/a51.py:

    A51(key_bin, frame_int)

và:

    generate_keystream()

trả về:

    (downlink_bits, uplink_bits)

Mỗi luồng gồm 114 bít.
"""

import pytest

from src.a51 import A51


# ============================================================
# DỮ LIỆU KIỂM THỬ
# ============================================================

FRAME = 0x134

# Khóa 64 bít toàn 0.
KEY_ALL_ZERO = "0" * 64

# Khóa 64 bít toàn 1.
KEY_ALL_ONE = "1" * 64

# Khóa tham chiếu.
REFERENCE_KEY_HEX = 0x1223456789ABCDEF

REFERENCE_KEY_BIN = f"{REFERENCE_KEY_HEX:064b}"


# ============================================================
# HÀM HỖ TRỢ
# ============================================================

def normalize_bits(bits):
    """
    Chuẩn hóa dữ liệu keystream về dạng list[int].

    Hỗ trợ:
    - chuỗi "010101..."
    - list[int]
    - tuple[int]

    Kết quả:

        [0, 1, 0, 1, ...]

    Hàm cũng kiểm tra bảo đảm mọi phần tử đều là bít 0 hoặc 1.
    """

    if isinstance(bits, str):

        if any(bit not in "01" for bit in bits):
            raise AssertionError(
                "Keystream dạng chuỗi chỉ được chứa ký tự 0 hoặc 1."
            )

        return [
            int(bit)
            for bit in bits
        ]

    result = [
        int(bit)
        for bit in bits
    ]

    if any(
        bit not in (0, 1)
        for bit in result
    ):
        raise AssertionError(
            "Keystream chỉ được chứa giá trị 0 hoặc 1."
        )

    return result


def generate_full_keystream(key_bin, frame=FRAME):
    """
    Sinh toàn bộ 228 bít keystream của một frame.

    generate_keystream() được giả định trả về:

        downlink_bits, uplink_bits

    Trong đó:

        Downlink = 114 bít
        Uplink   = 114 bít

    Hàm trả về:

        228 bít = Downlink + Uplink
    """

    cipher = A51(
        key_bin,
        frame
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

    # Kiểm tra độ dài từng luồng.
    assert len(downlink_bits) == 114, (
        f"Downlink phải có 114 bít, "
        f"nhưng nhận được {len(downlink_bits)} bít."
    )

    assert len(uplink_bits) == 114, (
        f"Uplink phải có 114 bít, "
        f"nhưng nhận được {len(uplink_bits)} bít."
    )

    return (
        downlink_bits
        + uplink_bits
    )


def flip_last_bit(key_bin):
    """
    Đảo đúng bít cuối cùng của khóa.

    Ví dụ:

        ...0 -> ...1

    hoặc:

        ...1 -> ...0
    """

    if len(key_bin) != 64:
        raise ValueError(
            "Khóa phải có đúng 64 bít."
        )

    last_bit = key_bin[-1]

    flipped_bit = (
        "1"
        if last_bit == "0"
        else "0"
    )

    return (
        key_bin[:-1]
        + flipped_bit
    )


def calculate_difference_ratio(stream_a, stream_b):
    """
    Tính tỷ lệ số bít khác nhau giữa hai keystream.

    Ví dụ:

        100 bít
        có 45 bít khác nhau

    thì:

        difference_ratio = 0.45
    """

    if len(stream_a) != len(stream_b):
        raise ValueError(
            "Hai keystream phải có cùng độ dài."
        )

    different_bits = sum(
        bit_a != bit_b
        for bit_a, bit_b
        in zip(stream_a, stream_b)
    )

    difference_ratio = (
        different_bits
        / len(stream_a)
    )

    return (
        different_bits,
        difference_ratio
    )


# ============================================================
# TEST 1
# KHÓA KHÔNG ĐỦ 64 BÍT
# ============================================================

def test_short_key_raises_value_error():
    """
    Khóa chỉ có 63 bít phải bị từ chối.

    Kết quả mong đợi:

        ValueError
    """

    invalid_key = "0" * 63

    assert len(invalid_key) == 63

    with pytest.raises(ValueError):

        A51(
            invalid_key,
            FRAME
        )


# ============================================================
# TEST 2
# SỐ KHUNG ÂM
# ============================================================

def test_negative_frame_raises_value_error():
    """
    Số khung âm không hợp lệ.

    Kết quả mong đợi:

        ValueError
    """

    invalid_frame = -1

    with pytest.raises(ValueError):

        A51(
            REFERENCE_KEY_BIN,
            invalid_frame
        )


# ============================================================
# TEST 3
# KHÓA TOÀN BÍT 0
# ============================================================

def test_all_zero_key():
    """
    Kiểm tra khóa gồm 64 bít 0.

    Thuật toán vẫn phải:

    - khởi tạo được;
    - sinh đủ 228 bít;
    - chỉ sinh các giá trị 0 hoặc 1.
    """

    assert len(KEY_ALL_ZERO) == 64

    keystream = generate_full_keystream(
        KEY_ALL_ZERO
    )

    assert len(keystream) == 228

    assert set(
        keystream
    ).issubset({0, 1})


# ============================================================
# TEST 4
# KHÓA TOÀN BÍT 1
# ============================================================

def test_all_one_key():
    """
    Kiểm tra khóa gồm 64 bít 1.

    Thuật toán vẫn phải:

    - khởi tạo được;
    - sinh đủ 228 bít;
    - chỉ sinh các giá trị 0 hoặc 1.
    """

    assert len(KEY_ALL_ONE) == 64

    keystream = generate_full_keystream(
        KEY_ALL_ONE
    )

    assert len(keystream) == 228

    assert set(
        keystream
    ).issubset({0, 1})


# ============================================================
# TEST 5
# SO SÁNH KHÓA TOÀN 0 VÀ TOÀN 1
# ============================================================

def test_zero_and_one_keys_produce_different_keystreams():
    """
    Khóa toàn 0 và khóa toàn 1 không được sinh ra
    cùng một keystream.
    """

    stream_zero = generate_full_keystream(
        KEY_ALL_ZERO
    )

    stream_one = generate_full_keystream(
        KEY_ALL_ONE
    )

    assert stream_zero != stream_one, (
        "Khóa toàn 0 và khóa toàn 1 "
        "không được sinh cùng một keystream."
    )


# ============================================================
# TEST 6
# HAI KHÓA CHỈ KHÁC ĐÚNG 1 BÍT
# ============================================================

def test_keys_differ_by_exactly_one_bit():
    """
    Tạo hai khóa:

        key_a = khóa tham chiếu
        key_b = key_a nhưng đảo bít cuối

    Sau đó kiểm tra đúng là chỉ có 1 bít khác nhau.
    """

    key_a = REFERENCE_KEY_BIN

    key_b = flip_last_bit(
        key_a
    )

    number_of_different_bits = sum(
        bit_a != bit_b
        for bit_a, bit_b
        in zip(key_a, key_b)
    )

    assert len(key_a) == 64

    assert len(key_b) == 64

    assert number_of_different_bits == 1, (
        "Hai khóa dùng cho kiểm thử avalanche "
        "phải khác nhau đúng 1 bít."
    )


# ============================================================
# TEST 7
# ĐỘ NHẠY KHÓA - AVALANCHE EFFECT
# ============================================================

def test_one_bit_key_change_has_high_sensitivity():
    """
    Kiểm tra độ nhạy khóa (avalanche effect).

    Hai khóa chỉ khác đúng một bít cuối.

    Theo yêu cầu của bài:

        số bít keystream khác nhau
        phải lớn hơn 40%.

    Keystream được so sánh:

        228 bít
        =
        114 Downlink
        +
        114 Uplink
    """

    # Khóa thứ nhất.
    key_a = REFERENCE_KEY_BIN

    # Khóa thứ hai chỉ khác đúng bít cuối.
    key_b = flip_last_bit(
        key_a
    )

    # Sinh keystream với cùng frame.
    stream_a = generate_full_keystream(
        key_a,
        FRAME
    )

    stream_b = generate_full_keystream(
        key_b,
        FRAME
    )

    # Tính tỷ lệ khác nhau.
    (
        different_bits,
        difference_ratio
    ) = calculate_difference_ratio(
        stream_a,
        stream_b
    )

    # Yêu cầu > 40%.
    assert difference_ratio > 0.40, (
        "\n"
        "Độ nhạy khóa chưa đạt yêu cầu.\n"
        f"Số bít khác nhau: "
        f"{different_bits}/228\n"
        f"Tỷ lệ khác nhau: "
        f"{difference_ratio:.2%}\n"
        "Yêu cầu: > 40%"
    )


# ============================================================
# TEST 8
# KIỂM TRA CÙNG KHÓA + CÙNG FRAME CHO CÙNG KẾT QUẢ
# ============================================================

def test_same_key_and_frame_are_deterministic():
    """
    Với cùng khóa và cùng số khung,
    A5/1 phải sinh cùng một keystream.

    Ca này kiểm tra tính xác định (deterministic)
    của implementation.
    """

    stream_1 = generate_full_keystream(
        REFERENCE_KEY_BIN,
        FRAME
    )

    stream_2 = generate_full_keystream(
        REFERENCE_KEY_BIN,
        FRAME
    )
# ============================================================
# TEST 9
# FRAME VƯỢT QUÁ GIỚI HẠN 22 BÍT
# ============================================================

def test_frame_too_large_raises_value_error():
    """
    Số khung của A5/1 có 22 bít.

    Giá trị hợp lệ:
        0 <= frame < 2^22

    Frame = 2^22 phải bị từ chối.
    """

    invalid_frame = 1 << 22

    with pytest.raises(ValueError):
        A51(
            REFERENCE_KEY_BIN,
            invalid_frame
        )


# ============================================================
# TEST 10
# FRAME DẠNG BOOL KHÔNG HỢP LỆ
# ============================================================

def test_boolean_frame_raises_type_error():
    """
    True và False không được coi là
    số khung hợp lệ.
    """

    with pytest.raises(TypeError):
        A51(
            REFERENCE_KEY_BIN,
            True
        )
    assert stream_1 == stream_2, (
        "Cùng khóa và cùng frame "
        "phải sinh cùng một keystream."
    )
