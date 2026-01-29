let tileList = []
let tileSize = 7
let oldTps
let playingMineSweeper = false
let mouseHeld = false
let justFlagged = false
let sprites = {
  "mine": [
           0,0,0,3,0,0,0,
           0,0,1,1,1,0,0,
           0,1,1,1,1,1,0,
           3,1,1,1,1,1,3,
           0,1,1,1,1,1,0,
           0,0,1,1,1,0,0,
           0,0,0,3,0,0,0,
  ],
  "flag": [
    0,0,0,1,0,0,0,
    0,0,2,1,0,0,0,
    0,2,2,1,0,0,0,
    0,0,2,1,0,0,0,
    0,0,0,1,0,0,0,
    0,0,1,1,1,0,0,
    0,1,1,1,1,1,0,
  ],
  "1": [
    0,0,0,0,0,0,0,
    0,0,0,2,0,0,0,
    0,0,2,2,0,0,0,
    0,2,0,2,0,0,0,
    0,0,0,2,0,0,0,
    0,2,2,2,2,2,0,
    0,0,0,0,0,0,0,
  ],
  "2": [
    0,0,0,0,0,0,0,
    0,0,4,4,4,0,0,
    0,4,0,0,0,4,0,
    0,0,0,4,4,0,0,
    0,0,4,0,0,0,0,
    0,4,4,4,4,4,0,
    0,0,0,0,0,0,0,
  ],
  "3": [
    0,0,0,0,0,0,0,
    0,0,5,5,5,0,0,
    0,5,0,0,0,5,0,
    0,0,0,5,5,0,0,
    0,5,0,0,0,5,0,
    0,0,5,5,5,0,0,
    0,0,0,0,0,0,0,
  ],
  "4": [
      0,0,0,0,0,0,0,
      0,6,0,0,6,0,0,
      0,6,0,0,6,0,0,
      0,6,6,6,6,6,0,
      0,0,0,0,6,0,0,
      0,0,0,0,6,0,0,
      0,0,0,0,0,0,0,
    ],
  "5": [
    0,0,0,0,0,0,0,
    0,0,7,7,7,0,0,
    0,0,7,0,0,0,0,
    0,0,7,7,7,0,0,
    0,0,0,0,7,0,0,
    0,0,7,7,7,0,0,
    0,0,0,0,0,0,0,
  ],
  "6": [
    0,0,0,0,0,0,0,
    0,0,0,8,0,0,0,
    0,0,8,0,0,0,0,
    0,0,8,8,8,0,0,
    0,0,8,0,8,0,0,
    0,0,8,8,8,0,0,
    0,0,0,0,0,0,0,
  ],
  "7": [
    0,0,0,0,0,0,0,
    0,0,9,9,9,0,0,
    0,0,0,0,9,0,0,
    0,0,0,9,0,0,0,
    0,0,9,0,0,0,0,
    0,0,9,0,0,0,0,
    0,0,0,0,0,0,0,
  ],
  "8": [
    0,0,0,0,0,0,0,
    0,0,10,10,10,0,0,
    0,0,10,0,10,0,0,
    0,0,0,10,0,0,0,
    0,0,10,0,10,0,0,
    0,0,10,10,10,0,0,
    0,0,0,0,0,0,0,
  ],
}

class Tile {
  constructor(x, y) {
    this.type = null
    this.revealed = false
    this.flagged = false
    this.number = null
    this.x = x
    this.y = y
  }
  flag() {
    this.flagged = !this.flagged
    let canvas = document.getElementById("game")
    let ctx = canvas.getContext("2d")
    if (this.flagged) {
      drawSprite(this.x, this.y, "flag", ctx)
      return
    }
    //bottom edge
    ctx.fillStyle = "grey"
    ctx.fillRect(this.x * pixelSize, this.y * pixelSize, pixelSize*tileSize, pixelSize*tileSize);
    //top edge
    ctx.fillStyle = "white"
    ctx.fillRect(this.x * pixelSize, this.y * pixelSize, pixelSize*(tileSize - 1), pixelSize*(tileSize - 1));
    ctx.fillRect(this.x * pixelSize, (this.y + tileSize - 1) * pixelSize, pixelSize, pixelSize);
    //middle
    ctx.fillStyle = "#c2c2c2"
    ctx.fillRect((this.x + 1) * pixelSize, (this.y + 1) * pixelSize, pixelSize*(tileSize - 2), pixelSize*(tileSize - 2));
  }
  reveal(reveal=true) {
    if (this.flagged) {
      return
    }
    let canvas = document.getElementById("game")
    let ctx = canvas.getContext("2d")
    this.revealed = true
    if (!this.type) {
      generateGame()
      this.reveal()
    } else if (this.type == "mine") {

      
      ctx.fillStyle = "red"
      ctx.fillRect(this.x * pixelSize, this.y * pixelSize, pixelSize*tileSize, pixelSize*tileSize);
      drawSprite(this.x, this.y, "mine", ctx)
      revealAll()
      alert('you lost!')
      

      
    } else if (this.type == "safe") {
      ctx.fillStyle = "#969696"
      ctx.fillRect(this.x * pixelSize, this.y * pixelSize, pixelSize*tileSize, pixelSize*tileSize);
      ctx.fillStyle = "#c2c2c2"
      ctx.fillRect((this.x + 1) * pixelSize, (this.y + 1) * pixelSize, pixelSize*(tileSize - 2), pixelSize*(tileSize - 2));
      //get adjacent bombs
      this.adjacentBombs = getAdjacentMines(this.x, this.y)
      if (this.adjacentBombs == 0 && reveal) { 
        clearEmptyChain(this.x, this.y)
        return                             
      }
      drawSprite(this.x, this.y, this.adjacentBombs, ctx)

      
    }
  }
  spawn() {
    let canvas = document.getElementById("game")
    let ctx = canvas.getContext("2d")
    //bottom edge
    ctx.fillStyle = "grey"
    ctx.fillRect(this.x * pixelSize, this.y * pixelSize, pixelSize*tileSize, pixelSize*tileSize);
    //top edge
    ctx.fillStyle = "white"
    ctx.fillRect(this.x * pixelSize, this.y * pixelSize, pixelSize*(tileSize - 1), pixelSize*(tileSize - 1));
    ctx.fillRect(this.x * pixelSize, (this.y + tileSize - 1) * pixelSize, pixelSize, pixelSize);
    //middle
    ctx.fillStyle = "#c2c2c2"
    ctx.fillRect((this.x + 1) * pixelSize, (this.y + 1) * pixelSize, pixelSize*(tileSize - 2), pixelSize*(tileSize - 2));
    
  }
  setType(type) {
    this.type = type
  }
  getThis() {
    return this
  }
}

function drawSprite(x, y, sprite, ctx) {
  let spriteData = sprites[sprite]
  for (let i = 0; i<7; i++) {
    for (let j = 0; j<7; j++) {
      switch (spriteData[i*7 + j]) {
        case 1:
          ctx.fillStyle = "black";
          break;
        case 2: 
          ctx.fillStyle = "red";//1
          break;
        case 3:
          ctx.fillStyle = "#5c5c5c";
          break;
        case 4: 
          ctx.fillStyle = "#ed9a1c";//2
          break;
        case 5: 
          ctx.fillStyle = "#ffff3d";//3
          break;
        case 6: 
          ctx.fillStyle = "#e2ff3d";//4
          break;
        case 7: 
          ctx.fillStyle = "#48ff00";//5
          break;
        case 8: 
          ctx.fillStyle = "#3dffa1";//6
          break;
        case 9: 
          ctx.fillStyle = "#00ffe5";//7
          break;
        case 10: 
          ctx.fillStyle = "#00d5ff";//8
          break;
        case 0: 
          continue
      }
      ctx.fillRect((x + j) * pixelSize, (y + i) * pixelSize, pixelSize, pixelSize)
      
      
    }
  }
}
function clearEmptyChain(x, y) {
  let adjacents = getAdjacent(x, y)
  for (let adjacent in adjacents) {
    let tileThis = adjacents[adjacent].getThis()
    let tile = adjacents[adjacent]
    if (tileThis.type == "safe") {
      if (tileThis.adjacentBombs == 0) {
        if (!tileThis.revealed) { tile.reveal() }
        
      } else {
        if (!tileThis.revealed) { tile.reveal() }
      }
    }
  }
  
}
function getAdjacent(x, y) {
  adjacents = []
  for (let i=0;i<tileList.length;i++) {
    tile = tileList[i].getThis()
   if (tile.x - tileSize == x && tile.y == y) {  //right
      adjacents.push(tileList[i])
    }
    if (tile.x + tileSize == x && tile.y == y) {  //left
      adjacents.push(tileList[i])
    }
    if (tile.x == x && tile.y - tileSize == y) {
      //bottom
      adjacents.push(tileList[i])
    }
    if (tile.x == x && tile.y + tileSize == y) {
      //top
      adjacents.push(tileList[i])
    }
  }
  return adjacents
}
function getAdjacentMines(x, y) {
  adjacents = 0
  for (let i=0;i<tileList.length;i++) {
    tile = tileList[i].getThis()
   if (tile.x - tileSize == x && tile.y == y) {  //right
      if (tile.type == "mine") {
      adjacents++
      }
    }
    if (tile.x + tileSize == x && tile.y == y) {  //left
      if (tile.type == "mine") {
      adjacents++
      }
    }
    if (tile.x == x && tile.y - tileSize == y) {
      //bottom
      if (tile.type == "mine") {
      adjacents++
      }
    }
    if (tile.x == x && tile.y + tileSize == y) {
      //top
      if (tile.type == "mine") {
      adjacents++
      }
    }
    //corners
    //bottom rights are problems
    if (tile.x - tileSize == x && tile.y - tileSize == y) {  //bottom-right
      if (tile.type == "mine") {
      adjacents++
      }
    }
    if (tile.x + tileSize == x && tile.y - tileSize == y) {  //bottom-;eft
      if (tile.type == "mine") {
      adjacents++
      }
    }
    if (tile.x - tileSize == x && tile.y + tileSize == y) {
      //top-right
      if (tile.type == "mine") {
      adjacents++
      }
    }
    if (tile.x + tileSize == x && tile.y + tileSize == y) {
      //top-left
      if (tile.type == "mine") {
      adjacents++
      }
    }
  }
  return JSON.stringify(adjacents)
}
function revealAll() {
  for (let i = 0; i < tileList.length; i++) {
    if (tileList[i].getThis().flagged == false) {
    tileList[i].reveal(false)
    }
  }
}
function generateGame() {
  for (let tileIndex in tileList) {
    let tile = tileList[tileIndex]
    tile.setType("safe")
  }
  for (let i=0;i<randInt(Math.floor(tileList.length/6), Math.floor(tileList.length/5)); i++) {
    if (tileList[i].getThis().noMine == true) { continue }
    randBomb()
  }
}
function setTileSize(size) {
  tileSize = size//7 < size ? size : 7
}

function randInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}
function randBomb() {
  let bomb = randInt(0, tileList.length)
  tileList[bomb].setType("mine")
  return 
}
function endMSGame() {
  let canvas = document.getElementById("game")
  let ctx = canvas.getContext("2d")
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  tickInterval = window.setInterval(tick, 1000/oldTps);
  playingMineSweeper = false
}

function startMSGame(rowx=8, rowy=8) {
  if (playingMineSweeper) {
    alert('you are already active in a game!')
    return
  } 
  playingMineSweeper = true
  oldTps = tps
  window.clearInterval(tickInterval);
  for (let i = 0; i<rowy;i++) {
    for (let j = 0; j<rowx;j++) {
      let newTile = new Tile(50 + (tileSize * i), 5 + (tileSize * j))
      newTile.spawn()
      tileList.push(newTile)
    }
  }
}
function checkMouseHeld() {
  if (mouseHeld) {
      let mouseX = mousePos.x
        let mouseY = mousePos.y
        for (let i=0;i<tileList.length;i++) {
          let tileIndex =   tileList[i]
          let tile = tileIndex.getThis()
          if (isBetween(mouseX, tile.x, tile.x + (tileSize - 1))){
            if (isBetween(mouseY, tile.y, tile.y + (tileSize - 1))) {
            tileIndex.flag()
            justFlagged = true
       }
      }
    }
  }
}

window.addEventListener("mousedown", (e) => {
    if (!playingMineSweeper) { return }
    mouseHeld = true
    setTimeout(checkMouseHeld, 1000)
})
window.addEventListener('mouseup', (e)=> {
  mouseHeld = false
  clearTimeout(checkMouseHeld)
  if (justFlagged) { justFlagged = false; return }
  let mouseX = mousePos.x
    let mouseY = mousePos.y
    for (let i=0;i<tileList.length;i++) {
      let tileIndex =   tileList[i]
      let tile = tileIndex.getThis()
      if (isBetween(mouseX, tile.x, tile.x + (tileSize - 1))){
        if (isBetween(mouseY, tile.y, tile.y + (tileSize - 1))) {
        tileIndex.reveal()
        removeInterval(checkMouseClick)
    }
   }
  }
})
function isBetween(num, min, max) {
  if (num >= min && num <= max) {
    return true
  }
  return false
}
//create game buttons
const injectGame = () => {

 
  


  
let startMSButton = document.createElement("button");
startMSButton.textContent = "Start";
startMSButton.onclick = function() {startMSGame()}
let endMSButton = document.createElement("button");
endMSButton.textContent = "End";
endMSButton.onclick = function() {endMSGame()}
document.getElementById("toolControls").appendChild(startMSButton); 
document.getElementById("toolControls").appendChild(endMSButton); 
}
runAfterLoadList.push(injectGame)



