"""
tests/run_verification.py

Chạy đối chiếu độc lập A5/1 với test vector tham chiếu.

Người phụ trách:
Lại Hoàng Thế Vũ

Cách chạy:

    python tests/run_verification.py

Giả định giao diện của src/a51.py:

    A51(key_bin, frame_int)

và:

    generate_keystream()

trả về:

    (downlink_bits, uplink_bits)

Mỗi luồng gồm 114 bít.
"""

from pathlib import Path
import sys


# ============================================================
# THIẾT LẬP ĐƯỜNG DẪN PROJECT
# ============================================================

# Khi chạy:
#
#     python tests/run_verification.py
#
# Python bắt đầu từ thư mục tests/.
# Đoạn này thêm thư mục gốc project vào sys.path
# để có thể import src.a51.

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


from src.a51 import A51


# ============================================================
# TEST VECTOR THAM CHIẾU
# ============================================================

KEY_HEX = 0x1223456789ABCDEF

KEY_BIN = f"{KEY_HEX:064b}"

FRAME = 0x134


# Theo bộ test vector được sử dụng trong project.

EXPECTED_UPLINK_HEX = (
    "534EAA582FE8151AB6E1855A728C00"
)

EXPECTED_DOWNLINK_HEX = (
    "24FD35A35D5FB6526D32F906DF1AC0"
)


# ============================================================
# HÀM HỖ TRỢ
# ============================================================

def normalize_bits(bits):
    """
    Chuyển output về list[int].

    Hỗ trợ:
    - chuỗi "010101..."
    - list[int]
    - tuple[int]
    """

    if isinstance(bits, str):

        if any(
            bit not in "01"
            for bit in bits
        ):
            raise ValueError(
                "Keystream chỉ được chứa bít 0 hoặc 1."
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
        raise ValueError(
            "Keystream chỉ được chứa bít 0 hoặc 1."
        )

    return result


def reference_hex_to_114_bits(hex_string):
    """
    Chuyển test vector hexadecimal thành 114 bít.

    Chuỗi tham chiếu được lưu trong:

        15 byte = 120 bít

    Trong đó:

        114 bít đầu có ý nghĩa
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


def bits_114_to_hex(bits):
    """
    Chuyển 114 bít keystream thành dạng hexadecimal.

    114 bít được thêm 6 bít 0 ở cuối để tạo:

        120 bít = 15 byte

    Output được đóng gói MSB-first.
    """

    bits = normalize_bits(bits)

    if len(bits) != 114:
        raise ValueError(
            "Keystream phải có đúng 114 bít, "
            f"nhưng nhận được {len(bits)} bít."
        )

    bit_string = "".join(
        str(bit)
        for bit in bits
    )

    # Thêm 6 bít đệm.
    bit_string += "0" * 6

    hex_value = int(
        bit_string,
        2
    )

    return f"{hex_value:030X}"


def compare_stream(
    actual_bits,
    expected_hex
):
    """
    So sánh keystream thực tế với test vector tham chiếu.
    """

    actual_bits = normalize_bits(
        actual_bits
    )

    expected_bits = reference_hex_to_114_bits(
        expected_hex
    )

    different_bits = sum(
        actual != expected
        for actual, expected
        in zip(
            actual_bits,
            expected_bits
        )
    )

    is_match = (
        actual_bits
        == expected_bits
    )

    return (
        is_match,
        different_bits
    )


def print_stream_result(
    title,
    expected_hex,
    actual_bits
):
    """
    In kết quả đối chiếu cho một luồng.
    """

    actual_bits = normalize_bits(
        actual_bits
    )

    actual_hex = bits_114_to_hex(
        actual_bits
    )

    (
        is_match,
        different_bits
    ) = compare_stream(
        actual_bits,
        expected_hex
    )

    print(
        f"{title} (114 bit):"
    )

    print(
        f"  Chuan tham chieu : "
        f"{expected_hex}"
    )

    print(
        f"  Nhom tu cai dat  : "
        f"{actual_hex}"
    )

    if is_match:

        print(
            "  Ket luan         : "
            "[ KHOP 100% - MATCH ]"
        )

    else:

        difference_ratio = (
            different_bits
            / 114
        )

        print(
            "  Ket luan         : "
            "[ KHONG KHOP - MISMATCH ]"
        )

        print(
            f"  So bit khac      : "
            f"{different_bits}/114 "
            f"({difference_ratio:.2%})"
        )

    print()

    return is_match


# ============================================================
# CHẠY ĐỐI CHIẾU
# ============================================================

def main():
    """
    Chạy A5/1 với test vector chuẩn và in bảng đối chiếu.
    """

    cipher = A51(
        KEY_BIN,
        FRAME
    )

    # Theo giao diện src/a51.py:
    #
    # generate_keystream()
    #
    # trả về:
    #
    # (downlink_bits, uplink_bits)

    (
        downlink_bits,
        uplink_bits
    ) = cipher.generate_keystream()

    downlink_bits = normalize_bits(
        downlink_bits
    )

    uplink_bits = normalize_bits(
        uplink_bits
    )


    # ========================================================
    # KIỂM TRA ĐỘ DÀI
    # ========================================================

    if len(uplink_bits) != 114:

        raise ValueError(
            "Uplink phải có 114 bít, "
            f"nhưng nhận được "
            f"{len(uplink_bits)} bít."
        )

    if len(downlink_bits) != 114:

        raise ValueError(
            "Downlink phải có 114 bít, "
            f"nhưng nhận được "
            f"{len(downlink_bits)} bít."
        )


    # ========================================================
    # IN BẢNG
    # ========================================================

    print(
        "=" * 72
    )

    print(
        "           "
        "BANG DOI CHIEU TEST VECTOR CHUAN GSM (A5/1)"
    )

    print(
        "=" * 72
    )

    print(
        f"Khoa phien (Key)  : "
        f"0x{KEY_HEX:016X}"
    )

    print(
        f"So khung (Frame)  : "
        f"0x{FRAME:06X}"
    )

    print(
        "-" * 72
    )

    print()


    # ========================================================
    # UPLINK
    # ========================================================

    uplink_match = print_stream_result(
        "Luong Uplink",
        EXPECTED_UPLINK_HEX,
        uplink_bits
    )


    # ========================================================
    # DOWNLINK
    # ========================================================

    downlink_match = print_stream_result(
        "Luong Downlink",
        EXPECTED_DOWNLINK_HEX,
        downlink_bits
    )


    # ========================================================
    # KẾT LUẬN
    # ========================================================

    print(
        "=" * 72
    )

    if (
        uplink_match
        and downlink_match
    ):

        print(
            "KET QUA CUOI:"
        )

        print(
            "[ PASS - CA HAI LUONG "
            "DEU KHOP TEST VECTOR ]"
        )

        print(
            "=" * 72
        )

        return 0

    else:

        print(
            "KET QUA CUOI:"
        )

        print(
            "[ FAIL - CO LUONG "
            "KHONG KHOP TEST VECTOR ]"
        )

        print(
            "=" * 72
        )

        return 1


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    raise SystemExit(
        main()
    )
