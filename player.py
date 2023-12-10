from init import PG, SPRITE, SPRITES
from constants import PLAYER_SPEED

class Player(SPRITE):
    def __init__(self, x, y):
        SPRITE.__init__(self)
        self.image = SPRITES['player']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = PLAYER_SPEED

    def update(self):
        key = PG.key.get_pressed()
        if key[PG.K_LEFT] or key[PG.K_a]:
            self.rect.centerx -= self.speed
        if key[PG.K_RIGHT] or key[PG.K_d]:
            self.rect.centerx += self.speed
        if key[PG.K_UP] or key[PG.K_w]:
            self.rect.centery -= self.speed
        if key[PG.K_DOWN] or key[PG.K_s]:
            self.rect.centery += self.speed

    