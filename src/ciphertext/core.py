"""CipherText core encryption utilities."""

from __future__ import annotations


def _shift_char(char: str, shift: int) -> str:
    if char.isupper():
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif char.islower():
        alphabet = "abcdefghijklmnopqrstuvwxyz"
    else:
        return char

    index = alphabet.index(char)
    return alphabet[(index + shift) % len(alphabet)]


def caesar_encrypt(text: str, shift: int = 3) -> str:
    """Encrypt text using a Caesar cipher."""
    shift = shift % 26
    return "".join(_shift_char(char, shift) for char in text)


def caesar_decrypt(text: str, shift: int = 3) -> str:
    """Decrypt text encrypted with a Caesar cipher."""
    return caesar_encrypt(text, -shift)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SUBSTITUTION_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"


def _normalize_key(key: str) -> str:
    return "".join(ch.upper() for ch in key if ch.isalpha())


def _validate_substitution_key(key: str) -> str:
    normalized = _normalize_key(key)
    if len(normalized) == 0:
        raise ValueError("Substitution key must contain at least one letter.")
    if len(normalized) > 26:
        raise ValueError("Substitution key must contain at most 26 letters.")

    unique_key = []
    seen = set()
    for ch in normalized:
        if ch not in seen:
            seen.add(ch)
            unique_key.append(ch)

    for ch in ALPHABET:
        if ch not in seen:
            unique_key.append(ch)
            if len(unique_key) == 26:
                break

    return "".join(unique_key)


def _make_substitution_maps(key: str) -> tuple[dict[str, str], dict[str, str]]:
    substitution_key = _validate_substitution_key(key)
    forward = {plain: cipher for plain, cipher in zip(ALPHABET, substitution_key)}
    backward = {cipher: plain for plain, cipher in zip(ALPHABET, substitution_key)}
    return forward, backward


def substitution_encrypt(text: str, key: str = SUBSTITUTION_KEY) -> str:
    """Encrypt text using a substitution cipher with the provided key."""
    forward, _ = _make_substitution_maps(key)
    lower_forward = {plain.lower(): cipher.lower() for plain, cipher in forward.items()}
    result = []
    for char in text:
        if char.isupper():
            result.append(forward.get(char, char))
        elif char.islower():
            result.append(lower_forward.get(char, char))
        else:
            result.append(char)
    return "".join(result)


def substitution_decrypt(text: str, key: str = SUBSTITUTION_KEY) -> str:
    """Decrypt text encrypted with a substitution cipher with the provided key."""
    _, backward = _make_substitution_maps(key)
    lower_backward = {cipher.lower(): plain.lower() for cipher, plain in backward.items()}
    result = []
    for char in text:
        if char.isupper():
            result.append(backward.get(char, char))
        elif char.islower():
            result.append(lower_backward.get(char, char))
        else:
            result.append(char)
    return "".join(result)


def encrypt(text: str, shift: int = 3, cipher: str = "caesar", key: str = SUBSTITUTION_KEY) -> str:
    """Encrypt text with the selected cipher."""
    if cipher == "caesar":
        return caesar_encrypt(text, shift)
    if cipher == "substitution":
        return substitution_encrypt(text, key=key)
    raise ValueError(f"Unsupported cipher: {cipher}")


def decrypt(text: str, shift: int = 3, cipher: str = "caesar", key: str = SUBSTITUTION_KEY) -> str:
    """Decrypt text with the selected cipher."""
    if cipher == "caesar":
        return caesar_decrypt(text, shift)
    if cipher == "substitution":
        return substitution_decrypt(text, key=key)
    raise ValueError(f"Unsupported cipher: {cipher}")
