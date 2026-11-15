"""Optional Tkinter graphical interface."""

import tkinter as tk
from tkinter import ttk
from .analyzer import analyze_safe


def main() -> None:
    root = tk.Tk()
    root.title("Arithmetic Expression Analyzer")
    root.geometry("800x650")
    ttk.Label(root, text="Expression:").pack(anchor="w", padx=10, pady=(10, 0))
    entry = ttk.Entry(root)
    entry.pack(fill="x", padx=10)
    output = tk.Text(root, wrap="none")
    output.pack(fill="both", expand=True, padx=10, pady=10)

    def run() -> None:
        output.delete("1.0", tk.END)
        output.insert("1.0", analyze_safe(entry.get()))

    ttk.Button(root, text="Analyze", command=run).pack(pady=(0, 10))
    root.mainloop()


if __name__ == "__main__":
    main()
