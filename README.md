# CipherText

A simple cipher app that encrypts and decrypts text using a Caesar cipher.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Usage

Run the app and open the CipherText window:

```bash
python -m ciphertext
```

The window lets you enter text, choose a shift amount, and toggle decrypt mode.

Optional prefill values from the command line:

```bash
python -m ciphertext "Hello, World!" --shift 3
```

```bash
python -m ciphertext "Khoor, Zruog!" --shift 3 --decrypt
```

If the package is installed, you can also run:

```bash
ciphertext
```
