import threading
from random import choice, randint


import pygame
from pygame.sprite import Sprite


class SpriteBase(Sprite):
    def __init__(self, screen, image_paths, location,size=0,speed=1,image_index=0):
        Sprite.__init__(self)
        self.win = screen
        self.images = []
        for path in image_paths:
            image = pygame.image.load(path)
            if size != 0:
                image = pygame.transform.scale(image, (image.get_width()+size, image.get_height()+size))
            self.images.append(image)
        self.current_index = image_index
        self.image = self.images[self.current_index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed  # 每次移动的像素,默认1个
        self.speeds = [choice([-1, 1]), choice([-1, 1])]  # x的速度，y的速度

    # def thread_run(self,fun):
    #     threading.Thread(target=fun).run()

    def timer_run(self,second,fun):
        """
        定时执行，只做一次，如果重复请回调进行
        :param fun: 要执行的方法
        :param second: 多长时间执行，秒
        :return:
        """
        threading.Timer(second, fun, ()).start()


    def playSound(self, path):
        player = pygame.mixer.Sound(path)
        player.play()

    def getWidth(self):
        return self.win.get_width()

    def getHeight(self):
        return self.win.get_height()

    def random(self, star, end):
        return randint(star, end)

    def draw(self):
        self.win.blit(self.image, self.rect)

    def move(self, pos_X, pos_Y):
        self.rect.center = [pos_X, pos_Y]

    def moveRand(self):
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



