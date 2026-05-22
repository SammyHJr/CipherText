"""Launcher wrapper for the CipherText app."""

from __future__ import annotations

from . import __main__ as app_main


def main() -> None:
    app_main.main()


if __name__ == "__main__":
    main()
