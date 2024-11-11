import arcade as bora
import math
import random as ra
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "D-Day Invasion"

SP_Y = 550
AMERIC_SPEED = 0.3
AMERIC_SPAWN_TIME = 1
HORIZONTAL_SPAWN_POINTS = [100, SCREEN_WIDTH / 2, 790]
BULLET_SPAWN_TIME = 0.1


class Americanus(bora.Sprite):
    def __init__(self, game):
        super().__init__("american1.png", 0.1)

        self.spawn()
        self.center_y = 550
        self.color = (100, 255, 100)
        self.move_angle = ra.randint(self.left_angle, self.right_angle)
        self.part_x = math.cos(math.radians(self.move_angle))
        self.part_y = math.sin(math.radians(self.move_angle))
        self.change_x = AMERIC_SPEED * self.part_x
        self.change_y = AMERIC_SPEED * self.part_y
        self.game = game

    def spawn(self):
        spx = ra.choice(HORIZONTAL_SPAWN_POINTS)
        self.center_x = spx
        if spx == HORIZONTAL_SPAWN_POINTS[0]:
            self.right_angle = -30
            self.left_angle = -100
        elif spx == HORIZONTAL_SPAWN_POINTS[1]:
            self.right_angle = -50
            self.left_angle = -120
        elif spx == HORIZONTAL_SPAWN_POINTS[2]:
            self.right_angle = -75
            self.left_angle = -154



    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.top < 170:
            self.game.active = False



class Bullet(bora.Sprite):
    def __init__(self, gun):
        super().__init__("pulya.png", 0.3)
        self.color = (255, 0, 0)
        self.center_x = gun.center_x
        self.center_y = gun.center_y
        self.angle = gun.angle
        self.change_x = 12 * gun.part_x
        self.change_y = 12 * gun.part_y

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class Gun(bora.Sprite):
    def __init__(self):
        super().__init__("gun_rb.png", 0.4)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 3.3

    def update(self):
        self.angle += self.change_angle
        self.part_x = math.cos(math.radians(self.angle))
        self.part_y = math.sin(math.radians(self.angle))


class Dot(bora.Sprite):
    def __init__(self):
        super().__init__("dot_rg.png", 0.5)

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 140

    def update(self):
        pass


class Game(bora.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = bora.load_texture("D-day_bg.png")
        self.dot = Dot()
        self.gun = Gun()
        self.enemies = bora.SpriteList()
        self.american_spawn_time = time.time()

        self.bullets = bora.SpriteList()
        self.active = True
        self.aftomat = False
        self.bullet_spawn_time = time.time()

    def update(self, delta_time: float):
        if self.active == True:
            self.dot.update()
            self.gun.update()
            self.bullets.update()
            self.enemies.update()

            if time.time() - self.american_spawn_time >= AMERIC_SPAWN_TIME:
                americanus = Americanus(self)
                self.enemies.append(americanus)
                self.american_spawn_time = time.time()

            if time.time() - self.bullet_spawn_time >= BULLET_SPAWN_TIME:
                self.shoot()
                self.bullet_spawn_time = time.time()

            for pulya in self.bullets:
                zdohshiye = bora.check_for_collision_with_list(pulya, self.enemies)
                if zdohshiye:
                    for i in zdohshiye:
                        i.kill()
                    pulya.kill()


    def shoot(self):
        if self.aftomat == True:
            bullet = Bullet(self.gun)
            self.bullets.append(bullet)


    def on_draw(self):
        self.clear((255, 255, 255))

        bora.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)

        self.bullets.draw()
        self.gun.draw()
        self.dot.draw()
        self.enemies.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.active == True:
            if button == bora.MOUSE_BUTTON_LEFT:
                self.aftomat = True


    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.active == True:
            self.aftomat = False

    def on_key_press(self, symbol: int, modifiers: int):
        if self.active == True:
            if symbol == bora.key.A:
                self.gun.change_angle = 2.5

            if symbol == bora.key.D:
                self.gun.change_angle = -2.5

    def on_key_release(self, symbol: int, modifiers: int):
        if self.active == True:
            if symbol == bora.key.A:
                self.gun.change_angle = 0

            if symbol == bora.key.D:
                self.gun.change_angle = 0


game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

bora.run()
