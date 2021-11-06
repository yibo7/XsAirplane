# 地图
import pygame


class GameBackground(object):
    # 初始化地图
    def __init__(self, scene):
        # 加载相同张图片资源,做交替实现地图滚动
        self.image_index = -1
        self.image1 = None
        self.image2 = None
        self.next_map()
        # 保存场景对象
        self.main_scene = scene
        # 辅助移动地图
        self.y1 = 0
        self.y2 = -self.main_scene.size[1]
        self.speed = 1

    def next_map(self):
        if self.image_index <3:
            self.image_index +=1
        else:
            self.image_index =0

        path = f"images/scenes/{self.image_index}.png"
        self.image1 = pygame.image.load(path)
        self.image2 = pygame.image.load(path)

    def change_speed(self,spe):
        self.speed = spe

    # 计算地图图片绘制坐标
    def action(self):
        self.y1 = self.y1 + self.speed
        self.y2 = self.y2 + self.speed
        if self.y1 >= self.main_scene.size[1]:
            self.y1 = 0
        if self.y2 >= 0:
            self.y2 = -self.main_scene.size[1]

    # 绘制地图的两张图片
    def draw(self):
        self.action()
        self.main_scene.scene.blit(self.image1, (0, self.y1))
        self.main_scene.scene.blit(self.image2, (0, self.y2))