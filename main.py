import pygame, sys
from World import Level

pygame.init()
clock = pygame.time.Clock()

screenWidth = 1200
screenHight = 700
screen = pygame.display.set_mode((screenWidth, screenHight))
background = pygame.image.load(r"Platfomer\Assets\Forest.png")
pygame.display.set_caption("Platformer")
Level = Level(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0,0))  

    Level.run()

    pygame.display.flip()
    clock.tick(60)