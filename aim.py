from init import SPRITE, SPRITES

class Aim(SPRITE):
    def __init__(self):
        SPRITE.__init__(self)
        self.image = SPRITES['aim']
        self.rect = self.image.get_rect()

    def update(self, mouse_x, mouse_y):
        self.rect.centerx = mouse_x
        self.rect.centery = mouse_y