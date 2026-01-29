import tkinter as tk
from modes import Modes
from tkinter import ttk
import ttkbootstrap as tb
import minesweeper as ms

class GameSelector:
    def __init__(self, Root=None):
        root = Root if not Root == None else tb.Window(themename="darkly")
        for widget in root.winfo_children():
            widget.destroy()
        root.title("Minesweeper gamemode selection")
        root.geometry("400x300")
        root.resizable(False, False)
        modes = Modes().modesArray()

        label = tb.Label(root, text="Pick Your Difficulty!", font=("Segoe UI", 16))
        label.pack(pady=10)

        modes_var = tk.StringVar(root)
        modes_var.set(modes[0])

        dropdown = ttk.Combobox(root, textvariable=modes_var, values=modes, state="readonly")
        dropdown.pack(pady=15)

        def onclick():
            diff = modes_var.get()
            for widget in root.winfo_children():
                widget.destroy()

            ms.MineSweeper(diff, root)

        submit = tb.Button(root, text="Play", width=16, command=onclick)
        submit.pack(pady=5)

        if not Root:
            root.mainloop()
if __name__ == "__main__":
    GameSelector()
