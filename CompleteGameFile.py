import pygame, sys
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.pos = posX, posY
        #sprite
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.25
        self.image = self.animations["Idle"][self.frameIndex]
        self.rect = self.image.get_rect(topleft = self.pos)

        #movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.6
        self.jumpSpeed = -12

        #status
        self.status = 'Idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onLeft = False
        self.onRight = False

    def importCharacterAssets(self):
        characterPath = (r"Platfomer\\Assets\\Player\\")
        self.animations = {"Idle":[], "Run":[], "Jump":[]}

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importFolder(fullPath)

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            flippedImage = pygame.transform.flip(image, True, False)
            self.image = flippedImage

        if self.onGround and self.onRight:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.onGround and self.onLeft:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.onGround:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facingRight = False
        elif keys[pygame.K_d]:
            self.facingRight = True
            self.direction.x = 1
        elif keys[pygame.K_r]:
            self.rect = self.image.get_rect(topleft = self.pos)
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.onGround == True:
            self.jump()

    def getStatus(self):
        if self.direction.y < 0:
            self.status = 'Jump'
        else:
            if self.direction.x != 0:
                self.status = 'Run'
            else:
                self.status = 'Idle'#

        if self.rect.y >=700:
            pygame.quit()
            sys.exit()

    def jump(self):
        self.direction.y = self.jumpSpeed

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.getInput()
        self.getStatus()
        self.animate()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.frames = []
        self.frames.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\1.png"))
        self.frames.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\2.png"))
        self.frames.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\3.png"))
        self.frames.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\4.png"))
        self.frameIndex = 0
        self.animationSpeed = 0.25
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(topleft = (posX, posY))

    def update(self):
        pass

class World:
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
            "X    P                                                                                   X",
            "X                                                    LFFR    LF   LF  T     LFFFFFFFFFFFRX",
            "X                                     LFFFFFFFFFFFR  1002    12   12  C     1000000000002X",
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
        self.enemies.update()

        self.player.update()
        self.getPlayerOnGround()
        self.horizontalMovement()
        self.verticalMovement()
        self.player.draw(self.screenSurface)

class Tile(pygame.sprite.Sprite):
    def __init__(self, posX, posY, TileType):
        super().__init__()
        self.image = TileType
        self.rect = self.image.get_rect(topleft = (posX, posY))
    
    def update(self, shiftX):
        self.rect.x += shiftX

def importFolder(path):
    surfaceList = []
    for _,__,imageFiles in walk(path):
        for image in imageFiles:
            fullPath = path + "\\" + image
            imageSurf = pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurf)

    return surfaceList

pygame.init()
clock = pygame.time.Clock()

screenWidth = 1200
screenHight = 700
screen = pygame.display.set_mode((screenWidth, screenHight))
background = pygame.image.load(r"Platfomer\Assets\Forest.png")
pygame.display.set_caption("Platformer")
World = World(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0,0))  

    World.run()

    pygame.display.flip()
    clock.tick(60)