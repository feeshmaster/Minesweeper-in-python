import random


sprites = {
    "1": [
        [".", "1", "."],
        ["1", "1", "."],
        [".", "1", "."],
        [".", "1", "."],
        ["1", "1", "1"],
    ],
    "2": [
        ["2", "2", "2"],
        [".", ".", "2"],
        ["2", "2", "2"],
        ["2", ".", "."],
        ["2", "2", "2"],
    ],
    "3": [
        ["3", "3", "3"],
        [".", ".", "3"],
        [".", "3", "3"],
        [".", ".", "3"],
        ["3", "3", "3"],
    ],
    "4": [
        ["4", ".", "4"],
        ["4", ".", "4"],
        ["4", "4", "4"],
        [".", ".", "4"],
        [".", ".", "4"],
    ],
    "5": [
        ["5", "5", "5"],
        ["5", ".", "."],
        ["5", "5", "5"],
        [".", ".", "5"],
        ["5", "5", "5"],
    ],
    "6": [
        ["6", "6", "6"],
        ["6", ".", "."],
        ["6", "6", "6"],
        ["6", ".", "6"],
        ["6", "6", "6"],
    ],
    "7": [
        ["7", "7", "7"],
        [".", ".", "7"],
        [".", "7", "."],
        [".", "7", "."],
        [".", "7", "."],
    ],
    "8": [
        ["8", "8", "8"],
        ["8", ".", "8"],
        ["8", "8", "8"],
        ["8", ".", "8"],
        ["8", "8", "8"],
    ],
    "flag": [
        [".", "F", "F", "."],
        [".", "F", "F", "F"],
        [".", "F", "F", "."],
        [".", "P", ".", "."],
        ["P", "P", "P", "."],
    ],
    "mine": [
        [".", "B", "B", "B", "."],
        ["B", "B", "B", "B", "B"],
        ["B", "B", "B", "B", "B"],
        ["B", "B", "B", "B", "B"],
        [".", "B", "B", "B", "."],
    ],
}

colors = {
    ".": None,
    "1": "#0000FF",
    "2": "#008000",
    "3": "#FF0000",
    "4": "#000080",
    "5": "#800000",
    "6": "#008080",
    "7": "#000000",
    "8": "#808080",
    "F": "#FF0000",
    "P": "#000000",
    "B": "#000000",
}


class Tile:
    def __init__(self, canvas, x, y, tileSize, offsetX, offsetY, isMine=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.tileSize = tileSize
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.edge = 4
        self.isMine = isMine
        self.flagged = False
        self.shown = False
        self.sprite = None  
        self.mines = 0  
        self.grid = None  

    def draw(self):
        x1 = self.x * self.tileSize + self.offsetX
        y1 = self.y * self.tileSize + self.offsetY
        x2 = x1 + self.tileSize
        y2 = y1 + self.tileSize

        edge = self.edge
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#7d7d7d", outline="")
        
        self.canvas.create_rectangle(
            x1, y1, x2 - edge, y2 - edge, fill="#ffffff", outline=""
        )
        
        self.canvas.create_rectangle(
            x1 + edge, y1 + edge, x2 - edge, y2 - edge, fill="#bababa", outline=""
        )

    def setMine(self):
        self.isMine = True
        self.sprite = "mine"

    def setGrid(self, grid):
        self.grid = grid
        if self.isMine:
            return
        offsets = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]
        count = 0
        for dx, dy in offsets:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny].isMine:
                    count += 1
        self.mines = count
        self.sprite = str(count)

    def draw_sprite(self, sprite):
        if sprite == "0":
            return
        sprite = sprites[sprite]

        x1 = self.x * self.tileSize + self.offsetX + self.edge
        y1 = self.y * self.tileSize + self.offsetY + self.edge
        x2 = x1 + self.tileSize - self.edge * 2
        y2 = y1 + self.tileSize - self.edge * 2

        w = x2 - x1
        h = y2 - y1

        rows = len(sprite)
        cols = len(sprite[0])
        ps = int(min(w / cols, h / rows))
        sprite_w = cols * ps
        sprite_h = rows * ps

        cx = x1 + (w - sprite_w) / 2
        cy = y1 + (h - sprite_h) / 2

        for r in range(rows):
            for c in range(cols):
                cell = sprite[r][c]
                if cell == ".":
                    continue
                color = colors[cell]
                if color is None:
                    continue
                px1 = cx + c * ps
                py1 = cy + r * ps
                px2 = px1 + ps
                py2 = py1 + ps
                self.canvas.create_rectangle(px1, py1, px2, py2, fill=color, outline="")

    def show(self, flag=None):
        if self.shown:
            return


        if flag is not None:
            if flag:
                self.draw_sprite("flag")
            else:
                self.draw()
            return

        if self.flagged:
            return

        x1 = self.x * self.tileSize + self.offsetX
        y1 = self.y * self.tileSize + self.offsetY
        x2 = x1 + self.tileSize
        y2 = y1 + self.tileSize

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bababa", outline="")
        self.shown = True

        if self.sprite:
            self.draw_sprite(self.sprite)
        if self.mines == 0:
            self.showAdjacent(self.x, self.y)

    def showAdjacent(self, x, y):
        offsets = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]

        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            tile = self.grid[cx][cy]

            if tile.flagged or tile.isMine:
                continue

            if not tile.shown:
                tile.show()  

            if tile.mines != 0:
                continue

            for dx, dy in offsets:
                nx = cx + dx
                ny = cy + dy

                if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                    neighbor = self.grid[nx][ny]

                    if not neighbor.shown and not neighbor.flagged:
                        stack.append((nx, ny))



