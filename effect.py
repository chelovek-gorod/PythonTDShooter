# ЭФФЕКТЫ (брызги, взрывы и прочие разовые анимации)

# из файла init импортируем PG(PyGame), класс SPRITE, словарь со спрайтами SPRITES, класс GROUP и словарь со звуками SOUNDS
from init import PG, SPRITE, SPRITES, GROUP, SOUNDS
# из библиотеки random импортируем функцию randint (для генерации случайных целых чисел)
from random import randint

# создаем группу спрайтов для хранения эффектов
effects_group = GROUP()

# класс Effect (наследуется от класса SPRITE из библиотеки PyGame)
class Effect(SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, вид эффекта и угол поворота)
    def __init__(self, x, y, effect_type = 'ricochet', direction = None):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.frame = 0 # задаем начальный кадр анимации
        self.frames = SPRITES[effect_type] # в поле frames сохраняем список всех кадров анимации
        self.frames_number = len(self.frames) # в поле frames_number сохраняем количество кадров анимации
        self.direction = -direction if direction else randint(0, 360) # если направление не задано - выбираем случайное
        self.image = PG.transform.rotate( self.frames[self.frame], self.direction ) # поворачиваем спрайт согласно направления
        self.rect = self.image.get_rect(center = (x, y)) # создаем прямоугольник по размерам спрайта с центрам в x и y
        # если вид анимации 'destroy' - проигрываем соответствующий звуковой эффект
        if effect_type == 'destroy' : SOUNDS['explosion'].play()

        effects_group.add(self) # добавляем пулю в группу спрайтов

    # метод обновления (принимает игровое окно, для отрисовки эффекта)
    def update(self, screen):
        self.image = PG.transform.rotate( self.frames[self.frame], self.direction ) # поворачиваем спрайт согласно направления 
        screen.blit(self.image, self.rect) # рисуем текущий кадр
        self.frame += 1 # переключаем кадр
        if self.frame == self.frames_number : self.kill() # если до этого был последний кадр - уничтожаем эффект