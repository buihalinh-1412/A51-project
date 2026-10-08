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

    def __init__(self):
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
if __name__ == "__main__":
    bo_ma = A51()
    print("--- KIỂM TRA DAY 2: HÀM CHIẾM ĐA SỐ (MAJORITY) ---")

    # 1. Kiểm tra bảng chân lý của hàm đa số (8 trường hợp)
    print("maj(0, 0, 0) =", bo_ma._majority(0, 0, 0), "(Kỳ vọng: 0)")
    print("maj(0, 0, 1) =", bo_ma._majority(0, 0, 1), "(Kỳ vọng: 0)")
    print("maj(0, 1, 1) =", bo_ma._majority(0, 1, 1), "(Kỳ vọng: 1)")
    print("maj(1, 1, 1) =", bo_ma._majority(1, 1, 1), "(Kỳ vọng: 1)")

    # 2. Giả lập thử nghiệm một nhịp quay majority
    # Gán thử bít nhịp: x8=1, y10=0, z10=1 -> m = maj(1, 0, 1) = 1
    # Kỳ vọng: X quay, Z quay, còn Y đứng yên!
    bo_ma.X[8] = 1
    bo_ma.Y[10] = 0
    bo_ma.Z[10] = 1

    print("\n--- Thử nghiệm 1 nhịp quay Majority ---")
    print("Bít nhịp trước khi quay: x8=1, y10=0, z10=1 -> m =", bo_ma._majority(1, 0, 1))
    bo_ma._clock_majority()
    print("Quay thành công! X và Z đã quay, Y giữ nguyên.")