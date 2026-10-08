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

import copy

# ---------------------------------------------------------------------------
# 1. Hằng số lấy từ slide (tên theo bảng ánh xạ ký hiệu trong
#    docs/tiny_a51_specification.md; chỉ số bắt đầu từ 0 như slide)
# ---------------------------------------------------------------------------

KEY_LENGTH = 23

# Độ dài các thanh ghi X, Y, Z [slide trang 46]
LENGTH_X, LENGTH_Y, LENGTH_Z = 6, 8, 9

# Vị trí bit điều khiển quay (clocking bit): x1, y3, z3 [slide trang 47]
CLOCK_INDEX_X, CLOCK_INDEX_Y, CLOCK_INDEX_Z = 1, 3, 3

# Các vị trí lấy ra để tính bit t (feedback bit) [slide trang 48]
TAPS_X, TAPS_Y, TAPS_Z = (2, 4, 5), (6, 7), (2, 7, 8)

# Vị trí bit đầu ra: x5, y7, z8 (bit cuối mỗi thanh ghi) [slide trang 47]
OUTPUT_INDEX_X, OUTPUT_INDEX_Y, OUTPUT_INDEX_Z = 5, 7, 8

# Dữ liệu ví dụ trên lớp [slide trang 49–50]
SLIDE_KEY = "10010101001110100110000"
SLIDE_PLAINTEXT = "111"

# Giá trị slide in ra khác với kết quả tính theo quy tắc (TD-002).
# Slide trang 50 ghi Z sau Bước 2 là 101001100; tính theo công thức
# t = z2 XOR z7 XOR z8 = 0 thì Z phải là 001001100.
SLIDE_RECORDED_MISMATCH = {
    2: {"register": "Z", "slide_value": "101001100", "slide_page": 50},
}


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
        >>> cipher.encrypt("111")
        '011'
    """

    def __init__(self, key: str, annotate_slide: bool = False) -> None:
        """Tạo bộ sinh với khoá K 23 bit.

        key: chuỗi 23 ký tự '0'/'1'.
        annotate_slide: nếu True, trace sẽ ghi chú thêm các bước mà slide
            in giá trị khác kết quả tính theo quy tắc (chỉ áp dụng khi khoá
            đúng là khoá ví dụ trên lớp). Không làm thay đổi kết quả tính.
        """
        self.key = _validate_bits(key, "Khoá K", KEY_LENGTH)
        self.annotate_slide = annotate_slide
        self.register_x: list[int] = []
        self.register_y: list[int] = []
        self.register_z: list[int] = []
        self.step_count = 0
        self.keystream = ""   # dãy S của lần mã hoá/giải mã gần nhất
        self.last_trace: list[dict] = []
        self.reset()

    # -- Khởi tạo ----------------------------------------------------------

    def reset(self) -> None:
        """Nạp khoá K -> XYZ: 6 bit đầu vào X, 8 bit tiếp vào Y, 9 bit cuối vào Z."""
        bits = [int(ch) for ch in self.key]
        self.register_x = bits[:LENGTH_X]
        self.register_y = bits[LENGTH_X:LENGTH_X + LENGTH_Y]
        self.register_z = bits[LENGTH_X + LENGTH_Y:]
        self.step_count = 0

    def get_state(self) -> dict[str, str]:
        """Trạng thái hiện tại dạng chuỗi, ví dụ {'X': '100101', ...}."""
        return {
            "X": _bits_to_str(self.register_x),
            "Y": _bits_to_str(self.register_y),
            "Z": _bits_to_str(self.register_z),
        }

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

        # Bước 1: đọc 3 bit điều khiển quay x1, y3, z3 và tính m = maj(x1, y3, z3)
        clock_x = self.register_x[CLOCK_INDEX_X]
        clock_y = self.register_y[CLOCK_INDEX_Y]
        clock_z = self.register_z[CLOCK_INDEX_Z]
        majority_bit = majority(clock_x, clock_y, clock_z)

        # Bước 2: thanh ghi nào có bit điều khiển bằng m thì quay
        rotated: list[str] = []
        feedback_bits: dict[str, int] = {}
        if clock_x == majority_bit:
            self.register_x, t = _rotate(self.register_x, TAPS_X)
            rotated.append("X")
            feedback_bits["X"] = t
        if clock_y == majority_bit:
            self.register_y, t = _rotate(self.register_y, TAPS_Y)
            rotated.append("Y")
            feedback_bits["Y"] = t
        if clock_z == majority_bit:
            self.register_z, t = _rotate(self.register_z, TAPS_Z)
            rotated.append("Z")
            feedback_bits["Z"] = t

        # Bước 3: tính bit sinh ra SAU khi quay: s_i = x5 XOR y7 XOR z8
        s_i = (
            self.register_x[OUTPUT_INDEX_X]
            ^ self.register_y[OUTPUT_INDEX_Y]
            ^ self.register_z[OUTPUT_INDEX_Z]
        )

        record = {
            "step": self.step_count,
            "clock_bits": {"x1": clock_x, "y3": clock_y, "z3": clock_z},
            "majority": majority_bit,
            "rotated_registers": rotated,
            "feedback_bits": feedback_bits,
            "state_before": state_before,
            "state_after": self.get_state(),
            "output_bit": s_i,
        }
        self._add_slide_note(record)

        self.step_count += 1
        return s_i, record

    def _add_slide_note(self, record: dict) -> None:
        """Ghi chú chỗ slide in khác kết quả tính (chỉ khi bật annotate_slide)."""
        if not self.annotate_slide or self.key != SLIDE_KEY:
            return
        info = SLIDE_RECORDED_MISMATCH.get(record["step"])
        if info is None:
            return
        register_name = info["register"]
        computed = record["state_after"][register_name]
        if computed != info["slide_value"]:
            record["slide_mismatch"] = {
                "register": register_name,
                "computed": computed,
                "slide": info["slide_value"],
                "slide_page": info["slide_page"],
                "affects_output": False,  # s_i dùng z8, cả hai giá trị đều có z8 = 0
                "note": "Slide ghi khác kết quả tính theo quy tắc quay (xem TD-002).",
            }

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
            keystream_bit, record = self.step_with_trace()
            bits.append(str(keystream_bit))
            trace.append(record)
        return "".join(bits), trace

    # -- Mã hoá / giải mã -------------------------------------------------

    def _xor_with_keystream(self, data: str, name: str) -> str:
        """XOR chuỗi bit với dãy S sinh mới từ khoá (dùng chung cho 2 chiều)."""
        bits = _validate_bits(data, name)
        self.reset()  # luôn bắt đầu từ trạng thái nạp khoá
        keystream, trace = self.generate_keystream(len(bits))
        self.keystream = keystream
        self.last_trace = trace
        return "".join(str(int(a) ^ int(b)) for a, b in zip(bits, keystream))

    def encrypt(self, plaintext: str) -> str:
        """Mã hoá: C = P XOR S. Trace của lần chạy lưu ở self.last_trace."""
        return self._xor_with_keystream(plaintext, "Bản rõ P")

    def decrypt(self, ciphertext: str) -> str:
        """Giải mã: P = C XOR S (cùng khoá thì sinh lại đúng dãy S)."""
        return self._xor_with_keystream(ciphertext, "Bản mã C")

    def export_trace(self) -> list[dict]:
        """Trả về bản sao trace của lần mã hoá/giải mã gần nhất (cho demo_cli)."""
        return copy.deepcopy(self.last_trace)
