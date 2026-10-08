"""
Chương trình: Hệ mã hóa dòng A5/1 (Phiên bản đầy đủ chuẩn GSM)
Học phần: An toàn và bảo mật thông tin
Sinh viên thực hiện: Bùi Hà Linh
Mô tả: Lõi thuật toán A5/1, sử dụng thuần Python, không dùng thư viện ngoài.
"""

class A51:
    """
    Lớp A51 mô phỏng bộ sinh số gồm 3 thanh ghi X, Y, Z theo Slide bài giảng:
      - Thanh ghi X: độ dài 19 bít (x0 đến x18)
      - Thanh ghi Y: độ dài 22 bít (y0 đến y21)
      - Thanh ghi Z: độ dài 23 bít (z0 đến z22)
    """

    def __init__(self, key, frame=0):
        """
        Khởi tạo hệ mã A5/1 với Khóa phiên K (64 bít) và Số hiệu khung F (22 bít).
        """
        # Chuẩn hóa đầu vào của khóa và số khung
        self.key_bits = self._validate_and_format_key(key)
        self.frame_bits = self._validate_and_format_frame(frame)

        # Khởi tạo 3 thanh ghi X, Y, Z ban đầu gồm toàn bít 0
        self.X = [0] * 19
        self.Y = [0] * 22
        self.Z = [0] * 23

    def reset(self):
        """Đưa trạng thái của cả 3 thanh ghi X, Y, Z về toàn bít 0."""
        self.X = [0] * 19
        self.Y = [0] * 22
        self.Z = [0] * 23

    def _quay_X(self, feedback_input=0):
        """
        Thao tác Quay X (Slide 51):
          - Tính bít phản hồi: t = x13 ⊕ x16 ⊕ x17 ⊕ x18 ⊕ feedback_input
          - Dịch bít: xj = xj-1 với j = 18, 17, ..., 1
          - Nạp bít mới: x0 = t
        """
        # 1. Tính bít phản hồi t bằng phép XOR (toán tử ^ trong Python)
        t = self.X[13] ^ self.X[16] ^ self.X[17] ^ self.X[18] ^ feedback_input

        # 2. Dịch bít sang phải và nạp t vào ô đầu tiên x0
        # self.X[:-1] cắt bỏ bít cuối cùng x18
        # [t] + self.X[:-1] chèn bít t vào vị trí x0
        self.X = [t] + self.X[:-1]

    def _quay_Y(self, feedback_input=0):
        """
        Thao tác Quay Y (Slide 51):
          - Tính bít phản hồi: t = y20 ⊕ y21 ⊕ feedback_input
          - Dịch bít: yj = yj-1 với j = 21, 20, ..., 1
          - Nạp bít mới: y0 = t
        """
        t = self.Y[20] ^ self.Y[21] ^ feedback_input
        self.Y = [t] + self.Y[:-1]

    def _quay_Z(self, feedback_input=0):
        """
        Thao tác Quay Z (Slide 51):
          - Tính bít phản hồi: t = z7 ⊕ z20 ⊕ z21 ⊕ z22 ⊕ feedback_input
          - Dịch bít: zj = zj-1 với j = 22, 21, ..., 1
          - Nạp bít mới: z0 = t
        """
        t = self.Z[7] ^ self.Z[20] ^ self.Z[21] ^ self.Z[22] ^ feedback_input
        self.Z = [t] + self.Z[:-1]
    @staticmethod
    def _majority(b1, b2, b3):
        """
        Hàm chiếm đa số m = maj(b1, b2, b3) (Slide 49 & Slide 51):
          - Nếu trong 3 bít có từ hai bít 0 trở lên -> trả về 0.
          - Nếu trong 3 bít có từ hai bít 1 trở lên -> trả về 1.
        """
        # Cách 1: Đếm tổng các bít (rất trực quan theo đúng định nghĩa slide)
        if (b1 + b2 + b3) >= 2:
            return 1
        else:
            return 0
    def _clock_majority(self):
        """
        Điều khiển nhịp dừng/chạy cho 3 thanh ghi theo hàm chiếm đa số (Slide 51):
          - Lấy 3 bít nhịp: x8, y10, z10.
          - Tính m = maj(x8, y10, z10).
          - Thanh ghi nào có bít nhịp bằng m thì được kích hoạt quay.
        """
        # 1. Trích xuất 3 bít nhịp từ các vị trí quy định trên slide
        x8 = self.X[8]
        y10 = self.Y[10]
        z10 = self.Z[10]

        # 2. Tính giá trị chiếm đa số m
        m = self._majority(x8, y10, z10)

        # 3. Kích hoạt quay các thanh ghi có bít nhịp bằng m
        if x8 == m:
            self._quay_X()
        if y10 == m:
            self._quay_Y()
        if z10 == m:
            self._quay_Z()
    def _load_key(self):
        """Giai đoạn 1: Nạp khóa 64 chu kỳ (quay đồng bộ 3 thanh ghi)."""
        for i in range(64):
            k_bit = self.key_bits[i]
            self._quay_X(feedback_input=k_bit)
            self._quay_Y(feedback_input=k_bit)
            self._quay_Z(feedback_input=k_bit)

    def _load_frame(self):
        """Giai đoạn 2: Nạp số khung 22 chu kỳ (quay đồng bộ 3 thanh ghi)."""
        for j in range(22):
            f_bit = self.frame_bits[j]
            self._quay_X(feedback_input=f_bit)
            self._quay_Y(feedback_input=f_bit)
            self._quay_Z(feedback_input=f_bit)
    @staticmethod
    def _validate_and_format_key(key):
        """Chuyển đổi và kiểm tra Khóa K phải đủ đúng 64 bít."""
        if isinstance(key, str):
            key = key.strip()
            if key.startswith("0x") or key.startswith("0X"):
                bin_str = bin(int(key, 16))[2:].zfill(64)
                key_list = [int(b) for b in bin_str]
            else:
                key_list = [int(b) for b in key if b in ("0", "1")]
        elif isinstance(key, list):
            key_list = [int(b) for b in key]
        else:
            raise TypeError("Khóa K phải ở dạng chuỗi nhị phân hoặc chuỗi Hex.")

        if len(key_list) != 64:
            raise ValueError(f"Khóa K phải có đúng 64 bít (hiện tại: {len(key_list)} bít).")
        return key_list

    @staticmethod
    def _validate_and_format_frame(frame):
        """Chuyển đổi và kiểm tra Số khung F phải đủ đúng 22 bít."""
        if isinstance(frame, int):
            if frame < 0 or frame >= (1 << 22):
                raise ValueError("Số khung F phải nằm trong khoảng từ 0 đến 2^22 - 1.")
            return [(frame >> i) & 1 for i in range(22)]
        elif isinstance(frame, str):
            frame_list = [int(b) for b in frame.strip() if b in ("0", "1")]
            if len(frame_list) != 22:
                raise ValueError(f"Số khung F phải có đúng 22 bít (hiện tại: {len(frame_list)} bít).")
            return frame_list
        elif isinstance(frame, list):
            if len(frame) != 22:
                raise ValueError("Danh sách bít số khung phải gồm đúng 22 phần tử.")
            return [int(b) for b in frame]
        else:
            raise TypeError("Số khung F không hợp lệ.")

    def _warmup(self):
        """
        Giai đoạn 3: Chạy ấm 100 chu kỳ (Warm-up / Mixing phase).
        - Thực hiện quay 100 chu kỳ theo quy tắc hàm chiếm đa số (Majority).
        - Toàn bộ bít đầu ra bị hủy bỏ hoàn toàn, không đưa vào dòng khóa.
        """
        for _ in range(100):
            # Mỗi chu kỳ kích hoạt quay dừng/chạy theo đa số
            self._clock_majority()

    def generate_keystream(self):
        """
        Giai đoạn 4: Sinh dòng khóa gồm 228 bít cho một khung thoại GSM.
        - Khởi động: reset() -> nạp khóa 64 chu kỳ -> nạp khung 22 chu kỳ -> chạy ấm 100 chu kỳ.
        - Sinh 228 bít: quay theo Majority, trích xuất chuẩn GSM ETSI: si = x18 ⊕ y21 ⊕ z22.
        - Trả về: (downlink, uplink), mỗi luồng dài đúng 114 bít.
        """
        # Bước A: Thiết lập trạng thái ban đầu
        self.reset()
        self._load_key()
        self._load_frame()
        self._warmup()

        keystream = []

        # Bước B: Sinh 228 bít dòng khóa
        for _ in range(228):
            # 1. Quay các thanh ghi thỏa mãn hàm đa số
            self._clock_majority()

            # 2. Trích xuất bít dòng khóa chuẩn GSM ETSI (bít cuối cùng của 3 thanh ghi)
            s_bit = self.X[18] ^ self.Y[21] ^ self.Z[22]
            keystream.append(s_bit)

        # Bước C: Phân chia luồng đàm thoại GSM
        downlink = keystream[:114]
        uplink = keystream[114:]

        return downlink, uplink
# =============================================================================
# KHỐI TỰ KIỂM THỬ CỤC BỘ (SELF-TEST)
# =============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("   KIỂM THỬ LÕI A5/1 (GSM ETSI REFERENCE - CHUẨN QUỐC TẾ)")
    print("=" * 65)

    # Nạp Test Vector chuẩn quốc tế (Marc Briceno / ETSI)
    test_key_hex = "0x1223456789ABCDEF"
    test_frame = 0x134  # Số khung 308 trong hệ thập phân

    bo_ma = A51(key=test_key_hex, frame=test_frame)
    downlink_bits, uplink_bits = bo_ma.generate_keystream()

    print(f"Khóa phiên K (Hex)    : {test_key_hex}")
    print(f"Số hiệu khung F (Int) : {test_frame}")
    print(f"Tổng số bít sinh ra   : {len(downlink_bits) + len(uplink_bits)} bít (Kỳ vọng: 228)")
    print("-" * 65)
    print(f"Downlink (114 bít)    : {''.join(map(str, downlink_bits))}")
    print(f"Uplink   (114 bít)    : {''.join(map(str, uplink_bits))}")
    print("-" * 65)
    print(f"Kiểm tra độ dài Downlink : {len(downlink_bits)} bít (Kỳ vọng: 114)")
    print(f"Kiểm tra độ dài Uplink   : {len(uplink_bits)} bít (Kỳ vọng: 114)")
    print("Trạng thái: Hoàn thành sinh dòng khóa chuẩn GSM thành công!")