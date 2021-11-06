from SpriteBase import SpriteBase


class BulletHero(SpriteBase):
    def __init__(self, sp, screen, img_index, xspeed=0, yspeed=15):
        self.x_speed = xspeed
        paths = []
        for i in range(6):
            paths.append(f"images/herobullet/{i}.png")

        pos = [sp.rect.left + 30, sp.rect.top - 30]

        super(BulletHero, self).__init__(screen, paths, pos, speed=yspeed, image_index=img_index)

    y_step = 0

    def action(self):
        if self.rect.top > 0:
            self.y_step += 1
            self.rect.y -= self.speed
            if self.x_speed != 0:
                self.rect.x += self.x_speed
            # if self.y_step % 2 ==0:
            #     self.rect.x+=1
            self.draw()
        else:
            self.kill()
