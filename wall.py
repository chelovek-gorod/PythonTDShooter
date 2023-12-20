# СТЕНЫ

# из файла init импортируем класс SPRITE, словарь со спрайтами SPRITES и класс GROUP
from init import SPRITE, SPRITES, GROUP

# создаем группу спрайтов для хранения стен
walls_group = GROUP()

# класс Wall (наследуется от класса SPRITE из библиотеки PyGame)
class Wall(SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y)
    def __init__(self, x, y, wall_type = 'wall_stone'):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.image = SPRITES[wall_type] # спрайт стены
        self.rect = self.image.get_rect() # создаем прямоугольник по размерам спрайта
        # задаем координаты прямоугольнику
        self.rect.x = x
        self.rect.y = y

        walls_group.add(self) # добавляем стену в группу спрайтов

    # метод отрисовки стен (принимает игровое окно)
    def draw(self, screen):
        # рисуем спрайт стены в её прямоугольнике
        screen.blit(self.image, self.rect)