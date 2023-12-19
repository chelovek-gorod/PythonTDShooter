# ПЛАЗМА от выстрелов ботов

# из файла init импортируем PG(PyGame), класс SPRITE, словарь со спрайтами SPRITES, класс GROUP и словарь со звуками SOUNDS
from init import PG, SPRITE, SPRITES, GROUP, SOUNDS
# из файла constants импортируем все необходимые переменные, которые понадобятся для создания и управления выстрелами врагов
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOT_PLASMA_SPEED, HALF_UNIT_SIZE
# из библиотеки math импортируем функции для расчетов синуса и косинуса, а так же функцию для перевода градусов в радианы
from math import sin, cos, radians
# из файла effect импортируем класс Effect (для создания анимированных эффектов)
from effect import Effect

# создаем группу спрайтов для хранения выстрелов врагов
plasmas_group = GROUP()

# класс Plasma (наследуется от класса SPRITE из библиотеки PyGame)
class Plasma(SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, и угол направления)
    def __init__(self, x, y, direction):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        image = SPRITES['plasma'] # исходный спрайт выстрела без поворота на какой-либо угол
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate( image, -direction ) # поворачиваем спрайт на необходимый угол
        self.rect = self.image.get_rect(center = (x, y)) # создаем прямоугольник по размерам спрайта с центрам в x и y
        self.direction = direction # задаем направление пули

        angle = radians(direction) # переводим направление в радианы (так как функции cos() и sin() принимают только радианы)
        self.speed_x = cos(angle) * BOT_PLASMA_SPEED # рассчитываем скорость плазмы по оси x
        self.speed_y = sin(angle) * BOT_PLASMA_SPEED # рассчитываем скорость плазмы по оси y

        # смещаем плазму к краю спрайта (появление в конце дула)
        self.center_x = x + self.speed_x * (HALF_UNIT_SIZE / BOT_PLASMA_SPEED)
        self.center_y = y + self.speed_y * (HALF_UNIT_SIZE / BOT_PLASMA_SPEED)
        # присваиваем прямоугольнику плазмы координаты её текущего местоположения
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        SOUNDS['plasma'].play() # проигрываем звук выстрела

        plasmas_group.add(self) # добавляем плазму в группу спрайтов

    # метод обновления (принимает группу спрайтов walls)
    def update(self, walls):
        # обновляем координаты плазмы
        self.center_x += self.speed_x
        self.center_y += self.speed_y
        # присваиваем прямоугольнику плазмы координаты её текущего местоположения
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
        # если плазма вылетит за пределы игрового окна - уничтожаем её
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH \
        or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT :
            return self.kill()
        # если плазма столкнется со стеной - создаем эффект вспышки и уничтожаем пулю
        if PG.sprite.spritecollide(self, walls, False):
            Effect(self.rect.centerx, self.rect.centery, 'splash')
            return self.kill()

    # метод отрисовки плазмы (принимает игровое окно)
    def draw(self, screen):
            # рисуем спрайт плазмы в её прямоугольнике
            screen.blit(self.image, self.rect)