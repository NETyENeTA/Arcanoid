from GameFiles.Configs import WindowApp
from core.GameElements.Systems.BlockSystem import BlockSystem
from core.GameElements.Paddle import Paddle
from core.GameElements.SystemItems.Ball import Ball, pg, Vec2
from core.GameElements.HUD import HUD

from core.App import AppConfigs as App


class BallSystem:

    @staticmethod
    def collide(direction: Vec2, ball_rect: pg.Rect, target_rect: pg.Rect) -> Vec2:
        """
        Обработка столкновения шарика с прямоугольником (блоком или ракеткой).
        Возвращает обновленный вектор направления и корректирует позицию ball_rect.
        """
        # 1. Считаем глубину проникновения по осям (overlap)
        # На сколько пикселей шарик зашел внутрь цели
        if direction.x > 0:
            overlap_x = ball_rect.right - target_rect.left
        else:
            overlap_x = target_rect.right - ball_rect.left

        if direction.y > 0:
            overlap_y = ball_rect.bottom - target_rect.top
        else:
            overlap_y = target_rect.bottom - ball_rect.top

        # 2. Определяем сторону отскока по минимальному проникновению

        # СЛУЧАЙ А: УДАР В УГОЛ (проникновения почти равны)
        if abs(overlap_x - overlap_y) < 4:
            direction.x *= -1
            direction.y *= -1
            # Выталкиваем из угла по обеим осям
            ball_rect.x -= overlap_x * (1 if direction.x < 0 else -1)
            ball_rect.y -= overlap_y * (1 if direction.y < 0 else -1)

        # СЛУЧАЙ Б: УДАР В ВЕРХ ИЛИ НИЗ (overlap_x > overlap_y)
        # Это значит, что по X мы зашли глубже, значит контакт был с горизонтальной гранью
        elif overlap_x > overlap_y:
            direction.y *= -1
            # Выталкиваем шарик за пределы по Y
            if direction.y < 0:
                ball_rect.bottom = target_rect.top
            else:
                ball_rect.top = target_rect.bottom

        # СЛУЧАЙ В: УДАР В БОК (overlap_y > overlap_x)
        else:
            direction.x *= -1
            # Выталкиваем шарик за пределы по X
            if direction.x < 0:
                ball_rect.right = target_rect.left
            else:
                ball_rect.left = target_rect.right

        return direction

    def __init__(self, paddle: Paddle, block_system: BlockSystem):

        self.paddle = paddle

        self.PaddleLeftPiece = paddle.hitbox.size[0] // 2

        self.BlockSystem = block_system
        self.Balls = [Ball(Vec2(500, 700), 14, is_sticky=True)]

    def add_ball(self, ball):
        self.Balls.append(ball)

    def add(self, pos: Vec2 | tuple[int, int], radius: int):
        self.add_ball(Ball(pos, radius, is_sticky=True))

    def get_paddle_direction(self, x_ball, x_player) -> float:
        sub = x_ball - x_player
        raw_x = sub / self.PaddleLeftPiece

        return max(-0.8, min(raw_x, 0.8))

    def update(self):

        for ball in self.Balls:

            ball.update()

            if ball.is_sticky:
                ball.hitbox.center = (self.paddle.hitbox.centerx, self.paddle.hitbox.top - ball.radius - 5)
                continue

            if ball.pos.y > WindowApp.H:
                if self.paddle.is_dead or len(self.Balls) > 1:
                    self.Balls.remove(ball)
                else:
                    ball.hitbox.bottom = WindowApp.bottom
                continue

            if ball.hitbox.bottom > WindowApp.bottom and len(self.Balls) == 1 and self.paddle.is_alive:
                # ball.direction.y = -1
                ball.direction.reflect_y(True)
                HUD.visualisate_damage()
                self.paddle.health -= 1
                self.paddle.damaged(0.5)
                App.sfx.pos_play("ball hit", ball.pos.x)

            if ball.direction.y > 0 and ball.hitbox.colliderect(self.paddle.hitbox):
                # ball.direction = self.collide(ball.direction, ball.hitbox, ball.paddle)
                ball.direction.reflect_y(True)
                ball.direction.x = self.get_paddle_direction(ball.center.x, self.paddle.hitbox.centerx)
                ball.direction.normalize()
                # self.paddle.bounce()
                App.sfx.pos_play("ball hit", ball.pos.x)

            collision_id = ball.hitbox.collidelist(self.BlockSystem.blocks)
            if collision_id != -1:
                block = self.BlockSystem[collision_id]
                ball.direction = self.collide(ball.direction, ball.hitbox, block.hitbox)
                block.hp -= 1

                if block.is_dead:
                    App.sfx.pos_play("ball hit a default block", ball.pos.x)
                    self.BlockSystem.remove(collision_id)
                    self.paddle.score += 10
                else:
                    self.paddle.score += 5
                    App.sfx.pos_play("ball hit", ball.pos.x)



    def cast_shadows(self):
        for ball in self.Balls:
            ball.cast_shadow()

    def draw(self):

        for ball in self.Balls:
            ball.draw()
