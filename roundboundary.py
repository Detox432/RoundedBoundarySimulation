import numpy as np
import pygame
import math
pygame.init()

n = int(input("Enter the number of balls you want: "))
W, H = 600, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
center = np.array([W / 2, H / 2])
R = 250
r = 12
pos = np.zeros((n,2))
for i in range(n):
    pos[i] = [W/2 + np.random.uniform(-R+r, R-r), H/2 + np.random.uniform(-R+r, R-r)]
vel = np.random.uniform(-200, 200, (n,2))


a = np.array([0,500])

running = True
while running:
    dt = clock.tick(60)/1000
    vel += 0.5*a*dt
    pos+= vel*dt
    pos_b = np.tile(pos, (n, 1, 1))
    center_vectors = pos_b - pos_b.transpose(1,0,2)
            
    center_vectors_magnitude = np.linalg.norm(center_vectors,axis=2)    
    isColliding = center_vectors_magnitude < 2*r
    isColliding = np.triu(isColliding, k=1)
    i,j = np.where(isColliding)
    
    normal = center_vectors[i,j]/center_vectors_magnitude[i,j,np.newaxis]
    offset = 2*r - center_vectors_magnitude[i,j, np.newaxis]
    pos[i] -= normal * offset/2
    pos[j] += normal * offset/2     
    vel_rel = vel[i] - vel[j]
    vel_dot_n =  np.sum(vel_rel*normal, axis = 1, keepdims=True)
    vel[i] -= vel_dot_n*normal
    vel[j] += vel_dot_n*normal
    loc = pos - center
    loc_magnitude = np.linalg.norm(loc,axis=1)
    isCollidingBoundary = loc_magnitude + r > R
    i_b = np.where(isCollidingBoundary)[0]
    normal_boundary = -loc[i_b]/loc_magnitude[i_b, np.newaxis]
    v_dot_n = np.sum(vel[i_b]*normal_boundary, axis = 1, keepdims = True)
    vel[i_b] -= 2*v_dot_n*normal_boundary
    offset_boundary = (R - r) * (loc[i_b] / loc_magnitude[i_b, np.newaxis])
    pos[i_b] = center + offset_boundary
    vel += 0.5*a*dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 # fill up

    screen.fill("black")
    pygame.draw.circle(screen, "white", center.astype(int), R, 2)
    for i in range(n):
        pygame.draw.circle(screen, "red", (int(pos[i][0]), int(pos[i][1])), r)
    

    pygame.display.flip()

pygame.quit()