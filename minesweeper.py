from modes import Modes
import ttkbootstrap as tb


class MineSweeper():
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
        self.start()


    def init_scoreboard(self):
        scoreBoard = tb.Frame(self.root)
        scoreBoard.pack(anchor="nw", padx=20, pady=10)

        scoreLabel = tb.Label(scoreBoard, text="Score ", font=("Segoe UI", 16, "bold"))
        scoreLabel.pack(side="left", padx=(20, 0))

        score = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        score.pack(side="left")

        minesLabel = tb.Label(scoreBoard, text="Mines ", font=("Segoe UI", 16, "bold"))
        minesLabel.pack(side="left", padx=(20, 0))

        mines = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        mines.pack(side="left")

        movesLabel = tb.Label(scoreBoard, text="Moves ", font=("Segoe UI", 16, "bold"))
        movesLabel.pack(side="left", padx=(200, 0))

        moves = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        moves.pack(side="left")

        timeLabel = tb.Label(scoreBoard, text="Time ", font=("Segoe UI", 16, "bold"))
        timeLabel.pack(side="left", padx=(60, 0))

        time = tb.Label(scoreBoard, text="0", font=("Segoe UI", 16, "bold"))
        time.pack(side="left")

        self.score = score
        self.mines = mines
        self.moves = moves
        self.time = time


    def init_canvas(self):
        self.canvas = tb.Canvas(self.root, width=700, height=500, bd=3, relief="solid")
        self.canvas.pack(pady=20)

    def start(self):
        self.root.mainloop()
    def destroy(self):
        self.root.destroy()

ms = MineSweeper("easy")