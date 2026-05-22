from ciphertext import decrypt, encrypt


def test_caesar_encrypt_default() -> None:
    assert encrypt("Hello, World!") == "Khoor, Zruog!"


def test_caesar_encrypt_with_shift() -> None:
    assert encrypt("abc xyz", shift=1) == "bcd yza"


def test_caesar_decrypt_default() -> None:
    assert decrypt("Khoor, Zruog!") == "Hello, World!"


def test_substitution_encrypt_default() -> None:
    assert encrypt("abc xyz", cipher="substitution") == "qwe bnm"


def test_substitution_decrypt_default() -> None:
    assert decrypt("qwe bnm", cipher="substitution") == "abc xyz"


def test_substitution_encrypt_with_user_key() -> None:
    user_key = "MNBVCXZLKJHGFDSAPOIUYTREWQ"
    cipher_text = encrypt("abc xyz", cipher="substitution", key=user_key)
    assert decrypt(cipher_text, cipher="substitution", key=user_key) == "abc xyz"


def test_substitution_key_validation() -> None:
    try:
        encrypt("hello", cipher="substitution", key="shortkey")
    except ValueError as exc:
        assert "26 letters" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid substitution key")
