"""Tab A5/1 Text: mã hóa và giải mã một đoạn văn bản ngắn.

Dùng crypt_bytes của src/file_crypto.py; không tự cài lại thuật toán.
Người phụ trách: Nguyễn Thị Nhật Linh.
"""

import tkinter as tk
from tkinter import ttk

from src.file_crypto import crypt_bytes

SAMPLE_KEY = "1223456789ABCDEF"
SAMPLE_FRAME = 0x134  # = 308


def parse_key(text):
    """Kiểm tra khóa 16 ký tự hex; trả về khóa viết hoa, sai thì ném ValueError."""
    key = text.strip()
    if len(key) != 16 or any(c not in "0123456789abcdefABCDEF" for c in key):
        raise ValueError("Khóa phải gồm đúng 16 ký tự hex (0-9, A-F).")
    return key.upper()


def parse_frame(text):
    """Đọc số khung (thập phân hoặc 0x...); sai thì ném ValueError."""
    try:
        frame = int(text.strip() or "0", 0)
    except ValueError:
        raise ValueError("Số khung phải là số nguyên, ví dụ 308 hoặc 0x134.")
    if frame < 0:
        raise ValueError("Số khung không được âm.")
    return frame


def encrypt_text(text, key_text, frame_text):
    """Văn bản -> chuỗi hex bản mã."""
    key = parse_key(key_text)
    frame = parse_frame(frame_text)
    return crypt_bytes(text.encode("utf-8"), key, frame).hex().upper()


def decrypt_hex(hex_text, key_text, frame_text):
    """Chuỗi hex bản mã -> văn bản."""
    key = parse_key(key_text)
    frame = parse_frame(frame_text)
    cleaned = "".join(hex_text.split())
    try:
        data = bytes.fromhex(cleaned)
    except ValueError:
        raise ValueError("Bản mã phải là chuỗi hex hợp lệ (cặp ký tự 0-9, A-F).")
    return crypt_bytes(data, key, frame).decode("utf-8", errors="replace")


class A51TextTab(ttk.Frame):
    """Giao diện mã hóa / giải mã văn bản bằng A5/1."""

    def __init__(self, parent):
        super().__init__(parent)
        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=8)
        ttk.Label(form, text="Khóa (16 ký tự hex):").grid(row=0, column=0, sticky="w")
        self.key_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.key_var, width=24).grid(
            row=0, column=1, padx=6)
        ttk.Label(form, text="Số khung:").grid(row=0, column=2, sticky="w")
        self.frame_var = tk.StringVar(value="0")
        ttk.Entry(form, textvariable=self.frame_var, width=10).grid(
            row=0, column=3, padx=6)
        ttk.Button(form, text="Nạp khóa mẫu", command=self.load_sample).grid(
            row=0, column=4, padx=6)

        ttk.Label(self, text="Văn bản:").pack(anchor="w", padx=10)
        self.plain_box = tk.Text(self, height=6)
        self.plain_box.pack(fill="x", padx=10, pady=4)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=10, pady=4)
        ttk.Button(buttons, text="Mã hóa", command=self.do_encrypt).pack(side="left")
        ttk.Button(buttons, text="Giải mã", command=self.do_decrypt).pack(
            side="left", padx=8)

        ttk.Label(self, text="Bản mã (hex):").pack(anchor="w", padx=10)
        self.cipher_box = tk.Text(self, height=6)
        self.cipher_box.pack(fill="x", padx=10, pady=4)

        self.message_var = tk.StringVar()
        self.message = ttk.Label(self, textvariable=self.message_var)
        self.message.pack(anchor="w", padx=10, pady=6)

    def load_sample(self):
        """Điền khóa mẫu 1223456789ABCDEF và khung 0x134 (= 308)."""
        self.key_var.set(SAMPLE_KEY)
        self.frame_var.set(str(SAMPLE_FRAME))
        self.message_var.set("Đã nạp khóa mẫu và số khung 308 (0x134).")

    @staticmethod
    def _set_text(box, value):
        box.delete("1.0", "end")
        box.insert("1.0", value)

    def do_encrypt(self):
        """Đọc ô văn bản, hiện bản mã dạng hex ở ô dưới."""
        try:
            text = self.plain_box.get("1.0", "end-1c")
            result = encrypt_text(text, self.key_var.get(), self.frame_var.get())
        except ValueError as error:
            self.message_var.set("Lỗi: " + str(error))
            return
        self._set_text(self.cipher_box, result)
        self.message_var.set("Đã mã hóa xong (%d byte)." % (len(result) // 2))

    def do_decrypt(self):
        """Đọc ô hex, hiện lại văn bản ở ô trên."""
        try:
            hex_text = self.cipher_box.get("1.0", "end-1c")
            result = decrypt_hex(hex_text, self.key_var.get(), self.frame_var.get())
        except ValueError as error:
            self.message_var.set("Lỗi: " + str(error))
            return
        self._set_text(self.plain_box, result)
        self.message_var.set("Đã giải mã xong.")
