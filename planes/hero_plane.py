import time
import pygame
from bullets.bullet_hero import BulletHero
from planes.plance_base import PlanceBase
from sprites.text_show import TextShow


class HeroPlane(PlanceBase):
    def __init__(self, screen, lv):
        self.bullet_leve = 0
        self.bullet_speed = 0.2
        self.enmey_kill_count = 0
        self.live = lv
        super(HeroPlane, self).__init__(screen)

    def get_speed(self):
        return 10

    def getLocation(self):
        return [220, 650]

    def getImagePaths(self):
        paths = []
        for i in range(4):
            paths.append(f"images/hero/{i}.png")
        return paths

    def next_bluet(self):
        if self.bullet_leve<2:
            self.bullet_leve += 1

        self.bullet_speed = 0.1
        self.enmey_kill_count = 0

    def update_kill_count(self):
        self.enmey_kill_count += 1

    def creat_bluet(self):

        bullet_img_index = self.bullet_leve

        rand = self.random(1, 100)
        is_seng_big = False
        if rand < 5:
            is_seng_big = True

        if 50 < self.enmey_kill_count < 100:
            if rand < 10:
                is_seng_big = True
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=1))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=-1))
        elif 100 < self.enmey_kill_count < 300:
            if rand < 20:
                is_seng_big = True
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=3))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=-3))
        elif self.enmey_kill_count > 300:
            if rand < 30:
                is_seng_big = True
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=6))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=3))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=-3))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=6))
        else:
            self.bluets.add(BulletHero(self, self.win, bullet_img_index))

        if is_seng_big:
            self.bluets.add(BulletHero(self, self.win, self.bullet_leve+3, xspeed=3, yspeed=10))
            self.bluets.add(BulletHero(self, self.win, self.bullet_leve+3, xspeed=-3, yspeed=10))

        self.bluets.update()
        self.timer_run(self.bullet_speed, self.creat_bluet)
        self.playSound("sounds/send.wav")

    def action(self):
        self.__control()
        self.draw()

        for em in self.bluets.sprites():
            em.action()

    def collide(self):
        self.collide_count += 1

        if not self.__is_changing:
            self.timer_run(1, self.__change_model)

        if self.collide_count > self.live:
            self.kill()

    __is_changing = False

    def __change_model(self):
        self.__is_changing = True
        for i in range(5):
            self.change_image(1)
            time.sleep(0.3)
            self.change_image(2)
            time.sleep(0.3)
            self.change_image(3)
            time.sleep(0.3)
            self.change_image(0)
            time.sleep(0.3)

        self.__is_changing = False

    def __control(self):
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_UP]:
            self.moveUp()
        elif key_press[pygame.K_DOWN]:
            self.moveDown()
        elif key_press[pygame.K_LEFT]:
            self.moveLeft()
        elif key_press[pygame.K_RIGHT]:
            self.moveRight()

    def moveLeft(self):
        if self.rect.left > 0:  # 显示rect的范围，不至于玩家坦克移出屏幕
            self.rect.x -= self.speed

    def moveRight(self):
        if self.rect.right < self.win.get_width():
            self.rect.x += self.speed

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def moveDown(self):
        if self.rect.bottom < self.win.get_height():
            self.rect.y += self.speed
