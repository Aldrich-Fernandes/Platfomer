import pygame, sys, random
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
        self.sprites = []
        self.sprites.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\1.png"))
        self.sprites.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\2.png"))
        self.sprites.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\3.png"))
        self.sprites.append(pygame.image.load(r"Platfomer\\Assets\\Enemy\\Walk\\4.png"))

        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(topleft = (posX, posY))

        self.direction = pygame.math.Vector2(0,0)
        self.direction.x = 1
        self.speed = 2

    def animate(self):
        self.frame += 0.2

        if self.frame  >= len(self.sprites):
            self.frame = 0

        if self.direction.x >= 0:
            self.image = self.sprites[int(self.frame)]
        else:
            flippedImage = pygame.transform.flip(self.sprites[int(self.frame)], True, False)
            self.image = flippedImage     

    def update(self, shiftX):
        self.animate()
        self.rect.x += shiftX

class Tile(pygame.sprite.Sprite):
    def __init__(self, posX, posY, TileType):
        super().__init__()
        self.image = TileType
        self.rect = self.image.get_rect(topleft = (posX, posY))
    
    def update(self, shiftX):
        self.rect.x += shiftX

class bullet(pygame.sprite.Sprite):
    pass


def importFolder(path):
    surfaceList = []
    for _,__,imageFiles in walk(path):
        for image in imageFiles:
            fullPath = path + "\\" + image
            imageSurf = pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurf)

    return surfaceList