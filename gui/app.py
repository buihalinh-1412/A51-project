"""Cửa sổ chính của ứng dụng demo A5/1 và TinyA5/1 (Tkinter).

Chạy từ thư mục gốc dự án:  python -m gui.app
Mỗi tab nạp bằng try/except ImportError: nếu file tab chưa có thì hiện nhãn
"Chưa có" để ứng dụng vẫn mở được.
Người phụ trách: Nguyễn Thị Nhật Linh.
"""

import importlib
import tkinter as tk
from tkinter import ttk

# (tiêu đề tab, tên module, tên class)
TABS = [
    ("TinyA5/1", "gui.tab_tiny", "TinyTab"),
    ("A5/1 Text", "gui.tab_a51_text", "A51TextTab"),
    ("Mã hóa File", "gui.tab_file", "FileTab"),
    ("Tấn công", "gui.tab_attack", "AttackTab"),
]


class App(tk.Tk):
    """Cửa sổ chính gồm một Notebook 4 tab."""

    def __init__(self):
        super().__init__()
        self.title("Demo A5/1 và TinyA5/1")
        self.geometry("860x600")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)
        self.tabs = {}
        for title, module_name, class_name in TABS:
            self.tabs[title] = self._load_tab(title, module_name, class_name)

    def _load_tab(self, title, module_name, class_name):
        """Nạp một tab; thiếu file hoặc class thì thay bằng nhãn 'Chưa có'."""
        try:
            module = importlib.import_module(module_name)
            tab = getattr(module, class_name)(self.notebook)
        except (ImportError, AttributeError):
            tab = ttk.Frame(self.notebook)
            ttk.Label(tab, text="Chưa có", font=("TkDefaultFont", 14)).pack(
                expand=True)
        self.notebook.add(tab, text=title)
        return tab


if __name__ == "__main__":
    App().mainloop()
