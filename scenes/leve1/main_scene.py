# 主场景中增加如下代码，一个用来绘制，一个用来计算坐标，分工明确

from threading import Timer

import pygame
from pygame.sprite import spritecollide

from planes.boss_plance import BossPlance
from planes.enemy_plance import EnemyPlance
from planes.hero_plane import HeroPlane
from scenes.leve1.background import GameBackground
from sprites.text_show import TextShow

"""
主场景,一般来说场景也应该是通过一个集合来管理，但考虑到这个程序只是简单的演示，
所以只使用了一个主场景类来简单实现不同场景的切换
"""


class MainScene(object):

    # 初始化主场景
    def __init__(self, screen):
        """
        初始化
        :param screen:要将这个场景的所有精灵绘制到哪个界面
        """

        self.boss_kill_count = 0  # boss 碰撞计数器
        self.enemy_kill_count = 0  # 普通敌机碰撞计数器
        self.hero_kill_count = 0  # 英雄机碰撞计数器
        self.hero_live = 100  # 设置英雄机的生成次数
        self.hero_is_live = True  # 跟踪英雄机的生命状态，是否还活着
        self.boss_is_live = False  # 跟踪boss机的生命状态，是否还活着
        self.size = screen.get_size()  # 获取场景的大小
        self.scene = screen  # 场景
        self.map = GameBackground(self)  # 创建当前场景的滚动背景
        self.heros = pygame.sprite.Group()  # 所有英雄机精灵组，主要是用来做碰撞检测
        self.enemys = pygame.sprite.Group()  # 所有敌机精灵组
        self.create_hero()  # 创建一个英雄机
        self.create_enemy()  # 创建普通敌机
        # 30秒后，创建第一个boss机
        Timer(30, self.create_boss, ()).start()

        # 播放背景音乐
        pygame.mixer.music.load("sounds/bg.mp3")
        pygame.mixer.music.play(-1, 0)

    def create_hero(self):
        """
        创建英雄机
        :return:
        """
        self.heros.add(HeroPlane(self.scene, self.hero_live))

    def create_enemy(self):
        """
        创建普通敌机
        :return:
        """
        if self.hero_is_live: # 如果英雄机还活着，才创建，否则停止创建
            enemy = EnemyPlance(self.scene)
            self.enemys.add(enemy) # 将敌机添加到普通敌机精灵组
            self.enemys.update()  # 这个方法好像也不用调用
            enemy_time = 1      # 默认1秒创建一个敌机
            if self.boss_is_live: # 当boss机出现的时候，应该减少普通敌机，所以3秒再合建一个普通敌机
                enemy_time = 3
            Timer(enemy_time, self.create_enemy, ()).start() # 回调敌机创建方法

    def boss_kill(self, boss):
        """
        这个方法是在boss创建的时候传给boss机对象的,目的是让boss机被击爆后触发这个方法
        :param boss:
        :return:
        """
        self.enemys.remove(boss) # 从敌机精灵组中移除boss
        self.boss_is_live = False # 告诉当前场景，boss已经被击爆了
        self.boss_kill_count += 1 # boss被击爆的次数

        self.map.change_speed(10) # 如果 有boss被击爆，将地图的滚动速度变快

        Timer(20, self.reset_map_speed, ()).start() # 20秒后恢复地图的速度

        Timer(30, self.create_boss, ()).start() # 30秒后再创建一个boss机
        Timer(60, self.create_boss, ()).start() # 30秒后再创建一个boss机

        for hero in self.heros: #
            hero.next_bluet()  # 击爆了boss机，所以可以升级英雄机的子弹

    def reset_map_speed(self):
        """
        重置地图片的速度为正常模式，将切换到下一个地图
        这是在击爆boss机并进入快速地图滚动模式后的恢复与更换
        :return:
        """
        self.map.change_speed(2)
        self.map.next_map()

    def create_boss(self):
        """
        创建boss机
        :return:
        """
        if self.hero_is_live: # 如果英雄机还活着，再创建
            boss = BossPlance(self.scene, self.boss_kill)
            self.enemys.add(boss)
            self.boss_is_live = True # 标记场景的boss机还有

    def actions(self):
        self.map.draw() # 绘制地图

        # 检测英雄机是否与敌机碰撞
        for hero in self.heros:
            hero.action()
            hero_link_enemys = spritecollide(hero, self.enemys, False)
            if hero_link_enemys:
                hero.collide()
                self.hero_kill_count += 1

        # 检测敌机是否与英雄机的子弹碰撞，如果有，清除子弹并调用敌机中弹em.collide()
        for em in self.enemys.sprites():
            em.action()
            for hero in self.heros:
                bluet_link_enemys = spritecollide(em, hero.bluets, True)
                if bluet_link_enemys:
                    em.collide()
                    self.enemy_kill_count += 1
                    hero.update_kill_count()  # 累加击敌数

            # 检测 英雄机与敌机的子弹是否碰撞
            for hero in self.heros:
                bluet_link_hero = spritecollide(hero, em.bluets, True)
                if bluet_link_hero:
                    hero.collide()
                    self.hero_kill_count += 1

        # 如果英雄机的生命总数减去被击中的次数小于0,要结束游戏，所以要将self.hero_is_live = False
        live = self.hero_live - self.hero_kill_count
        if live < 0:
            # live = 0
            self.hero_is_live = False

        TextShow(self.scene, f"生命值:{live}  击中:{self.enemy_kill_count}", 16, [98, 224, 79], 160, 30,
                 (self.scene.get_width() - 100, 30))

        if not self.hero_is_live:
            TextShow(self.scene, "游戏结束", 30, [255, 0, 0], 300, 80,
                     (self.scene.get_width() / 2, self.scene.get_height() / 2))
