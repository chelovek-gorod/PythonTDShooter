# ПЕРСОНАЖ ИГРОКА

# из файла init импортируем PG(PyGame), класс SPRITE, словарь со спрайтами SPRITES и словарь со звуками SOUNDS
from init import PG, SPRITE, SPRITES, SOUNDS
# из файла constants импортируем все необходимые переменные, которые понадобятся для создания и управления персонажем игрока
from constants import FPS, HALF_UNIT_SIZE, UNIT_HP, PLAYER_ARMOR, PLAYER_SPEED, \
    PLAYER_SHUT_TIMEOUT, PLAYER_RELOAD_TIMEOUT, PLAYER_BULLETS, BOT_PLASMA_POWER
# из файла utils импортируем функцию, поворачивающую спрайт к определенной цели 
from utils import turn_sprite_to_target
# из файла bullet импортируем класс Bullet (для создания объектов пуль)
from bullet import Bullet
# из файла healthbar импортируем класс Healthbar (для создания полосы здоровья)
from healthbar import Healthbar
# из файла label импортируем класс Label (для создания текстовых спрайтов)
from label import Label
# из файла effect импортируем класс Effect (для создания анимированных эффектов)
from effect import Effect
# из библиотеки random импортируем функцию randint (для генерации случайных целых чисел)
from random import randint

# класс Player (наследуется от класса SPRITE из библиотеки PyGame)
class Player(SPRITE):
    # функция-конструктор (создает объект игрового персонажа)
    def __init__(self):
        SPRITE.__init__(self)
        self.start_image = SPRITES['player'] # исходный спрайт игрока без поворота на какой-либо угол
        self.image = self.start_image # в поле image будем хранить повернутый спрайт для отрисовки
        self.rect = PG.Rect( (0, 0), (HALF_UNIT_SIZE, HALF_UNIT_SIZE) ) # создаем прямоугольник-маску в двое меньше спрайта игрока
        self.speed = PLAYER_SPEED # в поле speed записываем скорость игрока
        self.direction = 0 # задаем начальное направление игрока (любое от 0 до 360 градусов, он все равно потом повернется к прицелу)

        self.shut_frames = round(PLAYER_SHUT_TIMEOUT * FPS) # число кадров для следующего выстрела (для обновления)
        self.shut_delay = self.shut_frames # текущее число кадров для следующего выстрела (каждый кадр будем проверять)
        self.is_shooting = False # пытается ли игрок стрелять (сменим на True при зажатии левой кнопки мыши)

        self.bullets_fill = PLAYER_BULLETS # максимальный запас патронов (для обновления числа пуль после перезарядки)
        self.bullets = 0 # текущее число пуль
        self.reload_frames = round(PLAYER_RELOAD_TIMEOUT * FPS) # количество кадров, для перезарядки оружия
        self.reload_delay = self.reload_frames # текущий номер кадра перезарядки (если перезаряжаемся)

        self.hp = UNIT_HP # в поле hp записываем жизни персонажа игрока
        self.healthbar = Healthbar(self)  # создаем полоску здоровья
        self.armor = PLAYER_ARMOR # в поля armor записываем защиту игрока

        # создаем текстовый спрайт в верхнем левом углу, зеленого цвета, с количеством патронов
        self.bullets_label = Label(0, 0, 24, 6, (0, 255, 0), 'left', f'Bullets: {self.bullets}')

    # метод обновления (принимает координаты x и y курсора мыши, события мыши, группы спрайтов plasmas и walls)
    def update(self, mouse_x, mouse_y, events, plasmas, walls):
        # поворачиваем игрока к курсору мыши
        turn_sprite_to_target(self, mouse_x, mouse_y)
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate(self.start_image, -self.direction) # поворачиваем спрайт на необходимый угол

        # перезарядка
        if self.reload_delay > 0 : # если есть кадры перезарядки
            self.reload_delay -= 1 # отнимаем 1 кадр
            if self.reload_delay == 0 : # если перезарядились (нет больше кадров ожидания перезарядки)
                self.bullets = self.bullets_fill # пополняем запас патронов на максимальное значение
                self.bullets_label.render(f'Bullets: {self.bullets}') # обновляем текст с числом пуль
        # считаем кадры до следующего выстрела
        if self.shut_delay > 0 : self.shut_delay -= 1
        # если зажана левая кнопка мыши - активируем проверку стрельбы
        for event in events:
            if event.type == PG.MOUSEBUTTONDOWN and event.button == 1 : self.is_shooting = True
            if event.type == PG.MOUSEBUTTONUP and event.button == 1 : self.is_shooting = False
        # если готовы стрелять и стрельба активирована - стреляем
        if self.is_shooting and self.shut_delay == 0 and self.bullets > 0:
            self.shut_delay = self.shut_frames # добавляем кадры ожидания следующего выстрела
            Bullet(self.rect.centerx, self.rect.centery, self.direction) # создаем пулю
            self.bullets -= 1 # отнимем пулю из своего запаса
            self.bullets_label.render(f'Bullets: {self.bullets}') # обновляем текст с числом пуль
            if self.bullets == 0 : # если пули закончились - перезаряжаемся
                self.reload_delay = self.reload_frames # задаем число кадров, необходимое для перезарядки
                self.bullets_label.render(f'Reloading...') # обновляем текст с числом пуль
                SOUNDS['reload'].play() # проигрываем звуковой эффект перезарядки

        # сохраняем позицию игрока до перемещения
        pos_x, pos_y = self.rect.center

        # получаем список нажатых клавиш
        key = PG.key.get_pressed()

        # проверяем ручную перезарядку (если игрок нажал на клавишу [R] и пуль не максимум, но больше нуля)
        if key[PG.K_r] and self.bullets > 0 and self.bullets < self.bullets_fill:
            self.bullets = 0 # обнуляем пули (для того что бы игрок не смог стрелять в процессе перезарядки)
            self.reload_delay = self.reload_frames # задаем число кадров, необходимое для перезарядки
            self.bullets_label.render(f'Reloading...') # обновляем текст с числом пуль
            SOUNDS['reload'].play() # проигрываем звуковой эффект перезарядки

        # двигаем игрока, если нажаты клавиши для перемещения
        if key[PG.K_LEFT] or key[PG.K_a]:
            self.rect.centerx -= self.speed
        if key[PG.K_RIGHT] or key[PG.K_d]:
            self.rect.centerx += self.speed
        if key[PG.K_UP] or key[PG.K_w]:
            self.rect.centery -= self.speed
        if key[PG.K_DOWN] or key[PG.K_s]:
            self.rect.centery += self.speed

        # проверяем столкновение со стенами
        if PG.sprite.spritecollide(self, walls, False):
            # возвращаем игрока в предыдущую позицию
            self.rect.center = (pos_x, pos_y)

        # проверяем столкновение с плазмой
        for plasma in PG.sprite.spritecollide(self, plasmas, True):
            # если было столкновение - отнимаем HP, рисуем эффект брызг крови
            self.hp -= round(BOT_PLASMA_POWER / PLAYER_ARMOR)
            Effect(plasma.rect.centerx, plasma.rect.centery, 'blood' + str(randint(1,3)), plasma.direction)
            # обновляем полосу здоровья, если HP > 0
            if self.hp >= 0 : self.healthbar.render()

    # метод отрисовки персонажа игрока (принимает игровое окно)
    def draw(self, screen):
        # рисуем спрайт в прямоугольнике с центром в текущей позиции игрока
        screen.blit(self.image, self.image.get_rect(center = (self.rect.center)))
        self.healthbar.draw(screen) # рисуем полосу здоровья