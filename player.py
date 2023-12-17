from init import PG, SPRITE, SPRITES
from constants import FPS, PLAYER_SPEED, PLAYER_DIRECTION, PLAYER_SHUT_TIMEOUT
from utils import turn_sprite_to_target
from bullet import Bullet

class Player(SPRITE):
    def __init__(self, x, y):
        SPRITE.__init__(self)
        self.start_image = SPRITES['player'] # исходный спрайт игрока без поворота на какой-либо угол
        self.image = self.start_image # self.image - здесь будем хранить повернутый спрайт для отрисовки
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = PLAYER_SPEED
        self.direction = PLAYER_DIRECTION

        self.shut_frames = round(PLAYER_SHUT_TIMEOUT * FPS)
        self.shut_delay = self.shut_frames
        self.is_shooting = False

    def update(self, mouse_x, mouse_y, events):
        # поворачиваем игрока к курсору мыши
        turn_sprite_to_target(self, mouse_x, mouse_y)
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate(self.start_image, -self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)

        # считаем кадры до следующего выстрела
        if self.shut_delay > 0 : self.shut_delay -= 1
        # если зажана левая кнопка мыши - активируем проверку стрельбы
        for event in events:
            if event.type == PG.MOUSEBUTTONDOWN and event.button == 1 : self.is_shooting = True
            if event.type == PG.MOUSEBUTTONUP and event.button == 1 : self.is_shooting = False
        # если готовы стрелять и стрельба активирована - стреляем
        if self.is_shooting and self.shut_delay == 0:
            self.shut_delay = self.shut_frames
            Bullet(self.rect.centerx, self.rect.centery, self.direction)

        # двигаем игрока, если нажаты клавиши для перемещения
        key = PG.key.get_pressed()
        if key[PG.K_LEFT] or key[PG.K_a]:
            self.rect.centerx -= self.speed
        if key[PG.K_RIGHT] or key[PG.K_d]:
            self.rect.centerx += self.speed
        if key[PG.K_UP] or key[PG.K_w]:
            self.rect.centery -= self.speed
        if key[PG.K_DOWN] or key[PG.K_s]:
            self.rect.centery += self.speed

    