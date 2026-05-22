"""Local wrapper package for CipherText development."""

from __future__ import annotations

import os
from pathlib import Path

pkg_dir = Path(__file__).resolve().parent
src_ciphertext = pkg_dir.parent / "src" / "ciphertext"
if str(src_ciphertext) not in __path__:
    __path__.insert(0, str(src_ciphertext))

from .core import caesar_decrypt, caesar_encrypt, decrypt, encrypt

__all__ = ["caesar_encrypt", "caesar_decrypt", "encrypt", "decrypt"]
__version__ = "0.1.0"
