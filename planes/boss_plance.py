import time

from bullets.bullet_enmey import BulletEnmey
from planes.plance_base import PlanceBase

"""
boss 敌机
"""


class BossPlance(PlanceBase):  # boss机派生自PlanceBase，要重写PlanceBase相关的方法
    def __init__(self, sc, fun):
        self.boss_kill = fun
        self.screen = sc
        super(BossPlance, self).__init__(sc)
        self.is_right = self.rect.x < self.win.get_width() / 2

    def get_size(self):  # 重写基类方法，将鼠标放上去看说明
        return 10

    def get_speed(self):  # 重写基类方法，将鼠标放上去看说明
        return 2

    def getImagePaths(self):  # 重写基类方法，将鼠标放上去看说明
        paths = []
        for i in range(7):
            paths.append(f"images/boss/{i}.png")
        return paths

    def getLocation(self):  # 重写基类方法，将鼠标放上去看说明
        # boss机在创建的时候，我们给他一个随机位置，并且出现上场景上方不可见区域
        location = [self.random(20, self.screen.get_width() - 30), -50]
        return location

    def creat_bluet(self):  # 重写基类方法，将鼠标放上去看说明
        # 子弹在创建的时候播放一个声音
        self.playSound("sounds/bosssend.wav")
        # 每次发送连着快速发送5个枚子弹
        for i in range(5):
            bullet = BulletEnmey(self, self.win, _speed=17)
            bullet_index = self.random(4, 8)  # 随机获取子弹的造型图片
            bullet.change_image(bullet_index)
            self.bluets.add(bullet)
            self.bluets.update()  # 这个方法的调用好像不需要也行
            time.sleep(0.2)  # 速度很快
        if not self.__is_killing:  # kill的并不会销毁这个实体
            self.timer_run(3, self.creat_bluet)  # 每3秒发送一次子弹

    def action(self):  # 重写基类方法，将鼠标放上去看说明

        # 将所有子弹的动作绘制到场景内存中
        for em in self.bluets.sprites():
            em.action()

        if self.rect.y < 100:  # boss机创建后会一直往前走100步
            self.rect.y += self.speed
        else:  # 当boss机向前走了100步后，就一直让他左右走动

            if self.is_right:
                self.rect.x += 1
                if self.rect.right > self.win.get_width():
                    self.is_right = False
            else:
                self.rect.x -= 1
                if self.rect.left < 0:
                    self.is_right = True

        # 将变动绘制到屏幕
        self.draw()

    def boss_kl(self):
        """
        boss机被击爆
        :return:
        """
        self.__is_killing = True
        self.playSound("sounds/bossbz.wav")
        self.change_image(6)
        time.sleep(2)
        self.kill()
        self.boss_kill(self)

    def collide(self):  # 重写基类方法，将鼠标放上去看说明
        self.collide_count += 1  # 统计boss机被击中的次数
        # 当boss机被击中大于50次的时，这个boss机进入燃烧状态
        if self.collide_count > 50 and not self.__is_changing:  # boss机中弹10次才让他消失
            # 将__is_changing设置为True,从上面的if里可以看出，这是为了防止下次来再时重复调用这个change_model
            # 因为change_model有延时操作，并且change_model只允许调用一次
            self.__is_changing = True
            self.timer_run(1, self.change_model)

    __is_changing = False  # 辅助锁定变量

    def change_model(self):
        # boss 机燃烧 10次后结果生命
        for i in range(10):
            self.change_image(1)
            time.sleep(0.5)
            self.change_image(2)
            time.sleep(0.5)
            self.change_image(3)
            time.sleep(0.5)
            self.change_image(4)
            time.sleep(0.5)
            self.change_image(5)
            time.sleep(0.5)

        self.boss_kl()  # boss机结束生命

    __is_killing = False
