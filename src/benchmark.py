import csv
import os
import sys
import time
from pathlib import Path


# Cho phép chạy trực tiếp bằng:
# python src/benchmark.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.file_crypto import crypt_bytes


KEY_HEX = "1223456789ABCDEF"
START_FRAME = 0

DEFAULT_SIZES = (
    1024,
    10240,
    51200,
    102400,
)


def run_benchmark(sizes=DEFAULT_SIZES) -> list:
    """
    Đo tốc độ crypt_bytes với các kích thước dữ liệu khác nhau.

    Mỗi phần tử kết quả có dạng:
    {
        "size": int,
        "seconds": float,
        "kib_per_s": float
    }
    """
    results = []

    for size in sizes:
        data = os.urandom(size)

        start = time.perf_counter()

        crypt_bytes(
            data,
            KEY_HEX,
            START_FRAME,
        )

        end = time.perf_counter()

        seconds = end - start
        kib_per_s = size / 1024 / seconds

        results.append(
            {
                "size": size,
                "seconds": seconds,
                "kib_per_s": kib_per_s,
            }
        )

    return results


def save_csv(results, output_path=None):
    """Ghi kết quả benchmark vào docs/benchmark.csv."""
    if output_path is None:
        output_path = PROJECT_ROOT / "docs" / "benchmark.csv"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "size",
                "seconds",
                "kib_per_s",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    return output_path


def print_results(results):
    """In bảng kết quả benchmark ra Terminal."""
    print(
        f"{'Kich thuoc':<15}"
        f"{'Thoi gian (s)':<20}"
        f"{'KiB/s':<15}"
    )

    print("-" * 50)

    for result in results:
        size_kib = result["size"] / 1024

        print(
            f"{size_kib:<15.2f}"
            f"{result['seconds']:<20.6f}"
            f"{result['kib_per_s']:<15.2f}"
        )


if __name__ == "__main__":
    benchmark_results = run_benchmark()

    print_results(benchmark_results)

    csv_path = save_csv(benchmark_results)

    print()
    print(f"Da ghi ket qua vao: {csv_path}")
