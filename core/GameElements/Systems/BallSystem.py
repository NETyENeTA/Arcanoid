from Libraries.Animations.Functions.Lerp import lerp, lerp_tuple
from Libraries.Math.Trigonometry import Sinus
from typing import Callable

from GameFiles.Configs import WindowApp
from core.GameElements.Systems.BlockSystem import BlockSystem
from core.GameElements.Paddle import Paddle
from core.GameElements.Systems.BonusSystem import BonusSystem
from core.GameElements.Systems.Items.Ball import Ball, pg, Vec2
from core.GameElements.HUD import HUD

from core.App import AppConfigs as App


class BallSystem:
    class Default:
        MAX_SPEED = Vec2(10, 10)


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

    def __init__(self, paddle: Paddle, block_system: BlockSystem, end_game: Callable, pass_level: Callable):

        self.paddle = paddle

        self.PaddleLeftPiece = paddle.hitbox.size[0] // 2

        self.BlockSystem = block_system
        self.Balls = [Ball(Vec2(500, 700), 14, is_sticky=True)]

        self.end_game = end_game
        self.pass_level = pass_level

        self.is_end_game = False
        self.is_passed_level = False

    def rise_speed(self):
        for ball in self.Balls:
            if ball.speed.y < BallSystem.Default.MAX_SPEED.y:
                ball.speed.y *= 1.1

    def add_ball(self, ball):
        self.Balls.append(ball)
        if ball.is_sticky:
            self.BlockSystem.BonusSystem.is_stickyBall_here = True

    def add(self, pos: Vec2 | tuple[int, int], radius: int, is_sticky: bool = True):
        self.add_ball(Ball(pos, radius, is_sticky=is_sticky))
        if is_sticky:
            self.BlockSystem.BonusSystem.is_stickyBall_here = True

    def get_paddle_direction(self, x_ball, x_player) -> float:
        sub = x_ball - x_player
        raw_x = sub / self.PaddleLeftPiece

        return max(-0.8, min(raw_x, 0.8))


    def update_sticky(self):

        for ball in self.Balls[:]:

            # ball.update()

            if ball.is_sticky:
                value = Sinus.smooth_01(App.ticks() / 400)

                ball.hitbox.centerx = lerp(ball.hitbox.centerx, self.paddle.hitbox.centerx, 0.2)
                ball.hitbox.bottom = lerp(ball.hitbox.bottom,
                                          self.paddle.hitbox.top - 5 - (15 * value), 0.5)


    def update(self):

        for ball in self.Balls[:]:

            ball.update()

            if ball.is_sticky:
                value = Sinus.smooth_01(App.ticks() / 400)

                ball.hitbox.centerx = lerp(ball.hitbox.centerx, self.paddle.hitbox.centerx, 0.2)
                ball.hitbox.bottom = lerp(ball.hitbox.bottom,
                                          self.paddle.hitbox.top - 5 - (15 * value), 0.5)


                continue

            if self.is_passed_level and len(self.Balls) == 1 and ball.hitbox.bottom > WindowApp.bottom:
                ball.direction.reflect_y(True)
                App.sfx.pos_play("ball hit", ball.pos.x)
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

                if self.paddle.is_dead:
                    self.end_game()
                    self.is_end_game = True

            if (ball.direction.y > 0 and ball.hitbox.colliderect(self.paddle.hitbox)
                    and self.paddle.is_alive and not self.is_passed_level):
                # ball.direction = self.collide(ball.direction, ball.hitbox, ball.paddle)
                ball.direction.reflect_y(True)
                ball.direction.x = self.get_paddle_direction(ball.center.x, self.paddle.hitbox.centerx)
                ball.direction.normalize()
                # self.paddle.bounce()
                App.sfx.pos_play("ball hit", ball.pos.x)

            collision_id = ball.hitbox.collidelist(self.BlockSystem.blocks)

            if self.is_end_game and collision_id != -1:
                block = self.BlockSystem[collision_id]
                ball.direction = self.collide(ball.direction, ball.hitbox, block.hitbox)
                App.sfx.pos_play("ball hit", ball.pos.x)
                continue

            if collision_id != -1:
                block = self.BlockSystem[collision_id]
                ball.direction = self.collide(ball.direction, ball.hitbox, block.hitbox)
                block.hp -= 1

                if block.is_dead:
                    App.sfx.pos_play("ball hit a default block", ball.pos.x)
                    self.BlockSystem.kill(collision_id, 0.3)
                    self.paddle.add_score(10)

                    if len(self.BlockSystem.blocks) == 0:
                        self.pass_level()

                else:
                    self.paddle.add_score(5)
                    App.sfx.pos_play("ball hit", ball.pos.x)
                    self.BlockSystem.BonusSystem.spawn(block.center, 0.15)



    def cast_shadows(self):
        for ball in self.Balls:
            ball.cast_shadow()

    def draw_debug(self):

        for ball in self.Balls:
            ball.debug_draw()

    def draw(self):


        if self.is_passed_level:
            for ball in self.Balls:
                ball.draw_dashed()

        else:
            for ball in self.Balls:
                ball.old_draw()


