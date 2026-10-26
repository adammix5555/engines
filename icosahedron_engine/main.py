import pygame
import random
import math
import functions

pygame.init()

icon = pygame.image.load("assets\\icon.png")

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Icosahedron Engine")
pygame.display.set_icon(icon)

Arial = pygame.font.SysFont('Arial', 15)
debug = pygame.font.SysFont('Arial', 10)

debug_txt = True
rgb = False

boids_num = 50
detection_range = 15

mouse_attraction = 200

mouse_x, mouse_y = pygame.mouse.get_pos()

class Boids:
    def __init__(self):
        self.speed = random.randint(175, 300)
        self.pos_x, self.pos_y = random.randint(0, width), random.randint(0, height)
        self.rotation = random.randint(0, 360) * (math.pi / 180)
        self.velocity_x = math.cos(self.rotation) * self.speed
        self.velocity_y = math.sin(self.rotation) * self.speed

    def update(self, dt, m_x, m_y, mouse_att):
        self.pos_x += self.velocity_x * dt
        self.pos_y += self.velocity_y * dt

        a_dist_x = m_x - self.pos_x
        a_dist_y = m_y - self.pos_y
        a_dist = math.hypot(a_dist_x, a_dist_y)

        if a_dist < mouse_att:
            if mouse_pressed[0] == True:
                self.rotation = math.atan2(m_y - self.pos_y, m_x - self.pos_x)

                target_x = math.cos(self.rotation) * self.speed
                target_y = math.sin(self.rotation) * self.speed

                self.velocity_x += (target_x - self.velocity_x) * 3 * dt
                self.velocity_y += (target_y - self.velocity_y) * 3 * dt

            elif mouse_pressed[2] == True:
                dist_x = self.pos_x - m_x
                dist_y = self.pos_y - m_y

                self.rotation = math.atan2(dist_y, dist_x)

                target_x = math.cos(self.rotation) * self.speed
                target_y = math.sin(self.rotation) * self.speed

                self.velocity_x += (target_x - self.velocity_x) * 3 * dt
                self.velocity_y += (target_y - self.velocity_y) * 3 * dt

    def check_others(self, dt, o_pos_x, o_pos_y, o_rot, o_speeds, radius):
        space = 35
        close_other_rot = []
        close_other_speed = []

        for i in range(len(o_pos_x)):

            other_x = o_pos_x[i]
            other_y = o_pos_y[i]
            other_rot = o_rot[i]
            other_speed = o_speeds[i]

            if other_x - self.pos_x == 0 and other_y - self.pos_y == 0:
                continue

            dist_x = self.pos_x - other_x
            dist_y = self.pos_y - other_y

            dist = math.hypot(dist_x, dist_y)

            if dist < space and dist > 0:
                force = (space - dist) / space
                angle = math.atan2(dist_y, dist_x)

                self.velocity_x += math.cos(angle) * force * 500 * dt
                self.velocity_y += math.sin(angle) * force * 500 * dt

            if dist < radius and dist > 0:
                close_other_rot.append(other_rot)
                close_other_speed.append(other_speed)

        if len(close_other_rot) > 0:
            sum_cos = 0
            sum_sin = 0
            
            for rot in close_other_rot:
                sum_cos += math.cos(rot)
                sum_sin += math.sin(rot)
            
            avg_rot = math.atan2(sum_sin, sum_cos)
            avg_speed = sum(close_other_speed) / len(close_other_speed)
            
            target_x = math.cos(avg_rot) * self.speed
            target_y = math.sin(avg_rot) * self.speed

            self.velocity_x += (target_x - self.velocity_x) * 3 * dt
            self.velocity_y += (target_y - self.velocity_y) * 3 * dt

            self.speed = avg_speed

    def fuck_walls(self, dt):
        force = 600
        space = 50
        
        if self.pos_x < space:
            self.velocity_x += force * dt
        elif self.pos_x > width - space:
            self.velocity_x -= force * dt
            
        if self.pos_y < space:
            self.velocity_y += force * dt
        elif self.pos_y > height - space:
            self.velocity_y -= force * dt

boids = [Boids() for i in range(boids_num)]

positions_x = []
positions_y = []
rotations = []
speeds = []

while True:
    dt = fpsClock.tick(fps) / 1000
    screen.fill((0, 0, 0))

    if len(speeds) != 0:
        avg_boid_speed = sum(speeds) / len(speeds)
    else:
        avg_boid_speed = 200

    positions_x.clear()
    positions_y.clear()
    rotations.clear()
    speeds.clear()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if rgb:
        color = functions.rgb(1)
    else:
        color = (255, 255, 255)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                debug_txt = not debug_txt
            if event.key == pygame.K_g:
                rgb = not rgb

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                mouse_attraction += 20
            elif event.y < 0:
                mouse_attraction -= 20

            if mouse_attraction < 0:
                mouse_attraction = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                mouse_attraction = 200

    for boid in boids:
        boid.update(dt, mouse_x, mouse_y, mouse_attraction)
        boid.check_others(dt, positions_x, positions_y, rotations, speeds, detection_range)
        boid.fuck_walls(dt)

        boid.rotation = math.atan2(boid.velocity_y, boid.velocity_x)

        positions_x.append(int(boid.pos_x))
        positions_y.append(int(boid.pos_y))
        rotations.append(boid.rotation)
        speeds.append(boid.speed)

        tri_length = 6
        tri_width = 6
        
        x1 = boid.pos_x + math.cos(boid.rotation) * tri_length
        y1 = boid.pos_y + math.sin(boid.rotation) * tri_length

        x2 = boid.pos_x + math.cos(boid.rotation + 2.5) * tri_width
        y2 = boid.pos_y + math.sin(boid.rotation + 2.5) * tri_width

        x3 = boid.pos_x + math.cos(boid.rotation - 2.5) * tri_width
        y3 = boid.pos_y + math.sin(boid.rotation - 2.5) * tri_width

        pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3)])

    fps_text = Arial.render(f'Fps: {int(fpsClock.get_fps())}', False, (255, 255, 255))
        
    speed_text = debug.render(f'avg speed: {float(avg_boid_speed)}', False, (255, 255, 255))
    count_text = debug.render(f'count: {int(boids_num)}', False, (255, 255, 255))
    att_text = debug.render(f'attraction range: {int(mouse_attraction)}', False, (255, 255, 255))
    radius_text = debug.render(f'radius: {int(detection_range)}', False, (255, 255, 255))
    color_text = debug.render(f'rgb, color: {bool(rgb)}, {(color)}', False, (255, 255, 255))

    screen.blit(fps_text, (10, 10))

    if debug_txt:
        screen.blit(speed_text, (10, 30))
        screen.blit(count_text, (10, 50))
        screen.blit(att_text, (10, 70))
        screen.blit(radius_text, (10, 90))
        screen.blit(color_text, (10, 110))

    pygame.display.flip()