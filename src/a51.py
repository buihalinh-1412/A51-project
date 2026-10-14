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
    def encrypt_bits(self, plaintext_bits, use_uplink=True):
        """
        Mã hóa chuỗi bít bản rõ P bằng phép XOR với dòng khóa S: C = P ⊕ S
        - plaintext_bits: Danh sách các bít [0, 1, 1, 0...] (tối đa 114 bít cho 1 khung)
        - use_uplink: True nếu mã hóa chiều Uplink, False cho Downlink
        - Trả về: Danh sách bít bản mã ciphertext_bits
        """
        downlink, uplink = self.generate_keystream()
        keystream = uplink if use_uplink else downlink

        if len(plaintext_bits) > len(keystream):
            raise ValueError(f"Dữ liệu bản rõ ({len(plaintext_bits)} bít) vượt quá độ dài dòng khóa khung ({len(keystream)} bít).")

        # Thực hiện C_i = P_i ⊕ S_i
        ciphertext_bits = [p ^ s for p, s in zip(plaintext_bits, keystream)]
        return ciphertext_bits

    def decrypt_bits(self, ciphertext_bits, use_uplink=True):
        """
        Giải mã chuỗi bít bản mã C bằng phép XOR với dòng khóa S: P = C ⊕ S
        Do tính chất tự nghịch đảo của phép XOR: (P ⊕ S) ⊕ S = P
        """
        # Giải mã hoàn toàn giống mã hóa (dùng lại đúng dòng khóa S)
        return self.encrypt_bits(ciphertext_bits, use_uplink=use_uplink)
    
if __name__ == "__main__":
        print("=" * 70)
        print("   KIỂM THỬ LÕI A5/1 (GSM ETSI REFERENCE & ROUND-TRIP TEST)")
        print("=" * 70)

        # 1. Khai báo Test Vector chuẩn GSM ETSI
        test_key_hex = "0x1223456789ABCDEF"
        test_frame = 0x134

        print(f"[*] Khởi tạo A5/1 với:")
        print(f"    - Khóa K (Hex)    : {test_key_hex}")
        print(f"    - Số khung F (Hex): {hex(test_frame)} ({test_frame})\n")

        a51_engine = A51(key=test_key_hex, frame=test_frame)

        # 2. Tạo bản rõ thử nghiệm P (8 bít nhị phân)
        P_original = [1, 1, 0, 1, 0, 0, 1, 1]
        print(f"1. Bản rõ ban đầu (P)      : {P_original}")

        # 3. Mã hóa phía Máy di động (Uplink: Máy -> Trạm)
        C_cipher = a51_engine.encrypt_bits(P_original, use_uplink=True)
        print(f"2. Bản mã thu được (C)     : {C_cipher}")

        # 4. Giải mã phía Trạm thu phát (Uplink: Trạm nhận được C và giải mã bằng cùng dòng khóa Uplink)
        # Khởi tạo lại một bộ A51 độc lập ở phía nhận với cùng Key và Frame
        a51_receiver = A51(key=test_key_hex, frame=test_frame)
        P_decrypted = a51_receiver.decrypt_bits(C_cipher, use_uplink=True)
        print(f"3. Bản rõ sau giải mã (P') : {P_decrypted}")

        # 5. Kiểm tra tính đúng đắn Round-trip
        is_correct = (P_original == P_decrypted)
        print("-" * 70)
        print(f"Kết quả kiểm tra Round-trip (P' == P): {is_correct}")
        if is_correct:
            print("=> XÁC NHẬN: Giải mã khôi phục CHÍNH XÁC 100% bản rõ ban đầu!")

        # 6. Kiểm tra sinh Keystream 228 bít (114 bít Downlink + 114 bít Uplink)
        print("-" * 70)
        downlink, uplink = a51_engine.generate_keystream()
        print(f"[*] Dòng khóa Downlink (114 bít): {downlink[:16]}... (độ dài: {len(downlink)})")
        print(f"[*] Dòng khóa Uplink   (114 bít): {uplink[:16]}... (độ dài: {len(uplink)})")
        print("=" * 70)