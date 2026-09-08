import numpy as np
import pygame
pygame.init()

n = int(input("Enter the number of balls you want: "))
W, H = 600, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
center = np.array([W / 2, H / 2])
R = 250
r = 12
pos = np.random.uniform(-R+r, R-r, (n,2))
pos += np.array([W/2, H/2])

vel = np.random.uniform(-200, 200, (n,2))
m = 1

a = np.array([0,500])

running = True
while running:
    ref_point_y = center[1] + R 
    heights_from_ref = ref_point_y - pos[:, 1]

    total_pe = np.sum(m * a[1] * heights_from_ref)
    total_ke = 0.5 * m * np.sum(vel ** 2)

    print("Total Energy = ",total_ke+total_pe)
    substeps = 16
    frame_time = clock.tick(60)/1000
    dt = frame_time/substeps
    for _ in range(substeps):


        # RK4 IMPLEMENTATION
        # slope_v = a
        # slope_p_1 = vel
        # slope_p_2 = vel + 0.5*slope_p_1*dt
        # slope_p_3 = vel + 0.5*slope_p_2*dt
        # slope_p_4 = vel + slope_p_3*dt

        # pos += (slope_p_1 + slope_p_2*2 + slope_p_3*2 + slope_p_4)*(dt/6.0)
        # vel += dt*slope_v
        
        vel += 0.5*a*dt
        pos += vel*dt
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

        vel+= 0.5*a*dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 

    screen.fill("black")
    pygame.draw.circle(screen, "white", center.astype(int), R, 2)
    for i in range(n):
        pygame.draw.circle(screen, "red", (int(pos[i][0]), int(pos[i][1])), r)
    

    pygame.display.flip()

pygame.quit()