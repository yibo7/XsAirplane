# 主场景中增加如下代码，一个用来绘制，一个用来计算坐标，分工明确

from threading import Timer

import pygame
from pygame.sprite import spritecollide

from planes.boss_plance import BossPlance
from planes.enemy_plance import EnemyPlance
from planes.hero_plane import HeroPlane
from scenes.leve1.background import GameBackground
from sprites.text_show import TextShow


class MainScene(object):

    # 初始化主场景
    def __init__(self, screen):
        # 创建地图对象
        self.boss_kill_count = 0
        self.enemy_kill_count = 0
        self.hero_kill_count = 0
        self.hero_live = 100
        self.hero_is_live = True
        self.size = screen.get_size()
        self.scene = screen
        self.boss_is_live = False
        self.map = GameBackground(self)
        self.heros = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.create_hero()
        self.create_enemy()


        Timer(30, self.create_boss, ()).start()
        pygame.mixer.music.load("sounds/bg.mp3")
        pygame.mixer.music.play(-1, 0)



    def create_hero(self):
        self.heros.add(HeroPlane(self.scene,self.hero_live))

    def create_enemy(self):
        """
        创建敌机
        :return:
        """
        if self.hero_is_live:
            enemy = EnemyPlance(self.scene)
            self.enemys.add(enemy)
            self.enemys.update()
            enemy_time = 1
            if self.boss_is_live:
                enemy_time = 3
            Timer(enemy_time, self.create_enemy, ()).start()



    def boss_kill(self, boss):
        self.enemys.remove(boss)
        self.boss_is_live = False
        self.boss_kill_count += 1

        self.map.change_speed(10)
        Timer(20, self.reset_map_speed, ()).start()

        Timer(30, self.create_boss, ()).start()
        Timer(60, self.create_boss, ()).start()

        for hero in self.heros:
            hero.next_bluet()  # 将要切换场景，所以重置击敌数,妆更换子弹

    def reset_map_speed(self):
        self.map.change_speed(2)
        self.map.next_map()

    def create_boss(self):
        if self.hero_is_live:
            boss = BossPlance(self.scene, self.boss_kill)
            self.enemys.add(boss)
            self.boss_is_live = True


    def actions(self):
        self.map.draw()

        # 检测英雄机是否与敌机碰撞
        for hero in self.heros:
            hero.action()
            hero_link_enemys = spritecollide(hero, self.enemys, False)
            if hero_link_enemys:
                hero.collide()
                self.hero_kill_count +=1

        # 检测敌机是否与英雄机的子弹碰撞，如果有，清除子弹并调用敌机中弹em.collide()
        for em in self.enemys.sprites():
            em.action()
            for hero in self.heros:
                bluet_link_enemys = spritecollide(em, hero.bluets, True)
                if bluet_link_enemys:
                    em.collide()
                    self.enemy_kill_count += 1
                    hero.update_kill_count() # 累加击敌数

            # 检测 英雄机与敌机的子弹是否碰撞
            for hero in self.heros:
                bluet_link_hero = spritecollide(hero, em.bluets, True)
                if bluet_link_hero:
                    hero.collide()
                    self.hero_kill_count += 1

        live = self.hero_live - self.hero_kill_count
        if live < 0:
            live = 0
            self.hero_is_live = False

        TextShow(self.scene, f"生命值:{live}  击中:{self.enemy_kill_count}", 16, [98, 224, 79], 160, 30, (self.scene.get_width() - 100, 30))

        if not self.hero_is_live:
            TextShow(self.scene, "游戏结束", 30, [255, 0, 0], 300, 80,
                     (self.scene.get_width() / 2, self.scene.get_height() / 2))
