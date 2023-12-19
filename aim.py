# ПРИЦЕЛ (игровой курсор)

# из файла init импортируем класс SPRITE и словарь со спрайтами SPRITES
from init import SPRITE, SPRITES

# класс Aim (наследуется от класса SPRITE из библиотеки PyGame)
class Aim(SPRITE):
    # функция-конструктор (создает объект)
    def __init__(self):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.image = SPRITES['aim'] # в поле image присваиваем спрайт
        self.rect = self.image.get_rect() # создаем прямоугольник по размерам спрайта и присваиваем в поле rect

    # метод обновления (принимает координаты курсора мыши)
    def update(self, mouse_x, mouse_y):
        # обновляем координаты прямоугольника, в котором будем рисовать прицел
        self.rect.centerx = mouse_x
        self.rect.centery = mouse_y