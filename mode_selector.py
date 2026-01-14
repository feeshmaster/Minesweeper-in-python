import tkinter as tk
from modes import Modes
from tkinter import ttk

root = tk.Tk()
root.title("Minesweeper gamemode selection")
root.geometry("400x300")
modes = Modes().modesArray()


modes_var = tk.StringVar(root)
modes_var.set(modes[0])

dropdown = ttk.Combobox(root, textvariable=modes_var, values=modes, state="readonly")
dropdown.pack()



root.mainloop()