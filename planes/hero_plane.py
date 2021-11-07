import time
import pygame
from bullets.bullet_hero import BulletHero
from planes.plance_base import PlanceBase
from sprites.text_show import TextShow

"""
英雄机
"""


class HeroPlane(PlanceBase):
    """
    英雄机
    所有的飞机都会派生自 PlanceBase，要实现基类的相关方法
    """

    def __init__(self, screen, lv):
        self.bullet_leve = 0
        self.bullet_speed = 0.2
        self.enmey_kill_count = 0
        self.live = lv
        super(HeroPlane, self).__init__(screen)

    def get_speed(self):
        """
        重写基类的速度,将英雄机的速度设置为10
        :return:
        """
        return 10

    def getLocation(self):
        """
        重写英雄机的创建位置，由于我们的屏幕是 512, 768
        我们要将英雄机创建的时候出现的位置在场景的底下上一点，所以可以设置成220,650
        :return:
        """
        return [220, 650]

    def getImagePaths(self):
        """
        设置英雄机的造型图片
        :return:
        """
        paths = []
        for i in range(4):
            paths.append(f"images/hero/{i}.png")
        return paths

    def next_bluet(self):
        """
        升级英雄机子弹
        1.让英雄机的子弹切换到下一造型，
        2.并将子弹速度设置为：0.1 越小越快
        3.将本场景中的击敌数(enmey_kill_count)值归零，因为英雄机是根据击敌数来改变散弹类型的
        :return:
        """
        if self.bullet_leve < 2:
            self.bullet_leve += 1

        self.bullet_speed = 0.1
        self.enmey_kill_count = 0

    def update_kill_count(self):
        """
        让英雄机的击敌数加1
        :return:
        """
        self.enmey_kill_count += 1

    def creat_bluet(self):
        """
        创建一次子弹，也就是发送一次子弹
        :return:
        """
        bullet_img_index = self.bullet_leve  # 子弹的造型

        # 发送子弹的同时，随机发送导弹
        # 默认规则是取出100内的随机数，并做对比
        # 默认情况下导弹随机数小于5才发送
        rand = self.random(1, 100)
        is_seng_big = False
        if rand < 5:
            is_seng_big = True

        if 50 < self.enmey_kill_count < 100:  # 当击敌数大于50并小于100时，子弹变成二级散弹
            if rand < 10:  # 当击敌数达到二级时，导弹随机机率也会变大一倍
                is_seng_big = True
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=1))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=-1))
        elif 100 < self.enmey_kill_count < 300:  # 当击敌数大于100并小于300时，子弹变成三级散弹
            if rand < 20:  # 当击敌数达到三级时，导弹随机机率也会变大一倍
                is_seng_big = True
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=3))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=-3))
        elif self.enmey_kill_count > 300:  # 当击敌数大300时，子弹变成顶级散弹
            if rand < 30:  # 当击敌数达到最后一级时，导弹随机机率也会变大一倍
                is_seng_big = True
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=6))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=3))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=-3))
            self.bluets.add(BulletHero(self, self.win, bullet_img_index, xspeed=6))
        else:  # 默认情况下，一次只发一枚子弹
            self.bluets.add(BulletHero(self, self.win, bullet_img_index))

        if is_seng_big:  # 是否发送导弹
            self.bluets.add(BulletHero(self, self.win, self.bullet_leve + 3, xspeed=3, yspeed=10))
            self.bluets.add(BulletHero(self, self.win, self.bullet_leve + 3, xspeed=-3, yspeed=10))

        self.bluets.update()
        self.timer_run(self.bullet_speed, self.creat_bluet)  # 定时回调这个发送子弹的方法，bullet_speed是间隔时间
        # self.playSound("sounds/send.wav")

    def action(self):
        """
        将这个精灵的所有动作绘制到内存，由前面的update统一更新
        :return:
        """
        self.__control()  # 对英雄机的控制动作
        self.draw()  # 开始绘制到屏幕

        for em in self.bluets.sprites():  # 将所有子弹的动作绘制到屏幕
            em.action()

    def collide(self):
        """
        如果英雄机被碰撞，这个方法会被调用
        :return:
        """
        self.collide_count += 1  # 累加碰撞次数

        if not self.__is_changing:  # 加个锁，主要是为了防止重复调用__change_model
            self.timer_run(1, self.__change_model)

        if self.collide_count > self.live:  # 达到指定的碰撞总次数，英雄机将消失
            self.kill()

    __is_changing = False

    def __change_model(self):
        """
        被碰撞后，更改英雄机的造型为着火模式
        :return:
        """
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
        """
        对英雄机的上，下，左，右控制
        :return:
        """
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
        if self.rect.left > 0:  # 如果超出左边，将不再移动
            self.rect.x -= self.speed

    def moveRight(self):
        if self.rect.right < self.win.get_width():  # 如果超出右边，将不再移动
            self.rect.x += self.speed

    def moveUp(self):
        if self.rect.top > 0:  # 如果超出上边，将不再移动
            self.rect.y -= self.speed

    def moveDown(self):
        if self.rect.bottom < self.win.get_height():  # 如果超出下边，将不再移动
            self.rect.y += self.speed
