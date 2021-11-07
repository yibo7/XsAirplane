import pygame

from SpriteBase import SpriteBase

"""
所有战机的基类，这里将战机的共性集中在一起，提供给所有有战机使用
"""


class PlanceBase(SpriteBase):

    def __init__(self, screen):
        """
        在子类要调用这个初始化方法
        :param screen:
        """
        location = self.getLocation()  # 获取子类重写的位置
        paths = self.getImagePaths()  # 获取子类重写的造型
        sp = self.get_speed()  # 获取子类重写的速度
        self.size = self.get_size()  # 获取子类重写的战机大小
        imageIndex = self.get_default_image()  # 获取子类重写的默认造型
        super(PlanceBase, self).__init__(screen, paths, location, size=self.size, speed=sp, image_index=imageIndex)

        self.bluets = pygame.sprite.Group()  # 这是精灵组，为所有的战机创建一个子弹夹
        self.creat_bluet()  # 开始构建(放射)子弹
        self.collide_count = 0  # 定义战机的碰撞次数计数器

    def get_default_image(self):
        """
        获取点击的默认造型,这样可以随机生成战机，比如 小敌机
        默认为0,也就是第一个造型
        :return:
        """
        return 0

    def get_size(self):
        """
        创建战机时的大小，默认为0，将按原图片大小
        :return:
        """
        return 0

    def get_speed(self):
        """
        在子类要实现战机创建时的速度
        :return:
        """
        raise Exception('子类中必须实现get_speed')

    def creat_bluet(self):
        """
        在子类要实现战机的的子弹创建过程
        :return:
        """
        raise Exception('子类中必须实现creat_bluet')

    def getImagePaths(self):
        """
        在子类要加载战机的的所有造型
        :return:
        """
        raise Exception('子类中必须实现getImagePaths')

    def getLocation(self):
        """
        在子类要实现战机的创建时的位置
        :return:
        """
        raise Exception('子类中必须实现getLocation')

    def action(self):
        """
        在子类要实现战机的所有动作
        :return:
        """
        raise Exception('子类中必须实现getLocation')

    def collide(self):
        """
        在子类要实现战机的的碰撞处理过程及显示效果
        :return:
        """
        raise Exception('子类中必须实现collide')
