sprites = {
    "1": [
        ['.','1','.'],
        ['1','1','.'],
        ['.','1','.'],
        ['.','1','.'],
        ['1','1','1'],
    ],

    "2": [
        ['2','2','2'],
        ['.','.','2'],
        ['2','2','2'],
        ['2','.','.'],
        ['2','2','2'],
    ],

    "3": [
        ['3','3','3'],
        ['.','.','3'],
        ['.','3','3'],
        ['.','.','3'],
        ['3','3','3'],
    ],

    "4": [
        ['4','.','4'],
        ['4','.','4'],
        ['4','4','4'],
        ['.','.','4'],
        ['.','.','4'],
    ],

    "5": [
        ['5','5','5'],
        ['5','.','.'],
        ['5','5','5'],
        ['.','.','5'],
        ['5','5','5'],
    ],

    "6": [
        ['6','6','6'],
        ['6','.','.'],
        ['6','6','6'],
        ['6','.','6'],
        ['6','6','6'],
    ],

    "7": [
        ['7','7','7'],
        ['.','.','7'],
        ['.','7','.'],
        ['.','7','.'],
        ['.','7','.'],
    ],

    "8": [
        ['8','8','8'],
        ['8','.','8'],
        ['8','8','8'],
        ['8','.','8'],
        ['8','8','8'],
    ],

    "flag": [
        ['.','F','F','.'],
        ['.','F','F','F'],
        ['.','F','F','.'],
        ['.','P','.','.'],
        ['P','P','P','.'],
    ],

    "bomb": [
        ['.','B','B','B','.'],
        ['B','B','B','B','B'],
        ['B','B','B','B','B'],
        ['B','B','B','B','B'],
        ['.','B','B','B','.'],
    ],
}

colors = {
    '.': None,         

    '1': '#0000FF',     
    '2': '#008000',     
    '3': '#FF0000',     
    '4': '#000080',     
    '5': '#800000',     
    '6': '#008080',     
    '7': '#000000',     
    '8': '#808080',     

    'F': '#FF0000',     
    'P': '#000000',     
    'B': '#000000',     
}




class Tile():
    def __init__(self, canvas, x, y, tileSize, offsetX, offsetY, isMine=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.tileSize = tileSize
        self.isMine = isMine
        self.offsetX = offsetX
        self.offsetY = offsetY
    def draw(self):
        x1 = self.x * self.tileSize + self.offsetX
        y1 = self.y * self.tileSize + self.offsetY
        x2 = x1 + self.tileSize
        y2 = y1 + self.tileSize

        edge = 4  
        self.edge = edge
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#7d7d7d", outline=""
        )
        self.canvas.create_rectangle(
            x1, y1,
            x2 - edge, y2 - edge,
            fill="#ffffff", outline=""
        )
        self.canvas.create_rectangle(
            x1 + edge, y1 + edge,
            x2 - edge, y2 - edge,
            fill="#bababa", outline=""
        )

        self.draw_sprite("1", self.x, self.y)
    def setMine(self):
        self.isMine = True
    def draw_sprite(self, sprite, x, y):
        sprite = sprites[sprite]

        x1 = self.x * self.tileSize + self.offsetX
        y1 = self.y * self.tileSize + self.offsetY
        x2 = x1 + self.tileSize
        y2 = y1 + self.tileSize

        x1 += self.edge
        y1 += self.edge
        x2 -= self.edge
        y2 -= self.edge

        w = x2 - x1
        h = y2 - y1

        rows = len(sprite)
        cols = len(sprite[0])

        ps = min(w / cols, h / rows)  

        for r in range(rows):
            for c in range(cols):
                cell = sprite[r][c]
                if cell == '.':
                    continue

                color = colors[cell]
                if color is None:
                    continue

                px1 = x1 + c * ps
                py1 = y1 + r * ps
                px2 = px1 + ps
                py2 = py1 + ps

                self.canvas.create_rectangle(
                    px1, py1, px2, py2,
                    fill=color,
                    outline=""
                )


