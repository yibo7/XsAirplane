import time

from bullets.bullet_enmey import BulletEnmey
from planes.plance_base import PlanceBase


class BossPlance(PlanceBase):
    def __init__(self, sc, fun):
        self.boss_kill = fun
        self.screen = sc
        super(BossPlance, self).__init__(sc)
        self.is_right = self.rect.x < self.win.get_width() / 2

    def get_size(self):
        return 10

    def get_speed(self):
        return 2

    def getImagePaths(self):
        paths = []
        for i in range(7):
            paths.append(f"images/boss/{i}.png")
        return paths

    def getLocation(self):
        location = [self.random(20, self.screen.get_width()-30), -50]
        return location

    def creat_bluet(self):
        self.playSound("sounds/bosssend.wav")
        for i in range(5):
            bullet = BulletEnmey(self, self.win, _speed=17)
            bullet_index = self.random(4, 8)
            bullet.change_image(bullet_index)
            self.bluets.add(bullet)
            self.bluets.update()
            time.sleep(0.2)
        if not self.__is_killing:  # kill的并不会销毁这个实体
            self.timer_run(3, self.creat_bluet)

    def action(self):

        for em in self.bluets.sprites():
            em.action()

        if self.rect.y < 100:
            self.rect.y += self.speed
        else:

            if self.is_right:
                self.rect.x += 1
                if self.rect.right > self.win.get_width():
                    self.is_right = False
            else:
                self.rect.x -= 1
                if self.rect.left < 0:
                    self.is_right = True

        self.draw()

    __is_changing = False

    def change_model(self):

        # while True:
        #     if self.__is_killing:
        #         break
        #     self.change_image(1)
        #     time.sleep(0.3)
        #     self.change_image(2)
        #     time.sleep(0.3)
        #     self.change_image(3)
        #     time.sleep(0.3)
        #     self.change_image(4)
        #     time.sleep(0.3)
        #     self.change_image(5)
        #     time.sleep(0.3)
        for i in range(10):
            self.change_image(1)
            time.sleep(0.5)
            self.change_image(2)
            time.sleep(0.5)
            self.change_image(3)
            time.sleep(0.5)
            self.change_image(4)
            time.sleep(0.5)
            self.change_image(5)
            time.sleep(0.5)

        self.boss_kl()

    __is_killing = False

    def boss_kl(self):
        self.__is_killing = True
        self.playSound("sounds/bossbz.wav")
        self.change_image(6)
        time.sleep(2)
        self.kill()
        self.boss_kill(self)


    def collide(self):
        self.collide_count += 1

        if self.collide_count > 50 and not self.__is_changing:  # boss机中弹10次才让他消失
            self.__is_changing = True
            self.timer_run(1, self.change_model)

        # if self.collide_count > 50 and not self.__is_killing:  # boss机中弹10次才让他消失
        #     self.__is_killing = True
        #     self.timer_run(1, self.boss_kl)
