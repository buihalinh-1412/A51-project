import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.a51 import A51


KEY_HEX = "1223456789ABCDEF"
KEY = bytes.fromhex(KEY_HEX)

FRAME = 0x134

EXPECTED_DOWNLINK_HEX = "534EAA582FE8151AB6E1855A728C00"
EXPECTED_UPLINK_HEX = "24FD35A35D5FB6526D32F906DF1AC0"


def normalize_bits(bits):
    """Chuẩn hóa dữ liệu bit về list số nguyên 0/1."""
    return [int(bit) for bit in bits]


def reference_hex_to_114_bits(hex_string):
    """
    Đổi chuỗi hex 15 byte thành 114 bit có ý nghĩa.

    Test vector được đóng gói thành 120 bit,
    trong đó 6 bit cuối là padding.
    """
    raw = bytes.fromhex(hex_string)

    bits = []

    for byte in raw:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)

    return bits[:114]


def bits_to_reference_hex(bits):
    """
    Đóng gói 114 bit thành 15 byte giống định dạng test vector.

    Thêm 6 bit 0 ở cuối để đủ 120 bit.
    """
    bits = normalize_bits(bits)

    if len(bits) != 114:
        raise ValueError("Keystream phai co dung 114 bit.")

    padded = bits + [0] * 6

    output = bytearray()

    for index in range(0, len(padded), 8):
        value = 0

        for bit in padded[index:index + 8]:
            value = (value << 1) | bit

        output.append(value)

    return bytes(output).hex().upper()


def main():
    cipher = A51(KEY, FRAME)

    downlink_bits, uplink_bits = cipher.generate_keystream()

    expected_downlink_bits = reference_hex_to_114_bits(
        EXPECTED_DOWNLINK_HEX
    )

    expected_uplink_bits = reference_hex_to_114_bits(
        EXPECTED_UPLINK_HEX
    )

    downlink_match = (
        normalize_bits(downlink_bits)
        == expected_downlink_bits
    )

    uplink_match = (
        normalize_bits(uplink_bits)
        == expected_uplink_bits
    )

    actual_downlink_hex = bits_to_reference_hex(
        downlink_bits
    )

    actual_uplink_hex = bits_to_reference_hex(
        uplink_bits
    )

    separator = "=" * 72

    print(separator)
    print("BANG DOI CHIEU TEST VECTOR CHUAN GSM (A5/1)")
    print(separator)

    print(f"Khoa phien (Key) : 0x{KEY_HEX}")
    print(f"So khung (Frame) : 0x{FRAME:06X}")

    print()
    print("Luong Downlink (114 bit):")
    print(f"  Chuan tham chieu : {EXPECTED_DOWNLINK_HEX}")
    print(f"  Nhom tu cai dat  : {actual_downlink_hex}")
    print(
        "  Ket luan         : "
        + (
            "[ KHOP 100% - MATCH ]"
            if downlink_match
            else "[ KHONG KHOP - FAIL ]"
        )
    )

    print()
    print("Luong Uplink (114 bit):")
    print(f"  Chuan tham chieu : {EXPECTED_UPLINK_HEX}")
    print(f"  Nhom tu cai dat  : {actual_uplink_hex}")
    print(
        "  Ket luan         : "
        + (
            "[ KHOP 100% - MATCH ]"
            if uplink_match
            else "[ KHONG KHOP - FAIL ]"
        )
    )

    print()
    print(separator)

    if downlink_match and uplink_match:
        print("KET QUA CUOI: PASS")
        return 0

    print("KET QUA CUOI: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
