import numpy as np
import pygame
import random
pygame.init()

W, H = 300, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

x = W // 2
y = 100.0
v = 300.0
r = 20

a = 500
running = True

while running:
    dt = 0.016
    clock.tick(60)
    v += 0.5*a*dt
    y = y + v*dt
    if y > H-r:
        offset = y+r-H
        y-= offset
        y = H-r
        v = -1*(v)
    v+=0.5*a*dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    



            # FILL UP

    screen.fill("black")
    pygame.draw.circle(screen, "red", (x, int(y)), r)
    pygame.display.flip()

pygame.quit()