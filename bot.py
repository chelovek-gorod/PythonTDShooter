# ВРАГИ

# из файла init импортируем PG(PyGame), класс SPRITE, словарь со спрайтами SPRITES и класс GROUP (для создания групп спрайтов)
from init import PG, SPRITE, SPRITES, GROUP
# из файла constants импортируем все необходимые переменные, которые понадобятся для создания и управления врагами
from constants import FPS, UNIT_HP, BOT_ARMOR, DROID_ARMOR, CYBORG_ARMOR, BOT_SPEED, DROID_SPEED, CYBORG_SPEED, \
    BOT_PLASMA_MIN_TIMEOUT, BOT_PLASMA_MAX_TIMEOUT, DROID_PLASMA_MIN_TIMEOUT, DROID_PLASMA_MAX_TIMEOUT, \
    CYBORG_PLASMA_MIN_TIMEOUT, CYBORG_PLASMA_MAX_TIMEOUT, PLAYER_BULLET_POWER
# из файла utils импортируем функцию, поворачивающую спрайт к определенной цели 
from utils import turn_sprite_to_target
# из файла plasma импортируем класс Plasma (для создания объектов плазмы от вражеских выстрелов)
from plasma import Plasma
# из файла healthbar импортируем класс Healthbar (для создания полосок здоровья)
from healthbar import Healthbar
# из библиотеки random импортируем функцию randint (для генерации случайных целых чисел)
from random import randint
# из файла effect импортируем класс Effect (для создания анимированных эффектов)
from effect import Effect

# создаем группу спрайтов для хранения врагов
bots_group = GROUP()

# класс Bot (наследуется от класса SPRITE из библиотеки PyGame)
class Bot(SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, и вид врага)
    def __init__(self, x, y, bot_type = 'droid'):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.start_image = SPRITES[bot_type] # исходный спрайт врага без поворота на какой-либо угол
        self.image = self.start_image # в поле image будем хранить повернутый спрайт для отрисовки
        self.rect = self.image.get_rect(center = (x, y)) # создаем прямоугольник по размерам спрайта с центрам в x и y
        self.hp = UNIT_HP # в поле hp записываем жизни врага
        # в поля armor и speed записываем защиту и скорость, время перезарядки в зависимости от типа врага
        if bot_type == 'droid':
            self.armor = DROID_ARMOR
            self.speed = DROID_SPEED
            self.shut_min_frames = round(DROID_PLASMA_MIN_TIMEOUT * FPS) # минимальное число кадров для следующего выстрела
            self.shut_max_frames = round(DROID_PLASMA_MAX_TIMEOUT * FPS) # максимальное число кадров для следующего выстрела
            self.shut_delay = randint(self.shut_min_frames, self.shut_max_frames) # число кадров для следующего выстрела
        elif bot_type == 'cyborg':
            self.armor = CYBORG_ARMOR
            self.speed = CYBORG_SPEED
            self.shut_min_frames = round(CYBORG_PLASMA_MIN_TIMEOUT * FPS) # минимальное число кадров для следующего выстрела
            self.shut_max_frames = round(CYBORG_PLASMA_MAX_TIMEOUT * FPS) # максимальное число кадров для следующего выстрела
            self.shut_delay = randint(self.shut_min_frames, self.shut_max_frames) # число кадров для следующего выстрела
        else:
            self.armor = BOT_ARMOR
            self.speed = BOT_SPEED
            self.shut_min_frames = round(BOT_PLASMA_MIN_TIMEOUT * FPS) # минимальное число кадров для следующего выстрела
            self.shut_max_frames = round(BOT_PLASMA_MAX_TIMEOUT * FPS) # максимальное число кадров для следующего выстрела
            self.shut_delay = randint(self.shut_min_frames, self.shut_max_frames) # число кадров для следующего выстрела
        self.direction = 0 # задаем начальное направление врага (любое от 0 до 360 градусов, он все равно потом повернется к игроку)
        self.move_dir = randint(0, 3) # в поле move_dir сторона, направления движения: 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево.

        self.healthbar = Healthbar(self) # создаем полоску здоровья

        bots_group.add(self) # добавляем врага в группу спрайтов

    # метод обновления (принимает объект player, группы спрайтов bullets и walls, и игровое окно screen)
    def update(self, player, bullets, walls, screen):
        # поворачиваем врага к игроку
        turn_sprite_to_target(self, player.rect.centerx, player.rect.centery)
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate(self.start_image, -self.direction) # поворачиваем спрайт на необходимый угол

        # считаем кадры до следующего выстрела
        if self.shut_delay > 0 : self.shut_delay -= 1
        # если готовы стрелять - стреляем
        if self.shut_delay == 0:
            self.shut_delay = randint(self.shut_min_frames, self.shut_max_frames)
            Plasma(self.rect.centerx, self.rect.centery, self.direction) # создаем плазменный выстрел

        # сохраняем позицию до перемещения
        pos_x, pos_y = self.rect.center

        # пробуем сменить направление движения врага
        if randint(0, 30) < 1 : self.move_dir = randint(0, 3)
        # двигаемся
        if self.move_dir == 3:
            self.rect.centerx -= self.speed
        if self.move_dir == 1:
            self.rect.centerx += self.speed
        if self.move_dir == 0:
            self.rect.centery -= self.speed
        if self.move_dir == 2:
            self.rect.centery += self.speed

        # проверяем столкновение со стенами
        if PG.sprite.spritecollide(self, walls, False):
            # возвращаем врага в предыдущую позицию если столкнулись со стеной
            self.rect.center = (pos_x, pos_y)
            self.move_dir = randint(0, 3) # задаем новое случайное направление

        # перебираем все пули игрока, с которыми столкнулся враг (True - уничтожит пулю)
        for bullet in PG.sprite.spritecollide(self, bullets, True):
            # если было столкновение - отнимаем HP, рисуем эффекты зеленых брызг
            self.hp -= round(PLAYER_BULLET_POWER / self.armor)
            Effect(self.rect.centerx, self.rect.centery, 'slime' + str(randint(1,3)), bullet.direction)
            # обновляем полосу здоровья, если HP > 0
            if self.hp > 0 : self.healthbar.render()
            else:
                # если HP <= 0 создаем взрыв, уничтожаем полосу здоровья и бота
                Effect(bullet.rect.centerx, bullet.rect.centery, 'destroy')
                self.healthbar.kill()
                return self.kill()

        # отрисовка бота и его полоски здоровья
        screen.blit(self.image, self.image.get_rect(center = (self.rect.center)))
        self.healthbar.draw(screen)