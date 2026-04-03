import pygame, math


class InputHandler:
    def __init__(self):
        self.autopilot = False

    def handle(self, engine):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if pygame.K_1 <= e.key <= pygame.K_9:
                    idx = e.key - pygame.K_1
                    if idx < len(engine.planets): engine.target = engine.planets[idx]
                if e.key == pygame.K_f: self.autopilot = not self.autopilot
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: return False

        dx, dy, dz = engine.target.pos[0] - engine.cam[0], engine.target.pos[1] - engine.cam[1], engine.target.pos[2] - \
                     engine.cam[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        sy, cy, sp, cp = math.sin(engine.yaw), math.cos(engine.yaw), math.sin(engine.pitch), math.cos(engine.pitch)
        acc = 180.0 * (25.0 if keys[pygame.K_LSHIFT] else 1.0)

        if self.autopilot and dist > 350:
            aspeed = 2200.0
            engine.vel[0] += sy * cp * aspeed * 0.016
            engine.vel[1] -= sp * aspeed * 0.016
            engine.vel[2] += cy * cp * aspeed * 0.016
        else:
            if keys[pygame.K_w]: engine.vel[0] += sy * cp * acc * 0.016; engine.vel[1] -= sp * acc * 0.016; engine.vel[
                2] += cy * cp * acc * 0.016
            if keys[pygame.K_s]: engine.vel[0] -= sy * cp * acc * 0.016; engine.vel[1] += sp * acc * 0.016; engine.vel[
                2] -= cy * cp * acc * 0.016
            if keys[pygame.K_a]: engine.vel[0] -= cy * acc * 0.016; engine.vel[2] += sy * acc * 0.016
            if keys[pygame.K_d]: engine.vel[0] += cy * acc * 0.016; engine.vel[2] -= sy * acc * 0.016
            if keys[pygame.K_LCTRL]: engine.vel[1] += acc * 0.016
            if keys[pygame.K_SPACE]: engine.vel[1] -= acc * 0.016
        return True
