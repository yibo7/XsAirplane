from SpriteBase import SpriteBase

"""
英雄机的子弹
"""

class BulletHero(SpriteBase):
    def __init__(self, sp, screen, img_index, xspeed=0, yspeed=15):
        """
        创建英雄机子弹
        :param sp: 来自哪个英雄机
        :param screen: 要将子弹绘制到哪个场景
        :param img_index: 子弹的默认造型
        :param xspeed: 子弹的横向速度
        :param yspeed: 子弹的纵向速度
        """
        self.x_speed = xspeed # 子弹每次移动的横向步数
        # self.y_step = 0
        paths = []
        for i in range(6):
            paths.append(f"images/herobullet/{i}.png")

        # 子弹的位置应该出现在英雄机的中上方
        pos = [sp.rect.left + 30, sp.rect.top - 50]

        super(BulletHero, self).__init__(screen, paths, pos, speed=yspeed, image_index=img_index)



    def action(self):
        if self.rect.top > 0: # 如果子弹还没到屏幕的最上方，就一直向上移动
            # self.y_step += 1
            self.rect.y -= self.speed

            if self.x_speed != 0: # 向上移动的同时是否横着走，x_speed为正数，表示向右横，为负数表达向左横
                self.rect.x += self.x_speed
            self.draw()
        else:
            self.kill()
