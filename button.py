# КНОПКИ для игрового меню

# из файла init импортируем PG(PyGame), класс SPRITE, класс GROUP, словарь со шрифтами FONTS и словарь со звуками SOUNDS
from init import PG, SPRITE, GROUP, FONTS, SOUNDS

# настройки размеров кнопки, обводки и текста
BTN_WIDTH = 360 # ширина кнопки
BTN_HEIGHT = 60 # высота кнопки
BTN_RADIUS = 20 # радиус скругления кнопки
BTN_BORDER = 2 # толщина обводки кнопки (появляется при наведении курсора на кнопку)
FONT_SIZE = 36 # размер текста в кнопке
BTN_FULL_W = BTN_WIDTH + BTN_BORDER * 2 # ширина кнопки с учетом обводки
BTN_FULL_H = BTN_HEIGHT + BTN_BORDER * 2 # ширина кнопки ширина кнопки с учетом обводки
BTN_CENTER = (BTN_WIDTH / 2, BTN_HEIGHT / 2) # координаты центра кнопки (для вставки текста в центр)

# создаем группу кнопок
buttons_group = GROUP()

# класс Button (наследуется от класса SPRITE из библиотеки PyGame, для группировки всех кнопок в группу спрайтов)
class Button (SPRITE):
    # функция-конструктор (создает объект, принимает координаты x и y, функцию клика, текст, цвета текста, кнопки и активации)
    def __init__(self, x, y, onclick, text, text_color = (255, 255, 255), button_color = (0, 0, 0, 192), active_color = (0, 255, 0)):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.font = PG.font.Font(FONTS['button'], FONT_SIZE) # в поле font записываем шрифт, заданного размера
        self.text = text # в поле text сохраняем текст кнопки
        self.text_color = text_color # в поле text_color сохраняем цвет текста
        self.button_color = button_color # в поле button_color сохраняем цвет кнопки
        self.active_color = active_color # в поле active_color сохраняем цвета текста и обводки кнопки при наведении курсора
        self.x = x # координата x положения центра кнопки
        self.y = y # координата y положения центра кнопки
        self.is_active = False # наведен ли курсор на кнопку (True - курсор наведен на кнопку)
        self.render() # вызываем метод отрисовки кнопки
        self.onclick = onclick # в поле onclick сохраняем функцию, которая запустится при клике по кнопке

        buttons_group.add(self)  # добавляем кнопку в группу спрайтов
    
    # метод отрисовки текста и подложки (принимает текст)
    def render(self):
        # создаем кнопку
        self.image = PG.Surface((BTN_FULL_W, BTN_FULL_H), PG.SRCALPHA) # создаем изображение для кнопки с прозрачным фоном
        # рисуем скругленный прямоугольник
        PG.draw.rect(self.image, self.button_color, PG.Rect(BTN_BORDER, BTN_BORDER, BTN_WIDTH, BTN_HEIGHT), border_radius = BTN_RADIUS)
        if self.is_active : # если наведен курсор - рисуем обводку
            PG.draw.rect(self.image, self.active_color, PG.Rect(BTN_BORDER, BTN_BORDER, BTN_WIDTH, BTN_HEIGHT), BTN_BORDER, BTN_RADIUS)
        self.rect = self.image.get_rect(center = (self.x, self.y)) # создаем прямоугольник с центром в координатах self.x и self.y
        # создаем текст
        text_color = self.active_color if self.is_active else self.text_color # определяем цвет текста (зависит от наведения курсора)
        text_image = self.font.render(self.text, True, text_color) # создаем изображение из текста (True - сглаживать пиксели)
        text_rect = text_image.get_rect(center = BTN_CENTER) # создаем прямоугольник с центром в координатах BTN_CENTER
        self.image.blit(text_image, text_rect) # отображаем текстовое изображение на кнопке

    # метод обновления (принимает положение курсора мыши и события)
    def update(self, mouse_x, mouse_y, events):
        # если мышь наведена на кнопку
        if mouse_x > self.rect.x and mouse_x < self.rect.right and mouse_y > self.rect.y and mouse_y < self.rect.bottom:
            for event in events: # если мышь нажата - активируем функцию, привязанную к кнопке
                if event.type == PG.MOUSEBUTTONUP and event.button == 1:
                    SOUNDS['click'].play()
                    return self.onclick()
            if self.is_active == False: # если кнопка не активна (курсор навели только что)
                self.is_active = True # меняем состояние кнопки
                self.render() # перерисовываем кнопку с обводкой и новым цветом текста
                SOUNDS['menu'].play()
        # если мышь не наведена на кнопку, но кнопка активна
        elif self.is_active == True:
            self.is_active = False # меняем состояние кнопки
            self.render() # перерисовываем кнопку без обводки и стандартным цветом текста

    # метод отрисовки кнопки (принимает игровое окно)
    def draw(self, screen):
        # рисуем спрайт кнопки в его прямоугольнике
        screen.blit(self.image, self.rect)