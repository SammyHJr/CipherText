"""Command-line and windowed entrypoint for the CipherText app."""

from __future__ import annotations

import argparse
import sys

from .core import decrypt, encrypt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch CipherText with a windowed UI or prefill values from the command line."
    )
    parser.add_argument("text", nargs="?", default="", help="Optional text to prefill")
    parser.add_argument(
        "--shift",
        type=int,
        default=3,
        help="Caesar cipher shift amount (default: 3)",
    )
    parser.add_argument(
        "--decrypt",
        action="store_true",
        help="Prefill the UI in decrypt mode",
    )
    return parser.parse_args()


def launch_gui(text: str = "", shift: int = 3, decrypt_mode: bool = False) -> None: ##launch the gui
    try:
        import tkinter as tk    # Importing tkinter for GUI functionality, with a fallback to CLI if it's not available
        from tkinter import messagebox  # Importing messagebox for displaying informational and error messages in the GUI
    except ImportError:
        print("Tkinter is not available. Falling back to command-line mode.")
        return run_cli(text, shift, decrypt_mode)

    root = tk.Tk()
    root.title("CipherText")        # Name of the program
    root.geometry("800x800")        # Set a fixed window size
    root.configure(bg="#ffffff")  # Set a light background color for better aesthetics
    root.resizable(False, False)      # Enable resizing to maintain layout integrity

    tk.Label(
        root, 
        text="Enter text:",
        background="#ffffff"
    ).pack(anchor="w", padx=10, pady=(10, 0))  # Label for the input text area
    
    input_text = tk.Text(   # this is the text area where the user will input the text to be encrypted or decrypted
        root,
        height=8,
        wrap="word",
        bd=2,
        relief="solid",
        bg="#ffffff",
        highlightthickness=1,
        highlightbackground="#cccccc",
        insertbackground="black",
    )                          
    input_text.pack(fill="both", padx=10, pady=(0, 10))                         # Pack the input text area to fill the available space with padding
    input_text.insert("1.0", text)                                              # Prefill the input text area with the provided text argument

    options_frame = tk.Frame(root, bg="#ffffff")
    options_frame.pack(fill="x", padx=10)

    shift_var = tk.IntVar(value=shift)
    decrypt_var = tk.BooleanVar(value=decrypt_mode)
    substitution_key_var = tk.StringVar(value="QWERTYUIOPASDFGHJKLZXCVBNM")

    tk.Label(
        options_frame,
        text="Shift:",
        bg="#ffffff",
    ).grid(row=0, column=0, sticky="w")
    
    tk.Spinbox(
        options_frame,
        from_=-25,
        to=25,
        textvariable=shift_var,
        width=5,
        bg="#ffffff",
        fg="black",
        insertbackground="black",
        relief="solid",
        bd=1,
    ).grid(row=0, column=1, sticky="w", padx=(5, 20))  # Spinbox for selecting the shift value, allowing values from -25 to 25
    tk.Checkbutton(
        options_frame,
        text="Decrypt",
        variable=decrypt_var,
        bg="#ffffff",
        activebackground="#ffffff",
        selectcolor="#ffffff",
    ).grid(row=0, column=2, sticky="w")

    tk.Label(
        options_frame,
        text="Key:",
        bg="#ffffff",
    ).grid(row=1, column=0, sticky="w", pady=(8, 0))
    tk.Entry(
        options_frame,
        textvariable=substitution_key_var,
        width=30,
        bg="#ffffff",
        fg="black",
        insertbackground="black",
        relief="solid",
        bd=1,
    ).grid(row=1, column=1, columnspan=2, sticky="w", padx=(5, 0), pady=(8, 0))

    tk.Label(root, text="Result:", bg="#ffffff").pack(anchor="w", padx=10, pady=(10, 0))
    output_text = tk.Text(
        root,
        height=8,
        wrap="word",
        state="disabled",
        bd=2,
        relief="solid",
        bg="#ffffff",
        highlightthickness=1,
        highlightbackground="#cccccc",
        fg="black",
        insertbackground="black",
    )                          # Text area for displaying the output result, set to disabled to
    output_text.pack(fill="both", padx=10, pady=(0, 10))

    def process_text() -> None:
        input_value = input_text.get("1.0", "end-1c")
        if not input_value.strip():
            messagebox.showinfo("CipherText", "Please enter text to process.")
            return

        try:
            current_shift = int(shift_var.get())
        except (ValueError, tk.TclError):
            messagebox.showerror("CipherText", "Shift must be a number.")
            return

        if decrypt_var.get():
            result = decrypt(input_value, shift=current_shift)
        else:
            result = encrypt(input_value, shift=current_shift)

        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", result)
        output_text.config(state="disabled")

    def process_substitution() -> None:
        input_value = input_text.get("1.0", "end-1c")
        if not input_value.strip():
            messagebox.showinfo("CipherText", "Please enter text to process.")
            return

        if decrypt_var.get():
            result = decrypt(input_value, cipher="substitution")
        else:
            result = encrypt(input_value, cipher="substitution")

        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", result)
        output_text.config(state="disabled")
    def process_substitution() -> None:
        input_value = input_text.get("1.0", "end-1c")
        if not input_value.strip():
            messagebox.showinfo("CipherText", "Please enter text to process.")
            return

        current_key = substitution_key_var.get().strip()
        if not current_key:
            messagebox.showerror("CipherText", "Please enter a substitution key.")
            return

        try:
            if decrypt_var.get():
                result = decrypt(input_value, cipher="substitution", key=current_key)
            else:
                result = encrypt(input_value, cipher="substitution", key=current_key)
        except ValueError as exc:
            messagebox.showerror("CipherText", str(exc))
            return

        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", result)
        output_text.config(state="disabled")
    button_frame = tk.Frame(root, bg="#ffffff")
    button_frame.pack(fill="x", padx=10, pady=(0, 10))

    tk.Button(
        button_frame,
        text="Run",
        command=process_text,
        bg="#000000",
        fg="white",
        activebackground="#313131",
        activeforeground="black",
        bd=0,
        relief="flat",
        padx=12,
        pady=6,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
    ).pack(side="left")
    tk.Button(
        button_frame, 
        text="Clear", 
        command=lambda: input_text.delete("1.0", "end"),
        bg="#000000",
        fg="white",
        activebackground="#313131",
        activeforeground="black",
        bd=0,
        relief="raised",
        padx=12,
        pady=6,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
    ).pack(side="left", padx=10)
    tk.Button(
        button_frame,
        text="Substitution",
        command=process_substitution,
        bg="#000000",
        fg="white",
        activebackground="#313131",
        activeforeground="black",
        bd=0,
        relief="flat",
        padx=12,
        pady=6,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
    ).pack(side="left", padx=10)
    tk.Button(
        button_frame, 
        text="Quit", 
        command=root.destroy,
        bg="#000000",
        fg="white",
        activebackground="#313131",
        activeforeground="black",
        bd = 0,
        relief="ridge",
        padx=12,
        pady=6,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
    ).pack(side="right")

    root.mainloop()


def run_cli(text: str, shift: int, decrypt_mode: bool) -> None:
    if decrypt_mode:
        output = decrypt(text, shift=shift)
    else:
        output = encrypt(text, shift=shift)
    print(output)


def main() -> None:
    args = parse_args()
    if "-h" in sys.argv or "--help" in sys.argv:
        return
    launch_gui(text=args.text, shift=args.shift, decrypt_mode=args.decrypt)


if __name__ == "__main__":
    main()
