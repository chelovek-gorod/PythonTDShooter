# ВРАГИ

# из файла init импортируем PG(PyGame), класс SPRITE, словарь со спрайтами SPRITES и класс GROUP (для создания групп спрайтов)
from init import PG, SPRITE, SPRITES, GROUP
# из файла constants импортируем все необходимые переменные, которые понадобятся для создания и управления врагами
from constants import FPS, UNIT_HP, SPIDER_ARMOR, SPIDER_SPEED, SPIDER_TIMEOUT, PLAYER_BULLET_POWER
# из файла healthbar импортируем класс Healthbar (для создания полосок здоровья)
from healthbar import Healthbar
# из библиотеки random импортируем функцию randint (для генерации случайных целых чисел)
from random import randint
# из файла effect импортируем класс Effect (для создания анимированных эффектов)
from effect import Effect

# создаем группу спрайтов для хранения врагов
spiders_group = GROUP()

# класс Bot (наследуется от класса SPRITE из библиотеки PyGame)
class Spider(SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, и вид врага)
    def __init__(self, x, y):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.frames = SPRITES['spider'] # в поле frames сохраняем список всех кадров анимации
        self.frames_number = len(self.frames) # в поле frames_number сохраняем количество кадров анимации
        self.frame = 0 # задаем начальный кадр анимации
        self.animation_speed = 2 # задаем скорость анимации
        self.animation_frame = self.animation_speed # определяем через сколько кадров сменить кадр анимации
        self.image = self.frames[self.frame] # в поле image будем хранить повернутый спрайт для отрисовки
        self.rect = self.image.get_rect(center = (x, y)) # создаем прямоугольник по размерам спрайта с центрам в x и y
        self.is_active = True # в поле is_active определяем активен ли паук (бежит и может атаковать игрока)
        self.await_frames = round(SPIDER_TIMEOUT * FPS) # число кадров задержки активации
        self.await_delay = 0 # текущий кадр задержки активации
        self.hp = UNIT_HP # в поле hp записываем жизни врага
        self.armor = SPIDER_ARMOR # в поле armor записываем скорость
        self.speed = SPIDER_SPEED # в поле speed записываем защиту
        self.direction = randint(0, 3) * 90 # определяем начальное направление движения
        self.image = PG.transform.rotate(self.image, -self.direction + 90) # поворачиваем кадр, согласно направления движения

        self.healthbar = Healthbar(self) # создаем полоску здоровья

        spiders_group.add(self) # добавляем врага в группу спрайтов

    # метод атаки
    def strike(self):
        self.is_active = False # деактивируем паука
        self.await_delay = self.await_frames # задаем число кадров для задержки активации

    # метод обновления (принимает группы спрайтов bullets и walls, и игровое окно screen)
    def update(self, bullets, walls, screen):
        if self.is_active: # если паучок активен
            pos_x, pos_y = self.rect.center # сохраняем позицию до перемещения
            # если не настало время смены кадра
            if self.animation_frame > 0 : self.animation_frame -= 1 # отнимаем кадр от счетчика скорости анимации
            else: # иначе обновляем счетчик скорости анимации
                self.animation_frame = self.animation_speed
                self.frame += 1 # переходим к следующему кадру
                if self.frame == self.frames_number : self.frame = 0  # переходим к первому кадру, если дошли до конца
                self.image = PG.transform.rotate(self.frames[self.frame], -self.direction + 90) # поворачиваем кадр

            # пробуем сменить направление движения врага
            if randint(0, 100) < 1:
                self.direction = randint(0, 3) * 90 # определяем новое направление движения
                self.image = PG.transform.rotate(self.frames[self.frame], -self.direction + 90) # поворачиваем кадр
            # двигаемся
            if self.direction == 270:
                self.rect.centerx -= self.speed
            if self.direction == 90:
                self.rect.centerx += self.speed
            if self.direction == 0:
                self.rect.centery -= self.speed
            if self.direction == 180:
                self.rect.centery += self.speed

            # проверяем столкновение со стенами
            if PG.sprite.spritecollide(self, walls, False):
                # возвращаем врага в предыдущую позицию если столкнулись со стеной
                self.rect.center = (pos_x, pos_y) 
                self.direction = randint(0, 3) * 90 # определяем новое направление движения
                self.image = PG.transform.rotate(self.frames[self.frame], -self.direction + 90) # поворачиваем кадр
        # если паучок не активен
        else:
            self.await_delay -= 1 # уменьшаем число кадров задержки активации
            if self.await_delay < 1 : self.is_active = True # если задержка закончилась - активируем паучка

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
        screen.blit(self.image, self.rect)
        self.healthbar.draw(screen)