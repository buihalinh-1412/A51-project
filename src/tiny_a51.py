"""
tiny_a51.py — Lõi hệ mã TinyA5/1 kèm cơ chế lưu vết (trace log).

Người phụ trách: Hoàng Yến Nhi (việc 2.2, Giai đoạn 2).

Đặc tả dùng để cài đặt (slide Chương 2, bản "Updated", trang 46–50;
docs/tiny_a51_specification.md):

- 3 thanh ghi X, Y, Z dài 6, 8, 9 bit (x0..x5, y0..y7, z0..z8) [trang 46].
- Khoá K 23 bit, phân bổ K -> XYZ: 6 bit đầu vào X, 8 bit tiếp vào Y,
  9 bit cuối vào Z; ký tự đầu của mỗi đoạn là chỉ số 0 [trang 46, 49].
- Mỗi bước sinh số [trang 47]:
    m = maj(x1, y3, z3)   (hàm chiếm đa số)
    nếu x1 = m thì quay X; nếu y3 = m thì quay Y; nếu z3 = m thì quay Z
    s_i = x5 XOR y7 XOR z8   (tính SAU khi quay)
- Quay một thanh ghi [trang 48]:
    X: t = x2 XOR x4 XOR x5;  xj = x(j-1) với j = 5..1;  x0 = t
    Y: t = y6 XOR y7;         yj = y(j-1) với j = 7..1;  y0 = t
    Z: t = z2 XOR z7 XOR z8;  zj = z(j-1) với j = 8..1;  z0 = t
- Mã hoá C = P XOR S; giải mã P = C XOR S [trang 47, 50].

Quy ước code (docs/coding_convention.md mục 5–8):
- Mỗi thanh ghi là list các số nguyên 0/1; phần tử [0] ứng với x0 của slide.
- Lõi KHÔNG dùng print() và KHÔNG dùng thư viện mật mã; chỉ xử lý dữ liệu và
  trả về kết quả hoặc nhật ký (trace). Phần in ra màn hình do demo_cli.py làm.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Hằng số lấy từ slide
# ---------------------------------------------------------------------------

KEY_LENGTH = 23

# Độ dài từng thanh ghi [slide trang 46]
REGISTER_SIZES = {"X": 6, "Y": 8, "Z": 9}

# Bit điều khiển quay (clocking bit): x1, y3, z3 [slide trang 47]
CLOCK_INDEX = {"X": 1, "Y": 3, "Z": 3}

# Các vị trí lấy ra để tính bit t (feedback taps) [slide trang 48]
TAPS = {"X": (2, 4, 5), "Y": (6, 7), "Z": (2, 7, 8)}

# Bit đầu ra: x5, y7, z8 (bit cuối mỗi thanh ghi) [slide trang 47]
OUTPUT_INDEX = {"X": 5, "Y": 7, "Z": 8}

REGISTER_NAMES = ("X", "Y", "Z")

# Dữ liệu ví dụ trên lớp [slide trang 49–50]
SLIDE_KEY = "10010101001110100110000"
SLIDE_PLAINTEXT = "111"



# ---------------------------------------------------------------------------
# 2. Hàm phụ trợ (thuần, không phụ thuộc trạng thái)
# ---------------------------------------------------------------------------

def _validate_bits(bits: str, name: str, length: int | None = None) -> str:
    """Kiểm tra chuỗi chỉ gồm ký tự '0'/'1' (và đúng độ dài nếu có yêu cầu).

    Trả về chính chuỗi đó (đã bỏ khoảng trắng) nếu hợp lệ, ngược lại ném ValueError.
    """
    if not isinstance(bits, str):
        raise ValueError(f"{name} phải là chuỗi nhị phân, nhận được {type(bits).__name__}")
    cleaned = bits.replace(" ", "")
    if cleaned == "" or any(ch not in "01" for ch in cleaned):
        raise ValueError(f"{name} chỉ được chứa ký tự 0 và 1, nhận được {bits!r}")
    if length is not None and len(cleaned) != length:
        raise ValueError(f"{name} phải dài đúng {length} bit, nhận được {len(cleaned)} bit")
    return cleaned


def majority(a: int, b: int, c: int) -> int:
    """Hàm chiếm đa số maj(a, b, c).

    Theo slide trang 47: nếu có từ hai bit 0 trở lên thì trả về 0, ngược lại trả về 1.
    """
    return 1 if (a + b + c) >= 2 else 0


def _bits_to_str(register: list[int]) -> str:
    """Đổi thanh ghi [1, 0, 0, ...] thành chuỗi '100...' để ghi vào trace."""
    return "".join(str(b) for b in register)


def _feedback_bit(register: list[int], taps: tuple[int, ...]) -> int:
    """Tính bit t = XOR các bit ở vị trí tap."""
    t = 0
    for index in taps:
        t ^= register[index]
    return t


def _rotate(register: list[int], taps: tuple[int, ...]) -> tuple[list[int], int]:
    """Quay một thanh ghi theo slide trang 48.

    1. Tính t từ các vị trí tap.
    2. Dịch: phần tử j nhận giá trị của phần tử j-1 (j từ cuối về 1),
       bit cuối cùng bị đẩy ra ngoài.
    3. Đưa t vào vị trí 0.

    Trả về (thanh ghi mới, t). Không sửa list đầu vào.
    """
    t = _feedback_bit(register, taps)
    new_register = [t] + register[:-1]
    return new_register, t


# ---------------------------------------------------------------------------
# 3. Lớp TinyA51
# ---------------------------------------------------------------------------

class TinyA51:
    """Bộ sinh dãy số ngẫu nhiên S (keystream) TinyA5/1.

    Ví dụ:
        >>> cipher = TinyA51("10010101001110100110000")
        >>> keystream, trace = cipher.generate_keystream(3)
        >>> keystream
        '100'
    """

    def __init__(self, key: str) -> None:
        """Tạo bộ sinh với khoá K 23 bit (chuỗi 23 ký tự '0'/'1')."""
        self.key = _validate_bits(key, "Khoá K", KEY_LENGTH)
        self.registers: dict[str, list[int]] = {}
        self.step_count = 0
        self.reset()

    # -- Khởi tạo ----------------------------------------------------------

    def reset(self) -> None:
        """Đưa 3 thanh ghi về trạng thái ban đầu nạp từ khoá (K -> XYZ)."""
        start = 0
        for name in REGISTER_NAMES:
            size = REGISTER_SIZES[name]
            segment = self.key[start:start + size]
            self.registers[name] = [int(ch) for ch in segment]
            start += size
        self.step_count = 0

    def get_state(self) -> dict[str, str]:
        """Trạng thái hiện tại dạng chuỗi, ví dụ {'X': '100101', ...}."""
        return {name: _bits_to_str(self.registers[name]) for name in REGISTER_NAMES}

    # -- Một bước sinh số -------------------------------------------------

    def step_with_trace(self) -> tuple[int, dict]:
        """Thực hiện một bước sinh số và trả về (bit s_i, bản ghi trace).

        Bản ghi trace có dạng:
        {
            "step": 0,
            "clock_bits": {"x1": 0, "y3": 0, "z3": 1},
            "majority": 0,
            "rotated_registers": ["X", "Y"],
            "feedback_bits": {"X": 1, "Y": 1},
            "state_before": {"X": "100101", "Y": "01001110", "Z": "100110000"},
            "state_after":  {"X": "110010", "Y": "10100111", "Z": "100110000"},
            "output_bit": 1
        }
        """
        state_before = self.get_state()

        # Bước 1: đọc 3 bit điều khiển quay và tính hàm chiếm đa số
        clock_values = {name: self.registers[name][CLOCK_INDEX[name]] for name in REGISTER_NAMES}
        m = majority(clock_values["X"], clock_values["Y"], clock_values["Z"])

        # Bước 2: thanh ghi nào có bit điều khiển bằng m thì quay
        rotated: list[str] = []
        feedback_bits: dict[str, int] = {}
        for name in REGISTER_NAMES:
            if clock_values[name] == m:
                self.registers[name], t = _rotate(self.registers[name], TAPS[name])
                rotated.append(name)
                feedback_bits[name] = t

        # Bước 3: tính bit sinh ra SAU khi quay: s_i = x5 XOR y7 XOR z8
        output_bit = (
            self.registers["X"][OUTPUT_INDEX["X"]]
            ^ self.registers["Y"][OUTPUT_INDEX["Y"]]
            ^ self.registers["Z"][OUTPUT_INDEX["Z"]]
        )

        record = {
            "step": self.step_count,
            "clock_bits": {
                "x1": clock_values["X"],
                "y3": clock_values["Y"],
                "z3": clock_values["Z"],
            },
            "majority": m,
            "rotated_registers": rotated,
            "feedback_bits": feedback_bits,
            "state_before": state_before,
            "state_after": self.get_state(),
            "output_bit": output_bit,
        }

        self.step_count += 1
        return output_bit, record

    # -- Sinh nhiều bit ----------------------------------------------------

    def generate_keystream(self, length: int) -> tuple[str, list[dict]]:
        """Sinh `length` bit dãy S tiếp theo.

        Trả về (dãy S dạng chuỗi '0'/'1', danh sách bản ghi trace từng bước).
        Gọi tiếp lần nữa sẽ sinh tiếp từ trạng thái hiện tại; muốn bắt đầu
        lại từ khoá thì gọi reset().
        """
        if not isinstance(length, int) or length < 0:
            raise ValueError("Số bit cần sinh phải là số nguyên không âm")
        bits: list[str] = []
        trace: list[dict] = []
        for _ in range(length):
            bit, record = self.step_with_trace()
            bits.append(str(bit))
            trace.append(record)
        return "".join(bits), trace
