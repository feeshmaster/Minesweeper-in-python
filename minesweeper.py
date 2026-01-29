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
        self.ticks = 0
        self.movesMade = 0
        self.lost = False
        self.root = root
        self.init_scoreboard()
        self.init_canvas()
        self.init_game()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.time.update()
        self.moves.update()
        self.tick()
        self.start()

    def create_popup(self, t):
        top = tb.Toplevel(self.root)
        top.title("Message")
        top.geometry("300x140")
        top.resizable(False, False)

        top.grab_set()

        tb.Label(
        top,
        text=t,
        bootstyle="info",
        font=("Segoe UI", 12, "bold")

    ).pack(pady=(25, 15))

        tb.Button(
        top,
        text="Close",
        command=lambda: self.close((top, self.root)),
        bootstyle="danger"
    ).pack(pady=10)
    def close(self, t):
        for i in t:
            i.destroy()
    def init_scoreboard(self):
        scoreBoard = tb.Frame(self.root, background=self.root.cget('bg'))
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
            side="left", padx=(160, 0)
        )
        self.moves = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        self.moves.pack(side="left")

        tb.Label(scoreBoard, text="Time ", font=("Segoe UI", 16, "bold")).pack(
            side="left", padx=(10, 0)
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
        if not tile.shown:
            self.movesMade += 1 
            self.moves.config(text=str(self.movesMade)) 
        if tile.isMine and not tile.flagged:
            self.lose()
        tile.show()
        self.winCheck()
        
        
        
    def winCheck(self):
        mines = self.mode["mines"]
        right = 0
        unshown = 0
        for x in self.grid:
            for tile in x:
                if not tile.shown:
                    unshown += 1
                    if tile.isMine:
                        right += 1
        if unshown == right:
            self.win()
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
        self.winCheck()

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
    def tick(self): 
        self.ticks += 1 
        self.time.config(text=str(self.ticks)) 
        
        self.time.after(1000, self.tick)
        score = 10000
        if self.movesMade and self.ticks:
            score -= int((self.ticks * self.movesMade))
        self.score.config(text=str(score))
    def lose(self):
        self.lost = True
        for x in self.grid:
            for tile in x:
                tile.show()
        self.create_popup("You lose!")
    def win(self):
       if self.lost:
           return
       self.create_popup("You win!") 