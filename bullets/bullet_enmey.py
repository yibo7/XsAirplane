from SpriteBase import SpriteBase


class BulletEnmey(SpriteBase):
    def __init__(self, plance, screen, _speed=None):
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
