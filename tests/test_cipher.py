from ciphertext import decrypt, encrypt


def test_caesar_encrypt_default() -> None:
    assert encrypt("Hello, World!") == "Khoor, Zruog!"


def test_caesar_encrypt_with_shift() -> None:
    assert encrypt("abc xyz", shift=1) == "bcd yza"


def test_caesar_decrypt_default() -> None:
    assert decrypt("Khoor, Zruog!") == "Hello, World!"
