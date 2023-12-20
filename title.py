# ЗАГОЛОВКИ для игрового меню

# из файла init импортируем PG(PyGame), класс SPRITE, класс GROUP и словарь со шрифтами FONTS
from init import PG, SPRITE, GROUP, FONTS

# создаем группу кнопок
titles_group = GROUP()

# класс Title (наследуется от класса SPRITE из библиотеки PyGame, для группировки всех кнопок в группу спрайтов)
class Title (SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, текст, размер шрифта и цвета текста)
    def __init__(self, x, y, text, font_size, text_color = (255, 255, 255), shadow_color = (0, 0, 0), shadow_size = 3):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        font = PG.font.Font(FONTS['bold'], font_size) # в поле font записываем шрифт, заданного размера
        self.text = font.render(text, True, text_color) # создаем изображение из текста (True - сглаживать пиксели)
        self.shadow = font.render(text, True, shadow_color + ( int(128 / shadow_size**2), )) # создаем изображение тени
        self.text_rect = self.text.get_rect() # создаем прямоугольник по размерам изображения из текста
        self.width = shadow_size * 2 + self.text_rect.width # рассчитываем ширину изображения, для отображения текста с тенью
        self.height = shadow_size * 2 + self.text_rect.height  # рассчитываем высоту изображения, для отображения текста с тенью
        self.half_width = int(self.width / 2) # рассчитываем центр по оси x изображения, для отображения текста с тенью
        self.half_height = int(self.height / 2) # рассчитываем центр по оси y изображения, для отображения текста с тенью
        self.image = PG.Surface((self.width, self.height), PG.SRCALPHA) # создаем изображения, для отображения текста с тенью
        self.rect = self.image.get_rect(center = (x, y)) # создаем прямоугольник по размерам изображения, для отображения текста с тенью
        # цикл отрисовки тени текста со смещением на 1 пиксель по четырем направлениям
        for i in range(shadow_size):
            # тень со смещением влево
            self.text_rect.centerx = self.half_width - i
            self.text_rect.centery = self.half_height
            self.image.blit(self.shadow, self.text_rect)
            # тень со смещением вправо
            self.text_rect.centerx = self.half_width + i
            self.text_rect.centery = self.half_height
            self.image.blit(self.shadow, self.text_rect)
            # тень со смещением вверх
            self.text_rect.centerx = self.half_width
            self.text_rect.centery = self.half_height - i
            self.image.blit(self.shadow, self.text_rect)
            # тень со смещением вниз
            self.text_rect.centerx = self.half_width
            self.text_rect.centery = self.half_height + i
            self.image.blit(self.shadow, self.text_rect)
        # текст над тенью
        self.text_rect.centerx = self.half_width
        self.text_rect.centery = self.half_height
        self.image.blit(self.text, self.text_rect)

        titles_group.add(self) # добавляем заголовок в группу спрайтов

    # метод отрисовки заголовка (принимает игровое окно)
    def draw(self, screen):
        # рисуем спрайт заголовка в его прямоугольнике
        screen.blit(self.image, self.rect)