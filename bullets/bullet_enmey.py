from SpriteBase import SpriteBase

"""
敌机子弹
"""


class BulletEnmey(SpriteBase):
    def __init__(self, plance, screen, _speed=None):
        """
        创建敌机子弹,注意：通过基类的change_image可以更换子弹造型
        :param plance: 敌机（哪个敌机）
        :param screen: 在哪个场景上绘制
        :param _speed: 子弹的速度
        """
        paths = []
        for i in range(9):
            paths.append(f"images/enemybullet/{i}.png")

        pos = [plance.rect.left + 30, plance.rect.top + 50]
        imageIndex = 0  # self.random(0,5)
        if _speed is None:
            _speed = self.random(5, 11)
        super(BulletEnmey, self).__init__(screen, paths, pos, speed=_speed, image_index=imageIndex)

    def action(self):

        if self.rect.bottom < self.win.get_height():
            self.rect.y += self.speed
            if self.speed > 10:
                self.moveRand()
            self.draw()
        else:
            self.kill()
