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
if __name__ == "__main__":
    bo_ma = A51()
    print("--- KIỂM TRA KHỞI TẠO BỘ SINH SỐ A5/1 ---")
    print("Độ dài thanh ghi X:", len(bo_ma.X), "bít (Kỳ vọng: 19)")
    print("Độ dài thanh ghi Y:", len(bo_ma.Y), "bít (Kỳ vọng: 22)")
    print("Độ dài thanh ghi Z:", len(bo_ma.Z), "bít (Kỳ vọng: 23)")

    # Thử nghiệm phép Quay X với bít nạp vào là 1
    bo_ma._quay_X(feedback_input=1)
    print("Trạng thái X sau 1 lần quay với bít nạp 1:")
    print("x0 =", bo_ma.X[0], "(Kỳ vọng: 1)")
    print("Toàn bộ X:", "".join(map(str, bo_ma.X)))