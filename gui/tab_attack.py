"""Tab "Tấn công": minh họa tấn công dùng lại dòng khóa (Two-Time Pad).

Phụ trách: Trần Đại Lộc. Chạy riêng: python -m gui.tab_attack
Gọi hàm theo hợp đồng: simulate_scenario, crib_drag (src/attack_two_time_pad.py).
"""
import os
import tkinter as tk
from tkinter import ttk

try:
    from src.attack_two_time_pad import crib_drag, simulate_scenario
    USING_STUBS = False
except ImportError:  # code thật chưa có -> dùng hàm giả để làm giao diện
    from gui._contract_stubs import crib_drag, simulate_scenario
    USING_STUBS = True

from gui.tab_file import parse_frame

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_P1 = os.path.join(ROOT_DIR, "examples", "p1.txt")
SAMPLE_P2 = os.path.join(ROOT_DIR, "examples", "p2.txt")


class AttackTab(ttk.Frame):
    """Giao diện mô phỏng dùng lại số khung và dò crib."""

    def __init__(self, parent):
        super().__init__(parent)
        self.result = None  # kết quả simulate_scenario gần nhất
        self._build()

    def _build(self):
        pad = {"padx": 8, "pady": 3}
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="P1:").grid(row=0, column=0, sticky="nw", **pad)
        self.p1 = tk.Text(self, height=3, width=60, wrap="word")
        self.p1.grid(row=0, column=1, columnspan=2, sticky="ew", **pad)
        ttk.Label(self, text="P2:").grid(row=1, column=0, sticky="nw", **pad)
        self.p2 = tk.Text(self, height=3, width=60, wrap="word")
        self.p2.grid(row=1, column=1, columnspan=2, sticky="ew", **pad)
        ttk.Button(self, text="Nạp file mẫu", command=self._load_samples).grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(self, text="Khóa (16 hex):").grid(row=3, column=0, sticky="w", **pad)
        self.key_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.key_var, width=24).grid(row=3, column=1, sticky="w", **pad)
        ttk.Label(self, text="Số khung P1:").grid(row=4, column=0, sticky="w", **pad)
        self.frame_var = tk.StringVar(value="0")
        ttk.Entry(self, textvariable=self.frame_var, width=12).grid(row=4, column=1, sticky="w", **pad)

        self.reuse_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Dùng lại số khung", variable=self.reuse_var).grid(
            row=5, column=1, sticky="w", **pad)
        ttk.Button(self, text="Chạy mô phỏng", command=self._simulate).grid(row=6, column=1, sticky="w", **pad)

        ttk.Label(self, text="C1 ⊕ C2 (hex):").grid(row=7, column=0, sticky="nw", **pad)
        self.xor_text = tk.Text(self, height=3, width=60, wrap="char", state="disabled")
        self.xor_text.grid(row=7, column=1, columnspan=2, sticky="ew", **pad)
        self.status_var = tk.StringVar(value="CHÚ Ý: đang dùng hàm GIẢ (chưa có src/attack_two_time_pad.py)"
                                       if USING_STUBS else "")
        ttk.Label(self, textvariable=self.status_var, wraplength=560).grid(
            row=8, column=0, columnspan=3, sticky="w", **pad)

        ttk.Label(self, text="Crib (từ đoán trong P1):").grid(row=9, column=0, sticky="w", **pad)
        self.crib_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.crib_var, width=24).grid(row=9, column=1, sticky="w", **pad)
        ttk.Button(self, text="Dò crib", command=self._drag).grid(row=10, column=1, sticky="w", **pad)

        cols = ("pos", "text", "score")
        self.table = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c, title, w in (("pos", "Vị trí", 70), ("text", "Đoạn chữ lộ ra", 300), ("score", "Điểm", 80)):
            self.table.heading(c, text=title)
            self.table.column(c, width=w, anchor="w")
        self.table.grid(row=11, column=0, columnspan=3, sticky="nsew", **pad)
        self.rowconfigure(11, weight=1)

    # ---------- tiện ích ----------
    @staticmethod
    def _get(widget):
        return widget.get("1.0", "end-1c")

    def _set_xor(self, s):
        self.xor_text.configure(state="normal")
        self.xor_text.delete("1.0", "end")
        self.xor_text.insert("1.0", s)
        self.xor_text.configure(state="disabled")

    def _load_samples(self):
        try:
            with open(SAMPLE_P1, encoding="utf-8") as f1, open(SAMPLE_P2, encoding="utf-8") as f2:
                a, b = f1.read().strip(), f2.read().strip()
        except OSError as e:
            self.status_var.set(f"Lỗi: không đọc được file mẫu ({e})")
            return
        self.p1.delete("1.0", "end")
        self.p1.insert("1.0", a)
        self.p2.delete("1.0", "end")
        self.p2.insert("1.0", b)
        self.status_var.set("Đã nạp examples/p1.txt và examples/p2.txt")

    # ---------- hành động ----------
    def _simulate(self):
        try:
            p1 = self._get(self.p1).encode("utf-8")
            p2 = self._get(self.p2).encode("utf-8")
            if not p1 or not p2:
                raise ValueError("P1 và P2 không được để trống")
            f1 = parse_frame(self.frame_var.get())
            f2 = f1 if self.reuse_var.get() else f1 + 1
            self.result = simulate_scenario(p1, p2, self.key_var.get().strip(), f1, f2)
        except Exception as e:
            self.result = None
            self.status_var.set(f"Lỗi: {type(e).__name__}: {e}")
            return
        self._set_xor(self.result["c1_xor_c2"].hex())
        if self.result["reused"]:
            self.status_var.set("Hai dòng khóa TRÙNG nhau")
        else:
            self.status_var.set("Hai dòng khóa KHÁC nhau")
        for row in self.table.get_children():
            self.table.delete(row)

    def _drag(self):
        if self.result is None:
            self.status_var.set("Hãy bấm 'Chạy mô phỏng' trước")
            return
        crib = self.crib_var.get().encode("utf-8")
        if not crib:
            self.status_var.set("Lỗi: chưa nhập crib")
            return
        try:
            rows = crib_drag(self.result["c1"], self.result["c2"], crib, top=10)
        except Exception as e:
            self.status_var.set(f"Lỗi: {type(e).__name__}: {e}")
            return
        for row in self.table.get_children():
            self.table.delete(row)
        for r in rows:
            self.table.insert("", "end", values=(r["offset"], r["text"], f"{r['score']:.2f}"))
        self.status_var.set(f"Đã dò crib, hiện {len(rows)} kết quả cao điểm nhất")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tab Tấn công")
    AttackTab(root).pack(fill="both", expand=True)
    root.mainloop()
