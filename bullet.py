from init import PG, SPRITE, SPRITES, GROUP
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_BULLET_SPEED, PLAYER_HALF_SPRITE_SIZE
from math import sin, cos, radians

bullets_group = GROUP()

class Bullet(SPRITE):
    def __init__(self, x, y, direction):
        SPRITE.__init__(self)
        image = SPRITES['player_bullet']
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate( image, -direction )
        self.rect = self.image.get_rect(center = (x, y))
        self.direction = direction

        self.speed = PLAYER_BULLET_SPEED
        angle = radians(direction)
        self.speed_x = cos(angle) * self.speed
        self.speed_y = sin(angle) * self.speed

        # смещаем пулю к краю спрайта (появление в конце дула)
        self.center_x = x + self.speed_x * (PLAYER_HALF_SPRITE_SIZE / self.speed)
        self.center_y = y + self.speed_y * (PLAYER_HALF_SPRITE_SIZE / self.speed)
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        bullets_group.add(self)

    def update(self):
        self.center_x += self.speed_x
        self.center_y += self.speed_y
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH \
        or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT :
            self.kill()

    def draw(self, screen):
            screen.blit(self.image, self.rect)