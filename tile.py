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
        self.canvas.create_rectangle(self.x * self.tileSize + self.offsetX, self.y * self.tileSize + self.offsetY, self.x * self.tileSize + self.tileSize + self.offsetX, self.y * self.tileSize + self.tileSize + self.offsetY, fill="blue")
    def setMine(self):
        self.isMine = True