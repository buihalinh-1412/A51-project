import pytest

from src.file_crypto import crypt_bytes, encrypt_file, decrypt_file


KEY_A = "1223456789ABCDEF"
KEY_B = "FEDCBA9876543210"
FRAME = 0


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"A",
        bytes(range(56)),
        bytes(range(57)),
        bytes(range(58)),
        bytes(range(256)) * 40,  # 10 KB
    ],
    ids=[
        "0B",
        "1B",
        "56B",
        "57B",
        "58B",
        "10KB",
    ],
)
def test_crypt_bytes_round_trip(data):
    """Mã hóa hai lần với cùng khóa và frame phải thu lại dữ liệu gốc."""
    encrypted = crypt_bytes(data, KEY_A, FRAME)
    decrypted = crypt_bytes(encrypted, KEY_A, FRAME)

    assert decrypted == data


def test_wrong_key_does_not_recover_plaintext():
    """Giải bằng khóa khác không được trả về bản rõ ban đầu."""
    data = b"Hello A5/1 - file crypto test"

    encrypted = crypt_bytes(data, KEY_A, FRAME)
    wrong_decrypted = crypt_bytes(encrypted, KEY_B, FRAME)

    assert wrong_decrypted != data


def test_encrypt_decrypt_file_round_trip(tmp_path):
    """Mã hóa rồi giải mã file phải giữ nguyên nội dung."""
    original_data = bytes(range(256)) * 4

    input_file = tmp_path / "input.bin"
    encrypted_file = tmp_path / "encrypted.bin"
    decrypted_file = tmp_path / "decrypted.bin"

    input_file.write_bytes(original_data)

    encrypt_file(
        input_file,
        encrypted_file,
        KEY_A,
        start_frame=FRAME,
    )

    decrypt_file(
        encrypted_file,
        decrypted_file,
        KEY_A,
    )

    assert decrypted_file.read_bytes() == original_data


def test_encrypt_file_same_input_output_raises_value_error(tmp_path):
    """Không được ghi file mã hóa đè lên chính file đầu vào."""
    file_path = tmp_path / "same_file.txt"
    file_path.write_bytes(b"Hello A5/1")

    with pytest.raises(ValueError):
        encrypt_file(
            file_path,
            file_path,
            KEY_A,
            start_frame=FRAME,
        )


def test_invalid_key_length_raises_value_error():
    """Khóa không đủ 16 ký tự hex phải bị từ chối."""
    invalid_key = "1234"

    with pytest.raises(ValueError):
        crypt_bytes(
            b"Hello",
            invalid_key,
            FRAME,
        )


def test_invalid_key_for_encrypt_file_raises_value_error(tmp_path):
    """encrypt_file cũng phải từ chối khóa sai độ dài."""
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.enc"

    input_file.write_bytes(b"Hello A5/1")

    with pytest.raises(ValueError):
        encrypt_file(
            input_file,
            output_file,
            "1234",
            start_frame=FRAME,
        )
from src.a51 import A51
from src.file_crypto import crypt_bytes, _bits_to_bytes


def test_crypt_bytes_khop_voi_a51():
    key, frame = "1223456789ABCDEF", 0x134
    # Mã hóa 57 byte 0 thì kết quả chính là dòng khóa của 2 khung
    ks = crypt_bytes(bytes(57), key, frame)
    down1, up1 = A51(key, frame).generate_keystream()
    down2, up2 = A51(key, frame + 1).generate_keystream()
    assert ks == _bits_to_bytes(down1 + up1 + down2 + up2)
