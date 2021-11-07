# 按间距中的绿色按钮以运行脚本。

import pygame

from scenes.leve1.main_scene import MainScene
clock = pygame.time.Clock()

def update():
    """
    将内存中绘制好的结果，更新到场景中
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
    pygame.mixer.init()  # 要播放声音前得先初始化这个组件
    window = pygame.display.set_mode([512, 768])  # 开启一个宽是512,高是768 像素的窗口
    # window.fill([255, 255, 255])
    sceneManger = MainScene(window) # 创建主场景

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 监听用户的事件，如果点击了关闭窗口的按钮，将退出
                running = False
            # sceneManger.eventAction(event)

        # window.fill([255, 255, 255]) # 测试将界面填充为白色

        # actions 是将所有精灵的动态综合到内存里，在while循环快速的变化下进行，然后调用update更新到场景窗口中，所以会呈现出动画效果
        sceneManger.actions()
        update()
        clock.tick(60)  # 每秒播放60贴

    pygame.quit()  # 最后退出程序，这个方法正常情况下无法执行到，除非running = False，也就是用户点击了关闭
