# 按间距中的绿色按钮以运行脚本。

import pygame

from scenes.leve1.main_scene import MainScene
clock = pygame.time.Clock()

def update():
    """
    flip函数将重新绘制整个屏幕对应的窗口。
    update函数仅仅重新绘制窗口中有变化的区域。
    如果仅仅是几个物体在移动，那么他只重绘其中移动的部分，没有变化的部分，并不进行重绘。update比flip速度更快。
    因此在一般的游戏中，如果不是场景变化非常频繁的时候，我们建议使用update函数，而不是flip函数。
    :return:
    :return:
    """
    # pygame.display.flip()
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode([512, 768])
    # window.fill([255, 255, 255])
    sceneManger = MainScene(window)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # sceneManger.eventAction(event)
        # window.fill([255, 255, 255])
        sceneManger.actions()
        update()
        clock.tick(60)

    pygame.quit()
