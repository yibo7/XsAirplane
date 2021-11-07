import threading
from random import choice, randint

import pygame
from pygame.sprite import Sprite

"""
所有动画精灵的基类，所有动的东西都可以派生自这个类，这个方法提供了最本的精灵操作
"""


class SpriteBase(Sprite):
    def __init__(self, screen, image_paths, location, size=0, speed=1, image_index=0):
        """
        精灵初始化
        :param screen:要将精灵绘制到哪个场景，也就是创建时的窗口
        :param image_paths: 精灵的造型图片
        :param location:    精灵创建时的位置
        :param size:    精灵创建时的大小
        :param speed:   精灵移动时的速度，越大越快
        :param image_index: 精灵默认的造型图片
        """
        Sprite.__init__(self)
        self.win = screen
        self.images = []
        for path in image_paths:
            image = pygame.image.load(path)
            if size != 0:
                image = pygame.transform.scale(image, (image.get_width() + size, image.get_height() + size))
            self.images.append(image)
        self.current_index = image_index
        self.image = self.images[self.current_index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed  # 每次移动的像素,默认1个
        self.speeds = [choice([-1, 1]), choice([-1, 1])]  # x的速度，y的速度

    # def thread_run(self,fun):
    #     threading.Thread(target=fun).run()

    def timer_run(self, second, fun):
        """
        定时执行，只做一次，如果重复请回调进行
        :param fun: 要执行的方法
        :param second: 多长时间执行，秒
        :return:
        """
        threading.Timer(second, fun, ()).start()

    def playSound(self, path):
        """
        播放声音
        :param path: 声音的文件的相对路径
        :return:
        """
        player = pygame.mixer.Sound(path)
        player.play()

    def getWidth(self):
        """
        获取精灵的宽
        :return:
        """
        return self.win.get_width()

    def getHeight(self):
        """
        获取精灵的高
        :return:
        """
        return self.win.get_height()

    def random(self, star, end):
        """
        获取一个随机整数
        :param star: 范围的开始
        :param end: 范围的结束
        :return: 随机数
        """
        return randint(star, end)

    def draw(self):
        """
        将精灵绘制到场景中，这里只是内存绘制，最终要通过update更新到场景
        :return:
        """
        self.win.blit(self.image, self.rect)

    def move(self, pos_X, pos_Y):
        """
        精灵的移动
        :param pos_X:
        :param pos_Y:
        :return:
        """
        self.rect.center = [pos_X, pos_Y]

    def moveRand(self):
        """
        让当前这个精灵随机移动
        :return:
        """
        self.rect = self.rect.move(self.speeds)
        if self.rect.left < 0 or self.rect.right > self.win.get_width():
            self.speeds[0] = -self.speeds[0]
        if self.rect.top < 0 or self.rect.bottom > self.win.get_height():
            self.speeds[1] = -self.speeds[1]

    def change_image(self, index):
        """
        更换造型
        :param index: 对象的图片索引
        :return:
        """
        self.current_index = index
        self.image = self.images[self.current_index]
        # 设置坐标值，也就是新的造型坐标设置为当前造型的坐标位置
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def next_image(self):
        """
        下一个造型
        :return:
        """
        index = self.current_index
        index += 1
        if index >= len(self.images):
            index = 0
        self.change_image(index)
