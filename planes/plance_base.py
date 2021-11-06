import pygame

from SpriteBase import SpriteBase


class PlanceBase(SpriteBase):

    def __init__(self, screen):
        location = self.getLocation()
        paths = self.getImagePaths()
        sp = self.get_speed()
        s = self.get_size()
        imageIndex = self.get_default_image()
        super(PlanceBase, self).__init__(screen, paths, location, size=s, speed=sp, image_index=imageIndex)

        self.bluets = pygame.sprite.Group()
        self.creat_bluet()
        self.collide_count = 0

    def get_default_image(self):
        return 0

    def get_size(self):
        return 0

    def get_speed(self):
        raise Exception('子类中必须实现get_speed')

    def creat_bluet(self):
        raise Exception('子类中必须实现creat_bluet')

    def getImagePaths(self):
        raise Exception('子类中必须实现getImagePaths')

    def getLocation(self):
        raise Exception('子类中必须实现getLocation')

    def action(self):
        raise Exception('子类中必须实现getLocation')

    def collide(self):
        raise Exception('子类中必须实现collide')
