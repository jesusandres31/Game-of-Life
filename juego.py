import pygame
import numpy as np
import time

WIDTH, HEIGHT = 600, 600
nX, nY = 60, 60
xSize = WIDTH/nX
ySize = HEIGHT/nY

# Initialize PyGame
pygame.init()

# Set size of screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Define background color
BG_COLOR = (10, 10, 10)
LIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (128, 128, 128)
# Celdas vivas = 1; Celdas muertas = 0
# Intialize status of cells
status = np.zeros((nX, nY))

pauseRun = False

running = True
# Bucle de ejecucion
while running:

    # Copy status
    newStatus = np.copy(status)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            pauseRun = not pauseRun

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            #newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newStatus[x, y] = not mouseClick[2]

    # Clean background
    screen.fill(BG_COLOR)

    for x in range(0, nX):
        for y in range(0, nY):

            if not pauseRun:

                # Numero de vecinos
                nNeigh = status[(x-1) % nX, (y-1) % nY] + status[(x) % nX, (y-1) % nY] + \
                    status[(x+1) % nX, (y-1) % nY] + status[(x-1) % nX, (y) % nY] + \
                    status[(x+1) % nX, (y) % nY] + status[(x-1) % nX, (y+1) % nY] + \
                    status[(x) % nX, (y+1) % nY] + \
                    status[(x+1) % nX, (y+1) % nY]

                # Rule 1: Una celula muerta con 3 vecinas revive
                if status[x, y] == 0 and nNeigh == 3:
                    newStatus[x, y] = 1

                # Rule 2: Una celula viva con mas de 3 vecinos o menos de 2 muere
                elif status[x, y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newStatus[x, y] = 0

            poly = [(x*xSize, y*ySize),
                    ((x+1)*xSize, y*ySize),
                    ((x+1)*xSize, (y+1)*ySize),
                    (x*xSize, (y+1)*ySize)]

            if newStatus[x, y] == 1:
                pygame.draw.polygon(screen, LIVE_COLOR, poly, 0)
            else:
                pygame.draw.polygon(screen, DEAD_COLOR, poly, 1)

    status = np.copy(newStatus)
    time.sleep(0.1)
    pygame.display.flip()

pygame.quit()
