import pygame
from Entities import *

class Level:
    def __init__(self, screen):
        #Tiles:
        self.FloorTile = pygame.image.load(r"Platfomer\Assets\Tiles\FloorTile.png")
        self.LeftFloorEdge = pygame.image.load(r"Platfomer\Assets\Tiles\LeftFloorEdge.png")
        self.RightFloorEdge = pygame.image.load(r"Platfomer\Assets\Tiles\RightFloorEdge.png")
        self.ColumnTop = pygame.image.load(r"Platfomer\Assets\Tiles\ColumnTop.png")
        self.Column = pygame.image.load(r"Platfomer\Assets\Tiles\Column.png")
        self.LeftColumnWall = pygame.image.load(r"Platfomer\Assets\Tiles\LeftColumnWall.png")
        self.RightColumnWall = pygame.image.load(r"Platfomer\Assets\Tiles\RightColumnWall.png")
        self.Filling = pygame.image.load(r"Platfomer\Assets\Tiles\Filling.png")
        self.WorldBorder = pygame.image.load(r"Platfomer\Assets\Tiles\WorldBorder.png")

        #Level setup
        self.levelSetup()
        self.screenSurface = screen

        #World shift
        self.screenWidth = 1200
        self.screenHight = 700
        self.worldShift = 0
        self.currentX = 0

    def getPlayerOnGround(self):
        if self.player.sprite.onGround:
            self.player.onGround = True
        else:
            self.player.onGround = False

    def levelSetup(self):
        #MaxJumpHight = 2
        #HorizontalMaxJump = 5
        TileMap = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X                                                                                        X",
            "X                                                                                        X",
            "X                                                                                        X",
            "X                                                                                        X",
            "X                                                                                        X",
            "X                                                                                        X",
            "X                                                                                        X",
            "X    P                                                                            E      X",
            "X                                           E        LFFR    LF   LF  T     LFFFFFFFFFFFRX",
            "X        E                 E          LFFFFFFFFFFFR  1002    12   12  C     1000000000002X",
            "XLFFFFFFFFFFFFFR     LFFFFFFFFFFFFR   1000000000002  1002    12   12  C     1000000000002X",
            "X000000000000002     10000000000002   1000000000002  1002    12   12  C     1000000000002X",
            "X000000000000002     10000000000002   1000000000002  1002    12   12  C     1000000000002X"]

        self.Tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        for y in range(len(TileMap)):
            for x in range(len(TileMap[y])):
                location = TileMap[y][x]
                posY = 0 + (y*50)
                posX = 0 + (x*50)

                if location == "F":
                    NewTile = Tile(posX, posY, self.FloorTile)
                    self.Tiles.add(NewTile)
                elif location == "L":
                    NewTile = Tile(posX, posY, self.LeftFloorEdge)
                    self.Tiles.add(NewTile)
                elif location == "R":
                    NewTile = Tile(posX, posY, self.RightFloorEdge)
                    self.Tiles.add(NewTile)
                elif location == "T":
                    NewTile = Tile(posX, posY, self.ColumnTop)
                    self.Tiles.add(NewTile)
                elif location == "C":
                    NewTile = Tile(posX, posY, self.Column)
                    self.Tiles.add(NewTile)
                elif location == "1":
                    NewTile = Tile(posX, posY, self.LeftColumnWall)
                    self.Tiles.add(NewTile)
                elif location == "2":
                    NewTile = Tile(posX, posY, self.RightColumnWall)
                    self.Tiles.add(NewTile)
                elif location == "0":
                    NewTile = Tile(posX, posY, self.Filling)
                    self.Tiles.add(NewTile)
                elif location == "X":
                    NewTile = Tile(posX, posY, self.WorldBorder)
                    self.Tiles.add(NewTile)
                elif location == "E":
                    NewEnemy = Enemy(posX, posY)
                    self.enemies.add(NewEnemy)
                elif location == "P":
                    PlayerSprite = Player(posX, posY)
                    self.player.add(PlayerSprite)
    
    def worldScrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < self.screenWidth / 4 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
        elif playerX > self.screenWidth - (self.screenWidth/4) and directionX > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8

    def horizontalMovement(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.Tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right
            
        if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.right < self.currentX or player.direction.x <= 0):
            player.onRight = False

    def verticalMovement(self):
        player = self.player.sprite
        player.applyGravity()

        for sprite in self.Tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        if player.onGround and (player.direction.y < 0 or player.direction.y > 1):
            player.onGround = False
        if player.onCeiling and player.direction.y >0:
            player.onCeiling = False

    def run(self):
        self.Tiles.update(self.worldShift)
        self.Tiles.draw(self.screenSurface)
        self.worldScrollX()

        self.enemies.draw(self.screenSurface)
        self.enemies.update(self.worldShift)

        self.player.update()
        self.getPlayerOnGround()
        self.horizontalMovement()
        self.verticalMovement()
        self.player.draw(self.screenSurface)
