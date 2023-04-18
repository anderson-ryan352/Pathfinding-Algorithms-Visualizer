import pygame


class Button:
    def __init__(self, x,y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def isActivated(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
