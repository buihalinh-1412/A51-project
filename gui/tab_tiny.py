"""Tab TinyA5/1: hiện từng bước chạy của bản Tiny (bảng trace).

Gọi TinyA51.step_with_trace() của src/tiny_a51.py để lấy dữ liệu từng bước,
không tự viết lại thuật toán. Người phụ trách: Nguyễn Thị Nhật Linh.
"""

import tkinter as tk
from tkinter import ttk

from src.tiny_a51 import SLIDE_KEY, SLIDE_PLAINTEXT, TinyA51

COLUMNS = ("step", "x", "y", "z", "m", "rotated", "s")
HEADINGS = ("Bước", "X", "Y", "Z", "m", "Thanh ghi quay", "sᵢ")
SLIDE_NOTE = "Z đúng sau bước 2 = 001001100 (slide in 101001100)"


class TinyTab(ttk.Frame):
    """Giao diện chạy TinyA5/1 từng bước hoặc chạy hết."""

    def __init__(self, parent):
        super().__init__(parent)
        self.cipher = None
        self.plaintext = ""
        self.keystream = ""

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=8)
        ttk.Label(form, text="Khóa K (23 bit):").grid(row=0, column=0, sticky="w")
        self.key_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.key_var, width=28).grid(row=0, column=1, padx=6)
        ttk.Label(form, text="Bản rõ P (bit):").grid(row=0, column=2, sticky="w")
        self.plain_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.plain_var, width=18).grid(row=0, column=3, padx=6)

        state = ttk.Frame(self)
        state.pack(fill="x", padx=10)
        self.x_var = tk.StringVar(value="X = -")
        self.y_var = tk.StringVar(value="Y = -")
        self.z_var = tk.StringVar(value="Z = -")
        for var in (self.x_var, self.y_var, self.z_var):
            ttk.Label(state, textvariable=var, font=("Courier", 12)).pack(
                side="left", padx=12)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=10, pady=8)
        ttk.Button(buttons, text="Bước tiếp", command=self.next_step).pack(side="left")
        ttk.Button(buttons, text="Chạy hết", command=self.run_all).pack(side="left", padx=6)
        ttk.Button(buttons, text="Reset", command=self.reset).pack(side="left")
        ttk.Button(buttons, text="Chạy ví dụ slide", command=self.run_slide).pack(
            side="left", padx=6)

        self.table = ttk.Treeview(self, columns=COLUMNS, show="headings", height=12)
        for name, heading in zip(COLUMNS, HEADINGS):
            self.table.heading(name, text=heading)
            self.table.column(name, width=110 if name in ("x", "y", "z") else 80,
                              anchor="center")
        self.table.column("rotated", width=120)
        self.table.pack(fill="both", expand=True, padx=10)

        self.result_var = tk.StringVar()
        ttk.Label(self, textvariable=self.result_var,
                  font=("TkDefaultFont", 11, "bold")).pack(anchor="w", padx=10, pady=4)
        self.note_var = tk.StringVar()
        ttk.Label(self, textvariable=self.note_var, foreground="gray40").pack(
            anchor="w", padx=10)
        self.message_var = tk.StringVar()
        ttk.Label(self, textvariable=self.message_var, foreground="firebrick").pack(
            anchor="w", padx=10, pady=4)

    # -- Hỗ trợ ------------------------------------------------------------

    def _start(self):
        """Tạo bộ sinh mới từ ô nhập; trả về False nếu nhập sai."""
        key = self.key_var.get().strip()
        plain = self.plain_var.get().strip()
        try:
            if plain and set(plain) - {"0", "1"}:
                raise ValueError("Bản rõ chỉ gồm ký tự 0 và 1.")
            self.cipher = TinyA51(key, annotate_slide=(key == SLIDE_KEY))
        except ValueError as error:
            self.message_var.set("Lỗi: " + str(error))
            self.cipher = None
            return False
        self.plaintext = plain
        self.keystream = ""
        self.message_var.set("")
        self._show_state()
        return True

    def _show_state(self):
        state = self.cipher.get_state()
        self.x_var.set("X = " + state["X"])
        self.y_var.set("Y = " + state["Y"])
        self.z_var.set("Z = " + state["Z"])

    def _do_step(self):
        """Chạy một bước, thêm một dòng vào bảng."""
        bit, record = self.cipher.step_with_trace()
        self.keystream += str(bit)
        after = record["state_after"]
        self.table.insert("", "end", values=(
            record["step"], after["X"], after["Y"], after["Z"],
            record["majority"], ",".join(record["rotated_registers"]), bit))
        if "slide_mismatch" in record:
            self.note_var.set(SLIDE_NOTE)
        self._show_state()

    def _show_result(self):
        """Khi đã chạy đủ số bit bản rõ thì hiện S và C."""
        if self.plaintext and len(self.keystream) == len(self.plaintext):
            cipher = "".join(str(int(a) ^ int(b))
                             for a, b in zip(self.plaintext, self.keystream))
            self.result_var.set("Dòng khóa S = %s, Bản mã C = %s" % (self.keystream, cipher))

    # -- Nút bấm -----------------------------------------------------------

    def next_step(self):
        """Chạy một bước (nếu chưa bắt đầu thì nạp khóa trước)."""
        if self.cipher is None and not self._start():
            return
        if self.plaintext and len(self.keystream) >= len(self.plaintext):
            self.message_var.set("Đã chạy đủ số bit của bản rõ. Bấm Reset để làm lại.")
            return
        self._do_step()
        self._show_result()

    def run_all(self):
        """Chạy hết các bước còn lại cho đủ số bit của bản rõ."""
        if self.cipher is None and not self._start():
            return
        if not self.plaintext:
            self.message_var.set("Lỗi: cần nhập bản rõ để biết chạy bao nhiêu bước.")
            return
        while len(self.keystream) < len(self.plaintext):
            self._do_step()
        self._show_result()

    def reset(self):
        """Xóa bảng và nạp lại khóa."""
        self.table.delete(*self.table.get_children())
        self.result_var.set("")
        self.note_var.set("")
        self.cipher = None
        self.keystream = ""
        self.message_var.set("")
        for var, name in ((self.x_var, "X"), (self.y_var, "Y"), (self.z_var, "Z")):
            var.set(name + " = -")

    def run_slide(self):
        """Điền ví dụ slide (K = SLIDE_KEY, P = 111) và chạy 3 bước."""
        self.reset()
        self.key_var.set(SLIDE_KEY)
        self.plain_var.set(SLIDE_PLAINTEXT)
        self.run_all()
