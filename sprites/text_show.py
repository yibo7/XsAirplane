import pygame
from pygame.sprite import Sprite


class TextShow(Sprite):
    def __init__(self, screen,text, size, color, width, height,pos):
        # Call the parent class (Sprite) constructor
        Sprite.__init__(self)

        self.font = pygame.font.SysFont("SimHei", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill((0,0,0,70))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - W / 2, height / 2 - H / 2])

        self.rect = self.image.get_rect()
        self.rect.center = pos

        screen.blit(self.image, self.rect)