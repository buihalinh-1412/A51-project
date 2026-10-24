# A5/1 Project

Project môn An toàn và bảo mật thông tin.

## Members
- Bùi Hà Linh
- Lại Hoàng Thế Vũ
- Hoàng Yến Nhi
- Nguyễn Thị Nhật Linh
- Trần Đại Lộc

# A5/1 và TinyA5/1

Đồ án môn An toàn và bảo mật thông tin: cài đặt hệ mã dòng TinyA5/1 và A5/1 bằng Python thuần, không dùng thư viện mật mã có sẵn cho phần lõi.

## Yêu cầu

- Python 3.10 trở lên
- Tkinter (có sẵn trong bộ cài Python chính thức; trên Linux có thể cần `sudo apt install python3-tk`)
- pytest (xem `requirements.txt`)

## Cài đặt

1. Clone repository và vào thư mục dự án:

```bash
git clone <URL-repository>
cd A51-project
```

2. Cài thư viện:

```bash
pip install -r requirements.txt
```

## Chạy chương trình

Chạy các lệnh sau ở thư mục gốc của dự án.

**Giao diện đồ họa (GUI):**

```bash
python -m gui.app
```

**Giao diện dòng lệnh (CLI):**

```bash
python demo_cli.py
```

**Kiểm thử:**

```bash
python -m pytest tests/ -v
```

**Đo tốc độ:**

```bash
python -m src.benchmark
```

Nếu gặp lỗi `No module named 'src'`, chạy lại lệnh trên ở thư mục gốc, hoặc đặt biến môi trường `PYTHONPATH`:
- PowerShell: `$env:PYTHONPATH="."`
- Linux/macOS: `export PYTHONPATH=.`

## Cấu trúc thư mục

```
A51-project/
├── src/                   # Mã nguồn lõi (a51, tiny_a51, file_crypto, benchmark...)
├── gui/                   # Mã nguồn giao diện Tkinter
├── tests/                 # Bộ kiểm thử tự động (pytest)
├── examples/              # Tệp mẫu phục vụ demo & tấn công
├── docs/                  # Báo cáo, tài liệu đặc tả & bằng chứng kiểm thử
├── demo_cli.py            # Chương trình chạy CLI
├── requirements.txt       # Danh sách thư viện phụ thuộc
└── README.md              # Tài liệu hướng dẫn sử dụng
```

