from modes import Modes
import ttkbootstrap as tb
from tile import Tile
import random


class MineSweeper:
    def __init__(self, difficulty):
        self.mode = Modes().modes[difficulty]
        self.init_root()

    def init_root(self):
        root = tb.Window(themename="darkly")
        root.title(f"Minesweeper {self.mode['name']}")
        root.geometry("800x600")

        self.root = root
        self.init_scoreboard()
        self.init_canvas()
        self.init_game()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.start()

    def init_scoreboard(self):
        scoreBoard = tb.Frame(self.root)
        scoreBoard.pack(anchor="nw", padx=20, pady=10)

        tb.Label(scoreBoard, text="Score ", font=("Segoe UI", 16, "bold")).pack(
            side="left", padx=(20, 0)
        )
        self.score = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        self.score.pack(side="left")

        tb.Label(scoreBoard, text="Mines ", font=("Segoe UI", 16, "bold")).pack(
            side="left", padx=(20, 0)
        )
        self.mines = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        self.mines.pack(side="left")

        tb.Label(scoreBoard, text="Moves ", font=("Segoe UI", 16, "bold")).pack(
            side="left", padx=(200, 0)
        )
        self.moves = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        self.moves.pack(side="left")

        tb.Label(scoreBoard, text="Time ", font=("Segoe UI", 16, "bold")).pack(
            side="left", padx=(60, 0)
        )
        self.time = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        self.time.pack(side="left")

    def init_canvas(self):
        self.canvas = tb.Canvas(self.root, width=700, height=500, bd=3, relief="solid")
        self.canvas.pack(pady=20)

    def init_game(self):
        self.canvas.update()
        self.w = self.mode["w"]
        self.h = self.mode["h"]
        self.grid = []
        self.tileSize = min(
            self.canvas.winfo_width() // self.w,
            self.canvas.winfo_height() // self.h,
            50,
        )
        self.offsetX = (self.canvas.winfo_width() - self.tileSize * self.w) // 2
        self.offsetY = (self.canvas.winfo_height() - self.tileSize * self.h) // 2

        for x in range(self.w):
            self.grid.append([])
            for y in range(self.h):
                self.grid[x].append(
                    Tile(self.canvas, x, y, self.tileSize, self.offsetX, self.offsetY)
                )
                self.grid[x][y].draw()

        self.minesPlaced = False
        self.minesLeft = self.mode["mines"]
        self.mines.config(text=str(self.minesLeft))

    def start(self):
        self.root.mainloop()

    def on_canvas_click(self, event):
        gx = (event.x - self.offsetX) // self.tileSize
        gy = (event.y - self.offsetY) // self.tileSize

        if gx < 0 or gy < 0 or gx >= self.w or gy >= self.h:
            return

        tile = self.grid[gx][gy]

        if not self.minesPlaced:
            self.place_mines(gx, gy)
            self.minesPlaced = True

        tile.show()

    def on_right_click(self, event):
        gx = (event.x - self.offsetX) // self.tileSize
        gy = (event.y - self.offsetY) // self.tileSize

        if gx < 0 or gy < 0 or gx >= self.w or gy >= self.h:
            return

        tile = self.grid[gx][gy]
        tile.flagged = not tile.flagged
        if tile.flagged:
            self.minesLeft -= 1
        else:
            self.minesLeft += 1
        self.mines.config(text=str(self.minesLeft))
        tile.show(flag=tile.flagged)

    def place_mines(self, safe_x, safe_y):
        placed = 0
        forbidden = {
            (safe_x + dx, safe_y + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if 0 <= safe_x + dx < self.w and 0 <= safe_y + dy < self.h
        }

        while placed < self.mode["mines"]:
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            if (x, y) in forbidden:
                continue
            tile = self.grid[x][y]
            if not tile.isMine:
                tile.setMine()
                placed += 1

        for x in range(self.w):
            for y in range(self.h):
                self.grid[x][y].setGrid(self.grid)


ms = MineSweeper("easy")
