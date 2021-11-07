import threading
import time
import pygame
from bullets.bullet_enmey import BulletEnmey
from planes.plance_base import PlanceBase

"""
普通敌机
"""


class EnemyPlance(PlanceBase):  # 普通敌机机派生自PlanceBase，要重写PlanceBase相关的方法
    def __init__(self, sc):
        self.screen = sc
        self.move_type = self.random(0, 1)  # 敌机的活动方式 0为直线下
        self.bullet_index = self.random(0, 3)
        self.collide_count = 0
        self.live = self.random(1, 3)
        super(EnemyPlance, self).__init__(sc)

    def get_default_image(self):
        imageIndex = self.random(0, 5)

        return imageIndex

    def get_size(self):
        size = self.random(-50, 10)  # 随机大小
        return size

    def get_speed(self):
        return self.random(2, 5)

    def getImagePaths(self):
        paths = []
        for i in range(7):
            paths.append(f"images/enemy/{i}.png")
        return paths

    def getLocation(self):
        location = [self.random(20, self.screen.get_width() - 60), -50]
        return location

    def creat_bluet(self):
        bullet = BulletEnmey(self, self.win)
        bullet.change_image(self.bullet_index)
        self.bluets.add(bullet)
        self.bluets.update()
        self.timer_run(1, self.creat_bluet)

    def action(self):

        for em in self.bluets.sprites():
            em.action()
        if self.move_type == 1:
            self.move_rand()
        else:
            self.move_small()

        self.draw()

    def move_small(self):
        if self.rect.bottom < self.win.get_height():
            self.rect.y += self.speed
        else:
            self.kill()

    def move_rand(self):

        self.rect.y += 1
        self.moveRand()

    def change_model(self):
        self.playSound("sounds/bz1.wav")
        time.sleep(0.5)
        self.kill()

    def collide(self):
        self.collide_count += 1
        if self.collide_count > self.live:
            self.change_image(6)
            self.timer_run(0.1, self.change_model)
