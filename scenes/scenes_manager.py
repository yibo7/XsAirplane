from scenes.leve1.main_scene import MainScene


# class ScenesManager:
#     def __init__(self, wind):
#         self.win = wind
#         self.scenes = [MainScene(wind)]
#         self.current_scene = self.scenes[0]
#
#     def draw(self):
#         self.current_scene.action()
#         self.current_scene.draw()
#
#     def eventAction(self, ev):
#         if ev.type == self.enemy_creat:
#             self.enemys.append(EnemyPlance(self.scene))