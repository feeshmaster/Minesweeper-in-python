import tkinter as tk

root = tk.Tk()
root.title("Minesweeper!")
root.geometry("800x600")

canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, 
                   width=canvas_width, 
                   height=canvas_height, 
                   bg="black")

canvas.pack(pady=20, padx=20)




root.mainloop()