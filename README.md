# Hệ mã dòng A5/1 và TinyA5/1

Đồ án môn **An toàn và bảo mật thông tin** — cài đặt hệ mã dòng A5/1 và phiên bản thu nhỏ TinyA5/1 bằng Python thuần, không dùng thư viện mật mã có sẵn cho phần lõi.

## Thành viên nhóm 5

| Họ và tên | MSSV |
|---|---|
| Bùi Hà Linh (nhóm trưởng) | 11240066 |
| Lại Hoàng Thế Vũ | 11245824 |
| Hoàng Yến Nhi | 11242041 |
| Trần Đại Lộc | 11240736 |
| Nguyễn Thị Nhật Linh | 11245415 |

## Yêu cầu môi trường

- Python 3.10 trở lên
- Tkinter (có sẵn trong bộ cài Python chính thức; trên Linux có thể cần `sudo apt install python3-tk`)
- pytest (khai báo trong `requirements.txt`)

## Cài đặt

```bash
git clone https://github.com/buihalinh-1412/A51-project.git
cd A51-project
pip install -r requirements.txt
```

## Chạy chương trình

Chạy các lệnh sau ở thư mục gốc của dự án.

| Lệnh | Chức năng |
|---|---|
| `python -m gui.app` | Mở giao diện đồ họa (4 tab) |
| `python demo_cli.py` | Mở giao diện dòng lệnh dạng menu |
| `python -m pytest tests/ -v` | Chạy toàn bộ bộ kiểm thử (kết quả mong đợi: 51 passed) |
| `python tests/run_verification.py` | Đối chiếu test vector GSM (kết quả mong đợi: PASS) |
| `python src/benchmark.py` | Đo tốc độ và ghi `docs/benchmark.csv` |

> Nếu gặp lỗi `No module named 'src'`, đặt biến môi trường trước khi chạy:
> - PowerShell: `$env:PYTHONPATH="."`
> - Linux/macOS: `export PYTHONPATH=.`

## Cấu trúc thư mục

```
A51-project/
├── src/              # Mã nguồn lõi (a51, tiny_a51, file_crypto, benchmark...)
├── gui/              # Giao diện đồ họa Tkinter (4 tab)
├── tests/            # Bộ kiểm thử tự động (pytest)
├── examples/         # File văn bản mẫu phục vụ demo tấn công
├── docs/             # Tài liệu đặc tả, sơ đồ và bằng chứng kiểm thử
├── demo_cli.py       # Giao diện dòng lệnh
├── requirements.txt  # Thư viện phụ thuộc
└── README.md
```