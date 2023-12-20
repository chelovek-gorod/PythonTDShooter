# ТЕКСТ для вывода игровой информации (номер уровня и прочее)

# из файла init импортируем PG(PyGame), класс SPRITE, класс GROUP и словарь со шрифтами FONTS
from init import PG, SPRITE, GROUP, FONTS

# создаем группу текстовых спрайтов
labels_group = GROUP()

# класс Label (наследуется от класса SPRITE из библиотеки PyGame, для группировки всех надписей в группу спрайтов)
class Label (SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, размер шрифта и отступов, цвет текста, расположение и сам текст)
    def __init__(self, x, y, size = 24, offset = 6, color = (0, 255, 0), align = 'center', start_text = ''):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.font = PG.font.Font(FONTS['label'], size) # в поле font записываем шрифт, заданного размера
        self.color = color # в поле color сохраняем цвет текста
        self.align = align # в поле align сохраняем строку, отвечающую за расположение текста в блоке с надписью (центр, лево, право)
        self.offset = offset # в поле offset сохраняем строку размер отступа от текста (будем рисовать полу-прозрачную подложку)
        self.x = x # координата x (для текста по центу - будет центром текста, для текста справа - координатой правой грани подложки)
        self.y = y # координата y - будет координатой верхней грани подложки)
        self.render(start_text) # вызываем метод генерирующий текст и подложку

        labels_group.add(self)  # добавляем текст в группу спрайтов
    
    # метод отрисовки текста и подложки (принимает текст)
    def render(self, text):
        text_image = self.font.render(str(text), True, self.color) # создаем изображение из текста (True - сглаживать пиксели)
        text_image_rect = text_image.get_rect() # создаем прямоугольник по размерам изображения из текста
        # создаем подложку для текста по размерам изображения из текста + отступы, с прозрачным фоном
        self.image = PG.Surface((text_image_rect.width + self.offset * 2, text_image_rect.height + self.offset * 2), PG.SRCALPHA)
        self.image.fill((0,0,0,128)) # закрашиваем подложку полу-прозрачным черным цветом (4-я цифра - прозрачность 128 из 255)
        self.rect = self.image.get_rect() # создаем прямоугольник по размерам подложки текста
        self.rect.y = self.y # задаем полученному прямоугольнику координату y
        # если текст должен быть прижат к левой стороне
        if self.align == 'left' :
            text_image_rect.left = self.offset # смещаем текст от левого края подложки на ширину отступа
            self.rect.x = self.x # задаем для подложки координату x 
        # если текст должен быть прижат к правой стороне
        elif self.align == 'right' :
            text_image_rect.right = text_image_rect.width + self.offset # смещаем текст от правого края подложки на ширину отступа
            self.rect.x = self.x - self.rect.width # задаем для подложки координату x 
        # иначе - текст располагается по центру, относительно своей координаты x
        else:
            text_image_rect.centerx = text_image_rect.width * 0.5 + self.offset # размещаем текст в центре подложки
            self.rect.x = self.x - self.rect.width * 0.5 # задаем для подложки координату x 
        self.image.blit(text_image, text_image_rect) # отображаем текстовое изображение на подложки

    # метод отрисовки надписи (принимает игровое окно)
    def draw(self, screen):
        # рисуем спрайт с текстом в его прямоугольнике
        screen.blit(self.image, self.rect)