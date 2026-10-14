"""
Học phần: An toàn và bảo mật thông tin.
Người phụ trách: Bùi Hà Linh.

Lõi thuật toán A5/1 viết bằng Python thuần, KHÔNG dùng thư viện mật mã.
File này KHÔNG in ra màn hình; phần tự kiểm tra nằm ở tests/run_verification.py.

Cấu trúc (register_x = R1, register_y = R2, register_z = R3; chỉ số từ 0):
  register_x: 19 bít, bít nhịp x8,  taps x13 x16 x17 x18   [S#, trang]
  register_y: 22 bít, bít nhịp y10, taps y20 y21           [S#, trang]
  register_z: 23 bít, bít nhịp z10, taps z7 z20 z21 z22    [S#, trang]
Quay một thanh ghi: t = XOR(taps) ^ (bít nạp ngoài); dịch xj = x(j-1); x0 = t.
Bít keystream: x18 ^ y21 ^ z22 (lấy SAU khi quay). Lưu ý: x8/y10/z10 là bít NHỊP,
không phải bít output.

Quy trình mỗi khung: xoá -> nạp 64 bít khoá (quay cả 3, XOR bít khoá vào t)
 -> nạp 22 bít số khung (tương tự) -> 100 chu kỳ warm-up (quay theo majority,
 bỏ output) -> 228 chu kỳ sinh keystream (114 downlink + 114 uplink).

Quy ước bít (theo cài đặt tham chiếu của Marc Briceno) [S#, trang]:
  - Khoá dạng hex/bytes: byte đầu tiên trước, trong mỗi byte nạp bít LSB trước.
  - Khoá dạng chuỗi 64 ký tự 0/1: ký tự đầu là K0 (nạp trước), KHÁC quy ước hex (TD-003).
  - Số khung: nạp bít LSB (bít 0) trước.
  - Đóng gói keystream ra byte/hex: bít sinh ra đầu tiên nằm ở bít MSB.

Biểu diễn nội bộ: mỗi thanh ghi là một số nguyên (bitmask), bít thứ i của số = x_i.
Dịch "xj = x(j-1)" tương ứng phép dịch trái 1 bít (reg << 1).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Hằng số
# ---------------------------------------------------------------------------
LEN_X, LEN_Y, LEN_Z = 19, 22, 23
KEY_BITS = 64
FRAME_BITS = 22
WARMUP_CYCLES = 100
KEYSTREAM_BITS = 228          # mỗi khung
HALF = 114                    # mỗi hướng (downlink / uplink)

CLOCK_X, CLOCK_Y, CLOCK_Z = 8, 10, 10   # vị trí bít nhịp


def _mask(*positions: int) -> int:
    value = 0
    for p in positions:
        value |= 1 << p
    return value


MASK_X = (1 << LEN_X) - 1
MASK_Y = (1 << LEN_Y) - 1
MASK_Z = (1 << LEN_Z) - 1
TAPS_X = _mask(13, 16, 17, 18)
TAPS_Y = _mask(20, 21)
TAPS_Z = _mask(7, 20, 21, 22)

MAX_FRAMES = 1 << FRAME_BITS  # số khung tối đa trước khi số khung lặp lại


# ---------------------------------------------------------------------------
# Hàm phụ trợ
# ---------------------------------------------------------------------------
def _majority(b1: int, b2: int, b3: int) -> int:
    """Hàm chiếm đa số: 1 nếu có từ hai bít 1 trở lên, ngược lại 0."""
    return 1 if (b1 + b2 + b3) >= 2 else 0


def _parity(x: int) -> int:
    return bin(x).count("1") & 1


def _shift(register: int, mask: int, taps: int, feedback_input: int = 0) -> int:
    """Quay một thanh ghi: t = XOR(taps) ^ feedback_input; dịch; x0 = t."""
    t = _parity(register & taps) ^ feedback_input
    return ((register << 1) & mask) | t


def bits_to_hex(bits) -> str:
    """Gom danh sách bít thành chuỗi Hex, MSB-first (chuẩn test vector Briceno).
    Đệm 0 vào cuối nếu chưa đủ byte (114 bít -> 15 byte)."""
    bits = list(bits)
    bits += [0] * (-len(bits) % 8)
    out = []
    for i in range(0, len(bits), 8):
        v = 0
        for b in bits[i:i + 8]:
            v = (v << 1) | b
        out.append(f"{v:02X}")
    return "".join(out)


def _format_key(key) -> list:
    """Chuẩn hoá khoá về list 64 bít K0..K63. Chấp nhận: chuỗi hex 16 ký tự
    (có thể có 0x), bytes dài 8, chuỗi nhị phân 64 ký tự, list 64 bít."""
    if isinstance(key, (bytes, bytearray)):
        if len(key) != 8:
            raise ValueError(f"Khoá phải dài 8 byte (nhận {len(key)} byte).")
        return [(b >> i) & 1 for b in key for i in range(8)]
    if isinstance(key, str):
        s = key.strip().replace(" ", "")
        if s[:2] in ("0x", "0X"):
            s = s[2:]
        if len(s) == 64 and set(s) <= {"0", "1"}:
            return [int(c) for c in s]
        if len(s) != 16:
            raise ValueError(
                "Khoá phải là 16 ký tự hex (64 bít) hoặc 64 ký tự 0/1; "
                f"nhận {len(s)} ký tự.")
        try:
            raw = bytes.fromhex(s)
        except ValueError:
            raise ValueError("Khoá chứa ký tự không phải hex.") from None
        return [(b >> i) & 1 for b in raw for i in range(8)]
    if isinstance(key, (list, tuple)):
        if len(key) != KEY_BITS or any(b not in (0, 1) for b in key):
            raise ValueError("Khoá dạng list phải gồm đúng 64 phần tử 0/1.")
        return [int(b) for b in key]
    raise TypeError("Khoá phải là chuỗi hex/nhị phân, bytes hoặc list bít.")


def _format_frame(frame) -> list:
    """Chuẩn hoá số khung về list 22 bít F0..F21 (LSB trước)."""
    if isinstance(frame, bool):
        raise TypeError("Số khung không hợp lệ.")
    if isinstance(frame, int):
        if not 0 <= frame < MAX_FRAMES:
            raise ValueError("Số khung phải nằm trong [0, 2^22 - 1].")
        return [(frame >> i) & 1 for i in range(FRAME_BITS)]
    if isinstance(frame, str):
        s = frame.strip()
        if len(s) != FRAME_BITS or not set(s) <= {"0", "1"}:
            raise ValueError("Số khung dạng chuỗi phải gồm đúng 22 ký tự 0/1.")
        return [int(c) for c in s]
    if isinstance(frame, (list, tuple)):
        if len(frame) != FRAME_BITS or any(b not in (0, 1) for b in frame):
            raise ValueError("Số khung dạng list phải gồm đúng 22 bít 0/1.")
        return [int(b) for b in frame]
    raise TypeError("Số khung không hợp lệ.")


# ---------------------------------------------------------------------------
# Lớp A51
# ---------------------------------------------------------------------------
class A51:
    """Bộ sinh dòng khoá A5/1 cho một khoá phiên K (64 bít) và số khung F."""

    def __init__(self, key, frame=0) -> None:
        self.key_bits = _format_key(key)
        self.frame_bits = _format_frame(frame)
        # Luôn là int (sửa lỗi: trước đây lưu nguyên giá trị gốc, có thể là str/list)
        self.frame = sum(b << i for i, b in enumerate(self.frame_bits))
        self.register_x = self.register_y = self.register_z = 0

    # -- thanh ghi -----------------------------------------------------
    def reset(self) -> None:
        self.register_x = self.register_y = self.register_z = 0

    def get_state(self) -> dict:
        """Trạng thái dạng chuỗi bít x0..x18, y0..y21, z0..z22 (cho trace/debug)."""
        def to_str(reg, n):
            return "".join(str((reg >> i) & 1) for i in range(n))
        return {"X": to_str(self.register_x, LEN_X),
                "Y": to_str(self.register_y, LEN_Y),
                "Z": to_str(self.register_z, LEN_Z)}

    def _clock_r1(self, feedback_input: int = 0) -> None:
        self.register_x = _shift(self.register_x, MASK_X, TAPS_X, feedback_input)

    def _clock_r2(self, feedback_input: int = 0) -> None:
        self.register_y = _shift(self.register_y, MASK_Y, TAPS_Y, feedback_input)

    def _clock_r3(self, feedback_input: int = 0) -> None:
        self.register_z = _shift(self.register_z, MASK_Z, TAPS_Z, feedback_input)

    def _clock_all(self, bit: int) -> None:
        """Quay đồng bộ cả 3 thanh ghi, XOR 'bit' vào bít phản hồi (nạp khoá/khung)."""
        self._clock_r1(bit)
        self._clock_r2(bit)
        self._clock_r3(bit)

    def _clock_majority(self) -> None:
        """Quay theo hàm chiếm đa số của x8, y10, z10."""
        clock_bit_x = (self.register_x >> CLOCK_X) & 1
        clock_bit_y = (self.register_y >> CLOCK_Y) & 1
        clock_bit_z = (self.register_z >> CLOCK_Z) & 1
        majority_bit = _majority(clock_bit_x, clock_bit_y, clock_bit_z)
        if clock_bit_x == majority_bit:
            self._clock_r1()
        if clock_bit_y == majority_bit:
            self._clock_r2()
        if clock_bit_z == majority_bit:
            self._clock_r3()

    def _output_bit(self) -> int:
        return ((self.register_x >> (LEN_X - 1))
                ^ (self.register_y >> (LEN_Y - 1))
                ^ (self.register_z >> (LEN_Z - 1))) & 1

    # -- các giai đoạn -------------------------------------------------
    def _load_key(self) -> None:
        for k in self.key_bits:
            self._clock_all(k)

    def _load_frame(self) -> None:
        for f in self.frame_bits:
            self._clock_all(f)

    def _warmup(self) -> None:
        for _ in range(WARMUP_CYCLES):
            self._clock_majority()

    def generate_keystream(self):
        """Trả về (downlink, uplink): hai list 114 bít cho khung hiện tại."""
        self.reset()
        self._load_key()
        self._load_frame()
        self._warmup()
        keystream = []
        for _ in range(KEYSTREAM_BITS):
            self._clock_majority()
            keystream.append(self._output_bit())
        return keystream[:HALF], keystream[HALF:]

    # -- mã hoá / giải mã chuỗi bít (tối đa 114 bít, một khung) ---------
    def encrypt_bits(self, plaintext_bits, use_uplink: bool = False):
        """C = P xor S trên một khung. Mặc định dùng keystream downlink."""
        down, up = self.generate_keystream()
        keystream = up if use_uplink else down
        if len(plaintext_bits) > len(keystream):
            raise ValueError(
                f"Một khung chỉ mã được {len(keystream)} bít "
                f"(nhận {len(plaintext_bits)}). Dùng encrypt_bytes cho dữ liệu dài.")
        return [int(p) ^ s for p, s in zip(plaintext_bits, keystream)]

    def decrypt_bits(self, ciphertext_bits, use_uplink: bool = False):
        return self.encrypt_bits(ciphertext_bits, use_uplink)

    # -- mã hoá / giải mã dữ liệu dài (TD-005) --------------------------
    def keystream_bytes(self, nbytes: int, use_uplink: bool = False) -> bytes:
        """Sinh nbytes byte keystream: nối các khung liên tiếp (frame, frame+1, ...),
        mỗi khung lấy 114 bít, đóng gói MSB-first."""
        nbits = nbytes * 8
        frames_needed = -(-nbits // HALF)
        if self.frame + frames_needed > MAX_FRAMES:
            raise ValueError(
                "Dữ liệu quá dài: số khung vượt 2^22, keystream sẽ bị lặp lại.")
        bits = []
        for n in range(frames_needed):
            sub = A51(self.key_bits, self.frame + n)
            down, up = sub.generate_keystream()
            bits.extend(up if use_uplink else down)
        bits = bits[:nbits]
        out = bytearray()
        for i in range(0, nbits, 8):
            v = 0
            for b in bits[i:i + 8]:
                v = (v << 1) | b
            out.append(v)
        return bytes(out)

    def encrypt_bytes(self, data: bytes, use_uplink: bool = False) -> bytes:
        """Mã hoá dữ liệu bất kỳ độ dài (text, ảnh...). Bản mã dài bằng bản rõ."""
        keystream = self.keystream_bytes(len(data), use_uplink)
        return bytes(d ^ k for d, k in zip(data, keystream))

    def decrypt_bytes(self, data: bytes, use_uplink: bool = False) -> bytes:
        return self.encrypt_bytes(data, use_uplink)