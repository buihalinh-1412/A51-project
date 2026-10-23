"""Tab "Mã hóa File": chọn file -> mã hóa / giải mã bằng A5/1.

Phụ trách: Trần Đại Lộc. Chạy riêng: python -m gui.tab_file
Gọi hàm theo hợp đồng: encrypt_file, decrypt_file (src/file_crypto.py).
Không chứa thuật toán, chỉ là giao diện.
"""
import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Chỉ dùng hàm giả khi module src.file_crypto CHƯA TỒN TẠI.
# Nếu file_crypto có nhưng lỗi import bên trong (vd a51.py hỏng) thì phải báo lỗi thật,
# không được âm thầm chuyển sang hàm giả (sẽ "mã hóa" giả mà người dùng không biết).
try:
    from src.file_crypto import decrypt_file, encrypt_file
    USING_STUBS = False
except ModuleNotFoundError as _e:
    if _e.name not in ("src", "src.file_crypto"):
        raise
    from gui._contract_stubs import decrypt_file, encrypt_file
    USING_STUBS = True

STUB_MSG = "CHÚ Ý: đang dùng hàm GIẢ (chưa có src/file_crypto.py)"
PREVIEW_BYTES = 1024
MAX_PREVIEW_PNG = 20 * 1024 * 1024  # tránh nạp ảnh quá lớn vào bộ nhớ


def parse_frame(text):
    """Đọc số khung: '308' hoặc '0x134'. Rỗng = 0. Sai thì ValueError."""
    t = text.strip().lower()
    if not t:
        return 0
    try:
        value = int(t, 16) if t.startswith("0x") else int(t, 10)
    except ValueError:
        raise ValueError("Số khung phải là số nguyên (vd 0, 308 hoặc 0x134)")
    if value < 0:
        raise ValueError("Số khung không được âm")
    return value


class FileTab(ttk.Frame):
    """Giao diện mã hóa / giải mã file."""

    def __init__(self, parent):
        super().__init__(parent)
        self.path = ""
        self._q = queue.Queue()  # luồng làm việc gửi tiến độ/kết quả về luồng giao diện
        self._busy = False
        self._photo = None  # giữ tham chiếu, không thì Tkinter xóa ảnh
        self._build()
        self.after(100, self._poll)

    # ---------- dựng giao diện ----------
    def _build(self):
        pad = {"padx": 8, "pady": 4}
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)

        ttk.Button(self, text="Chọn file", command=self._choose).grid(row=0, column=0, sticky="w", **pad)
        self.path_var = tk.StringVar(value="(chưa chọn file)")
        ttk.Label(self, textvariable=self.path_var).grid(row=0, column=1, columnspan=2, sticky="w", **pad)

        ttk.Label(self, text="Khóa (16 ký tự hex):").grid(row=1, column=0, sticky="w", **pad)
        self.key_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.key_var, width=24).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(self, text="Số khung bắt đầu:").grid(row=2, column=0, sticky="w", **pad)
        self.frame_var = tk.StringVar(value="0")
        ttk.Entry(self, textvariable=self.frame_var, width=12).grid(row=2, column=1, sticky="w", **pad)

        btns = ttk.Frame(self)
        btns.grid(row=3, column=0, columnspan=3, sticky="w", **pad)
        self.btn_enc = ttk.Button(btns, text="Mã hóa", command=self._encrypt)
        self.btn_dec = ttk.Button(btns, text="Giải mã", command=self._decrypt)
        self.btn_enc.pack(side="left", padx=(0, 8))
        self.btn_dec.pack(side="left")

        self.bar = ttk.Progressbar(self, mode="determinate", maximum=100)
        self.bar.grid(row=4, column=0, columnspan=3, sticky="ew", **pad)

        self.msg_var = tk.StringVar(value=STUB_MSG if USING_STUBS else "")
        ttk.Label(self, textvariable=self.msg_var, wraplength=560).grid(
            row=5, column=0, columnspan=3, sticky="w", **pad)

        self.preview_frame = ttk.LabelFrame(self, text="Xem trước")
        self.preview_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", **pad)
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)
        self.preview_text = tk.Text(self.preview_frame, height=8, width=70, wrap="word", state="disabled")
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        self.preview_img = ttk.Label(self.preview_frame)

    # ---------- chọn file, xem trước ----------
    def _choose(self):
        p = filedialog.askopenfilename(title="Chọn file")
        if p:
            self.set_path(p)

    def set_path(self, p):
        """Đặt file đang làm việc (cũng dùng khi chạy thử không qua hộp thoại)."""
        self.path = p
        self.path_var.set(p)
        self.msg_var.set(STUB_MSG if USING_STUBS else "")
        self.bar["value"] = 0
        self._preview(p)

    def _preview(self, p):
        """.png hiện ảnh; file văn bản hiện 1KB đầu; còn lại báo không xem trước được."""
        self.preview_img.grid_forget()
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        self._photo = None
        try:
            with open(p, "rb") as f:
                head = f.read(PREVIEW_BYTES)
            if head.startswith(b"\x89PNG\r\n\x1a\n") and os.path.getsize(p) <= MAX_PREVIEW_PNG:
                self._photo = tk.PhotoImage(file=p)
                self.preview_text.grid_forget()
                self.preview_img.configure(image=self._photo)
                self.preview_img.grid(row=0, column=0)
                return
            if p.lower().endswith(".enc"):
                self._set_preview_text("(file đã mã hóa, không xem trước)")
                return
            try:
                text = head.decode("utf-8", errors="strict")
            except UnicodeDecodeError as e:
                # cắt ở ký tự cuối có thể bị đứt giữa chừng khi đọc đúng 1KB
                if e.start >= len(head) - 3 and len(head) == PREVIEW_BYTES:
                    text = head[:e.start].decode("utf-8")
                else:
                    self._set_preview_text("(dữ liệu nhị phân, không xem trước dạng chữ)")
                    return
            self._set_preview_text(text)
        except (OSError, tk.TclError) as e:
            self._set_preview_text(f"(không xem trước được: {e})")

    def _set_preview_text(self, s):
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", s)
        self.preview_text.configure(state="disabled")

    # ---------- mã hóa / giải mã (chạy trong luồng riêng) ----------
    def _encrypt(self):
        self._start("enc")

    def _decrypt(self):
        self._start("dec")

    def _start(self, mode):
        if self._busy:
            return
        if not self.path:
            self.msg_var.set("Lỗi: chưa chọn file")
            return
        if mode == "dec" and not self.path.lower().endswith(".enc"):
            # decrypt_file đọc 4 byte đầu làm số khung; file lạ sẽ ra rác mà không báo lỗi
            if not messagebox.askyesno(
                    "Giải mã",
                    "File này không có đuôi .enc (không phải file do chương trình mã hóa?).\n"
                    "Vẫn giải mã?"):
                return
        key = self.key_var.get().strip()
        try:
            frame = parse_frame(self.frame_var.get()) if mode == "enc" else 0
        except ValueError as e:
            self.msg_var.set(f"Lỗi: {e}")
            return
        out = self.path + (".enc" if mode == "enc" else ".dec")
        self._busy = True
        self.btn_enc.state(["disabled"])
        self.btn_dec.state(["disabled"])
        self.bar["value"] = 0
        self.msg_var.set("Đang xử lý...")
        threading.Thread(target=self._work, args=(mode, self.path, out, key, frame), daemon=True).start()

    def _work(self, mode, src, out, key, frame):
        """Chạy ở luồng phụ: KHÔNG đụng vào widget, chỉ gửi tin qua hàng đợi."""
        def progress(done, total):
            self._q.put(("progress", done, total))
        try:
            if mode == "enc":
                encrypt_file(src, out, key, frame, progress=progress)
            else:
                decrypt_file(src, out, key, progress=progress)
            self._q.put(("done", mode, out))
        except Exception as e:  # hiện lỗi lên Label, không để chương trình sập
            self._q.put(("error", f"{type(e).__name__}: {e}"))

    def _poll(self):
        """Chạy ở luồng giao diện: nhận tin từ luồng phụ."""
        try:
            while True:
                item = self._q.get_nowait()
                if item[0] == "progress":
                    self._update_bar(item[1], item[2])
                elif item[0] == "done":
                    self._finish(item[1], item[2])
                else:
                    self._fail(item[1])
        except queue.Empty:
            pass
        self.after(100, self._poll)

    def _update_bar(self, done, total):
        self.bar["value"] = 100 if total == 0 else 100 * done / total

    def _finish(self, mode, out):
        self._busy = False
        self.btn_enc.state(["!disabled"])
        self.btn_dec.state(["!disabled"])
        self.bar["value"] = 100
        verb = "mã hóa" if mode == "enc" else "giải mã"
        self.msg_var.set(f"Đã {verb} xong: {out}")
        self._preview(out)

    def _fail(self, text):
        self._busy = False
        self.btn_enc.state(["!disabled"])
        self.btn_dec.state(["!disabled"])
        self.msg_var.set(f"Lỗi: {text}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tab File")
    FileTab(root).pack(fill="both", expand=True)
    root.mainloop()


