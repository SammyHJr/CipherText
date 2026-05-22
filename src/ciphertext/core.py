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


def encrypt(text: str, shift: int = 3, cipher: str = "caesar") -> str:
    """Encrypt text with the selected cipher."""
    if cipher != "caesar":
        raise ValueError(f"Unsupported cipher: {cipher}")
    return caesar_encrypt(text, shift)


def decrypt(text: str, shift: int = 3, cipher: str = "caesar") -> str:
    """Decrypt text with the selected cipher."""
    if cipher != "caesar":
        raise ValueError(f"Unsupported cipher: {cipher}")
    return caesar_decrypt(text, shift)
