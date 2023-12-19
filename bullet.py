# ПУЛИ ИГРОКА

# из файла init импортируем PG(PyGame), класс SPRITE, словарь со спрайтами SPRITES, класс GROUP и словарь со звуками SOUNDS
from init import PG, SPRITE, SPRITES, GROUP, SOUNDS
# из файла constants импортируем все необходимые переменные, которые понадобятся для создания и управления пулями игрока
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_BULLET_SPEED, HALF_UNIT_SIZE
# из библиотеки math импортируем функции для расчетов синуса и косинуса, а так же функцию для перевода градусов в радианы
from math import sin, cos, radians
# из файла effect импортируем класс Effect (для создания анимированных эффектов)
from effect import Effect

# создаем группу спрайтов для хранения пуль игрока
bullets_group = GROUP()

# класс Bot (наследуется от класса SPRITE из библиотеки PyGame)
class Bullet(SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, и угол направления)
    def __init__(self, x, y, direction):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        image = SPRITES['player_bullet'] # исходный спрайт пули без поворота на какой-либо угол
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate( image, -direction ) # поворачиваем спрайт на необходимый угол
        self.rect = self.image.get_rect(center = (x, y)) # создаем прямоугольник по размерам спрайта с центрам в x и y
        self.direction = direction # задаем направление пули

        angle = radians(direction) # переводим направление в радианы (так как функции cos() и sin() принимают только радианы)
        self.speed_x = cos(angle) * PLAYER_BULLET_SPEED # рассчитываем скорость пули по оси x
        self.speed_y = sin(angle) * PLAYER_BULLET_SPEED # рассчитываем скорость пули по оси y

        # для перемещения пули будем хранить ее координаты в полях center_x и center_y
        # так как при передачи координат прямоугольнику, они округляться, и при маленькой скорости движения вообще не будет

        # смещаем пулю к краю спрайта (появление в конце дула)
        self.center_x = x + self.speed_x * (HALF_UNIT_SIZE / PLAYER_BULLET_SPEED)
        self.center_y = y + self.speed_y * (HALF_UNIT_SIZE / PLAYER_BULLET_SPEED)
        # присваиваем прямоугольнику пули координаты её текущего местоположения
        self.rect.centerx = self.center_x 
        self.rect.centery = self.center_y

        SOUNDS['shut'].play() # проигрываем звук выстрела
        
        bullets_group.add(self) # добавляем пулю в группу спрайтов

    # метод обновления (принимает группу спрайтов walls)
    def update(self, walls):
        # обновляем координаты пули
        self.center_x += self.speed_x
        self.center_y += self.speed_y
        # присваиваем прямоугольнику пули координаты её текущего местоположения
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
        # если пуля вылетит за пределы игрового окна - уничтожаем её
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH \
        or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT :
            return self.kill()
        # если пуля столкнется со стеной - создаем эффект вспышки и уничтожаем пулю
        if PG.sprite.spritecollide(self, walls, False):
            Effect(self.rect.centerx, self.rect.centery)
            return self.kill()

    # метод отрисовки пули (принимает игровое окно)
    def draw(self, screen):
            # рисуем спрайт пули в её прямоугольнике
            screen.blit(self.image, self.rect)